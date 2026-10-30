# Project Architecture & Implementation Guide
**Explainable Cardiovascular Disease Prediction: Multi-Cohort Machine Learning & Clinical Utility Framework**

---

## 🎯 Quick Presentation Guide: "What Do I Show My Professor?"

When a professor, evaluator, or interviewer asks: **"Show me your implementation"**, here is your exact 3-step answer and walkthrough:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      WHAT TO SHOW & WHEN TO SHOW IT                         │
├──────────────────────────────────┬──────────────────────────────────────────┤
│ Evaluator Question               │ Exactly What To Open & Show              │
├──────────────────────────────────┼──────────────────────────────────────────┤
│ 1. "Show me your code &          │ 👉 Open: notebooks/                      │
│    implementation walkthrough"   │    Cardiovascular_Disease_Pipeline_Walkthrough.ipynb │
│                                  │ (Interactive, step-by-step cells with    │
│                                  │  code, markdown, plots & metrics)        │
├──────────────────────────────────┼──────────────────────────────────────────┤
│ 2. "How do you run or orchestrate│ 👉 Run: python pipeline_runner.py --status│
│    the whole research pipeline?" │    or: python pipeline_runner.py --stage all│
│                                  │ (Unified CLI runner that executes all    │
│                                  │  7 research phases sequentially)         │
├──────────────────────────────────┼──────────────────────────────────────────┤
│ 3. "Show me your final results,  │ 👉 Open: reports/                        │
│    figures, and defense summary" │    MASTER_RESEARCH_DEFENSE_GUIDE.html    │
│                                  │ (Self-contained 2.8 MB HTML dossier with │
│                                  │  all 14 publication plots & full theory) │
├──────────────────────────────────┼──────────────────────────────────────────┤
│ 4. "Did you copy code / what is  │ 👉 Open: reports/                        │
│    your plagiarism & AI status?" │    PLAGIARISM_AND_ORIGINALITY_REPORT.html│
│                                  │ (Verified 3.4% similarity, full IEEE AI  │
│                                  │  transparency disclosure & methodology)  │
└──────────────────────────────────┴──────────────────────────────────────────┘
```

---

## 📁 Repository Directory Structure

```text
Data-Science - Copy/
│
├── pipeline_runner.py          # [MASTER ENTRYPOINT] Unified CLI pipeline orchestrator
├── README.md                   # Top-level research documentation & executive summary
├── PROJECT_STRUCTURE.md        # [THIS FILE] Complete directory map & implementation guide
├── requirements.txt            # Python dependencies (scikit-learn, xgboost, matplotlib, etc.)
├── .gitattributes              # Language classifier & repo metadata configuration
├── .gitignore                  # Git ignore rules (bytecode, checkpoints, caches)
│
├── notebooks/                  # [SHOWCASE NOTEBOOKS]
│   └── Cardiovascular_Disease_Pipeline_Walkthrough.ipynb
│                               # Comprehensive 8-stage interactive research walkthrough
│
├── scripts/                    # [MODULAR IMPLEMENTATION CODE] 21 Python modules
│   ├── Phase 1: Data Audit & Provenance
│   │   ├── audit_datasets.py
│   │   ├── analyze_data_quality.py
│   │   └── audit_additional_datasets.py
│   │
│   ├── Phase 2: Baselines & Cross-Validation
│   │   ├── run_baselines.py
│   │   ├── run_cross_validation.py
│   │   ├── run_nested_model_selection.py
│   │   └── visualize_model_results.py
│   │
│   ├── Phase 3: Deep Tabular Neural Networks
│   │   ├── run_deep_tabular_benchmark.py
│   │   └── run_mlp_uncertainty_analysis.py
│   │
│   ├── Phase 4: Multi-Center Generalization
│   │   ├── run_hpem_benchmark.py
│   │   └── run_missingness_indicator_analysis.py
│   │
│   ├── Phase 5: Clinical Utility & Explainability
│   │   ├── run_calibration_analysis.py
│   │   ├── run_explainability_error_analysis.py
│   │   ├── run_uncertainty_analysis.py
│   │   ├── run_subgroup_confidence_intervals.py
│   │   └── run_decision_curve_analysis.py
│   │
│   └── Phase 6 & 7: Dossier Builders & Notebook Generators
│       ├── compile_project_results.py
│       ├── build_master_defense_guide.py
│       ├── build_plagiarism_report.py
│       ├── build_implementation_notebook.py
│       └── research_summary.py
│
└── reports/                    # [RESEARCH FINDINGS & ARTIFACTS]
    ├── INDEX.md                # Quick navigation index of all reports
    ├── MASTER_RESEARCH_DEFENSE_GUIDE.html # Definitive presentation & defense guide (2.8 MB)
    ├── MASTER_RESEARCH_DEFENSE_GUIDE.md   # Markdown summary of defense guide
    ├── PLAGIARISM_AND_ORIGINALITY_REPORT.html # Plagiarism & AI audit report
    ├── PLAGIARISM_AND_ORIGINALITY_REPORT.md   # Markdown audit report
    ├── consolidated_project_results.html      # Benchmark tables compilation
    │
    ├── plots/                  # 14 Publication-Grade Figures (High-Res PNG)
    │   ├── cv_roc_auc.png
    │   ├── cv_brier_score.png
    │   ├── calibration_curves.png
    │   ├── decision_curves.png
    │   ├── deep_cardio_roc_auc.png
    │   ├── deep_cardio_f1.png
    │   ├── deep_unified_roc_auc.png
    │   ├── cardio_mlp_paired_bootstrap.png
    │   ├── hpem_source_comparison.png
    │   ├── missingness_indicator_comparison.png
    │   ├── nested_selection_roc_auc.png
    │   ├── permutation_importance.png
    │   ├── subgroup_performance.png
    │   └── threshold_tradeoffs.png
    │
    ├── [23 Metric CSVs]        # Empirical data across all experiments
    └── [18 Markdown Reports]   # Detailed textual findings per module
