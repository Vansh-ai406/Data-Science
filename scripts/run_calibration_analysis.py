"""Evaluate probability calibration with leakage-safe held-out predictions."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.metrics import brier_score_loss, log_loss
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
N_BINS = 10
MODELS = ("LogisticRegression", "XGBoost")


def calibration_statistics(
    y_true: np.ndarray, probabilities: np.ndarray
) -> tuple[dict[str, float], pd.DataFrame]:
    clipped = np.clip(probabilities, 1e-6, 1 - 1e-6)
    logits = np.log(clipped / (1 - clipped))

    def objective(parameters: np.ndarray) -> tuple[float, np.ndarray]:
        linear = parameters[0] + parameters[1] * logits
        fitted = 1 / (1 + np.exp(-np.clip(linear, -35, 35)))
        loss = np.logaddexp(0, linear) - y_true * linear
        gradient = np.array([np.sum(fitted - y_true), np.sum((fitted - y_true) * logits)])
        return float(np.mean(loss)), gradient / len(y_true)

    fitted_calibration = minimize(
        objective,
        x0=np.array([0.0, 1.0]),
        jac=True,
        method="BFGS",
    )
    bin_edges = np.linspace(0, 1, N_BINS + 1)
    bin_ids = np.minimum(np.digitize(clipped, bin_edges[1:-1]), N_BINS - 1)
    bin_rows = []
    weighted_error = 0.0
    for bin_number in range(N_BINS):
        selected = bin_ids == bin_number
        count = int(selected.sum())
        if not count:
            continue
        mean_predicted = float(clipped[selected].mean())
        observed_fraction = float(y_true[selected].mean())
        weighted_error += count / len(y_true) * abs(mean_predicted - observed_fraction)
        bin_rows.append(
            {
                "bin": bin_number + 1,
                "lower_bound": bin_edges[bin_number],
                "upper_bound": bin_edges[bin_number + 1],
                "n": count,
                "mean_predicted_probability": mean_predicted,
                "observed_positive_fraction": observed_fraction,
            }
        )
    return (
        {
            "brier_score": float(brier_score_loss(y_true, clipped)),
            "log_loss": float(log_loss(y_true, clipped, labels=[0, 1])),
            "calibration_intercept": float(fitted_calibration.x[0]),
            "calibration_slope": float(fitted_calibration.x[1]),
            "ece_10_bins": float(weighted_error),
        },
        pd.DataFrame(bin_rows),
    )


def collect_cardio_predictions(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    frame = pd.read_csv(path)
    if frame["patient_id"].duplicated().any():
        raise ValueError("Cardio70k contains repeated patient IDs; use grouped CV.")
    features = frame.drop(columns=["patient_id", "target"])
    target = frame["target"].astype(int)
    predictions = {
        model_name: np.full(len(frame), np.nan, dtype=float) for model_name in MODELS
    }
    splitter = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)
    for train_indices, test_indices in splitter.split(features, target):
        train_x, test_x = features.iloc[train_indices], features.iloc[test_indices]
        train_y = target.iloc[train_indices]
        models = make_models(CARDIO_CATEGORICAL, CARDIO_NUMERICAL)
        for model_name in MODELS:
            model = models[model_name]
            model.fit(train_x, train_y)
            predictions[model_name][test_indices] = model.predict_proba(test_x)[:, 1]
    rows = [
        {"cohort": "Cardio70k", "source": "All folds", "model": name, "target": target.to_numpy(), "probability": values}
        for name, values in predictions.items()
    ]
    return prediction_frame(rows), target


def collect_unified_predictions(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    feature_columns = UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL
    predictions = []
    for held_out_source in sorted(frame["source"].dropna().unique()):
        train = frame.loc[frame["source"] != held_out_source]
        test = frame.loc[frame["source"] == held_out_source]
        train_y = train["target"].astype(int)
        test_y = test["target"].astype(int)
        if train_y.nunique() != 2 or test_y.nunique() != 2:
            raise ValueError(f"Both target classes are required for {held_out_source}.")
        models = make_models(UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL)
        for model_name in MODELS:
            model = models[model_name]
            model.fit(train[feature_columns], train_y)
            predictions.append(
                pd.DataFrame(
                    {
                        "cohort": "Unified clinical",
                        "source": held_out_source,
                        "model": model_name,
                        "target": test_y.to_numpy(),
                        "probability": model.predict_proba(test[feature_columns])[:, 1],
                    }
                )
            )
    return pd.concat(predictions, ignore_index=True)


def prediction_frame(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.concat(
        [
            pd.DataFrame(
                {
                    "cohort": row["cohort"],
                    "source": row["source"],
                    "model": row["model"],
                    "target": row["target"],
                    "probability": row["probability"],
                }
            )
            for row in rows
        ],
        ignore_index=True,
    )


def evaluate_predictions(predictions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metric_rows = []
    bin_frames = []
    groups = [("Cardio70k", "All folds", predictions.loc[predictions["cohort"] == "Cardio70k"])]
    unified = predictions.loc[predictions["cohort"] == "Unified clinical"]
    groups.extend(
        [("Unified clinical", source, unified.loc[unified["source"] == source]) for source in sorted(unified["source"].unique())]
    )
    groups.append(("Unified clinical", "All held-out sources", unified))
    for cohort, source, cohort_rows in groups:
        for model_name, model_rows in cohort_rows.groupby("model", sort=False):
            y_true = model_rows["target"].to_numpy(dtype=int)
            probabilities = model_rows["probability"].to_numpy(dtype=float)
            metrics, bins = calibration_statistics(y_true, probabilities)
            metric_rows.append(
                {"cohort": cohort, "held_out_source": source, "model": model_name, "n": len(model_rows), **metrics}
            )
            bins.insert(0, "model", model_name)
            bins.insert(0, "held_out_source", source)
            bins.insert(0, "cohort", cohort)
            bin_frames.append(bins)
    return pd.DataFrame(metric_rows), pd.concat(bin_frames, ignore_index=True)


def plot_calibration(predictions: pd.DataFrame, metrics: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    for axis, cohort, source in [
        (axes[0], "Cardio70k", "All folds"),
        (axes[1], "Unified clinical", "All held-out sources"),
    ]:
        selected = predictions.loc[
            (predictions["cohort"] == cohort)
            & ((predictions["source"] == source) if cohort == "Cardio70k" else True)
        ]
        axis.plot([0, 1], [0, 1], linestyle="--", color="#68736f", label="Ideal calibration")
        for model_name, model_rows in selected.groupby("model", sort=False):
            model_metrics = metrics.loc[
                (metrics["cohort"] == cohort)
                & (metrics["held_out_source"] == source)
                & (metrics["model"] == model_name)
            ]
            _, bins = calibration_statistics(
                model_rows["target"].to_numpy(dtype=int),
                model_rows["probability"].to_numpy(dtype=float),
            )
            label = model_name
            if not model_metrics.empty:
                label += f" (Brier {model_metrics.iloc[0]['brier_score']:.3f})"
            axis.plot(
                bins["mean_predicted_probability"],
                bins["observed_positive_fraction"],
                marker="o",
                linewidth=1.8,
                label=label,
            )
        axis.set_title("Cardio70k: 5-fold OOF" if cohort == "Cardio70k" else "Unified cohort: held-out sources")
        axis.set_xlabel("Mean predicted probability")
        axis.set_ylabel("Observed positive fraction")
        axis.set_xlim(0, 1)
        axis.set_ylim(0, 1)
        axis.grid(alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Probability calibration on held-out predictions", fontsize=14)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    rows = [[str(value) for value in row] for row in frame[columns].itertuples(index=False, name=None)]
    widths = [max(len(column), *(len(row[index]) for row in rows)) for index, column in enumerate(columns)]
    header = "| " + " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    separator = "| " + " | ".join("-" * widths[index] for index in range(len(columns))) + " |"
    body = ["| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_report(metrics: pd.DataFrame, bins: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "calibration_metrics.csv"
    bins_path = output_dir / "calibration_bins.csv"
    report_path = output_dir / "calibration_analysis.md"
    metrics.to_csv(metrics_path, index=False)
    bins.to_csv(bins_path, index=False)
    columns = ["cohort", "held_out_source", "model", "n", "brier_score", "log_loss", "calibration_intercept", "calibration_slope", "ece_10_bins"]
    display = metrics[columns].copy()
    for column in columns[4:]:
        display[column] = display[column].map(lambda value: f"{value:.4f}")
    table = render_markdown_table(display, columns)
    text = f"""# Probability Calibration Analysis

