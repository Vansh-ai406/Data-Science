# Nested Cardio70k Model Selection

This stage uses nested stratified validation on Cardio70k to reduce the risk of selecting a model from the same data used for the final estimate. The outer loop estimates generalization performance, while the inner loop selects the candidate model using mean ROC-AUC on training folds only.

## Outer-fold results

Each outer fold has one selected model. Fold-level metrics are in `reports/nested_model_selection_folds.csv`.

| outer_fold | selected_model | inner_cv_mean_roc_auc | accuracy | precision | sensitivity | specificity | f1 | roc_auc | pr_auc | brier_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | XGBoost | 0.801 | 0.736 | 0.756 | 0.688 | 0.783 | 0.721 | 0.802 | 0.782 | 0.180 |
| 2 | XGBoost | 0.800 | 0.738 | 0.754 | 0.697 | 0.778 | 0.724 | 0.805 | 0.786 | 0.178 |
| 3 | XGBoost | 0.801 | 0.738 | 0.764 | 0.682 | 0.794 | 0.721 | 0.803 | 0.786 | 0.180 |
| 4 | XGBoost | 0.801 | 0.736 | 0.754 | 0.692 | 0.779 | 0.722 | 0.802 | 0.782 | 0.180 |
| 5 | XGBoost | 0.803 | 0.731 | 0.750 | 0.682 | 0.778 | 0.715 | 0.798 | 0.780 | 0.182 |

## Aggregated selection summary

| selected_model | n_outer_folds_selected | mean_inner_cv_roc_auc | accuracy_mean | accuracy_sd | precision_mean | precision_sd | sensitivity_mean | sensitivity_sd | specificity_mean | specificity_sd | f1_mean | f1_sd | roc_auc_mean | roc_auc_sd | pr_auc_mean | pr_auc_sd | brier_score_mean | brier_score_sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| XGBoost | 5 | 0.801 | 0.736 | 0.003 | 0.756 | 0.005 | 0.688 | 0.006 | 0.782 | 0.007 | 0.720 | 0.003 | 0.802 | 0.003 | 0.783 | 0.003 | 0.180 | 0.001 |

## Interpretation

The selected model is the one with the best mean inner-fold ROC-AUC. Those estimates are then evaluated on untouched outer folds. This protects the final performance numbers from circular model selection and gives a more credible model-ranking step before any final deployment or paper claim.

Machine-readable summary: `reports/nested_model_selection_summary.csv`.
