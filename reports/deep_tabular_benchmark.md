# Deep Tabular Benchmark

This stage benchmarks deeper tabular neural baselines against the strongest classical models while keeping the same train-only preprocessing and external-source evaluation protocol.

## Best Cardio70k model

- Best model: **XGBoost** | ROC-AUC **0.8016** | F1 **0.7202** | Accuracy **0.7353** | Precision **0.7550**

## Cardio70k summary

| model | accuracy_mean | precision_mean | f1_mean | roc_auc_mean | brier_score_mean |
| --- | --- | --- | --- | --- | --- |
| XGBoost | 0.7353 | 0.7550 | 0.7202 | 0.8016 | 0.1803 |
| MLP_Deep | 0.7330 | 0.7390 | 0.7252 | 0.8001 | 0.1814 |
| LogisticRegression | 0.7292 | 0.7651 | 0.7046 | 0.7938 | 0.1852 |

## Unified source-generalization summary

| model | accuracy_mean | precision_mean | f1_mean | roc_auc_mean | brier_score_mean |
| --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.6979 | 0.7547 | 0.7525 | 0.7449 | 0.2084 |
| MLP_Deep | 0.7019 | 0.7657 | 0.7570 | 0.7431 | 0.2088 |
| XGBoost | 0.6977 | 0.7486 | 0.7430 | 0.6989 | 0.2071 |

## Interpretation

The deep tabular benchmark should be read as a model-capability comparison under the same leakage-safe design. On the large Cardio70k cohort, the deep MLPs are expected to be competitive but not automatically better than tree ensembles; on the heterogeneous unified cohort, the generalization picture remains source-dependent and should be interpreted per cohort rather than pooled across sources.

This is the correct next research step after the baseline and nested selection stage. It preserves the original research workflow and provides the evidence needed before making stronger generalization claims.
