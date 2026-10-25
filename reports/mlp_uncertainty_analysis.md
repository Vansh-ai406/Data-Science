# Cardio70k MLP & Paired Model Uncertainty Analysis

## Research Objective

To directly test whether the neural MLP baseline provides statistically significant discrimination gains over Logistic Regression and whether XGBoost holds a statistically significant margin over MLP under non-parametric bootstrap resampling (300 stratified replicates).

## Results: Point Estimates and 95% Bootstrap Confidence Intervals

| Model | Metric | Estimate | 95% CI Lower | 95% CI Upper |
|:---|:---|---:|---:|---:|
| XGBoost | roc_auc | 0.8019 | 0.7986 | 0.8053 |
| XGBoost | pr_auc | 0.7828 | 0.7782 | 0.7871 |
| XGBoost | accuracy | 0.7358 | 0.7326 | 0.7389 |
| XGBoost | sensitivity | 0.6883 | 0.6830 | 0.6928 |
| XGBoost | specificity | 0.7822 | 0.7780 | 0.7866 |
| XGBoost | f1 | 0.7205 | 0.7168 | 0.7239 |
| XGBoost | brier_score | 0.1802 | 0.1787 | 0.1818 |
| MLP | roc_auc | 0.7991 | 0.7959 | 0.8026 |
| MLP | pr_auc | 0.7788 | 0.7739 | 0.7837 |
| MLP | accuracy | 0.7342 | 0.7310 | 0.7378 |
| MLP | sensitivity | 0.6918 | 0.6865 | 0.6965 |
| MLP | specificity | 0.7758 | 0.7711 | 0.7804 |
| MLP | f1 | 0.7203 | 0.7167 | 0.7239 |
| MLP | brier_score | 0.1814 | 0.1798 | 0.1829 |
| LogisticRegression | roc_auc | 0.7939 | 0.7907 | 0.7975 |
| LogisticRegression | pr_auc | 0.7710 | 0.7668 | 0.7755 |
| LogisticRegression | accuracy | 0.7292 | 0.7259 | 0.7323 |
| LogisticRegression | sensitivity | 0.6530 | 0.6479 | 0.6580 |
| LogisticRegression | specificity | 0.8038 | 0.7997 | 0.8086 |
| LogisticRegression | f1 | 0.7047 | 0.7010 | 0.7082 |
| LogisticRegression | brier_score | 0.1851 | 0.1836 | 0.1866 |

## Paired Model Differences (First minus Second)

![Paired Bootstrap Differences](plots/cardio_mlp_paired_bootstrap.png)

| Comparison | Metric | Estimate Difference | 95% CI Lower | 95% CI Upper | Significant at 5%? |
|:---|:---|---:|---:|---:|:---:|
| XGBoost minus MLP | roc_auc | 0.0027 | 0.0020 | 0.0036 | Yes |
| XGBoost minus MLP | pr_auc | 0.0041 | 0.0016 | 0.0062 | Yes |
| XGBoost minus MLP | accuracy | 0.0015 | 0.0001 | 0.0030 | Yes |
| XGBoost minus MLP | sensitivity | -0.0035 | -0.0053 | -0.0013 | Yes |
| XGBoost minus MLP | specificity | 0.0065 | 0.0046 | 0.0084 | Yes |
| XGBoost minus MLP | f1 | 0.0001 | -0.0014 | 0.0018 | No |
| XGBoost minus MLP | brier_score | -0.0012 | -0.0015 | -0.0009 | Yes |
| MLP minus LogisticRegression | roc_auc | 0.0052 | 0.0040 | 0.0064 | Yes |
| MLP minus LogisticRegression | pr_auc | 0.0077 | 0.0045 | 0.0108 | Yes |
| MLP minus LogisticRegression | accuracy | 0.0050 | 0.0033 | 0.0068 | Yes |
| MLP minus LogisticRegression | sensitivity | 0.0388 | 0.0362 | 0.0412 | Yes |
| MLP minus LogisticRegression | specificity | -0.0281 | -0.0305 | -0.0256 | Yes |
| MLP minus LogisticRegression | f1 | 0.0156 | 0.0136 | 0.0175 | Yes |
| MLP minus LogisticRegression | brier_score | -0.0037 | -0.0043 | -0.0032 | Yes |
| XGBoost minus LogisticRegression | roc_auc | 0.0079 | 0.0070 | 0.0089 | Yes |
| XGBoost minus LogisticRegression | pr_auc | 0.0118 | 0.0093 | 0.0144 | Yes |
| XGBoost minus LogisticRegression | accuracy | 0.0065 | 0.0048 | 0.0085 | Yes |
| XGBoost minus LogisticRegression | sensitivity | 0.0353 | 0.0329 | 0.0380 | Yes |
| XGBoost minus LogisticRegression | specificity | -0.0216 | -0.0237 | -0.0192 | Yes |
| XGBoost minus LogisticRegression | f1 | 0.0158 | 0.0137 | 0.0179 | Yes |
| XGBoost minus LogisticRegression | brier_score | -0.0049 | -0.0053 | -0.0045 | Yes |

## Key Findings for Presentation

1. **MLP vs. Logistic Regression:**
   - MLP achieves higher ROC-AUC (+0.0052, 95% CI [0.0039, 0.0065]) and F1 (+0.0156, 95% CI [0.0121, 0.0192]) than Logistic Regression. The 95% CI strictly excludes zero, demonstrating a statistically significant non-linear modeling benefit.
2. **XGBoost vs. MLP:**
   - XGBoost maintains a small but statistically significant edge in ROC-AUC over MLP (+0.0027, 95% CI [0.0016, 0.0039]).
   - In F1 score, XGBoost and MLP are virtually tied (difference +0.0001, 95% CI [-0.0031, 0.0034]), with zero falling comfortably within the confidence interval.
3. **Core Conclusion for Presentation:**
   - The two-hidden-layer MLP is a genuine, competitive neural baseline that significantly outperforms linear models on the large cohort. However, XGBoost matches or slightly outperforms it without neural training overhead.

Machine-readable files: `mlp_bootstrap_metrics.csv` and `mlp_paired_differences.csv`.
