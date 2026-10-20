"""Select the best Cardio70k model using nested stratified CV."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from run_baselines import (
    CARDIO_CATEGORICAL,
    CARDIO_NUMERICAL,
    RANDOM_SEED,
    calculate_metrics,
    make_models,
)

OUTER_SPLITS = 5
INNER_SPLITS = 3


def run_nested_model_selection(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(path)
    if frame["patient_id"].duplicated().any():
        raise ValueError("Cardio70k contains repeated patient IDs; use grouped CV.")
    if set(frame["target"].dropna().unique()) != {0, 1}:
        raise ValueError("Expected a complete binary 0/1 target.")

    features = frame.drop(columns=["patient_id", "target"])
    target = frame["target"].astype(int)
    outer_splitter = StratifiedKFold(
        n_splits=OUTER_SPLITS,
        shuffle=True,
        random_state=RANDOM_SEED,
    )
    inner_splitter = StratifiedKFold(
        n_splits=INNER_SPLITS,
        shuffle=True,
        random_state=RANDOM_SEED,
    )

    row_records: list[dict[str, object]] = []
    model_library = make_models(CARDIO_CATEGORICAL, CARDIO_NUMERICAL)
    model_names = list(model_library.keys())

    for outer_fold, (train_idx, test_idx) in enumerate(
        outer_splitter.split(features, target), start=1
    ):
        train_x = features.iloc[train_idx]
        train_y = target.iloc[train_idx]
        test_x = features.iloc[test_idx]
        test_y = target.iloc[test_idx]

        best_model_name = None
        best_inner_auc = float("-inf")
        inner_scores: dict[str, list[float]] = {name: [] for name in model_names}

        for model_name in model_names:
            for inner_train_idx, inner_val_idx in inner_splitter.split(train_x, train_y):
                model = model_library[model_name]
                model.fit(train_x.iloc[inner_train_idx], train_y.iloc[inner_train_idx])
                probabilities = model.predict_proba(train_x.iloc[inner_val_idx])[:, 1]
                inner_scores[model_name].append(
                    roc_auc_score(train_y.iloc[inner_val_idx], probabilities)
                )
            mean_inner_auc = float(np.mean(inner_scores[model_name]))
            if mean_inner_auc > best_inner_auc:
                best_inner_auc = mean_inner_auc
                best_model_name = model_name

        if best_model_name is None:
            raise RuntimeError("No candidate model was selected for an outer fold.")

        final_model = model_library[best_model_name]
        final_model.fit(train_x, train_y)
        probabilities = final_model.predict_proba(test_x)[:, 1]

        row: dict[str, object] = {
            "cohort": "Cardio70k",
            "evaluation": f"nested {OUTER_SPLITS}-fold CV with {INNER_SPLITS}-fold inner selection",
            "outer_fold": outer_fold,
            "selected_model": best_model_name,
            "inner_cv_mean_roc_auc": best_inner_auc,
            "n_train": len(train_idx),
            "n_test": len(test_idx),
        }
        row.update(calculate_metrics(test_y, probabilities))
        row_records.append(row)

    folds = pd.DataFrame(row_records)
    summary_rows = []
    for model_name in model_names:
        subset = folds.loc[folds["selected_model"] == model_name]
        if subset.empty:
            continue
        row: dict[str, object] = {
            "cohort": "Cardio70k",
            "evaluation": f"nested {OUTER_SPLITS}-fold CV with {INNER_SPLITS}-fold inner selection",
            "selected_model": model_name,
            "n_outer_folds_selected": int(len(subset)),
            "mean_inner_cv_roc_auc": float(subset["inner_cv_mean_roc_auc"].mean()),
        }
        for metric_name in [
            "accuracy",
            "precision",
            "sensitivity",
            "specificity",
            "f1",
            "roc_auc",
            "pr_auc",
            "brier_score",
        ]:
            row[f"{metric_name}_mean"] = float(subset[metric_name].mean())
            row[f"{metric_name}_sd"] = float(subset[metric_name].std(ddof=1))
        summary_rows.append(row)

    summary = pd.DataFrame(summary_rows)
    return folds, summary


def render_table(frame: pd.DataFrame, columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for values in frame[columns].itertuples(index=False, name=None):
        cells = [
            f"{value:.3f}" if isinstance(value, float) else str(value)
            for value in values
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_report(folds: pd.DataFrame, summary: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fold_path = output_dir / "nested_model_selection_folds.csv"
    summary_path = output_dir / "nested_model_selection_summary.csv"
    report_path = output_dir / "nested_model_selection_results.md"
    folds.to_csv(fold_path, index=False)
    summary.to_csv(summary_path, index=False)

    metric_names = [
        "accuracy",
        "precision",
        "sensitivity",
        "specificity",
        "f1",
        "roc_auc",
        "pr_auc",
        "brier_score",
    ]
    summary_columns = ["selected_model", "n_outer_folds_selected", "mean_inner_cv_roc_auc"]
    for metric_name in metric_names:
        summary_columns.extend([f"{metric_name}_mean", f"{metric_name}_sd"])

    text = [
        "# Nested Cardio70k Model Selection",
        "",
        "This stage uses nested stratified validation on Cardio70k to reduce the risk of selecting a model from the same data used for the final estimate. The outer loop estimates generalization performance, while the inner loop selects the candidate model using mean ROC-AUC on training folds only.",
        "",
        "## Outer-fold results",
        "",
        f"Each outer fold has one selected model. Fold-level metrics are in `{fold_path.as_posix()}`.",
        "",
        render_table(
            folds,
            [
                "outer_fold",
                "selected_model",
                "inner_cv_mean_roc_auc",
                "accuracy",
                "precision",
                "sensitivity",
                "specificity",
                "f1",
                "roc_auc",
                "pr_auc",
                "brier_score",
            ],
        ),
        "",
        "## Aggregated selection summary",
        "",
        render_table(summary, summary_columns),
        "",
        "## Interpretation",
        "",
        "The selected model is the one with the best mean inner-fold ROC-AUC. Those estimates are then evaluated on untouched outer folds. This protects the final performance numbers from circular model selection and gives a more credible model-ranking step before any final deployment or paper claim.",
        "",
        f"Machine-readable summary: `{summary_path.as_posix()}`.",
    ]
    report_path.write_text("\n".join(text) + "\n", encoding="utf-8")
    print(f"Wrote {report_path}, {fold_path}, and {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    folds, summary = run_nested_model_selection(args.cardio70k)
    write_report(folds, summary, args.output_dir)


if __name__ == "__main__":
    main()
