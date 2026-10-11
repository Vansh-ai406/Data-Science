# Cardio70k Cross-Validation Results

Each record is assigned to one held-out fold exactly once. Imputation, encoding, and scaling are fitted inside each training fold. Model hyperparameters were fixed in advance for this run; no tuning or resampling is performed.

## Pooled out-of-fold metrics

Each `_oof` score uses all held-out predictions combined. Fold mean and sample standard deviation summarize variation across the five folds; they are not confidence intervals.

| model | n | accuracy_oof | accuracy_fold_mean | accuracy_fold_sd | precision_oof | precision_fold_mean | precision_fold_sd | sensitivity_oof | sensitivity_fold_mean | sensitivity_fold_sd | specificity_oof | specificity_fold_mean | specificity_fold_sd | f1_oof | f1_fold_mean | f1_fold_sd | roc_auc_oof | roc_auc_fold_mean | roc_auc_fold_sd | pr_auc_oof | pr_auc_fold_mean | pr_auc_fold_sd | brier_score_oof | brier_score_fold_mean | brier_score_fold_sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 68581 | 0.729 | 0.729 | 0.004 | 0.765 | 0.765 | 0.005 | 0.653 | 0.653 | 0.005 | 0.804 | 0.804 | 0.005 | 0.705 | 0.705 | 0.004 | 0.794 | 0.794 | 0.003 | 0.771 | 0.771 | 0.004 | 0.185 | 0.185 | 0.001 |
| MLP | 68581 | 0.734 | 0.734 | 0.003 | 0.751 | 0.752 | 0.008 | 0.692 | 0.692 | 0.017 | 0.776 | 0.776 | 0.015 | 0.720 | 0.720 | 0.006 | 0.799 | 0.800 | 0.002 | 0.779 | 0.779 | 0.001 | 0.181 | 0.181 | 0.001 |
| RandomForest | 68581 | 0.726 | 0.726 | 0.003 | 0.738 | 0.738 | 0.005 | 0.693 | 0.693 | 0.004 | 0.759 | 0.759 | 0.007 | 0.715 | 0.715 | 0.003 | 0.789 | 0.789 | 0.002 | 0.773 | 0.773 | 0.002 | 0.187 | 0.187 | 0.001 |
| HistGradientBoosting | 68581 | 0.735 | 0.735 | 0.003 | 0.754 | 0.754 | 0.006 | 0.688 | 0.688 | 0.010 | 0.780 | 0.780 | 0.010 | 0.720 | 0.720 | 0.004 | 0.801 | 0.801 | 0.002 | 0.782 | 0.783 | 0.003 | 0.181 | 0.181 | 0.001 |
| XGBoost | 68581 | 0.736 | 0.736 | 0.003 | 0.756 | 0.756 | 0.005 | 0.688 | 0.688 | 0.006 | 0.782 | 0.782 | 0.007 | 0.720 | 0.720 | 0.003 | 0.802 | 0.802 | 0.003 | 0.783 | 0.783 | 0.003 | 0.180 | 0.180 | 0.001 |

## Interpretation

This is internal validation on Cardio70k, not external or prospective validation. The 5-fold results replace the single holdout as the main internal baseline estimate; prior holdout results remain exploratory. Repeated predictor profiles are retained because distinct IDs represent separate records and some identical profiles carry different labels. The next evaluation stage is nested model selection on training folds, then a locked final test only if one is reserved before further tuning.

Fold-level metrics: `reports/cross_validation_folds.csv`.
Summary metrics: `reports/cross_validation_summary.csv`.
