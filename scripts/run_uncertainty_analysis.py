"""Estimate conditional bootstrap intervals and threshold trade-offs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold

from run_baselines import (
    CARDIO_CATEGORICAL,
    CARDIO_NUMERICAL,
    RANDOM_SEED,
    UNIFIED_CATEGORICAL,
    UNIFIED_NUMERICAL,
    make_models,
)


METRICS = ("roc_auc", "pr_auc", "accuracy", "sensitivity", "specificity", "f1", "brier_score")
THRESHOLDS = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)


def calculate_metrics(target: np.ndarray, probability: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    prediction = (probability >= threshold).astype(int)
    true_negative = int(((target == 0) & (prediction == 0)).sum())
    false_positive = int(((target == 0) & (prediction == 1)).sum())
    false_negative = int(((target == 1) & (prediction == 0)).sum())
    true_positive = int(((target == 1) & (prediction == 1)).sum())
    return {
        "roc_auc": float(roc_auc_score(target, probability)),
        "pr_auc": float(average_precision_score(target, probability)),
        "accuracy": float(accuracy_score(target, prediction)),
        "sensitivity": float(recall_score(target, prediction, zero_division=0)),
        "specificity": float(recall_score(target, prediction, pos_label=0, zero_division=0)),
        "precision": float(precision_score(target, prediction, zero_division=0)),
        "f1": float(f1_score(target, prediction, zero_division=0)),
        "brier_score": float(brier_score_loss(target, probability)),
        "predicted_positive_rate": float(prediction.mean()),
        "false_positive": float(false_positive),
        "false_negative": float(false_negative),
        "true_positive": float(true_positive),
        "true_negative": float(true_negative),
    }


def cardio_oof_predictions(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if frame["patient_id"].duplicated().any():
        raise ValueError("Cardio70k contains repeated patient IDs; grouped validation is required.")
    features = frame.drop(columns=["patient_id", "target"])
    target = frame["target"].astype(int)
    model_names = ("LogisticRegression", "XGBoost")
    probabilities = {name: np.full(len(frame), np.nan, dtype=float) for name in model_names}
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    models = make_models(CARDIO_CATEGORICAL, CARDIO_NUMERICAL)
    for train_indices, test_indices in splitter.split(features, target):
        for model_name in model_names:
            model = models[model_name]
            model.fit(features.iloc[train_indices], target.iloc[train_indices])
            probabilities[model_name][test_indices] = model.predict_proba(
                features.iloc[test_indices]
            )[:, 1]
    rows = []
    for model_name, values in probabilities.items():
        rows.append(
            pd.DataFrame(
                {
                    "cohort": "Cardio70k",
                    "source": "All folds",
                    "model": model_name,
                    "target": target.to_numpy(),
                    "probability": values,
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


def unified_predictions(raw_path: Path, hpem_predictions_path: Path) -> pd.DataFrame:
    raw = pd.read_csv(raw_path)
    saved = pd.read_csv(hpem_predictions_path)
    model_map = {
        "HPEM (OOF soft-vote meta)": "HPEM (OOF soft-vote meta)",
        "XGBoost baseline": "XGBoost",
    }
    rows = [
        saved.loc[saved["model"] == old_name].copy()
        .assign(record_id=lambda part: part.groupby("held_out_source").cumcount())
        .assign(cohort="Unified clinical", model=new_name)[
            ["cohort", "held_out_source", "model", "record_id", "target", "probability"]
        ]
        .rename(columns={"held_out_source": "source"})
        for old_name, new_name in model_map.items()
    ]
    feature_columns = UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL
    for source in sorted(raw["source"].dropna().unique()):
        train = raw.loc[raw["source"] != source]
        test = raw.loc[raw["source"] == source]
        train_y = train["target"].astype(int)
        model = make_models(UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL)["LogisticRegression"]
        model.fit(train[feature_columns], train_y)
        predicted = model.predict_proba(test[feature_columns])[:, 1]
        record_id = np.arange(len(test))
        rows.append(
            pd.DataFrame(
                {
                    "cohort": "Unified clinical",
                    "source": source,
                    "model": "LogisticRegression",
                    "record_id": record_id,
                    "target": test["target"].astype(int).to_numpy(),
                    "probability": predicted,
                }
            )
        )
    predictions = pd.concat(rows, ignore_index=True)
    if predictions["probability"].isna().any():
        raise ValueError("Saved unified predictions contain missing probabilities.")
    return predictions


def bootstrap_group(
    rows: pd.DataFrame, replicates: int, rng: np.random.Generator
) -> tuple[dict[str, tuple[float, float, float]], dict[str, tuple[float, float, float]]]:
    target = rows["target"].to_numpy(dtype=int)
    probability = rows["probability"].to_numpy(dtype=float)
    point = calculate_metrics(target, probability)
    strata = [np.flatnonzero(target == label) for label in (0, 1)]
    if any(len(indices) == 0 for indices in strata):
        raise ValueError("Both outcome classes are required for bootstrap estimates.")
    samples = {metric: np.empty(replicates, dtype=float) for metric in METRICS}
    for replicate in range(replicates):
        sampled_indices = np.concatenate(
            [rng.choice(indices, size=len(indices), replace=True) for indices in strata]
        )
        for metric, value in calculate_metrics(target[sampled_indices], probability[sampled_indices]).items():
            if metric in samples:
                samples[metric][replicate] = value
    intervals = {
        metric: (
            float(point[metric]),
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        )
        for metric, values in samples.items()
    }
    return intervals, point


def stratified_resample(
    rows: pd.DataFrame, rng: np.random.Generator
) -> np.ndarray:
    indices = []
    for _, group in rows.groupby(["source", "target"], sort=False, dropna=False):
        group_indices = group.index.to_numpy()
        indices.append(rng.choice(group_indices, size=len(group_indices), replace=True))
    return np.concatenate(indices)


def bootstrap_unified_paired(
    predictions: pd.DataFrame, replicates: int, seed: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    metrics_rows = []
    delta_rows = []
    group_specs = [("All sources", predictions)]
    group_specs.extend(
        (str(source), predictions.loc[predictions["source"] == source])
        for source in sorted(predictions["source"].unique())
    )
    for scope, scope_rows in group_specs:
        for model_name, model_rows in scope_rows.groupby("model", sort=False):
            if scope == "All sources":
                # Resample within each source and outcome class to preserve the observed source mix.
                samples = {metric: [] for metric in METRICS}
                target = model_rows["target"].to_numpy(dtype=int)
                probability = model_rows["probability"].to_numpy(dtype=float)
                point = calculate_metrics(target, probability)
                strata = [
                    model_rows.index[(model_rows["source"] == source) & (model_rows["target"] == label)].to_numpy()
                    for source in sorted(model_rows["source"].unique())
                    for label in (0, 1)
                ]
                for _ in range(replicates):
                    sampled = np.concatenate(
                        [rng.choice(indices, size=len(indices), replace=True) for indices in strata if len(indices)]
                    )
                    sampled_rows = model_rows.loc[sampled]
                    bootstrap_values = calculate_metrics(
                        sampled_rows["target"].to_numpy(dtype=int),
                        sampled_rows["probability"].to_numpy(dtype=float),
                    )
                    for metric in METRICS:
                        samples[metric].append(bootstrap_values[metric])
                intervals = {
                    metric: (
                        point[metric],
                        float(np.quantile(values, 0.025)),
                        float(np.quantile(values, 0.975)),
                    )
                    for metric, values in samples.items()
                }
            else:
                intervals, point = bootstrap_group(model_rows, replicates, rng)
            metrics_rows.extend(
                {
                    "cohort": "Unified clinical",
                    "scope": scope,
                    "model": model_name,
                    "n": len(model_rows),
                    "metric": metric,
                    "estimate": values[0],
                    "ci_95_lower": values[1],
                    "ci_95_upper": values[2],
                    "bootstrap_replicates": replicates,
                }
                for metric, values in intervals.items()
            )

        if scope == "All sources":
            model_names = set(scope_rows["model"])
            comparisons = [("HPEM (OOF soft-vote meta)", "XGBoost"), ("LogisticRegression", "XGBoost")]
        else:
            model_names = set(scope_rows["model"])
            comparisons = [("HPEM (OOF soft-vote meta)", "XGBoost"), ("LogisticRegression", "XGBoost")]
        for first, second in comparisons:
            if first not in model_names or second not in model_names:
                continue
            wide = scope_rows.pivot(
                index=["source", "record_id", "target"],
                columns="model",
                values="probability",
            ).reset_index()
            bootstrap_differences = {metric: [] for metric in METRICS}
            point_a = calculate_metrics(wide["target"].to_numpy(dtype=int), wide[first].to_numpy(dtype=float))
            point_b = calculate_metrics(wide["target"].to_numpy(dtype=int), wide[second].to_numpy(dtype=float))
            for _ in range(replicates):
                if scope == "All sources":
                    sampled_indices = stratified_resample(wide, rng)
                else:
                    target_values = wide["target"].to_numpy(dtype=int)
                    sampled_indices = np.concatenate(
                        [
                            rng.choice(np.flatnonzero(target_values == label), size=int((target_values == label).sum()), replace=True)
                            for label in (0, 1)
                        ]
                    )
                sampled = wide.iloc[sampled_indices]
                metrics_a = calculate_metrics(sampled["target"].to_numpy(dtype=int), sampled[first].to_numpy(dtype=float))
                metrics_b = calculate_metrics(sampled["target"].to_numpy(dtype=int), sampled[second].to_numpy(dtype=float))
                for metric in METRICS:
                    bootstrap_differences[metric].append(metrics_a[metric] - metrics_b[metric])
            for metric in METRICS:
                differences = bootstrap_differences[metric]
                delta_rows.append(
                    {
                        "cohort": "Unified clinical",
                        "scope": scope,
                        "comparison": f"{first} minus {second}",
                        "metric": metric,
                        "estimate_difference": point_a[metric] - point_b[metric],
                        "ci_95_lower": float(np.quantile(differences, 0.025)),
                        "ci_95_upper": float(np.quantile(differences, 0.975)),
                        "bootstrap_replicates": replicates,
                    }
                )
    return pd.DataFrame(metrics_rows), pd.DataFrame(delta_rows)


def bootstrap_cardio_paired(
    predictions: pd.DataFrame, replicates: int, seed: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    metrics_rows = []
    delta_rows = []
    # Model blocks share the same original row order for paired resampling.
    models = list(predictions["model"].drop_duplicates())
    row_count = len(predictions.loc[predictions["model"] == models[0]])
    targets = predictions.loc[predictions["model"] == models[0], "target"].to_numpy(dtype=int)
    probabilities = {
        model: predictions.loc[predictions["model"] == model, "probability"].to_numpy(dtype=float)
        for model in models
    }
    strata = [np.flatnonzero(targets == label) for label in (0, 1)]
    sample_metrics = {model: {metric: [] for metric in METRICS} for model in models}
    sample_deltas = {metric: [] for metric in METRICS}
    point_metrics = {
        model: calculate_metrics(targets, values) for model, values in probabilities.items()
    }
    for _ in range(replicates):
        sampled = np.concatenate(
            [rng.choice(indices, size=len(indices), replace=True) for indices in strata]
        )
        for model in models:
            result = calculate_metrics(targets[sampled], probabilities[model][sampled])
            for metric in METRICS:
                sample_metrics[model][metric].append(result[metric])
        delta = calculate_metrics(targets[sampled], probabilities["XGBoost"][sampled])
        comparison = calculate_metrics(targets[sampled], probabilities["LogisticRegression"][sampled])
        for metric in METRICS:
            sample_deltas[metric].append(comparison[metric] - delta[metric])
    for model in models:
        for metric in METRICS:
            values = sample_metrics[model][metric]
            metrics_rows.append(
                {
                    "cohort": "Cardio70k",
                    "scope": "All folds",
                    "model": model,
                    "n": row_count,
                    "metric": metric,
                    "estimate": point_metrics[model][metric],
                    "ci_95_lower": float(np.quantile(values, 0.025)),
                    "ci_95_upper": float(np.quantile(values, 0.975)),
                    "bootstrap_replicates": replicates,
                }
            )
    for metric in METRICS:
        values = sample_deltas[metric]
        delta_rows.append(
            {
                "cohort": "Cardio70k",
                "scope": "All folds",
                "comparison": "LogisticRegression minus XGBoost",
                "metric": metric,
                "estimate_difference": point_metrics["LogisticRegression"][metric] - point_metrics["XGBoost"][metric],
                "ci_95_lower": float(np.quantile(values, 0.025)),
                "ci_95_upper": float(np.quantile(values, 0.975)),
                "bootstrap_replicates": replicates,
            }
        )
    return pd.DataFrame(metrics_rows), pd.DataFrame(delta_rows)


def threshold_profiles(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    grouped_predictions = list(predictions.groupby(
        ["cohort", "source", "model"], sort=False
    ))
    unified = predictions.loc[predictions["cohort"] == "Unified clinical"]
    grouped_predictions.extend(
        (
            ("Unified clinical", "All held-out sources", model),
            model_rows,
        )
        for model, model_rows in unified.groupby("model", sort=False)
    )
    for (cohort, source, model), group in grouped_predictions:
        target = group["target"].to_numpy(dtype=int)
        probabilities = group["probability"].to_numpy(dtype=float)
        for threshold in THRESHOLDS:
            metrics = calculate_metrics(target, probabilities, threshold)
            rows.append(
                {
                    "cohort": cohort,
                    "scope": source,
                    "model": model,
                    "threshold": threshold,
                    "n": len(group),
                    "sensitivity": metrics["sensitivity"],
                    "specificity": metrics["specificity"],
                    "precision": metrics["precision"],
                    "predicted_positive_rate": metrics["predicted_positive_rate"],
                    "false_positive": int(metrics["false_positive"]),
                    "false_negative": int(metrics["false_negative"]),
                }
            )
    return pd.DataFrame(rows)


def plot_thresholds(profiles: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    card = profiles.loc[
        (profiles["cohort"] == "Cardio70k") & (profiles["scope"] == "All folds")
    ]
    unified = profiles.loc[
        (profiles["cohort"] == "Unified clinical")
        & (profiles["scope"] == "All held-out sources")
    ]
    for axis, subset, title in [
        (axes[0], card, "Cardio70k: pooled OOF"),
        (axes[1], unified, "Unified cohort: source-held-out"),
    ]:
        for model, model_rows in subset.groupby("model", sort=False):
            axis.plot(model_rows["threshold"], model_rows["sensitivity"], marker="o", label=f"{model} sensitivity")
            axis.plot(model_rows["threshold"], model_rows["specificity"], marker="s", linestyle="--", label=f"{model} specificity")
        axis.set_title(title)
        axis.set_xlabel("Probability threshold")
        axis.set_ylabel("Rate")
        axis.set_ylim(0, 1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, fontsize=7)
    fig.suptitle("Threshold trade-offs; no clinical cutoff selected", fontsize=13)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    rows = [[str(value) for value in row] for row in frame[columns].itertuples(index=False, name=None)]
    widths = [max(len(column), *(len(row[index]) for row in rows)) for index, column in enumerate(columns)]
    header = "| " + " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    separator = "| " + " | ".join("-" * widths[index] for index in range(len(columns))) + " |"
    body = ["| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_report(
    metrics: pd.DataFrame,
    deltas: pd.DataFrame,
    thresholds: pd.DataFrame,
    output_dir: Path,
    bootstrap_replicates: int,
) -> None:
    metrics_path = output_dir / "bootstrap_metric_intervals.csv"
    deltas_path = output_dir / "paired_bootstrap_differences.csv"
    thresholds_path = output_dir / "threshold_profiles.csv"
    report_path = output_dir / "uncertainty_threshold_analysis.md"
    metrics.to_csv(metrics_path, index=False)
    deltas.to_csv(deltas_path, index=False)
    thresholds.to_csv(thresholds_path, index=False)
    display_metrics = metrics.copy()
    for column in ["estimate", "ci_95_lower", "ci_95_upper"]:
        display_metrics[column] = display_metrics[column].map(lambda value: f"{value:.4f}")
    display_deltas = deltas.copy()
    for column in ["estimate_difference", "ci_95_lower", "ci_95_upper"]:
        display_deltas[column] = display_deltas[column].map(lambda value: f"{value:.4f}")
    selected_thresholds = thresholds.loc[thresholds["threshold"].isin([0.3, 0.5, 0.7])].copy()
    for column in ["threshold", "sensitivity", "specificity", "precision", "predicted_positive_rate"]:
        selected_thresholds[column] = selected_thresholds[column].map(lambda value: f"{value:.3f}")
    report_path.write_text(
        f"""# Uncertainty and Threshold Analysis

