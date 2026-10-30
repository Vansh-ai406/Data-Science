# Research Reports & Artifacts Index
**Cardiovascular Disease Prediction Pipeline**

This directory contains all experimental outputs, empirical metric CSVs, analytical reports, high-resolution plots, and presentation dossiers.

---

## 🌟 Master Presentation & Defense Documents
Open these files in any web browser for visual presentations and defense reviews:
- **[`MASTER_RESEARCH_DEFENSE_GUIDE.html`](file:///reports/MASTER_RESEARCH_DEFENSE_GUIDE.html)** (2.8 MB): The complete, standalone presentation and defense dossier. Contains all project background, model theory, clinical metrics, 14 Base64-embedded figures, tabular benchmarks, and defense Q&A.
- **[`PLAGIARISM_AND_ORIGINALITY_REPORT.html`](file:///reports/PLAGIARISM_AND_ORIGINALITY_REPORT.html)** (14 KB): Academic integrity and originality audit report (3.4% similarity, IEEE AI disclosure).
- **[`consolidated_project_results.html`](file:///reports/consolidated_project_results.html)** (51 KB): Consolidated benchmark results viewer.

---

## 📈 Publication Figures (`plots/`)
All figures are saved in 300 DPI high-resolution PNG format:
| Figure | Description |
| :--- | :--- |
| [`plots/cv_roc_auc.png`](file:///reports/plots/cv_roc_auc.png) | 5-Fold Stratified Cross-Validation ROC-AUC comparison across baselines |
| [`plots/cv_brier_score.png`](file:///reports/plots/cv_brier_score.png) | Probabilistic Calibration Brier score comparison |
| [`plots/calibration_curves.png`](file:///reports/plots/calibration_curves.png) | Reliability diagram showing predicted probabilities vs observed event frequencies |
| [`plots/decision_curves.png`](file:///reports/plots/decision_curves.png) | Decision Curve Analysis (DCA): Net Clinical Benefit across decision thresholds |
| [`plots/cardio_mlp_paired_bootstrap.png`](file:///reports/plots/cardio_mlp_paired_bootstrap.png) | 1,000-iteration paired bootstrap differences (XGBoost vs MLP) |
| [`plots/deep_cardio_roc_auc.png`](file:///reports/plots/deep_cardio_roc_auc.png) | Deep Tabular MLP vs Gradient Boosting ROC-AUC on Cardio70k |
| [`plots/deep_cardio_f1.png`](file:///reports/plots/deep_cardio_f1.png) | Deep Tabular MLP vs Gradient Boosting F1-Score on Cardio70k |
| [`plots/deep_unified_roc_auc.png`](file:///reports/plots/deep_unified_roc_auc.png) | Multi-center performance across 5 clinical hospital cohorts |
| [`plots/hpem_source_comparison.png`](file:///reports/plots/hpem_source_comparison.png) | Multi-center Leave-One-Source-Out (LOSO) generalization gap |
| [`plots/missingness_indicator_comparison.png`](file:///reports/plots/missingness_indicator_comparison.png) | Impact of missingness indicator features across hospital sources |
| [`plots/nested_selection_roc_auc.png`](file:///reports/plots/nested_selection_roc_auc.png) | Nested 5x3 Cross-Validation outer fold ROC-AUC stability |
| [`plots/permutation_importance.png`](file:///reports/plots/permutation_importance.png) | Permutation feature importance on held-out test data |
| [`plots/subgroup_performance.png`](file:///reports/plots/subgroup_performance.png) | Error rates and sensitivity across age and sex demographic subgroups |
| [`plots/threshold_tradeoffs.png`](file:///reports/plots/threshold_tradeoffs.png) | Sensitivity, Specificity, and Net Benefit trade-offs across cutoffs |

---

## 📊 Empirical Results Datasets (CSVs)
| File | Experiment / Benchmark |
| :--- | :--- |
| `baseline_metrics.csv` | Baseline model metrics on initial holdout splits |
| `cross_validation_folds.csv` | Per-fold metrics for 5-fold Stratified CV on Cardio70k |
| `cross_validation_summary.csv` | Mean ± Std cross-validation performance across models |
| `nested_model_selection_folds.csv` | Outer fold evaluation metrics for nested CV |
| `nested_model_selection_summary.csv` | Pooled nested cross-validation performance |
| `deep_tabular_cardio_summary.csv` | Deep tabular MLP evaluation on Cardio70k cohort |
| `deep_tabular_unified_summary.csv` | Deep tabular MLP evaluation on Multi-Center Unified cohort |
| `mlp_bootstrap_metrics.csv` | 1,000 bootstrap metric estimates for MLP and XGBoost |
| `mlp_paired_differences.csv` | Paired $\Delta(\text{XGBoost} - \text{MLP})$ bootstrap differences |
| `hpem_summary.csv` | Leave-one-source-out generalization summary for HPEM |
| `hpem_source_metrics.csv` | Source-specific discrimination and calibration metrics |
| `hpem_heldout_predictions.csv` | Raw probabilistic predictions on held-out hospital sources |
| `calibration_metrics.csv` | Brier scores and Expected Calibration Error (ECE) |
| `calibration_bins.csv` | Decile-level calibration bin probabilities and event rates |
| `decision_curve_analysis.csv` | Net clinical benefit across risk thresholds $p_t \in [0.10, 0.90]$ |
| `subgroup_error_metrics.csv` | Sliced performance metrics across age and sex subgroups |
| `subgroup_confidence_intervals.csv` | 95% Clopper-Pearson exact binomial confidence intervals |
| `permutation_importance_summary.csv` | Top feature importance values and standard deviations |
| `permutation_importance_by_holdout.csv`| Feature importance broken down by individual hospital sources |
| `threshold_profiles.csv` | Model performance under F1, Youden's J, and F2 optimal cutoffs |
| `paired_bootstrap_differences.csv` | Paired statistical tests between baseline algorithms |
| `bootstrap_metric_intervals.csv` | Bootstrap empirical confidence intervals |
| `missingness_indicator_benchmark.csv` | Multi-center benchmark with vs without missingness indicators |

---

## 📝 Detailed Analytical Reports (Markdown)
| Markdown Report | Topic Covered |
| :--- | :--- |
| `dataset_audit.md` | Data provenance, variable definitions, and label distributions |
| `data_quality.md` | Missingness patterns, outlier boundaries, and physiological validity |
| `additional_dataset_suitability.md` | Suitability assessment of external ECG and synthetic image sets |
| `baseline_results.md` | Classical machine learning baseline benchmarks |
| `cross_validation_results.md` | 5-fold stratified cross-validation stability analysis |
| `nested_model_selection_results.md` | Nested CV hyperparameter tuning analysis |
| `deep_tabular_benchmark.md` | Tabular neural network architectures vs tree models |
| `mlp_uncertainty_analysis.md` | 1,000-iteration paired bootstrap between MLP and XGBoost |
| `hpem_benchmark.md` | Leakage-safe leave-one-source-out ensemble benchmark |
| `missingness_indicator_analysis.md` | Informative missingness vs pure imputation findings |
| `calibration_analysis.md` | Probabilistic calibration and reliability analysis |
| `explainability_error_analysis.md` | Feature importance and demographic subgroup error analysis |
| `subgroup_confidence_intervals.md` | Exact 95% confidence intervals for demographic subgroups |
| `decision_curve_analysis.md` | Clinical net benefit and Decision Curve Analysis (DCA) |
| `uncertainty_threshold_analysis.md` | Optimal clinical threshold selection analysis |
| `model_results_visual.md` | Visual summaries and plot interpretation guide |
| `research_summary.md` | Executive summary of research findings |
| `student_presentation_brief.md` | Quick speaking points and defense notes |
| `GITHUB_PROFILE_README_TEMPLATE.md` | Optimized GitHub profile template for Vansh-ai406 |

