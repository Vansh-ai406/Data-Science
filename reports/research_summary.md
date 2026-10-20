# Research Summary for Cardiovascular Disease Prediction

## Study protocol and data usage

This project follows a leak-safe, research-oriented workflow. The supplied data were treated as two separate clinical cohorts rather than as a single merged dataset. The large `CVD_Cardio70k_Cleaned.csv` file is used for internal discrimination benchmarking; the `CVD_Unified_Clinical_Dataset.csv` file is used for source-aware cross-cohort generalization testing. The ML-ready unified export is not treated as the canonical train set because imputation occurred before the train/test split, which would leak information.

## Key benchmark findings

- Best internal Cardio70k model: **XGBoost** with ROC-AUC **0.8019**, F1 **0.7205**, precision **0.7558**, and accuracy **0.7358**.
- Best nested-selection model: **XGBoost** with mean outer-fold ROC-AUC **0.8019**.
- Best generalization model across the unified multi-source dataset: **LogisticRegression** with mean ROC-AUC **0.7449**, F1 **0.7525**, and accuracy **0.6979**.

## Internal Cardio70k validation table

| model | accuracy_oof | precision_oof | f1_oof | roc_auc_oof | brier_score_oof |
| --- | --- | --- | --- | --- | --- |
| XGBoost | 0.7358 | 0.7558 | 0.7205 | 0.8019 | 0.1802 |
| HistGradientBoosting | 0.7349 | 0.7543 | 0.7198 | 0.8009 | 0.1806 |
| MLP | 0.7342 | 0.7513 | 0.7203 | 0.7991 | 0.1814 |
| LogisticRegression | 0.7292 | 0.7652 | 0.7047 | 0.7939 | 0.1851 |
| RandomForest | 0.7263 | 0.7378 | 0.7147 | 0.7892 | 0.1866 |

## Generalization view across the unified cohort

| model | accuracy_mean | precision_mean | f1_mean | roc_auc_mean | pr_auc_mean | brier_score_mean |
| --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.6979 | 0.7547 | 0.7525 | 0.7449 | 0.8234 | 0.2084 |
| MLP | 0.6989 | 0.7650 | 0.7539 | 0.7431 | 0.8251 | 0.2088 |
| RandomForest | 0.6849 | 0.7329 | 0.7343 | 0.7138 | 0.7907 | 0.2015 |
| XGBoost | 0.7108 | 0.7508 | 0.7490 | 0.7018 | 0.7773 | 0.2050 |
| HistGradientBoosting | 0.6947 | 0.7344 | 0.7360 | 0.6854 | 0.7714 | 0.2206 |

## Probability calibration

Cardio70k calibration uses pooled out-of-fold predictions; unified-cohort calibration uses leave-one-source-out predictions. These are diagnostics on the evaluated cohorts, not prospective calibration estimates. No post-hoc calibration was fit.

| cohort | held_out_source | model | n | brier_score | calibration_intercept | calibration_slope | ece_10_bins |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cardio70k | All folds | LogisticRegression | 68581 | 0.1851 | -0.0002 | 0.9987 | 0.0294 |
| Cardio70k | All folds | XGBoost | 68581 | 0.1802 | 0.0002 | 1.0019 | 0.0024 |
| Unified clinical | Mendeley_India | LogisticRegression | 1000 | 0.2768 | -0.0192 | 0.2752 | 0.2103 |
| Unified clinical | Mendeley_India | XGBoost | 1000 | 0.3244 | 0.3162 | 0.0120 | 0.2665 |
| Unified clinical | UCI_Cleveland | LogisticRegression | 303 | 0.1685 | -0.4851 | 0.7181 | 0.0965 |
| Unified clinical | UCI_Cleveland | XGBoost | 303 | 0.1722 | -0.3523 | 0.7083 | 0.0831 |
| Unified clinical | UCI_Hungary | LogisticRegression | 293 | 0.1591 | -0.7218 | 1.0011 | 0.1096 |
| Unified clinical | UCI_Hungary | XGBoost | 293 | 0.1601 | -0.3983 | 0.7665 | 0.0668 |
| Unified clinical | UCI_LongBeachVA | LogisticRegression | 199 | 0.1933 | 0.7555 | 0.4351 | 0.1406 |
| Unified clinical | UCI_LongBeachVA | XGBoost | 199 | 0.1937 | 0.7343 | 0.3635 | 0.1557 |
| Unified clinical | UCI_Switzerland | LogisticRegression | 123 | 0.2443 | 2.6950 | 0.3670 | 0.3500 |
| Unified clinical | UCI_Switzerland | XGBoost | 123 | 0.1748 | 2.4468 | 0.2975 | 0.2700 |
| Unified clinical | All held-out sources | LogisticRegression | 1918 | 0.2310 | -0.0607 | 0.4375 | 0.1336 |
| Unified clinical | All held-out sources | XGBoost | 1918 | 0.2521 | 0.1478 | 0.3502 | 0.1643 |

## Research interpretation

The strongest internal discriminator is XGBoost, and nested validation selected it in all five outer folds. Cardio70k XGBoost out-of-fold calibration is close to ideal (slope about 1.00), while calibration on the unified source-held-out cohort is substantially weaker and varies by source. Report the large cohort as internal validation and the unified cohort as a source-shift stress test, not as pooled or external clinical validation.

## Research status

Completed: data audit and quality analysis, leakage-safe baselines, internal cross-validation, nested selection, deep tabular benchmarking, source-held-out stress testing, figures/tables, calibration diagnostics, held-out permutation importance, exploratory subgroup/error analysis, and a leakage-safe HPEM adaptation benchmark. The adaptation did not outperform matched XGBoost source-held-out results and is not an exact reproduction of the paper protocol.

Remaining: (1) independent external validation on a compatible cohort; (2) uncertainty intervals and threshold-utility analysis for a prespecified use case; (3) verify coded subgroup semantics and obtain expert review; (4) exact reproduction of the foundation paper's HPEM on matched datasets/protocol if it is in scope; and (5) evaluate calibration prospectively or on an independent calibration cohort. Multimodal work requires valid patient-linked data. These research results do not establish clinical readiness.
