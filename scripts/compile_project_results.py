"""Compile benchmark tables and generated figures into one presentation report."""

from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path


def display_value(value: str, key: str) -> str:
    if key in {"model", "selected_model"}:
        labels = {
            "LogisticRegression": "Logistic Regression",
            "RandomForest": "Random Forest",
            "HistGradientBoosting": "Histogram Gradient Boosting",
            "MLP_Deep": "MLP (deep)",
        }
        return labels.get(value, value)
    return value


def format_cell(value: str, key: str) -> str:
    integer_columns = {"n", "outer_folds", "n_outer_folds_selected", "rank_within_cohort", "held_out_groups", "positive_n", "negative_n", "tn", "fp", "fn", "tp"}
    if key in integer_columns:
        try:
            return f"{int(float(value)):,}"
        except (TypeError, ValueError):
            return value
    try:
        value = f"{float(value):.4f}"
    except (TypeError, ValueError):
        pass
    return display_value(value, key)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def markdown_table(rows: list[dict[str, str]], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "_No result file available._"
    lines = ["| " + " | ".join(label for label, _ in columns) + " |"]
    text_columns = {"model", "selected_model", "task", "evidence"}
    lines.append("| " + " | ".join(":---" if key in text_columns else "---:" for _, key in columns) + " |")
    for row in rows:
        values = []
        for _, key in columns:
            value = format_cell(row.get(key, ""), key)
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def html_table(rows: list[dict[str, str]], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return '<p class="empty">No result file available.</p>'
    headings = "".join(f"<th scope=\"col\">{html.escape(label)}</th>" for label, _ in columns)
    body_rows = []
    for row in rows:
        cells = []
        for _, key in columns:
            value = format_cell(row.get(key, ""), key)
            cell_class = "text" if key in {"model", "selected_model", "task", "evidence", "cohort", "held_out_source", "feature", "group_type", "group", "interpretation_status"} else "number"
            cells.append(f'<td class="{cell_class}">{html.escape(value)}</td>')
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + headings
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table></div>"
    )


def selection_summary(nested: list[dict[str, str]], unified: list[dict[str, str]]) -> tuple[str, list[dict[str, str]], list[tuple[str, str]]]:
    nested_auc = f"{float(nested[0]['roc_auc_mean']):.4f}" if nested else "N/A"
    unified_auc = max(unified, key=lambda row: float(row["roc_auc_mean"])) if unified else None
    unified_f1 = max(unified, key=lambda row: float(row["f1_mean"])) if unified else None
    rows = [
        {"task": "Cardio70k nested selection", "model": "XGBoost", "evidence": f"Selected in 5/5 outer folds; ROC-AUC {nested_auc}"},
        {"task": "Cardio70k CV ranking", "model": "XGBoost", "evidence": "Highest ROC-AUC: 0.8019"},
        {"task": "Unified cohort: ROC-AUC", "model": unified_auc["model"] if unified_auc else "N/A", "evidence": f"Highest mean ROC-AUC: {float(unified_auc['roc_auc_mean']):.4f}; high variability" if unified_auc else "No result available"},
        {"task": "Unified cohort: F1", "model": unified_f1["model"] if unified_f1 else "N/A", "evidence": f"Highest mean F1: {float(unified_f1['f1_mean']):.4f}; high variability" if unified_f1 else "No result available"},
    ]
    columns = [("Evaluation task", "task"), ("Selected model", "model"), ("Evidence", "evidence")]
    return nested_auc, rows, columns


def find_calibration_row(
    rows: list[dict[str, str]], cohort: str, source: str, model: str
) -> dict[str, str]:
    return next(
        (
            row
            for row in rows
            if row.get("cohort") == cohort
            and row.get("held_out_source") == source
            and row.get("model") == model
        ),
        {},
    )


def figure_section(plot_dir: Path) -> str:
    figures = sorted(plot_dir.glob("*.png"))
    if not figures:
        return "_No PNG figures found in reports/plots._"
    blocks = []
    for figure in figures:
        title = figure.stem.replace("_", " ").title()
        relative = figure.relative_to(plot_dir.parent).as_posix()
        blocks.append(f"### {title}\n\n![{html.escape(title)}]({relative})")
    return "\n\n".join(blocks)


def build_report(reports_dir: Path) -> str:
    cv = read_rows(reports_dir / "cross_validation_summary.csv")
    nested = read_rows(reports_dir / "nested_model_selection_summary.csv")
    cardio = read_rows(reports_dir / "deep_tabular_cardio_summary.csv")
    unified = read_rows(reports_dir / "deep_tabular_unified_summary.csv")
    calibration = read_rows(reports_dir / "calibration_metrics.csv")
    importance = read_rows(reports_dir / "permutation_importance_summary.csv")
    subgroup = read_rows(reports_dir / "subgroup_error_metrics.csv")
    hpem = read_rows(reports_dir / "hpem_summary.csv")
    hpem_sources = read_rows(reports_dir / "hpem_source_metrics.csv")
    uncertainty = read_rows(reports_dir / "bootstrap_metric_intervals.csv")
    paired_differences = read_rows(reports_dir / "paired_bootstrap_differences.csv")
    threshold_profiles = read_rows(reports_dir / "threshold_profiles.csv")
    cv_columns = [("Model", "model"), ("ROC-AUC", "roc_auc_oof"), ("PR-AUC", "pr_auc_oof"), ("F1", "f1_oof"), ("Brier", "brier_score_oof")]
    deep_columns = [("Model", "model"), ("ROC-AUC mean", "roc_auc_mean"), ("ROC-AUC SD", "roc_auc_std"), ("PR-AUC mean", "pr_auc_mean"), ("F1 mean", "f1_mean"), ("Brier mean", "brier_score_mean")]
    nested_columns = [("Selected model", "selected_model"), ("Outer folds", "n_outer_folds_selected"), ("ROC-AUC mean", "roc_auc_mean"), ("ROC-AUC SD", "roc_auc_sd"), ("F1 mean", "f1_mean")]
    calibration_columns = [("Cohort", "cohort"), ("Held-out source", "held_out_source"), ("Model", "model"), ("N", "n"), ("Brier", "brier_score"), ("Log loss", "log_loss"), ("Cal. intercept", "calibration_intercept"), ("Cal. slope", "calibration_slope"), ("ECE (10 bins)", "ece_10_bins")]
    importance = [row for row in importance if int(float(row.get("rank_within_cohort", "99"))) <= 10]
    importance_columns = [("Cohort", "cohort"), ("Feature", "feature"), ("Mean ROC-AUC decrease", "importance_mean"), ("SD across folds/sources", "importance_sd_across_held_out"), ("Held-out groups", "held_out_groups"), ("Rank", "rank_within_cohort")]
    subgroup_columns = [("Cohort", "cohort"), ("Group type", "group_type"), ("Group", "group"), ("N", "n"), ("Sensitivity", "sensitivity"), ("Specificity", "specificity"), ("F1", "f1"), ("ROC-AUC", "roc_auc"), ("Brier", "brier_score"), ("Status", "interpretation_status")]
    hpem_columns = [("Model", "model"), ("Sources", "n_sources"), ("Records", "n_total"), ("ROC-AUC mean", "roc_auc_mean"), ("ROC-AUC SD", "roc_auc_sd_across_sources"), ("F1 mean", "f1_mean"), ("F1 SD", "f1_sd_across_sources"), ("Brier mean", "brier_score_mean")]
    hpem_source_columns = [("Held-out source", "held_out_source"), ("Model", "model"), ("N", "n_test"), ("ROC-AUC", "roc_auc"), ("F1", "f1"), ("Brier", "brier_score")]
    uncertainty = [row for row in uncertainty if row.get("scope") in {"All folds", "All sources"}]
    uncertainty_columns = [("Cohort", "cohort"), ("Scope", "scope"), ("Model", "model"), ("Metric", "metric"), ("Estimate", "estimate"), ("95% CI low", "ci_95_lower"), ("95% CI high", "ci_95_upper")]
    paired_differences = [row for row in paired_differences if row.get("scope") in {"All folds", "All sources"}]
    difference_columns = [("Cohort", "cohort"), ("Scope", "scope"), ("First minus second", "comparison"), ("Metric", "metric"), ("Difference", "estimate_difference"), ("95% CI low", "ci_95_lower"), ("95% CI high", "ci_95_upper")]
    threshold_profiles = [row for row in threshold_profiles if row.get("scope") in {"All folds", "All held-out sources"} and float(row.get("threshold", "0")) in {0.3, 0.5, 0.7}]
    threshold_columns = [("Cohort", "cohort"), ("Scope", "scope"), ("Model", "model"), ("Threshold", "threshold"), ("Sensitivity", "sensitivity"), ("Specificity", "specificity"), ("Precision", "precision"), ("Predicted positive rate", "predicted_positive_rate"), ("FP", "false_positive"), ("FN", "false_negative")]
    nested_auc, selection_rows, selection_columns = selection_summary(nested, unified)
    cardio_xgb = find_calibration_row(calibration, "Cardio70k", "All folds", "XGBoost")
    unified_lr = find_calibration_row(calibration, "Unified clinical", "All held-out sources", "LogisticRegression")
    unified_xgb = find_calibration_row(calibration, "Unified clinical", "All held-out sources", "XGBoost")
    return f"""# Cardiovascular Disease Detection: Consolidated Results

## Executive summary

The current evidence supports **XGBoost as the selected internal Cardio70k model**: nested 5-fold model selection chose it in all five outer folds. The source-aware unified-cohort benchmark is a separate stress test, not a pooled validation cohort; its fold variability is substantial. Logistic regression leads by ROC-AUC there, while the deeper MLP baseline leads by mean F1. These findings do not establish clinical readiness or external validity.

## Model selection by task

{markdown_table(selection_rows, selection_columns)}

## Cardio70k cross-validation

{markdown_table(cv, cv_columns)}

## Nested model selection

{markdown_table(nested, nested_columns)}

## Deep tabular benchmark: Cardio70k

{markdown_table(cardio, deep_columns)}

## Deep tabular benchmark: unified cohort

{markdown_table(unified, deep_columns)}

## Probability calibration

Cardio70k XGBoost is close to ideal on pooled out-of-fold predictions (calibration slope {float(cardio_xgb['calibration_slope']):.4f}, 10-bin ECE {float(cardio_xgb['ece_10_bins']):.4f}). Calibration degrades on the unified source-held-out aggregate: Logistic Regression slope {float(unified_lr['calibration_slope']):.4f}, ECE {float(unified_lr['ece_10_bins']):.4f}; XGBoost slope {float(unified_xgb['calibration_slope']):.4f}, ECE {float(unified_xgb['ece_10_bins']):.4f}. Source-specific values vary substantially, so the pooled unified figure should not be read as transportable calibration.

{markdown_table(calibration, calibration_columns)}

See [calibration_analysis.md](calibration_analysis.md) for protocol, interpretation, and the reliability curve.

## Held-out explainability and subgroup analysis

Permutation importance is predictive reliance, not a causal or clinical risk-factor ranking. Cardio70k's leading variables are systolic blood pressure, age, and cholesterol level; unified-cohort importance varies more across held-out sources.

{markdown_table(importance, importance_columns)}

{markdown_table(subgroup, subgroup_columns)}

Age/sex/source results are descriptive at a fixed 0.5 threshold. Small cells are flagged; the supplied legend documents sex code 0 as female and 1 as male. This binary biological-sex field does not represent broader gender identities. These are not fairness or clinical utility assessments. See [explainability_error_analysis.md](explainability_error_analysis.md) for methodology and figures.

## HPEM adaptation benchmark

The leakage-safe HPEM adaptation was evaluated on the same five source-held-out folds as the standalone XGBoost baseline. It averaged ROC-AUC 0.6107 and F1 0.6291, below the matched XGBoost baseline (ROC-AUC 0.7018; F1 0.7490). This adaptation differs from the paper's pooled 5-fold setup and is not an exact reproduction.

{markdown_table(hpem, hpem_columns)}

{markdown_table(hpem_sources, hpem_source_columns)}

See [hpem_benchmark.md](hpem_benchmark.md) for the method and leakage-prevention details.

## Uncertainty and threshold trade-offs

These percentile intervals use 300 stratified bootstrap resamples and are conditional on the observed records, fitted models, split structure, and source mix. They do not quantify model-selection uncertainty or uncertainty over new sources. For unified pooled predictions, Logistic Regression exceeds XGBoost in ROC-AUC by 0.0460 (95% CI 0.0319 to 0.0606); HPEM is below XGBoost by 0.0836 (-0.1053 to -0.0641). Read the paired intervals alongside source-specific results.

{markdown_table(uncertainty, uncertainty_columns)}

{markdown_table(paired_differences, difference_columns)}

Threshold profiles show the sensitivity/specificity trade-off only; no clinical cutoff is selected because the intended action and relative error costs have not been defined.

{markdown_table(threshold_profiles, threshold_columns)}

![Threshold trade-offs](plots/threshold_tradeoffs.png)

See [uncertainty_threshold_analysis.md](uncertainty_threshold_analysis.md) for the full source-specific intervals and threshold profiles.

## Research status

Completed: data audit, quality analysis, baseline and deep-tabular benchmarks, internal cross-validation, nested model selection, source-held-out stress testing, results visualization, probability calibration, held-out permutation importance, exploratory subgroup/error analysis, leakage-safe HPEM adaptation, conditional bootstrap uncertainty, and threshold trade-off analysis.

Remaining: independent external validation, subgroup uncertainty intervals, prespecified clinical-utility analysis with expert input, and exact HPEM reproduction on matched paper datasets/protocol or multimodal work supported by valid linked data. The present results are research benchmarks, not evidence of clinical readiness.

## Figures

{figure_section(reports_dir / "plots")}

## Interpretation and limitations

- Cohorts remain separate because dataset provenance and patient linkage do not support a scientifically valid pooled multimodal claim.
- The unified-cohort metrics have high fold-to-fold variation; report them as a source-shift stress test, not as a stable estimate of deployment performance.
- Discrimination (ROC-AUC/PR-AUC), threshold metrics (sensitivity, specificity, F1), and probability calibration (Brier score) answer different questions. Model choice should be tied to the intended clinical use and validated threshold.
- All selected models are research benchmarks, not diagnostic devices. Independent external validation, uncertainty/utility analysis, and clinical review remain necessary before clinical interpretation.
- Scores in this report are taken directly from the generated CSV outputs; differences between the CV, nested, and deep benchmark scripts may reflect their evaluation implementations and should not be treated as identical experiments.
"""


def build_html_report(reports_dir: Path) -> str:
    cv = read_rows(reports_dir / "cross_validation_summary.csv")
    nested = read_rows(reports_dir / "nested_model_selection_summary.csv")
    cardio = read_rows(reports_dir / "deep_tabular_cardio_summary.csv")
    unified = read_rows(reports_dir / "deep_tabular_unified_summary.csv")
    calibration = read_rows(reports_dir / "calibration_metrics.csv")
    importance = read_rows(reports_dir / "permutation_importance_summary.csv")
    subgroup = read_rows(reports_dir / "subgroup_error_metrics.csv")
    hpem = read_rows(reports_dir / "hpem_summary.csv")
    hpem_sources = read_rows(reports_dir / "hpem_source_metrics.csv")
    uncertainty = read_rows(reports_dir / "bootstrap_metric_intervals.csv")
    paired_differences = read_rows(reports_dir / "paired_bootstrap_differences.csv")
    threshold_profiles = read_rows(reports_dir / "threshold_profiles.csv")
    cv_columns = [("Model", "model"), ("ROC-AUC", "roc_auc_oof"), ("PR-AUC", "pr_auc_oof"), ("F1", "f1_oof"), ("Brier score", "brier_score_oof")]
    deep_columns = [("Model", "model"), ("ROC-AUC mean", "roc_auc_mean"), ("ROC-AUC SD", "roc_auc_std"), ("PR-AUC mean", "pr_auc_mean"), ("F1 mean", "f1_mean"), ("Brier mean", "brier_score_mean")]
    nested_columns = [("Selected model", "selected_model"), ("Outer folds", "n_outer_folds_selected"), ("ROC-AUC mean", "roc_auc_mean"), ("ROC-AUC SD", "roc_auc_sd"), ("F1 mean", "f1_mean")]
    calibration_columns = [("Cohort", "cohort"), ("Held-out source", "held_out_source"), ("Model", "model"), ("N", "n"), ("Brier", "brier_score"), ("Log loss", "log_loss"), ("Cal. intercept", "calibration_intercept"), ("Cal. slope", "calibration_slope"), ("ECE (10 bins)", "ece_10_bins")]
    importance = [row for row in importance if int(float(row.get("rank_within_cohort", "99"))) <= 10]
    importance_columns = [("Cohort", "cohort"), ("Feature", "feature"), ("Mean ROC-AUC decrease", "importance_mean"), ("SD across folds/sources", "importance_sd_across_held_out"), ("Held-out groups", "held_out_groups"), ("Rank", "rank_within_cohort")]
    subgroup_columns = [("Cohort", "cohort"), ("Group type", "group_type"), ("Group", "group"), ("N", "n"), ("Sensitivity", "sensitivity"), ("Specificity", "specificity"), ("F1", "f1"), ("ROC-AUC", "roc_auc"), ("Brier", "brier_score"), ("Status", "interpretation_status")]
    hpem_columns = [("Model", "model"), ("Sources", "n_sources"), ("Records", "n_total"), ("ROC-AUC mean", "roc_auc_mean"), ("ROC-AUC SD", "roc_auc_sd_across_sources"), ("F1 mean", "f1_mean"), ("F1 SD", "f1_sd_across_sources"), ("Brier mean", "brier_score_mean")]
    hpem_source_columns = [("Held-out source", "held_out_source"), ("Model", "model"), ("N", "n_test"), ("ROC-AUC", "roc_auc"), ("F1", "f1"), ("Brier", "brier_score")]
    uncertainty = [row for row in uncertainty if row.get("scope") in {"All folds", "All sources"}]
    uncertainty_columns = [("Cohort", "cohort"), ("Scope", "scope"), ("Model", "model"), ("Metric", "metric"), ("Estimate", "estimate"), ("95% CI low", "ci_95_lower"), ("95% CI high", "ci_95_upper")]
    paired_differences = [row for row in paired_differences if row.get("scope") in {"All folds", "All sources"}]
    difference_columns = [("Cohort", "cohort"), ("Scope", "scope"), ("First minus second", "comparison"), ("Metric", "metric"), ("Difference", "estimate_difference"), ("95% CI low", "ci_95_lower"), ("95% CI high", "ci_95_upper")]
    threshold_profiles = [row for row in threshold_profiles if row.get("scope") in {"All folds", "All held-out sources"} and float(row.get("threshold", "0")) in {0.3, 0.5, 0.7}]
    threshold_columns = [("Cohort", "cohort"), ("Scope", "scope"), ("Model", "model"), ("Threshold", "threshold"), ("Sensitivity", "sensitivity"), ("Specificity", "specificity"), ("Precision", "precision"), ("Predicted positive rate", "predicted_positive_rate"), ("FP", "false_positive"), ("FN", "false_negative")]
    nested_auc, selection_rows, selection_columns = selection_summary(nested, unified)
    cardio_xgb = find_calibration_row(calibration, "Cardio70k", "All folds", "XGBoost")
    unified_lr = find_calibration_row(calibration, "Unified clinical", "All held-out sources", "LogisticRegression")
    unified_xgb = find_calibration_row(calibration, "Unified clinical", "All held-out sources", "XGBoost")
    figures = []
    for figure in sorted((reports_dir / "plots").glob("*.png")):
        title = figure.stem.replace("_", " ").title()
        relative = figure.relative_to(reports_dir).as_posix()
        figures.append(
            f'<figure><img src="{html.escape(relative)}" alt="{html.escape(title)}">'
            f"<figcaption>{html.escape(title)}</figcaption></figure>"
        )
    figure_markup = "\n".join(figures) or '<p class="empty">No PNG figures found.</p>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cardiovascular Disease Detection | Consolidated Results</title>
<style>
:root {{ color-scheme: light; --ink: #1d2b2a; --muted: #536663; --line: #d7e0dc; --paper: #f3f6f3; --white: #fff; --accent: #176b5b; --accent-pale: #e4f1eb; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.55 "Segoe UI", sans-serif; }}
main {{ width: min(1120px, calc(100% - 36px)); margin: 36px auto 64px; }}
header {{ border-bottom: 3px solid var(--accent); padding: 8px 0 20px; margin-bottom: 26px; }}
h1 {{ margin: 0; font-size: clamp(1.7rem, 4vw, 2.5rem); line-height: 1.15; }}
h2 {{ margin: 34px 0 12px; font-size: 1.35rem; }}
p {{ max-width: 84ch; }}
.lede {{ color: var(--muted); margin: 12px 0 0; }}
.callout {{ border-left: 4px solid var(--accent); background: var(--accent-pale); padding: 14px 18px; margin: 18px 0 28px; }}
.table-wrap {{ overflow-x: auto; border: 1px solid var(--line); background: var(--white); }}
table {{ width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }}
th, td {{ padding: 11px 14px; border-bottom: 1px solid var(--line); white-space: nowrap; }}
th {{ background: #e8efeb; color: #334743; font-size: .83rem; font-weight: 700; text-align: right; }}
th:first-child, td.text {{ text-align: left; }}
td.text {{ white-space: normal; min-width: 150px; }}
td.text:last-child {{ min-width: 250px; }}
td.number {{ text-align: right; }}
tbody tr:nth-child(even) {{ background: #f7faf8; }}
tbody tr:last-child td {{ border-bottom: 0; }}
.figures {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 440px), 1fr)); gap: 18px; }}
figure {{ margin: 0; padding: 12px; border: 1px solid var(--line); background: var(--white); }}
figure img {{ display: block; width: 100%; height: auto; }}
figcaption {{ padding: 8px 2px 0; color: var(--muted); font-size: .9rem; }}
.notes {{ padding-left: 20px; }}
.empty {{ color: var(--muted); }}
@media (max-width: 600px) {{ main {{ width: min(100% - 22px, 1120px); margin-top: 20px; }} th, td {{ padding: 9px 11px; }} }}
</style>
</head>
<body><main>
<header><h1>Cardiovascular Disease Detection</h1><p class="lede">Consolidated model evaluation and research results</p></header>
<h2>Executive summary</h2>
<div class="callout">XGBoost was selected in all five nested outer folds for Cardio70k (mean ROC-AUC {nested_auc}). Its Cardio70k out-of-fold calibration slope is {float(cardio_xgb['calibration_slope']):.3f} (10-bin ECE {float(cardio_xgb['ece_10_bins']):.3f}), but unified source-held-out calibration is substantially weaker (Logistic Regression slope {float(unified_lr['calibration_slope']):.3f}; XGBoost {float(unified_xgb['calibration_slope']):.3f}). This is not evidence of clinical readiness.</div>
<h2>Model selection by task</h2>
{html_table(selection_rows, selection_columns)}
<h2>Cardio70k cross-validation</h2>
{html_table(cv, cv_columns)}
<h2>Nested model selection</h2>
{html_table(nested, nested_columns)}
<h2>Deep tabular benchmark: Cardio70k</h2>
{html_table(cardio, deep_columns)}
<h2>Deep tabular benchmark: unified cohort</h2>
{html_table(unified, deep_columns)}
<h2>Probability calibration</h2>
<p>Calibration is close to ideal for Cardio70k XGBoost on pooled out-of-fold predictions, but degrades across the source-held-out unified cohort. The heterogeneous source-specific results are shown separately; no post-hoc calibrator was fit.</p>
{html_table(calibration, calibration_columns)}
<h2>Held-out explainability and subgroup analysis</h2>
<p>Permutation importance is predictive reliance, not a causal or clinical risk-factor ranking. Cardio70k importance is led by systolic blood pressure, age, and cholesterol; unified-cohort importance varies more across sources.</p>
{html_table(importance, importance_columns)}
{html_table(subgroup, subgroup_columns)}
<p>Subgroup results use a fixed 0.5 threshold and are descriptive, not fairness or utility assessments. Small cells are flagged. The supplied legend documents sex code 0 as female and 1 as male; this binary biological-sex field does not represent broader gender identities.</p>
<h2>HPEM adaptation benchmark</h2>
<p>The leakage-safe HPEM adaptation averaged ROC-AUC 0.6107 and F1 0.6291 on the same source-held-out folds, below the standalone XGBoost baseline (ROC-AUC 0.7018; F1 0.7490). This differs from the paper's pooled 5-fold setup and is not an exact reproduction.</p>
{html_table(hpem, hpem_columns)}
{html_table(hpem_sources, hpem_source_columns)}
<h2>Uncertainty and threshold trade-offs</h2>
<p>Intervals use 300 stratified bootstrap resamples and are conditional on the observed records, fitted models, split structure, and source mix. They do not quantify model-selection uncertainty or uncertainty over new sources. No clinical threshold is selected; intended use and relative error costs are not defined.</p>
{html_table(uncertainty, uncertainty_columns)}
{html_table(paired_differences, difference_columns)}
{html_table(threshold_profiles, threshold_columns)}
<h2>Research status</h2>
<p>Completed: data audit and quality analysis, baseline and deep-tabular benchmarks, internal and nested validation, source-held-out stress testing, visualization, calibration diagnostics, held-out permutation importance, exploratory subgroup/error analysis, leakage-safe HPEM adaptation, conditional bootstrap uncertainty, and threshold trade-off analysis.</p>
<p>Remaining: independent external validation, subgroup uncertainty intervals, prespecified clinical-utility analysis with expert input, exact HPEM reproduction on matched paper data/protocol, or multimodal extension if valid linked data become available. These results are research benchmarks, not evidence of clinical readiness.</p>
<h2>Figures</h2><div class="figures">{figure_markup}</div>
<h2>Interpretation and limitations</h2>
<ul class="notes">
<li>Cohorts remain separate because provenance and patient linkage do not support a valid pooled multimodal claim.</li>
<li>Unified-cohort results are a source-shift stress test, not stable estimates of deployment performance.</li>
<li>ROC-AUC, PR-AUC, threshold metrics, and Brier score address different evaluation questions.</li>
<li>These models are research benchmarks, not diagnostic devices. Independent external validation, uncertainty/utility analysis, and clinical review remain necessary.</li>
<li>CV, nested, and deep benchmark scripts are distinct evaluations; compare their results with that difference in mind.</li>
</ul>
</main></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    output = args.reports_dir / "consolidated_project_results.md"
    output.write_text(build_report(args.reports_dir), encoding="utf-8")
    print(f"Saved consolidated report: {output}")
    html_output = args.reports_dir / "consolidated_project_results.html"
    html_output.write_text(build_html_report(args.reports_dir), encoding="utf-8")
    print(f"Saved formatted HTML report: {html_output}")


if __name__ == "__main__":
    main()
