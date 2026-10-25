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
| Cardio70k 5-fold CV | XGBoost ROC-AUC 0.8019 (conditional bootstrap 95% CI 0.7979-0.8052); MLP ROC-AUC 0.7991. Their F1 scores were nearly identical: 0.7205 and 0.7203. |
| Alternative fixed deep benchmark, also 5-fold | MLP ROC-AUC 0.7998; XGBoost ROC-AUC 0.8017. This is a second configuration on the same cohort, not an independent replication. |
| Unified source-held-out, mean across five sources | Logistic Regression had mean ROC-AUC 0.7449; MLP had the highest mean F1 at 0.7570. Large source-to-source variation means no single model wins every metric/source. |
| HPEM adaptation, same source-held-out folds | HPEM mean ROC-AUC 0.6107 and F1 0.6291; matched XGBoost baseline ROC-AUC 0.7018 and F1 0.7490. The adaptation did not outperform XGBoost. |
| Calibration | Cardio70k XGBoost out-of-fold ECE was 0.0024; unified XGBoost pooled ECE was 0.1643 and calibration varied by source. |

## Student-Level Contribution

This is an **empirical, data-centric contribution**, not a newly invented model architecture. The work combines careful cohort separation, leakage-safe validation, a direct neural-versus-classical comparison, five-source generalization analysis, calibration and error review, and a leakage-safe test of the foundation paper's HPEM idea. The neural model is close to XGBoost on the large cohort but does not consistently improve results across sources. The HPEM adaptation's negative result is reported rather than hidden.

## Limits and Next Work

The available data do not provide a compatible, independently collected external-validation cohort. The ECG archive has undocumented binary labels and no patient/source identifiers; the synthetic CT/MRI archive has no disease labels or linkage to the clinical patients. Neither is used to make unsupported CVD claims. Thresholds are shown as trade-offs, not as clinically selected cutoffs. The project is a research/student benchmark, not a diagnostic tool.

## Files for the Presentation

- Main tables and figures: `consolidated_project_results.html`
- Detailed methods and model results: `consolidated_project_results.md`
- Dataset access and suitability limits: `additional_dataset_suitability.md`

When presenting, describe the unified-cohort results as **source-held-out generalization stress testing**; do not call them independent external validation. Describe the MLP as a **neural baseline**, not a novel architecture.
