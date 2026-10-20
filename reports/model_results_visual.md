# Model Performance Visual Summary

## Best model recommendation

The strongest tested model on the Cardio70k cohort is **XGBoost** with ROC-AUC **0.8019**, F1 **0.7205**, precision **0.7558**, and accuracy **0.7358**.

## Graphical results

### Cardio70k 5-fold CV ROC-AUC

![Cardio70k ROC-AUC](plots/cv_roc_auc.png)

### Cardio70k 5-fold CV Brier score

![Cardio70k Brier score](plots/cv_brier_score.png)

### Nested model-selection ROC-AUC

![Nested selection ROC-AUC](plots/nested_selection_roc_auc.png)

## Tabular summary

### Cardio70k stratified 5-fold CV summary

| model | accuracy_oof | precision_oof | sensitivity_oof | specificity_oof | f1_oof | roc_auc_oof | pr_auc_oof | brier_score_oof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| XGBoost | 0.7358 | 0.7558 | 0.6883 | 0.7822 | 0.7205 | 0.8019 | 0.7828 | 0.1802 |
| HistGradientBoosting | 0.7349 | 0.7543 | 0.6884 | 0.7804 | 0.7198 | 0.8009 | 0.7824 | 0.1806 |
| MLP | 0.7342 | 0.7513 | 0.6918 | 0.7758 | 0.7203 | 0.7991 | 0.7788 | 0.1814 |
| LogisticRegression | 0.7292 | 0.7652 | 0.6530 | 0.8038 | 0.7047 | 0.7939 | 0.7710 | 0.1851 |
| RandomForest | 0.7263 | 0.7378 | 0.6930 | 0.7588 | 0.7147 | 0.7892 | 0.7731 | 0.1866 |

### Nested selection summary

| selected_model | n_outer_folds_selected | mean_inner_cv_roc_auc | accuracy_mean | precision_mean | sensitivity_mean | specificity_mean | f1_mean | roc_auc_mean | pr_auc_mean | brier_score_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| XGBoost | 5 | 0.8011 | 0.7358 | 0.7558 | 0.6883 | 0.7822 | 0.7205 | 0.8019 | 0.7831 | 0.1802 |

### Baseline holdout comparison

| model | feature_set | accuracy | precision | sensitivity | specificity | f1 | roc_auc | pr_auc | brier_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| XGBoost | Exclude BMI, pulse pressure, BP category | 0.7325 | 0.7474 | 0.6938 | 0.7705 | 0.7196 | 0.7993 | 0.7848 | 0.1815 |
| XGBoost | All candidate predictors | 0.7322 | 0.7482 | 0.6913 | 0.7722 | 0.7186 | 0.7992 | 0.7844 | 0.1815 |
| HistGradientBoosting | Exclude BMI, pulse pressure, BP category | 0.7298 | 0.7434 | 0.6929 | 0.7658 | 0.7173 | 0.7987 | 0.7840 | 0.1818 |
| HistGradientBoosting | All candidate predictors | 0.7293 | 0.7416 | 0.6951 | 0.7628 | 0.7176 | 0.7986 | 0.7836 | 0.1818 |
| MLP | All candidate predictors | 0.7322 | 0.7469 | 0.6939 | 0.7697 | 0.7194 | 0.7983 | 0.7817 | 0.1823 |
| MLP | Exclude BMI, pulse pressure, BP category | 0.7288 | 0.7479 | 0.6816 | 0.7751 | 0.7132 | 0.7977 | 0.7799 | 0.1823 |
| LogisticRegression | All candidate predictors | 0.7276 | 0.7592 | 0.6583 | 0.7956 | 0.7051 | 0.7922 | 0.7748 | 0.1855 |
| LogisticRegression | Exclude BMI, pulse pressure, BP category | 0.7273 | 0.7516 | 0.6705 | 0.7830 | 0.7087 | 0.7898 | 0.7755 | 0.1872 |
| RandomForest | All candidate predictors | 0.7248 | 0.7333 | 0.6973 | 0.7517 | 0.7149 | 0.7871 | 0.7709 | 0.1876 |
| RandomForest | Exclude BMI, pulse pressure, BP category | 0.7244 | 0.7332 | 0.6964 | 0.7518 | 0.7143 | 0.7867 | 0.7711 | 0.1877 |