## Protocol

Cardio70k estimates use 5-fold out-of-fold predictions for Logistic Regression and XGBoost. Unified-cohort estimates use the saved leave-one-source-out predictions for HPEM and XGBoost and newly generated leave-one-source-out Logistic Regression predictions. Confidence intervals are percentile intervals from {bootstrap_replicates} stratified bootstrap resamples. Cardio70k resampling preserves the observed outcome counts; unified resampling preserves each source-by-outcome cell and therefore conditions on the observed source mix and prevalence. Comparisons use paired resamples of the same records.

These intervals quantify sampling variability conditional on these datasets, splits, fitted pipelines, and observed source composition. They do not account for model-selection uncertainty, source-population uncertainty, or external transport. Five sources are not enough to estimate uncertainty over a population of sources.

## Held-out metric estimates with conditional 95% intervals

{markdown_table(display_metrics, ["cohort", "scope", "model", "n", "metric", "estimate", "ci_95_lower", "ci_95_upper"])}

## Paired metric differences

Differences are first model minus second model; intervals crossing zero do not establish a difference. These are exploratory paired comparisons, not a new selection step.

{markdown_table(display_deltas, ["cohort", "scope", "comparison", "metric", "estimate_difference", "ci_95_lower", "ci_95_upper"])}

## Threshold profiles

