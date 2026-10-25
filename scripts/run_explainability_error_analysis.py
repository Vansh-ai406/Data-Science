"""Run held-out permutation importance and descriptive subgroup error analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix, f1_score, precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold

from run_baselines import (
    CARDIO_CATEGORICAL,
    CARDIO_NUMERICAL,
    RANDOM_SEED,
    UNIFIED_CATEGORICAL,
    UNIFIED_NUMERICAL,
    make_models,
)


N_SPLITS = 5
MODEL_NAME = "XGBoost"
THRESHOLD = 0.5
AGE_BINS = [0, 45, 60, np.inf]
AGE_LABELS = ["<45", "45-59", "60+"]


def evaluate_groups(
    cohort: str,
    predictions: pd.DataFrame,
    group_columns: list[tuple[str, str]],
    minimum_group_size: int,
) -> pd.DataFrame:
    rows = []
    for group_type, column in group_columns:
        groups = [("All", predictions)] if column is None else list(predictions.groupby(column, dropna=False, sort=True))
        for group_value, subset in groups:
            y_true = subset["target"].to_numpy(dtype=int)
            probabilities = subset["probability"].to_numpy(dtype=float)
            predicted = (probabilities >= THRESHOLD).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_true, predicted, labels=[0, 1]).ravel()
            positive_count = int(y_true.sum())
            negative_count = len(y_true) - positive_count
            sufficient = len(y_true) >= minimum_group_size and min(positive_count, negative_count) >= 20
            display_group = (
                {0: "Female (code 0)", 1: "Male (code 1)"}.get(int(group_value), str(group_value))
                if group_type == "Sex"
                else str(group_value)
            )
            rows.append(
                {
                    "cohort": cohort,
                    "model": MODEL_NAME,
                    "group_type": group_type,
                    "group": display_group,
                    "n": len(y_true),
                    "positive_n": positive_count,
                    "negative_n": negative_count,
                    "prevalence": positive_count / len(y_true),
                    "predicted_positive_rate": float(predicted.mean()),
                    "sensitivity": tp / (tp + fn) if tp + fn else np.nan,
                    "specificity": tn / (tn + fp) if tn + fp else np.nan,
                    "precision": precision_score(y_true, predicted, zero_division=0),
                    "f1": f1_score(y_true, predicted, zero_division=0),
                    "roc_auc": roc_auc_score(y_true, probabilities) if len(np.unique(y_true)) == 2 else np.nan,
                    "brier_score": float(np.mean((probabilities - y_true) ** 2)),
                    "tn": int(tn),
                    "fp": int(fp),
                    "fn": int(fn),
                    "tp": int(tp),
                    "interpretation_status": "Reviewable" if sufficient else "Small cell: descriptive only",
                }
            )
    return pd.DataFrame(rows)


def add_age_band(frame: pd.DataFrame, age_column: str) -> pd.DataFrame:
    result = frame.copy()
    result["age_band"] = pd.cut(
        result[age_column], bins=AGE_BINS, labels=AGE_LABELS, right=False
    ).astype("string")
    return result


def fit_cardio(path: Path, repeats: int, minimum_group_size: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(path)
    if frame["patient_id"].duplicated().any():
        raise ValueError("Cardio70k contains repeated patient IDs; use grouped CV.")
    features = frame.drop(columns=["patient_id", "target"])
    target = frame["target"].astype(int)
    predictions = np.full(len(frame), np.nan, dtype=float)
    importance_rows = []
    splitter = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)
    for fold, (train_indices, test_indices) in enumerate(splitter.split(features, target), start=1):
        train_x, test_x = features.iloc[train_indices], features.iloc[test_indices]
        train_y, test_y = target.iloc[train_indices], target.iloc[test_indices]
        model = make_models(CARDIO_CATEGORICAL, CARDIO_NUMERICAL)[MODEL_NAME]
        model.fit(train_x, train_y)
        probabilities = model.predict_proba(test_x)[:, 1]
        predictions[test_indices] = probabilities
        fold_importance = permutation_importance(
            model,
            test_x,
            test_y,
            scoring="roc_auc",
            n_repeats=repeats,
            random_state=RANDOM_SEED + fold,
            n_jobs=-1,
        )
        importance_rows.extend(
            {
                "cohort": "Cardio70k",
                "held_out_group": f"Fold {fold}",
                "feature": feature,
                "importance_mean": float(fold_importance.importances_mean[index]),
                "importance_std_within_fold": float(fold_importance.importances_std[index]),
                "baseline_roc_auc": roc_auc_score(test_y, probabilities),
                "n_repeats": repeats,
            }
            for index, feature in enumerate(features.columns)
        )
    result = add_age_band(frame, "age_years")
    result["target"] = target
    result["probability"] = predictions
    groups = [("Overall", None), ("Sex", "sex"), ("Age band", "age_band")]
    return pd.DataFrame(importance_rows), evaluate_groups(
        "Cardio70k", result, groups, minimum_group_size
    )


def fit_unified(path: Path, repeats: int, minimum_group_size: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(path)
    feature_columns = UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL
    importance_rows = []
    prediction_frames = []
    for source_number, held_out_source in enumerate(sorted(frame["source"].dropna().unique()), start=1):
        train = frame.loc[frame["source"] != held_out_source]
        test = frame.loc[frame["source"] == held_out_source]
        train_y, test_y = train["target"].astype(int), test["target"].astype(int)
        if train_y.nunique() != 2 or test_y.nunique() != 2:
            raise ValueError(f"Both target classes are required for {held_out_source}.")
        model = make_models(UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL)[MODEL_NAME]
        model.fit(train[feature_columns], train_y)
        probabilities = model.predict_proba(test[feature_columns])[:, 1]
        fold_importance = permutation_importance(
            model,
            test[feature_columns],
            test_y,
            scoring="roc_auc",
            n_repeats=repeats,
            random_state=RANDOM_SEED + source_number,
            n_jobs=-1,
        )
        importance_rows.extend(
            {
                "cohort": "Unified clinical",
                "held_out_group": held_out_source,
                "feature": feature,
                "importance_mean": float(fold_importance.importances_mean[index]),
                "importance_std_within_fold": float(fold_importance.importances_std[index]),
                "baseline_roc_auc": roc_auc_score(test_y, probabilities),
                "n_repeats": repeats,
            }
            for index, feature in enumerate(feature_columns)
        )
        held_out = test.copy()
        held_out["probability"] = probabilities
        prediction_frames.append(held_out)
    held_out_predictions = pd.concat(prediction_frames, ignore_index=True)
    held_out_predictions = add_age_band(held_out_predictions, "age")
    groups = [("Overall", None), ("Source", "source"), ("Sex", "sex"), ("Age band", "age_band")]
    return pd.DataFrame(importance_rows), evaluate_groups(
        "Unified clinical", held_out_predictions, groups, minimum_group_size
    )


def summarize_importance(raw: pd.DataFrame) -> pd.DataFrame:
    summary = (
        raw.groupby(["cohort", "feature"], as_index=False)
        .agg(
            importance_mean=("importance_mean", "mean"),
            importance_sd_across_held_out=("importance_mean", "std"),
            held_out_groups=("held_out_group", "nunique"),
        )
        .fillna({"importance_sd_across_held_out": 0.0})
    )
    summary["rank_within_cohort"] = summary.groupby("cohort")["importance_mean"].rank(
        method="min", ascending=False
    ).astype(int)
    return summary.sort_values(["cohort", "rank_within_cohort"])


def plot_importance(summary: pd.DataFrame, output_path: Path) -> None:
    cohorts = list(summary["cohort"].drop_duplicates())
    fig, axes = plt.subplots(1, len(cohorts), figsize=(14, 6), squeeze=False, constrained_layout=True)
    for axis, cohort in zip(axes[0], cohorts):
        selected = summary.loc[summary["cohort"] == cohort].nsmallest(10, "rank_within_cohort")
        selected = selected.sort_values("importance_mean")
        axis.barh(
            selected["feature"],
            selected["importance_mean"],
            xerr=selected["importance_sd_across_held_out"],
            color="#287764" if cohort == "Cardio70k" else "#bd7045",
            alpha=0.9,
            capsize=2,
        )
        axis.axvline(0, color="#384541", linewidth=0.8)
        axis.set_title(cohort)
        axis.set_xlabel("Held-out ROC-AUC decrease after permutation")
        axis.grid(axis="x", alpha=0.2)
    fig.suptitle("Permutation importance (model reliance, not causal effect)", fontsize=13)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_subgroups(groups: pd.DataFrame, output_path: Path) -> None:
    group_types = ["Age band", "Sex code", "Source"]
    cohorts = ["Cardio70k", "Unified clinical"]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    for row_index, cohort in enumerate(cohorts):
        for column_index, group_type in enumerate(group_types):
            axis = axes[row_index, column_index]
            selected = groups.loc[
                (groups["cohort"] == cohort)
                & (groups["group_type"] == group_type)
                & (groups["interpretation_status"] == "Reviewable")
            ]
            if selected.empty:
                axis.text(0.5, 0.5, "Not applicable", ha="center", va="center")
                axis.set_axis_off()
                continue
            positions = np.arange(len(selected))
            axis.bar(positions - 0.18, selected["sensitivity"], width=0.36, label="Sensitivity", color="#287764")
            axis.bar(positions + 0.18, selected["specificity"], width=0.36, label="Specificity", color="#bd7045")
            axis.set_xticks(positions, selected["group"], rotation=35, ha="right")
            axis.set_ylim(0, 1)
            axis.set_title(f"{cohort}: {group_type}")
            axis.grid(axis="y", alpha=0.2)
            if row_index == 0 and column_index == 0:
                axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Held-out threshold performance by subgroup (threshold 0.5)", fontsize=13)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    rows = [[str(value) for value in row] for row in frame.itertuples(index=False, name=None)]
    widths = [max(len(column), *(len(row[index]) for row in rows)) for index, column in enumerate(columns)]
    header = "| " + " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    separator = "| " + " | ".join("-" * widths[index] for index in range(len(columns))) + " |"
    body = ["| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_report(
    importance: pd.DataFrame,
    groups: pd.DataFrame,
    importance_by_split: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "permutation_importance_summary.csv"
    split_path = output_dir / "permutation_importance_by_holdout.csv"
    subgroup_path = output_dir / "subgroup_error_metrics.csv"
    report_path = output_dir / "explainability_error_analysis.md"
    importance.to_csv(summary_path, index=False)
    importance_by_split.to_csv(split_path, index=False)
    groups.to_csv(subgroup_path, index=False)
    top_features = importance.groupby("cohort", sort=False).head(10)
    top_display = top_features.copy()
    for column in ["importance_mean", "importance_sd_across_held_out"]:
        top_display[column] = top_display[column].map(lambda value: f"{value:.4f}")
    top_text = render_markdown_table(top_display)
    display_columns = ["cohort", "group_type", "group", "n", "positive_n", "sensitivity", "specificity", "precision", "f1", "roc_auc", "brier_score", "interpretation_status"]
    display_groups = groups[display_columns].copy()
    for column in ["sensitivity", "specificity", "precision", "f1", "roc_auc", "brier_score"]:
        display_groups[column] = display_groups[column].map(lambda value: f"{value:.3f}" if pd.notna(value) else "NA")
    group_text = render_markdown_table(display_groups)
    report_path.write_text(
        f"""# Held-out Explainability and Error Analysis

