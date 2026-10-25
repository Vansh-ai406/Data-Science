"""Create a research-oriented summary across all provided clinical datasets."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def summarize_internal_and_generalization(reports_dir: Path) -> dict[str, object]:
    cv = pd.read_csv(reports_dir / "cross_validation_summary.csv")
    nested = pd.read_csv(reports_dir / "nested_model_selection_summary.csv")
    baseline = pd.read_csv(reports_dir / "baseline_metrics.csv")
    deep_cardio = pd.read_csv(reports_dir / "deep_tabular_cardio_summary.csv")
    deep_unified = pd.read_csv(reports_dir / "deep_tabular_unified_summary.csv")
    calibration_path = reports_dir / "calibration_metrics.csv"
    calibration = pd.read_csv(calibration_path) if calibration_path.exists() else pd.DataFrame()

    cardio_best = cv.sort_values("roc_auc_oof", ascending=False).iloc[0]
    unified = baseline[baseline["cohort"] == "Unified clinical"].copy()
    unified_mean = (
        unified.groupby("model")
        .agg(
            accuracy_mean=("accuracy", "mean"),
            precision_mean=("precision", "mean"),
            f1_mean=("f1", "mean"),
            roc_auc_mean=("roc_auc", "mean"),
            pr_auc_mean=("pr_auc", "mean"),
            brier_score_mean=("brier_score", "mean"),
        )
        .sort_values("roc_auc_mean", ascending=False)
    )
    generalization_best = unified_mean.iloc[0]

    summary = {
        "cardio_best_model": str(cardio_best["model"]),
        "cardio_best_accuracy": float(cardio_best["accuracy_oof"]),
        "cardio_best_precision": float(cardio_best["precision_oof"]),
        "cardio_best_f1": float(cardio_best["f1_oof"]),
        "cardio_best_roc_auc": float(cardio_best["roc_auc_oof"]),
        "generalization_best_model": str(generalization_best.name),
        "generalization_best_accuracy": float(generalization_best["accuracy_mean"]),
        "generalization_best_precision": float(generalization_best["precision_mean"]),
        "generalization_best_f1": float(generalization_best["f1_mean"]),
        "generalization_best_roc_auc": float(generalization_best["roc_auc_mean"]),
        "nested_best_model": str(nested.sort_values("roc_auc_mean", ascending=False).iloc[0]["selected_model"]),
        "nested_best_roc_auc": float(nested.sort_values("roc_auc_mean", ascending=False).iloc[0]["roc_auc_mean"]),
        "mlp_cardio": deep_cardio.loc[deep_cardio["model"] == "MLP_Deep"].iloc[0],
        "xgb_cardio_deep": deep_cardio.loc[deep_cardio["model"] == "XGBoost"].iloc[0],
        "mlp_unified": deep_unified.loc[deep_unified["model"] == "MLP_Deep"].iloc[0],
        "xgb_unified_deep": deep_unified.loc[deep_unified["model"] == "XGBoost"].iloc[0],
        "deep_unified_best_auc": deep_unified.sort_values("roc_auc_mean", ascending=False).iloc[0],
        "deep_unified_best_f1": deep_unified.sort_values("f1_mean", ascending=False).iloc[0],
        "cv_table": cv[["model", "accuracy_oof", "precision_oof", "f1_oof", "roc_auc_oof", "brier_score_oof"]].sort_values("roc_auc_oof", ascending=False),
        "unified_table": unified_mean.reset_index().rename(columns={"index": "model"}),
        "calibration_table": calibration,
    }
    return summary


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


def write_report(summary: dict[str, object], output_path: Path) -> None:
    cv_table = summary["cv_table"]
    unified_table = summary["unified_table"]
    calibration_table = summary["calibration_table"]
    text = [
        "# Research Summary for Cardiovascular Disease Prediction",
        "",
        "## Study protocol and data usage",
        "",
        "This project follows a leak-safe, research-oriented workflow. The supplied data were treated as two separate clinical cohorts rather than as a single merged dataset. The large `CVD_Cardio70k_Cleaned.csv` file is used for internal discrimination benchmarking; the `CVD_Unified_Clinical_Dataset.csv` file is used for source-aware cross-cohort generalization testing. The ML-ready unified export is not treated as the canonical train set because imputation occurred before the train/test split, which would leak information.",
        "",
        "## Key benchmark findings",
        "",
        f"- Best internal Cardio70k model: **{summary['cardio_best_model']}** with ROC-AUC **{summary['cardio_best_roc_auc']:.4f}**, F1 **{summary['cardio_best_f1']:.4f}**, precision **{summary['cardio_best_precision']:.4f}**, and accuracy **{summary['cardio_best_accuracy']:.4f}**.",
        f"- Best nested-selection model: **{summary['nested_best_model']}** with mean outer-fold ROC-AUC **{summary['nested_best_roc_auc']:.4f}**.",
        f"- Best generalization model across the unified multi-source dataset: **{summary['generalization_best_model']}** with mean ROC-AUC **{summary['generalization_best_roc_auc']:.4f}**, F1 **{summary['generalization_best_f1']:.4f}**, and accuracy **{summary['generalization_best_accuracy']:.4f}**.",
        "",
        "## Internal Cardio70k validation table",
        "",
        markdown_table(
            cv_table,
            ["model", "accuracy_oof", "precision_oof", "f1_oof", "roc_auc_oof", "brier_score_oof"],
        ),
        "",
        "## Generalization view across the unified cohort",
        "",
        markdown_table(
            unified_table,
            ["model", "accuracy_mean", "precision_mean", "f1_mean", "roc_auc_mean", "pr_auc_mean", "brier_score_mean"],
        ),
        "",
        "## Neural Baseline and Student Contribution",
        "",
        f"The two-hidden-layer scikit-learn MLP is a genuine neural-network baseline, not a newly proposed architecture. On Cardio70k 5-fold CV it scored ROC-AUC {summary['mlp_cardio']['roc_auc_mean']:.4f} and F1 {summary['mlp_cardio']['f1_mean']:.4f}; XGBoost scored ROC-AUC {summary['xgb_cardio_deep']['roc_auc_mean']:.4f} and F1 {summary['xgb_cardio_deep']['f1_mean']:.4f}.",
        "",
        f"Across unified source-held-out evaluations, MLP mean ROC-AUC/F1 were {summary['mlp_unified']['roc_auc_mean']:.4f}/{summary['mlp_unified']['f1_mean']:.4f}; standalone XGBoost was {summary['xgb_unified_deep']['roc_auc_mean']:.4f}/{summary['xgb_unified_deep']['f1_mean']:.4f}. Logistic Regression led mean ROC-AUC ({summary['deep_unified_best_auc']['model']}: {summary['deep_unified_best_auc']['roc_auc_mean']:.4f}) while {summary['deep_unified_best_f1']['model']} led mean F1 ({summary['deep_unified_best_f1']['f1_mean']:.4f}). Means are across five sources and are not independent external validation.",
        "",
        "The student-level contribution is the leakage-aware, source-aware comparison across separate cohorts, with calibration, error, and uncertainty analyses, including the documented negative HPEM adaptation result. Do not claim a novel neural architecture or clinical readiness.",
        "",
        "## Probability calibration",
        "",
        "Cardio70k calibration uses pooled out-of-fold predictions; unified-cohort calibration uses leave-one-source-out predictions. These are diagnostics on the evaluated cohorts, not prospective calibration estimates. No post-hoc calibration was fit.",
        "",
    ]
    if not calibration_table.empty:
        calibration_columns = ["cohort", "held_out_source", "model", "n", "brier_score", "calibration_intercept", "calibration_slope", "ece_10_bins"]
        text.extend([markdown_table(calibration_table, calibration_columns), ""])
    text.extend([
        "## Research interpretation",
        "",
        "The strongest internal discriminator is XGBoost, and nested validation selected it in all five outer folds. Cardio70k XGBoost out-of-fold calibration is close to ideal (slope about 1.00), while calibration on the unified source-held-out cohort is substantially weaker and varies by source. Report the large cohort as internal validation and the unified cohort as a source-shift stress test, not as pooled or external clinical validation.",
        "",
        "## Research status",
        "",
        "Completed: data audit and quality analysis, leakage-safe baselines, internal cross-validation, nested selection, deep tabular benchmarking, source-held-out stress testing, figures/tables, calibration diagnostics, held-out permutation importance, exploratory subgroup/error analysis, a leakage-safe HPEM adaptation benchmark, conditional bootstrap intervals, and threshold trade-off profiles. The HPEM adaptation did not outperform matched XGBoost results and is not an exact reproduction of the paper protocol.",
        "",
        "Remaining: (1) independent external validation on a compatible cohort; (2) prespecified clinical-utility analysis with expert input; (3) subgroup uncertainty intervals and clinical review; (4) exact reproduction of the foundation paper's HPEM on matched datasets/protocol if it is in scope; and (5) evaluate calibration prospectively or on an independent calibration cohort. The supplied legend documents sex code 0 as female and 1 as male; this binary biological-sex field does not represent broader gender identities. Bootstrap intervals are conditional on observed data and do not represent new-source uncertainty. Multimodal work requires valid patient-linked data. These research results do not establish clinical readiness.",
    ])
    output_path.write_text("\n".join(text) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    summary = summarize_internal_and_generalization(args.reports_dir)
    print('=== Research recommendation ===')
    print(f"Internal benchmark winner: {summary['cardio_best_model']} | ROC-AUC {summary['cardio_best_roc_auc']:.4f} | F1 {summary['cardio_best_f1']:.4f} | Accuracy {summary['cardio_best_accuracy']:.4f} | Precision {summary['cardio_best_precision']:.4f}")
    print(f"Nested selection winner: {summary['nested_best_model']} | ROC-AUC {summary['nested_best_roc_auc']:.4f}")
    print(f"Unified-source generalization winner: {summary['generalization_best_model']} | ROC-AUC {summary['generalization_best_roc_auc']:.4f} | F1 {summary['generalization_best_f1']:.4f} | Accuracy {summary['generalization_best_accuracy']:.4f}")
    out = args.reports_dir / "research_summary.md"
    write_report(summary, out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
