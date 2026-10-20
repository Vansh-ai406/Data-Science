"""Generate graphical and tabular summaries of the project model results."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


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
                text = f"{value:.4f}"
            else:
                text = str(value)
            cells.append(text)
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def plot_metric_bar(frame: pd.DataFrame, metric: str, title: str, output_path: Path) -> None:
    ordered = frame.sort_values(metric, ascending=False).copy()
    fig, ax = plt.subplots(figsize=(9, 5.5))
    colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"]
    ax.bar(ordered["model"], ordered[metric], color=colors[: len(ordered)])
    ax.set_title(title)
    ax.set_ylabel(metric)
    ax.set_xlabel("Model")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


def plot_nested_selection(summary: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    models = summary["selected_model"]
    roc_aucs = summary["roc_auc_mean"]
    ax.bar(models, roc_aucs, color="#2E86AB")
    ax.set_title("Nested model-selection ROC-AUC by selected model")
    ax.set_ylabel("Mean outer-fold ROC-AUC")
    ax.set_xlabel("Selected model")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


def build_report() -> None:
    repo = Path(__file__).resolve().parent.parent
    reports_dir = repo / "reports"
    plots_dir = reports_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    cv = pd.read_csv(reports_dir / "cross_validation_summary.csv")
    nested = pd.read_csv(reports_dir / "nested_model_selection_summary.csv")
    baseline = pd.read_csv(reports_dir / "baseline_metrics.csv")

    plot_metric_bar(
        cv,
        "roc_auc_oof",
        "Cardio70k 5-fold CV ROC-AUC by model",
        plots_dir / "cv_roc_auc.png",
    )
    plot_metric_bar(
        cv,
        "brier_score_oof",
        "Cardio70k 5-fold CV Brier score by model",
        plots_dir / "cv_brier_score.png",
    )
    plot_nested_selection(nested, plots_dir / "nested_selection_roc_auc.png")

    best_model = cv.sort_values("roc_auc_oof", ascending=False).iloc[0]
    summary_line = (
        f"Best tested Cardio70k model: {best_model['model']} | ROC-AUC={best_model['roc_auc_oof']:.4f} | "
        f"F1={best_model['f1_oof']:.4f} | Accuracy={best_model['accuracy_oof']:.4f} | Precision={best_model['precision_oof']:.4f}"
    )
    print("\n=== Best model ranking ===")
    print(cv[["model", "accuracy_oof", "precision_oof", "f1_oof", "roc_auc_oof", "brier_score_oof"]].sort_values("roc_auc_oof", ascending=False).to_string(index=False))
    print(f"\n{summary_line}\n")

    summary_md = [
        "# Model Performance Visual Summary",
        "",
        "## Best model recommendation",
        "",
        f"The strongest tested model on the Cardio70k cohort is **{best_model['model']}** with ROC-AUC **{best_model['roc_auc_oof']:.4f}**, F1 **{best_model['f1_oof']:.4f}**, precision **{best_model['precision_oof']:.4f}**, and accuracy **{best_model['accuracy_oof']:.4f}**.",
        "",
        "## Graphical results",
        "",
        "### Cardio70k 5-fold CV ROC-AUC",
        "",
        "![Cardio70k ROC-AUC](plots/cv_roc_auc.png)",
        "",
        "### Cardio70k 5-fold CV Brier score",
        "",
        "![Cardio70k Brier score](plots/cv_brier_score.png)",
        "",
        "### Nested model-selection ROC-AUC",
        "",
        "![Nested selection ROC-AUC](plots/nested_selection_roc_auc.png)",
        "",
        "## Tabular summary",
        "",
        "### Cardio70k stratified 5-fold CV summary",
        "",
        markdown_table(
            cv[[
                "model",
                "accuracy_oof",
                "precision_oof",
                "sensitivity_oof",
                "specificity_oof",
                "f1_oof",
                "roc_auc_oof",
                "pr_auc_oof",
                "brier_score_oof",
            ]].sort_values("roc_auc_oof", ascending=False),
            [
                "model",
                "accuracy_oof",
                "precision_oof",
                "sensitivity_oof",
                "specificity_oof",
                "f1_oof",
                "roc_auc_oof",
                "pr_auc_oof",
                "brier_score_oof",
            ],
        ),
        "",
        "### Nested selection summary",
        "",
        markdown_table(
            nested[[
                "selected_model",
                "n_outer_folds_selected",
                "mean_inner_cv_roc_auc",
                "accuracy_mean",
                "precision_mean",
                "sensitivity_mean",
                "specificity_mean",
                "f1_mean",
                "roc_auc_mean",
                "pr_auc_mean",
                "brier_score_mean",
            ]],
            [
                "selected_model",
                "n_outer_folds_selected",
                "mean_inner_cv_roc_auc",
                "accuracy_mean",
                "precision_mean",
                "sensitivity_mean",
                "specificity_mean",
                "f1_mean",
                "roc_auc_mean",
                "pr_auc_mean",
                "brier_score_mean",
            ],
        ),
        "",
        "### Baseline holdout comparison",
        "",
        markdown_table(
            baseline.loc[baseline["cohort"] == "Cardio70k", [
                "model",
                "feature_set",
                "accuracy",
                "precision",
                "sensitivity",
                "specificity",
                "f1",
                "roc_auc",
                "pr_auc",
                "brier_score",
            ]].sort_values("roc_auc", ascending=False),
            [
                "model",
                "feature_set",
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
    ]

    (reports_dir / "model_results_visual.md").write_text("\n".join(summary_md) + "\n", encoding="utf-8")
    print(f"Wrote {plots_dir} and {reports_dir / 'model_results_visual.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    report_dir = args.reports_dir
    cs = report_dir / "cross_validation_summary.csv"
    ns = report_dir / "nested_model_selection_summary.csv"
    bs = report_dir / "baseline_metrics.csv"
    if not cs.exists() or not ns.exists() or not bs.exists():
        raise FileNotFoundError("Required report CSVs were not found in the reports directory.")
    pd.read_csv(cs)
    pd.read_csv(ns)
    pd.read_csv(bs)
    build_report()


if __name__ == "__main__":
    main()