## Protocol

Cardio70k probabilities are out-of-fold predictions from stratified 5-fold cross-validation. Unified-cohort probabilities are generated by leaving each source out in turn and predicting only that held-out source. Preprocessing is fitted inside each training partition. The models are the selected Cardio70k model (XGBoost), the unified-cohort ROC-AUC leader (Logistic Regression), and Logistic Regression/XGBoost as a common comparator. This is a calibration diagnostic only; no post-hoc correction is fitted.

## Results

{table}

![Calibration curves](plots/calibration_curves.png)

Ten-bin ECE is a descriptive, bin-dependent summary rather than a confidence interval. Calibration intercept near 0 and slope near 1 are desirable; estimates are sensitive to sample size, case mix, and source shift. Brier score and log loss combine calibration and discrimination and should not be interpreted in isolation. Source-specific unified results should be read separately from the aggregate.

## Limitations and next work

These results do not establish prospective calibration or clinical utility. The unified cohort remains a heterogeneous source-held-out stress test. Next steps are explainability with out-of-fold/permutation methods, subgroup and error analysis, and external validation on an independently collected compatible cohort.

Metrics: `{metrics_path.name}`. Reliability bins: `{bins_path.name}`.
"""
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved {report_path}, {metrics_path}, and {bins_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    cardio_predictions, _ = collect_cardio_predictions(args.cardio70k)
    unified_predictions = collect_unified_predictions(args.unified_raw)
    predictions = pd.concat([cardio_predictions, unified_predictions], ignore_index=True)
    metrics, bins = evaluate_predictions(predictions)
    plot_calibration(predictions, metrics, args.output_dir / "plots" / "calibration_curves.png")
    write_report(metrics, bins, args.output_dir)


if __name__ == "__main__":
    main()
