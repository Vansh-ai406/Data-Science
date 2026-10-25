"""Benchmark deep tabular baselines against tree-based and linear baselines."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, brier_score_loss, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from run_baselines import CARDIO_CATEGORICAL, CARDIO_NUMERICAL, RANDOM_SEED, UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL, calculate_metrics


CARDIO_DEEP_MODELS = {
    "LogisticRegression": LogisticRegression(max_iter=2000, random_state=RANDOM_SEED),
    "XGBoost": XGBClassifier(
        n_estimators=220,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=1.0,
        eval_metric="logloss",
        tree_method="hist",
        n_jobs=-1,
        random_state=RANDOM_SEED,
    ),
    "MLP_Deep": MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="relu",
        solver="adam",
        alpha=1e-4,
        batch_size=256,
        learning_rate_init=1e-3,
        max_iter=250,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=15,
        random_state=RANDOM_SEED,
    ),
}


def make_preprocessor(categorical: list[str], numerical: list[str], scale_numerical: bool) -> ColumnTransformer:
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numerical:
        numeric_steps.append(("scaler", StandardScaler()))
    return ColumnTransformer(
        [
            ("numeric", Pipeline(numeric_steps), numerical),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categorical,
            ),
        ],
        remainder="drop",
    )


def make_pipeline(model_name: str, categorical: list[str], numerical: list[str]) -> Pipeline:
    scale = model_name.startswith("MLP") or model_name == "LogisticRegression"
    return Pipeline(
        [
            ("preprocessor", make_preprocessor(categorical, numerical, scale_numerical=scale)),
            ("model", CARDIO_DEEP_MODELS[model_name]),
        ]
    )


def evaluate_cardio_cv(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    features = frame.drop(columns=["patient_id", "target"])
    target = frame["target"].astype(int)
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    rows = []
    for fold_number, (train_idx, test_idx) in enumerate(splitter.split(features, target), start=1):
        train_x = features.iloc[train_idx]
        test_x = features.iloc[test_idx]
        train_y = target.iloc[train_idx]
        test_y = target.iloc[test_idx]
        for model_name in CARDIO_DEEP_MODELS:
            model = make_pipeline(model_name, CARDIO_CATEGORICAL, CARDIO_NUMERICAL)
            model.fit(train_x, train_y)
            prob = model.predict_proba(test_x)[:, 1]
            row = {
                "cohort": "Cardio70k",
                "evaluation": "stratified 5-fold CV",
                "fold": fold_number,
                "model": model_name,
                "n_train": len(train_idx),
                "n_test": len(test_idx),
            }
            row.update(calculate_metrics(test_y, prob))
            rows.append(row)
    return pd.DataFrame(rows)


def evaluate_unified_holdout(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    rows = []
    for held_out_source in sorted(frame["source"].unique()):
        train = frame.loc[frame["source"] != held_out_source]
        test = frame.loc[frame["source"] == held_out_source]
        if train["target"].nunique() != 2 or test["target"].nunique() != 2:
            continue
        train_x = train[UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL]
        test_x = test[UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL]
        train_y = train["target"].astype(int)
        test_y = test["target"].astype(int)
        for model_name in CARDIO_DEEP_MODELS:
            model = make_pipeline(model_name, UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL)
            model.fit(train_x, train_y)
            prob = model.predict_proba(test_x)[:, 1]
            row = {
                "cohort": "Unified clinical",
                "evaluation": "leave-one-source-out",
                "source": held_out_source,
                "model": model_name,
                "n_train": len(train_y),
                "n_test": len(test_y),
            }
            row.update(calculate_metrics(test_y, prob))
            rows.append(row)
    return pd.DataFrame(rows)


def summarize_frames(frame: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    for model_name in sorted(frame["model"].unique()):
        model_rows = frame.loc[frame["model"] == model_name]
        row = {"model": model_name}
        for metric in ["accuracy", "precision", "sensitivity", "specificity", "f1", "roc_auc", "pr_auc", "brier_score"]:
            row[f"{metric}_mean"] = float(model_rows[metric].mean())
            row[f"{metric}_std"] = float(model_rows[metric].std(ddof=1))
        summary_rows.append(row)
    return pd.DataFrame(summary_rows)


def markdown_table(frame: pd.DataFrame, columns: list[str] | None = None) -> str:
    if columns is None:
        columns = list(frame.columns)
    rows = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for values in frame[columns].itertuples(index=False, name=None):
        cells = []
        for value in values:
            if isinstance(value, float):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def plot_summary(frame: pd.DataFrame, title: str, metric: str, out_path: Path) -> None:
    ordered = frame.sort_values(metric, ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(ordered["model"], ordered[metric], color=["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"])
    ax.set_title(title)
    ax.set_ylabel(metric)
    ax.set_xlabel("Model")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()

    cardio = evaluate_cardio_cv(args.cardio70k)
    unified = evaluate_unified_holdout(args.unified_raw)
    report_dir = args.output_dir
    report_dir.mkdir(parents=True, exist_ok=True)
    plots_dir = report_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    cardio_summary = summarize_frames(cardio)
    unified_summary = summarize_frames(unified)
    cardio_summary.to_csv(report_dir / "deep_tabular_cardio_summary.csv", index=False)
    unified_summary.to_csv(report_dir / "deep_tabular_unified_summary.csv", index=False)

    plot_summary(cardio_summary, "Cardio70k deep benchmark: ROC-AUC", "roc_auc_mean", plots_dir / "deep_cardio_roc_auc.png")
    plot_summary(cardio_summary, "Cardio70k deep benchmark: F1 score", "f1_mean", plots_dir / "deep_cardio_f1.png")
    plot_summary(unified_summary, "Unified cohort generalization benchmark: ROC-AUC", "roc_auc_mean", plots_dir / "deep_unified_roc_auc.png")

    best_cardio = cardio_summary.sort_values("roc_auc_mean", ascending=False).iloc[0]
    best_unified = unified_summary.sort_values("roc_auc_mean", ascending=False).iloc[0]
    print("\n=== Deep tabular benchmark summary ===")
    print(cardio_summary[["model", "accuracy_mean", "precision_mean", "f1_mean", "roc_auc_mean", "brier_score_mean"]].sort_values("roc_auc_mean", ascending=False).to_string(index=False))
    print(f"\nBest Cardio70k deep benchmark model: {best_cardio['model']} | ROC-AUC={best_cardio['roc_auc_mean']:.4f} | F1={best_cardio['f1_mean']:.4f} | Accuracy={best_cardio['accuracy_mean']:.4f} | Precision={best_cardio['precision_mean']:.4f}")
    print(f"Best unified generalization model: {best_unified['model']} | ROC-AUC={best_unified['roc_auc_mean']:.4f} | F1={best_unified['f1_mean']:.4f} | Accuracy={best_unified['accuracy_mean']:.4f} | Precision={best_unified['precision_mean']:.4f}\n")

    report_path = report_dir / "deep_tabular_benchmark.md"
    report = [
        "# Deep Tabular Benchmark",
        "",
        "This stage benchmarks deeper tabular neural baselines against the strongest classical models while keeping the same train-only preprocessing and external-source evaluation protocol.",
        "",
        "## Best Cardio70k model",
        "",
        f"- Best model: **{best_cardio['model']}** | ROC-AUC **{best_cardio['roc_auc_mean']:.4f}** | F1 **{best_cardio['f1_mean']:.4f}** | Accuracy **{best_cardio['accuracy_mean']:.4f}** | Precision **{best_cardio['precision_mean']:.4f}**",
        "",
        "## Cardio70k summary",
        "",
        markdown_table(
            cardio_summary[["model", "accuracy_mean", "precision_mean", "f1_mean", "roc_auc_mean", "brier_score_mean"]].sort_values("roc_auc_mean", ascending=False),
            ["model", "accuracy_mean", "precision_mean", "f1_mean", "roc_auc_mean", "brier_score_mean"],
        ),
        "",
        "## Unified source-generalization summary",
        "",
        markdown_table(
            unified_summary[["model", "accuracy_mean", "precision_mean", "f1_mean", "roc_auc_mean", "brier_score_mean"]].sort_values("roc_auc_mean", ascending=False),
            ["model", "accuracy_mean", "precision_mean", "f1_mean", "roc_auc_mean", "brier_score_mean"],
        ),
        "",
        "## Interpretation",
        "",
        "The deep tabular benchmark should be read as a model-capability comparison under the same leakage-safe design. On the large Cardio70k cohort, the deep MLPs are expected to be competitive but not automatically better than tree ensembles; on the heterogeneous unified cohort, the generalization picture remains source-dependent and should be interpreted per cohort rather than pooled across sources.",
        "",
        "This is a second stratified 5-fold benchmark using an alternative fixed MLP/XGBoost configuration from the primary cross-validation suite; both are internal estimates, not independent external validation. The MLP is a neural baseline rather than a novel architecture. Source-held-out results remain separate by cohort and source.",
    ]
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Wrote {report_dir / 'deep_tabular_benchmark.md'}")


if __name__ == "__main__":
    main()