## Protocol

XGBoost was evaluated using Cardio70k stratified 5-fold out-of-fold predictions and unified-cohort leave-one-source-out predictions. Permutation importance was measured on each held-out fold/source using ROC-AUC decrease, then summarized across held-out units. Group metrics use the same held-out probabilities and a fixed 0.5 threshold. Age bands are <45, 45-59, and 60+. The supplied dataset legend documents the binary sex field as 0=female and 1=male; this coding does not represent a broader set of gender identities.

## Permutation importance

{top_text}

Permutation importance estimates how much this fitted model relies on a feature for ranking performance in these evaluation folds. It is not a causal effect, a clinical risk factor ranking, or proof of independent feature value. Correlated predictors can share or mask importance; source-specific importance can vary.

![Held-out permutation importance](plots/permutation_importance.png)

## Subgroup and source error metrics

{group_text}

![Subgroup error comparison](plots/subgroup_performance.png)

Rows marked `Small cell: descriptive only` have fewer than the configured minimum observations or fewer than 20 examples in either class and should not support comparative claims. These subgroup analyses are exploratory, unadjusted, and not fairness certification. Unified-cohort strata combine heterogeneous sources unless a row explicitly identifies a source; source-level results should be considered alongside subgroup results.

## Remaining research

Independent external validation, confidence intervals for subgroup metrics, threshold selection tied to a defined use case, and a protocol-grounded reproduction of the foundation-paper HPEM remain open. No clinical utility or deployment claim is supported by these experiments.

Files: `{summary_path.name}`, `{split_path.name}`, and `{subgroup_path.name}`.
""",
        encoding="utf-8",
    )
    print(f"Saved {report_path}, {summary_path}, {split_path}, and {subgroup_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--permutation-repeats", type=int, default=3)
    parser.add_argument("--minimum-group-size", type=int, default=30)
    args = parser.parse_args()
    if args.permutation_repeats < 1 or args.minimum_group_size < 1:
        parser.error("repeat count and minimum group size must be positive")
    cardio_importance, cardio_groups = fit_cardio(
        args.cardio70k, args.permutation_repeats, args.minimum_group_size
    )
    unified_importance, unified_groups = fit_unified(
        args.unified_raw, args.permutation_repeats, args.minimum_group_size
    )
    raw_importance = pd.concat([cardio_importance, unified_importance], ignore_index=True)
    importance = summarize_importance(raw_importance)
    groups = pd.concat([cardio_groups, unified_groups], ignore_index=True)
    plot_importance(importance, args.output_dir / "plots" / "permutation_importance.png")
    plot_subgroups(groups, args.output_dir / "plots" / "subgroup_performance.png")
    write_report(importance, groups, raw_importance, args.output_dir)


if __name__ == "__main__":
    main()
