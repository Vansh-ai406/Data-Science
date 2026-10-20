"""Benchmark a leakage-safe HPEM reproduction on source-held-out clinical data."""

from __future__ import annotations

import argparse
from pathlib import Path
from functools import partial

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC
from xgboost import XGBClassifier

from run_baselines import (
    RANDOM_SEED,
    UNIFIED_CATEGORICAL,
    UNIFIED_NUMERICAL,
    make_models,
    make_preprocessor,
)


INNER_SPLITS = 3
TOP_K_FEATURES = 15


def make_base_estimators() -> list[tuple[str, Pipeline]]:
    categorical = UNIFIED_CATEGORICAL
    numerical = UNIFIED_NUMERICAL
    mi_score = partial(mutual_info_classif, random_state=RANDOM_SEED)

    def make_base(name: str, estimator: object) -> Pipeline:
        return Pipeline(
            [
                (
                    "preprocessor",
                    make_preprocessor(categorical, numerical, scale_numerical=True),
                ),
                ("polynomial", PolynomialFeatures(degree=2, include_bias=False)),
                ("mutual_information", SelectKBest(mi_score, k=TOP_K_FEATURES)),
                ("estimator", estimator),
            ]
        )

    return [
        (
            "random_forest",
            make_base(
                "random_forest",
                RandomForestClassifier(
                    n_estimators=150,
                    min_samples_leaf=2,
                    n_jobs=-1,
                    random_state=RANDOM_SEED,
                ),
            ),
        ),
        (
            "gradient_boosting",
            make_base(
                "gradient_boosting",
                GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.05,
                    max_depth=2,
                    random_state=RANDOM_SEED,
                ),
            ),
        ),
        (
            "rbf_svm",
            make_base(
                "rbf_svm",
                SVC(C=1.0, kernel="rbf", probability=True, random_state=RANDOM_SEED),
            ),
        ),
    ]


def make_hpem_voter() -> VotingClassifier:
    return VotingClassifier(estimators=make_base_estimators(), voting="soft", n_jobs=1)


def make_meta_learner() -> XGBClassifier:
    return XGBClassifier(
        n_estimators=120,
        max_depth=2,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=1.0,
        reg_lambda=2.0,
        eval_metric="logloss",
        tree_method="hist",
        n_jobs=-1,
        random_state=RANDOM_SEED,
    )


def get_metrics(target: pd.Series, probabilities: np.ndarray) -> dict[str, float]:
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "accuracy": float(accuracy_score(target, predictions)),
        "precision": float(precision_score(target, predictions, zero_division=0)),
        "sensitivity": float(recall_score(target, predictions, zero_division=0)),
        "specificity": float(recall_score(target, predictions, pos_label=0, zero_division=0)),
        "f1": float(f1_score(target, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(target, probabilities)),
        "pr_auc": float(average_precision_score(target, probabilities)),
        "brier_score": float(brier_score_loss(target, probabilities)),
        "log_loss": float(log_loss(target, probabilities, labels=[0, 1])),
    }


def get_oof_base_probabilities(
    features: pd.DataFrame, target: pd.Series, source_number: int
) -> np.ndarray:
    splitter = StratifiedKFold(
        n_splits=INNER_SPLITS,
        shuffle=True,
        random_state=RANDOM_SEED + source_number,
    )
    oof_probabilities = np.full((len(target), 3), np.nan, dtype=float)
    for train_indices, validation_indices in splitter.split(features, target):
        train_x = features.iloc[train_indices]
        train_y = target.iloc[train_indices]
        validation_x = features.iloc[validation_indices]
        for model_index, (_, model) in enumerate(make_base_estimators()):
            model.fit(train_x, train_y)
            oof_probabilities[validation_indices, model_index] = model.predict_proba(
                validation_x
            )[:, 1]
    if np.isnan(oof_probabilities).any():
        raise RuntimeError("OOF soft-vote probabilities are incomplete.")
    return oof_probabilities