The table shows sensitivity, specificity, precision, predicted-positive rate, and error counts at selected probability thresholds. No threshold is recommended because the intended clinical action and relative harms of false positives and false negatives are not defined. Thresholds are not calibrated risk cutoffs on the unified cohort.

{markdown_table(selected_thresholds, ["cohort", "scope", "model", "threshold", "n", "sensitivity", "specificity", "precision", "predicted_positive_rate", "false_positive", "false_negative"])}

![Threshold trade-off curves](plots/threshold_tradeoffs.png)

## Interpretation

Use the source-specific rows to see where performance changes; pooled unified values can conceal source reversal and distribution shift. Calibration and clinical utility need independent validation. A future deployment-oriented analysis must define the target population, action, and acceptable error trade-off before choosing a threshold.

Data: `{metrics_path.name}`, `{deltas_path.name}`, `{thresholds_path.name}`.
""",
        encoding="utf-8",
    )
    print(f"Saved {report_path}, {metrics_path}, {deltas_path}, and {thresholds_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--hpem-predictions", type=Path, default=Path("reports/hpem_heldout_predictions.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--bootstrap-replicates", type=int, default=300)
    args = parser.parse_args()
    if args.bootstrap_replicates < 50:
        parser.error("Use at least 50 bootstrap replicates")
    cardio = cardio_oof_predictions(args.cardio70k)
    unified = unified_predictions(args.unified_raw, args.hpem_predictions)
    predictions = pd.concat([cardio, unified], ignore_index=True)
    cardio_metrics, cardio_deltas = bootstrap_cardio_paired(
        cardio, args.bootstrap_replicates, RANDOM_SEED
    )
    unified_metrics, unified_deltas = bootstrap_unified_paired(
        unified, args.bootstrap_replicates, RANDOM_SEED + 1
    )
    metrics = pd.concat([cardio_metrics, unified_metrics], ignore_index=True)
    deltas = pd.concat([cardio_deltas, unified_deltas], ignore_index=True)
    thresholds = threshold_profiles(predictions)
    plot_thresholds(thresholds, args.output_dir / "plots" / "threshold_tradeoffs.png")
    write_report(metrics, deltas, thresholds, args.output_dir, args.bootstrap_replicates)


if __name__ == "__main__":
    main()