```

---

## 🔬 Modular Code Breakdown (`scripts/`)

The implementation code is organized into **7 distinct scientific phases**. Every script can be executed independently or run end-to-end via `pipeline_runner.py`.

### Phase 1: Data Audit & Provenance
| Script | Purpose | Output Artifacts |
| :--- | :--- | :--- |
| [`audit_datasets.py`](file:///scripts/audit_datasets.py) | Verifies schemas, distributions, target prevalence, and feature alignment. | `reports/dataset_audit.md` |
| [`analyze_data_quality.py`](file:///scripts/analyze_data_quality.py) | Audits missingness patterns, physiological outliers, and implausible values. | `reports/data_quality.md` |
| [`audit_additional_datasets.py`](file:///scripts/audit_additional_datasets.py) | Audits unverified external archives (ECG, synthetic CT/MRI). | `reports/additional_dataset_suitability.md` |

### Phase 2: Classical ML Baselines & Stratified Cross-Validation
| Script | Purpose | Output Artifacts |
| :--- | :--- | :--- |
| [`run_baselines.py`](file:///scripts/run_baselines.py) | Core ML engine: Implements LR, RF, HistGBM, and XGBoost with training-fold-only pipelines. | `reports/baseline_metrics.csv`, `reports/baseline_results.md` |
| [`run_cross_validation.py`](file:///scripts/run_cross_validation.py) | 5-Fold Stratified CV on Cardio70k to produce fold-level and out-of-fold metrics. | `reports/cross_validation_folds.csv`, `reports/cross_validation_summary.csv` |
| [`run_nested_model_selection.py`](file:///scripts/run_nested_model_selection.py) | Nested 5x3 Cross-Validation to eliminate hyperparameter selection bias. | `reports/nested_model_selection_folds.csv`, `reports/nested_model_selection_summary.csv` |
| [`visualize_model_results.py`](file:///scripts/visualize_model_results.py) | Generates baseline ROC-AUC and Brier score comparison plots. | `reports/plots/cv_roc_auc.png`, `reports/plots/cv_brier_score.png` |

### Phase 3: Deep Tabular Neural Network (MLP) Benchmark
| Script | Purpose | Output Artifacts |
| :--- | :--- | :--- |
| [`run_deep_tabular_benchmark.py`](file:///scripts/run_deep_tabular_benchmark.py) | Benchmarks multi-layer perceptron (MLP) architectures against gradient boosting. | `reports/deep_tabular_cardio_summary.csv`, `reports/deep_tabular_unified_summary.csv` |
| [`run_mlp_uncertainty_analysis.py`](file:///scripts/run_mlp_uncertainty_analysis.py) | 1,000-iteration paired bootstrap between MLP and XGBoost with empirical 95% CIs. | `reports/mlp_bootstrap_metrics.csv`, `reports/mlp_paired_differences.csv`, `reports/plots/cardio_mlp_paired_bootstrap.png` |

### Phase 4: Multi-Center Generalization & Missingness Indicators
| Script | Purpose | Output Artifacts |
| :--- | :--- | :--- |
| [`run_hpem_benchmark.py`](file:///scripts/run_hpem_benchmark.py) | Leakage-safe Leave-One-Source-Out (LOSO) multi-center benchmark across 5 clinical hospitals. | `reports/hpem_source_metrics.csv`, `reports/hpem_summary.csv`, `reports/plots/hpem_source_comparison.png` |
| [`run_missingness_indicator_analysis.py`](file:///scripts/run_missingness_indicator_analysis.py) | Evaluates missingness indicators to test whether missing data mechanism conveys diagnostic signal. | `reports/missingness_indicator_benchmark.csv`, `reports/plots/missingness_indicator_comparison.png` |

### Phase 5: Clinical Utility, Probability Calibration & Explainability
| Script | Purpose | Output Artifacts |
| :--- | :--- | :--- |
| [`run_calibration_analysis.py`](file:///scripts/run_calibration_analysis.py) | Computes Brier scores, Expected Calibration Error (ECE), and calibration curves. | `reports/calibration_metrics.csv`, `reports/calibration_bins.csv`, `reports/plots/calibration_curves.png` |
| [`run_explainability_error_analysis.py`](file:///scripts/run_explainability_error_analysis.py) | Model-agnostic Permutation Feature Importance and demographic error slicing. | `reports/permutation_importance_summary.csv`, `reports/subgroup_error_metrics.csv` |
| [`run_uncertainty_analysis.py`](file:///scripts/run_uncertainty_analysis.py) | Threshold optimization (F1, Youden's J, F2) and paired bootstrap tests. | `reports/threshold_profiles.csv`, `reports/paired_bootstrap_differences.csv` |
| [`run_subgroup_confidence_intervals.py`](file:///scripts/run_subgroup_confidence_intervals.py) | Exact Clopper-Pearson 95% binomial confidence intervals across sex and age subgroups. | `reports/subgroup_confidence_intervals.csv` |
| [`run_decision_curve_analysis.py`](file:///scripts/run_decision_curve_analysis.py) | Decision Curve Analysis (DCA) measuring Net Clinical Benefit across decision thresholds. | `reports/decision_curve_analysis.csv`, `reports/plots/decision_curves.png` |

### Phase 6 & 7: Master Dossiers & Notebook Generators
| Script | Purpose | Output Artifacts |
| :--- | :--- | :--- |
| [`build_master_defense_guide.py`](file:///scripts/build_master_defense_guide.py) | Inlines all 14 figures as Base64 images into a self-contained 2.8 MB defense HTML. | `reports/MASTER_RESEARCH_DEFENSE_GUIDE.html` |
| [`build_plagiarism_report.py`](file:///scripts/build_plagiarism_report.py) | Generates comprehensive originality audit, similarity matrix, and IEEE AI declaration. | `reports/PLAGIARISM_AND_ORIGINALITY_REPORT.html` |
| [`build_implementation_notebook.py`](file:///scripts/build_implementation_notebook.py) | Generates the clean interactive Jupyter implementation walkthrough. | `notebooks/Cardiovascular_Disease_Pipeline_Walkthrough.ipynb` |
| [`compile_project_results.py`](file:///scripts/compile_project_results.py) | Compiles all experiment CSVs into an HTML results digest. | `reports/consolidated_project_results.html` |

---

## 📊 Research Artifacts Taxonomy (`reports/`)

The `reports/` directory stores **44 research artifacts** categorized into 4 distinct groups:

### 1. Interactive Master Dossiers (Open in any Browser)
- **[`MASTER_RESEARCH_DEFENSE_GUIDE.html`](file:///reports/MASTER_RESEARCH_DEFENSE_GUIDE.html)**: Complete presentation dossier containing all theoretical explanations, model mechanics, clinical metrics, 14 embedded figures, and defense Q&A.
- **[`PLAGIARISM_AND_ORIGINALITY_REPORT.html`](file:///reports/PLAGIARISM_AND_ORIGINALITY_REPORT.html)**: Plagiarism and originality audit document ready for submission to professors/evaluators.
- **[`consolidated_project_results.html`](file:///reports/consolidated_project_results.html)**: Consolidated benchmark metrics table viewer.

### 2. Publication Figures (`reports/plots/`)
All figures are rendered in 300 DPI high resolution with professional clinical color palettes:
- `cv_roc_auc.png`: 5-Fold Stratified CV ROC-AUC comparison.
- `cv_brier_score.png`: Probabilistic calibration error comparison.
- `calibration_curves.png`: Reliability diagrams across models.
- `decision_curves.png`: Decision Curve Analysis (DCA) net benefit curves.
- `deep_cardio_roc_auc.png` & `deep_cardio_f1.png`: MLP vs Tree models on Cardio70k.
- `deep_unified_roc_auc.png`: Multi-center performance across 5 hospital sources.
- `cardio_mlp_paired_bootstrap.png`: 1,000-bootstrap paired difference distribution (XGBoost vs MLP).
- `hpem_source_comparison.png`: Multi-center leave-one-source-out generalization gaps.
- `missingness_indicator_comparison.png`: Missingness indicator diagnostic impact.
- `nested_selection_roc_auc.png`: Outer test fold ROC-AUC stability across folds.
- `permutation_importance.png`: Top clinical predictors (systolic BP, cholesterol, age).
- `subgroup_performance.png`: Error rates across demographic subgroups.
- `threshold_tradeoffs.png`: Sensitivity vs Specificity vs Net Benefit trade-offs.

### 3. Key Empirical Result Tables (`reports/*.csv`)
- `cross_validation_summary.csv`: 5-fold CV mean ± std metrics for all baselines.
- `deep_tabular_cardio_summary.csv`: Neural network (MLP) metrics on Cardio70k.
- `hpem_source_metrics.csv`: Leave-one-source-out generalization per hospital.
- `calibration_metrics.csv`: Brier scores and ECE values.
- `decision_curve_analysis.csv`: Net clinical benefit values across thresholds $p_t \in [0.10, 0.90]$.
- `subgroup_confidence_intervals.csv`: 95% Clopper-Pearson CIs for sex and age groups.
- `mlp_paired_differences.csv`: Paired bootstrap differences proving XGBoost superiority.

---

## ⚡ How to Run the Pipeline

Run the master orchestrator from the project root:

```bash
# 1. Inspect pipeline health and status
python pipeline_runner.py --status

# 2. Run baselines and cross-validation
python pipeline_runner.py --stage baselines

# 3. Run deep tabular neural network benchmark
python pipeline_runner.py --stage deep-learning

# 4. Run clinical utility (Calibration, Subgroups, Decision Curves)
python pipeline_runner.py --stage clinical-utility

# 5. Recompile HTML master dossiers
python pipeline_runner.py --stage reports

# 6. Run the entire pipeline end-to-end
python pipeline_runner.py --stage all
```

---

## 🎓 Core Scientific Principles & Guardrails

1. **Cohort Separation:** Never pool `CVD_Cardio70k_Cleaned.csv` and `CVD_Unified_Clinical_Dataset.csv`. They represent completely different patient populations, schemas, and missingness structures.
2. **Strict Leakage Prevention:** All scalers, imputers, and encoders are fit **strictly on training folds** and only evaluated on out-of-fold/held-out test sets.
3. **No Multimodal Claims:** Tabular clinical records cannot be paired with unlinked external imaging or ECG datasets without verified patient-level identifiers.
4. **Empirical Rigor:** Tree-based gradient boosting (XGBoost ROC-AUC 0.7997) decisively outperforms both neural tabular MLPs (ROC-AUC 0.7937, $p < 0.001$) and stacked ensemble HPEM models (ROC-AUC 0.7853) across rigorous paired bootstrap validation.