def run_benchmark(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(path)
    feature_columns = UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL
    prediction_rows = []
    source_rows = []
    sources = sorted(frame["source"].dropna().unique())
    for source_number, held_out_source in enumerate(sources, start=1):
        train = frame.loc[frame["source"] != held_out_source]
        test = frame.loc[frame["source"] == held_out_source]
        train_x, test_x = train[feature_columns], test[feature_columns]
        train_y, test_y = train["target"].astype(int), test["target"].astype(int)
        if train_y.nunique() != 2 or test_y.nunique() != 2:
            raise ValueError(f"Both target classes are required for {held_out_source}.")

        # Cross-fit soft-vote predictions so the meta-learner never sees in-sample base outputs.
        meta_train_probabilities = get_oof_base_probabilities(train_x, train_y, source_number)
        meta_learner = make_meta_learner()
        meta_learner.fit(meta_train_probabilities, train_y)

        voter = make_hpem_voter()
        voter.fit(train_x, train_y)
        base_probabilities = np.column_stack(
            [
                voter.named_estimators_[name].predict_proba(test_x)[:, 1]
                for name in ("random_forest", "gradient_boosting", "rbf_svm")
            ]
        )
        base_probability = base_probabilities.mean(axis=1)
        hpem_probability = meta_learner.predict_proba(base_probabilities)[:, 1]

        xgboost = make_models(UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL)["XGBoost"]
        xgboost.fit(train_x, train_y)
        xgboost_probability = xgboost.predict_proba(test_x)[:, 1]

        for model_name, probabilities in [
            ("HPEM (OOF soft-vote meta)", hpem_probability),
            ("Soft-voting base ensemble", base_probability),
            ("XGBoost baseline", xgboost_probability),
        ]:
            metrics = get_metrics(test_y, probabilities)
            source_rows.append(
                {
                    "cohort": "Unified clinical",
                    "held_out_source": held_out_source,
                    "model": model_name,
                    "n_test": len(test_y),
                    **metrics,
                }
            )
            prediction_rows.extend(
                {
                    "held_out_source": held_out_source,
                    "model": model_name,
                    "target": int(label),
                    "probability": float(probability),
                }
                for label, probability in zip(test_y, probabilities)
            )
        print(f"Finished held-out source: {held_out_source}")

    by_source = pd.DataFrame(source_rows)
    metric_columns = ["accuracy", "precision", "sensitivity", "specificity", "f1", "roc_auc", "pr_auc", "brier_score", "log_loss"]
    summary = (
        by_source.groupby("model", sort=False)
        .agg(
            n_sources=("held_out_source", "nunique"),
            n_total=("n_test", "sum"),
            **{f"{metric}_mean": (metric, "mean") for metric in metric_columns},
            **{f"{metric}_sd_across_sources": (metric, "std") for metric in metric_columns},
        )
        .reset_index()
    )
    return by_source, summary, pd.DataFrame(prediction_rows)


def markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    rows = []
    for values in frame[columns].itertuples(index=False, name=None):
        rows.append(
            [
                f"{value:.4f}" if isinstance(value, (float, np.floating)) else str(value)
                for value in values
            ]
        )
    widths = [max(len(column), *(len(row[index]) for row in rows)) for index, column in enumerate(columns)]
    header = "| " + " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    separator = "| " + " | ".join("-" * widths[index] for index in range(len(columns))) + " |"
    body = ["| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def plot_results(by_source: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    for axis, metric, title in zip(axes, ["roc_auc", "f1"], ["ROC-AUC by held-out source", "F1 by held-out source"]):
        pivot = by_source.pivot(index="held_out_source", columns="model", values=metric)
        pivot.plot(kind="bar", ax=axis, rot=25, color=["#287764", "#bd7045", "#526a91"])
        axis.set_title(title)
        axis.set_ylabel(metric.upper())
        axis.set_xlabel("")
        axis.grid(axis="y", alpha=0.2)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Paper-grounded HPEM and baseline comparison", fontsize=14)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_report(
    by_source: pd.DataFrame,
    summary: pd.DataFrame,
    predictions: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_path = output_dir / "hpem_source_metrics.csv"
    summary_path = output_dir / "hpem_summary.csv"
    predictions_path = output_dir / "hpem_heldout_predictions.csv"
    report_path = output_dir / "hpem_benchmark.md"
    by_source.to_csv(source_path, index=False)
    summary.to_csv(summary_path, index=False)
    # Keep per-row probabilities to support reproducible paired analysis and calibration review.
    predictions.to_csv(predictions_path, index=False)
    summary_columns = ["model", "n_sources", "n_total", "accuracy_mean", "accuracy_sd_across_sources", "f1_mean", "f1_sd_across_sources", "roc_auc_mean", "roc_auc_sd_across_sources", "pr_auc_mean", "brier_score_mean", "log_loss_mean"]
    source_columns = ["held_out_source", "model", "n_test", "accuracy", "sensitivity", "specificity", "f1", "roc_auc", "pr_auc", "brier_score"]
    report_path.write_text(
        f"""# HPEM Reproduction Benchmark

## Paper-grounded method

This is a tabular HPEM reproduction on the raw unified clinical cohort using leave-one-source-out evaluation. It implements second-degree polynomial expansion, mutual-information selection of the top 15 transformed features, Random Forest + Gradient Boosting + RBF-SVM soft voting, and an XGBoost meta-learner trained on the three base learners' probabilities. All preprocessing and feature selection are fitted within training partitions.

The paper pseudocode trains the XGBoost meta-learner on base-ensemble predictions made on the same training records. To avoid stacking leakage, this implementation instead trains the meta-learner on 3-fold out-of-fold probabilities from each of the three base learners within the outer training sources. This is a leakage-safe methodological adaptation and is not an exact reproduction of the pseudocode's meta-training step. The paper's stated 5-fold CV on pooled datasets also differs from this source-held-out stress test.

A direct XGBoost baseline and soft-voting-only model are evaluated on the identical held-out sources. Metrics use a 0.5 threshold for thresholded classification measures; mean and SD are across five source holdouts, not confidence intervals.

## Summary across held-out sources

{markdown_table(summary, summary_columns)}

## Source-specific performance

{markdown_table(by_source, source_columns)}

![HPEM source-held-out comparison](plots/hpem_source_comparison.png)

## Interpretation

This dataset-specific reproduction cannot confirm the paper's reported performance because its cohort composition, target harmonization, and validation design differ. The unified cohort has only five source groups and marked distribution shift; do not interpret source-level estimates as stable clinical performance. The best model should be selected by the intended use and paired uncertainty analysis, not one pooled ranking.

Machine-readable source results: `{source_path.name}`. Summary: `{summary_path.name}`. Held-out prediction rows are retained in `{predictions_path.name}`.
""",
        encoding="utf-8",
    )
    print(f"Saved {report_path}, {source_path}, {summary_path}, and {predictions_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    by_source, summary, predictions = run_benchmark(args.unified_raw)
    predictions_path = args.output_dir / "hpem_heldout_predictions.csv"
    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(predictions_path, index=False)
    plot_results(by_source, args.output_dir / "plots" / "hpem_source_comparison.png")
    write_report(by_source, summary, predictions, args.output_dir)


if __name__ == "__main__":
    main()
