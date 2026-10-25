# Deep Tabular Benchmark

This stage benchmarks deeper tabular neural baselines against the strongest classical models using training-fold-only preprocessing. Cardio70k results use stratified 5-fold CV; unified results average leave-one-source-out evaluations over five sources. The separate primary CV report uses different fixed model settings, so these are related internal comparisons, not independent replications.

## Best Cardio70k model

- Best model: **XGBoost** | ROC-AUC **0.8017** | F1 **0.7197** | Accuracy **0.7350** | Precision **0.7550**

## Cardio70k summary

| model | accuracy_mean | precision_mean | f1_mean | roc_auc_mean | brier_score_mean |
| --- | --- | --- | --- | --- | --- |
| XGBoost | 0.7350 | 0.7550 | 0.7197 | 0.8017 | 0.1803 |
| MLP_Deep | 0.7339 | 0.7544 | 0.7182 | 0.7998 | 0.1813 |
| LogisticRegression | 0.7292 | 0.7652 | 0.7047 | 0.7939 | 0.1851 |

## Unified source-generalization summary

| model | accuracy_mean | precision_mean | f1_mean | roc_auc_mean | brier_score_mean |
| --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.6979 | 0.7547 | 0.7525 | 0.7449 | 0.2084 |
| MLP_Deep | 0.7019 | 0.7657 | 0.7570 | 0.7431 | 0.2088 |
| XGBoost | 0.6977 | 0.7486 | 0.7430 | 0.6989 | 0.2071 |

## Interpretation

The deep tabular benchmark is a second five-fold model comparison with a different fixed MLP/XGBoost configuration from the primary CV suite. The MLP is competitive but does not beat XGBoost on Cardio70k ROC-AUC. On the heterogeneous unified cohort, source-held-out results vary substantially; reported means are descriptive across five source holdouts, not external validation.

The two-hidden-layer MLP is a neural baseline, not a novel architecture. It is competitive on Cardio70k but does not consistently lead across source-held-out evaluations. Source-level outcomes should remain visible rather than being collapsed into a clinical generalization claim.
