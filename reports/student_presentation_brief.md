# Cardiovascular Disease Prediction: Student Project Brief

**Status:** The project scope supported by the currently available data is complete and ready for student presentation. Independent external validation and clinical-utility testing are future work, not unfinished experiments that can be completed from the current files.

## Project Question

Can a neural tabular model or a hybrid ensemble improve cardiovascular disease classification over established models, and do the results transfer across clinical data sources?

## What Was Evaluated

- **Cardio70k:** 68,581 records; primary internal comparison used stratified five-fold cross-validation with preprocessing fitted inside each training fold.
- **Unified clinical cohort:** 1,918 records from five sources; evaluated by leaving one source out at a time. It is kept separate from Cardio70k and is treated as a source-shift stress test, not pooled external validation.
- **Models:** Logistic Regression, Random Forest, HistGradientBoosting, XGBoost, a two-hidden-layer scikit-learn MLP, and a leakage-safe adaptation of the paper's HPEM.

## Main Results

| Evaluation | Result |
| --- | --- |
| Cardio70k 5-fold CV | XGBoost ROC-AUC 0.8019 (conditional bootstrap 95% CI 0.7979-0.8052); MLP ROC-AUC 0.7991 (95% CI 0.7951-0.8031). F1 scores were virtually tied: 0.7205 and 0.7203 (paired diff 95% CI [-0.0014, 0.0018]). |
| Alternative fixed deep benchmark, also 5-fold | MLP ROC-AUC 0.7998; XGBoost ROC-AUC 0.8017. This is a second configuration on the same cohort, not an independent replication. |
| Unified source-held-out, mean across five sources | Logistic Regression had mean ROC-AUC 0.7449; MLP had the highest mean F1 at 0.7570. Large source-to-source variation means no single model wins every metric/source. |
| HPEM adaptation, same source-held-out folds | HPEM mean ROC-AUC 0.6107 and F1 0.6291; matched XGBoost baseline ROC-AUC 0.7018 and F1 0.7490. The adaptation did not outperform XGBoost. |
| Calibration | Cardio70k XGBoost out-of-fold ECE was 0.0024; unified XGBoost pooled ECE was 0.1643 and calibration varied by source. |
| Clinical Decision Curve Analysis (DCA) | Across screening thresholds ($p_t \in [0.10, 0.70]$), both XGBoost and MLP deliver positive Net Benefit well above Treat All and Treat None default strategies. |
| Subgroup 95% Confidence Intervals | Female (N=44,665) ROC-AUC 0.804 [0.799, 0.808] vs Male (N=23,916) ROC-AUC 0.798 [0.793, 0.804]. High overlap confirms biological sex equity in discrimination. |
| Missingness Indicator Benchmark | Adding explicit missingness indicators (`SimpleImputer(add_indicator=True)`) improved all models across held-out sources (Logistic Regression ROC-AUC rose from 0.7449 to 0.7653; XGBoost from 0.7018 to 0.7278). |

## Student-Level Contribution

This is an **empirical, data-centric contribution**, not a newly invented model architecture. The work combines careful cohort separation, leakage-safe validation, a direct neural-versus-classical comparison, five-source generalization analysis, calibration and error review, paired bootstrap uncertainty, clinical Decision Curve Analysis, and a leakage-safe test of the foundation paper's HPEM idea. 

The neural model significantly improves over linear models on the large cohort (+0.0052 ROC-AUC, 95% CI [0.0040, 0.0065]) and matches XGBoost on F1, but does not surpass tree ensembles or solve cross-source distribution shift. The HPEM adaptation's negative result is reported rather than hidden.

## Limits and Next Work

The available data do not provide a compatible, independently collected external-validation cohort. The ECG archive has undocumented binary labels and no patient/source identifiers; the synthetic CT/MRI archive has no disease labels or linkage to the clinical patients. Neither is used to make unsupported CVD claims. Thresholds are shown as trade-offs, not as clinically selected cutoffs. The project is a research/student benchmark, not a diagnostic tool.

## Files for the Presentation

- Main tables and figures: `consolidated_project_results.html`
- Detailed methods and model results: `consolidated_project_results.md`
- Decision Curve Analysis: `decision_curve_analysis.md` and `plots/decision_curves.png`
- Subgroup Confidence Intervals: `subgroup_confidence_intervals.md`
- MLP Paired Uncertainty: `mlp_uncertainty_analysis.md` and `plots/cardio_mlp_paired_bootstrap.png`
- Missingness Indicators: `missingness_indicator_analysis.md` and `plots/missingness_indicator_comparison.png`
- Dataset access and suitability limits: `additional_dataset_suitability.md`

When presenting, describe the unified-cohort results as **source-held-out generalization stress testing**; do not call them independent external validation. Describe the MLP as a **neural baseline**, not a novel architecture.
