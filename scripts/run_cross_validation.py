"""Estimate Cardio70k baseline performance with stratified 5-fold CV."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedKFold

from run_baselines import (
    CARDIO_CATEGORICAL,
    CARDIO_NUMERICAL,
    RANDOM_SEED,
    calculate_metrics,
    make_models,
)


N_SPLITS = 5


def run_cross_validation(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(path)
    if frame["patient_id"].duplicated().any():
        raise ValueError("Cardio70k contains repeated patient IDs; use grouped CV.")
    if set(frame["target"].dropna().unique()) != {0, 1}:
        raise ValueError("Expected a complete binary 0/1 target.")

    features = frame.drop(columns=["patient_id", "target"])
    target = frame["target"].astype(int)
    splitter = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_SEED,
    )
    fold_rows = []
    pooled_predictions: dict[str, pd.Series] = {
        name: pd.Series(index=target.index, dtype=float)
        for name in make_models(CARDIO_CATEGORICAL, CARDIO_NUMERICAL)
    }

    for fold_number, (train_indices, test_indices) in enumerate(
        splitter.split(features, target), start=1
    ):
        train_x = features.iloc[train_indices]
        test_x = features.iloc[test_indices]
        train_y = target.iloc[train_indices]
        test_y = target.iloc[test_indices]
        for model_name, model in make_models(
            CARDIO_CATEGORICAL, CARDIO_NUMERICAL
        ).items():
            model.fit(train_x, train_y)
            probabilities = model.predict_proba(test_x)[:, 1]
            pooled_predictions[model_name].iloc[test_indices] = probabilities
            row: dict[str, object] = {
                "cohort": "Cardio70k",
                "evaluation": f"stratified {N_SPLITS}-fold CV",
                "fold": fold_number,
                "model": model_name,
                "n_train": len(train_indices),
                "n_test": len(test_indices),
            }
            row.update(calculate_metrics(test_y, probabilities))
            fold_rows.append(row)

    folds = pd.DataFrame(fold_rows)
    summary_rows = []
    for model_name, probabilities in pooled_predictions.items():
        metrics = calculate_metrics(target, probabilities)
        model_folds = folds.loc[folds["model"] == model_name]
        row: dict[str, object] = {
            "cohort": "Cardio70k",
            "evaluation": f"stratified {N_SPLITS}-fold CV",
            "model": model_name,
            "n": len(frame),
        }
        for metric_name, pooled_value in metrics.items():
            row[f"{metric_name}_oof"] = pooled_value
            row[f"{metric_name}_fold_mean"] = model_folds[metric_name].mean()
            row[f"{metric_name}_fold_sd"] = model_folds[metric_name].std(ddof=1)
        summary_rows.append(row)
    return folds, pd.DataFrame(summary_rows)


def render_table(frame: pd.DataFrame, columns: list[str]) -> str:
    rows = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for values in frame[columns].itertuples(index=False, name=None):
        cells = [
            f"{value:.3f}" if isinstance(value, float) else str(value)
            for value in values
        ]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def write_report(
    folds: pd.DataFrame, summary: pd.DataFrame, output_dir: Path
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fold_path = output_dir / "cross_validation_folds.csv"
    summary_path = output_dir / "cross_validation_summary.csv"
    report_path = output_dir / "cross_validation_results.md"
    folds.to_csv(fold_path, index=False)
    summary.to_csv(summary_path, index=False)

    metrics = [
        "accuracy",
        "precision",
        "sensitivity",
        "specificity",
        "f1",
        "roc_auc",
        "pr_auc",
        "brier_score",
    ]
    columns = ["model", "n"]
    for metric in metrics:
        columns.extend([f"{metric}_oof", f"{metric}_fold_mean", f"{metric}_fold_sd"])
    text = [
        "# Cardio70k Cross-Validation Results",
        "",
        "Each record is assigned to one held-out fold exactly once. Imputation, "
        "encoding, and scaling are fitted inside each training fold. Model "
        "hyperparameters were fixed in advance for this run; no tuning or "
        "resampling is performed.",
        "",
        "## Pooled out-of-fold metrics",
        "",
        "Each `_oof` score uses all held-out predictions combined. Fold mean and "
        "sample standard deviation summarize variation across the five folds; "
        "they are not confidence intervals.",
        "",
        render_table(summary, columns),
        "",
        "## Interpretation",
        "",
        "This is internal validation on Cardio70k, not external or prospective "
        "validation. The 5-fold results replace the single holdout as the main "
        "internal baseline estimate; prior holdout results remain exploratory. "
        "Repeated predictor profiles are retained because distinct IDs represent "
        "separate records and some identical profiles carry different labels. "
        "The next evaluation stage is nested model selection on training folds, "
        "then a locked final test only if one is reserved before further tuning.",
        "",
        f"Fold-level metrics: `{fold_path.as_posix()}`.",
        f"Summary metrics: `{summary_path.as_posix()}`.",
    ]
    report_path.write_text("\n".join(text) + "\n", encoding="utf-8")
    print(f"Wrote {report_path}, {fold_path}, and {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    folds, summary = run_cross_validation(args.cardio70k)
    write_report(folds, summary, args.output_dir)


if __name__ == "__main__":
    main()