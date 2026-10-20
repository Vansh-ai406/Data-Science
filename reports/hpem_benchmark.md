# HPEM Reproduction Benchmark

## Paper-grounded method

This is a tabular HPEM reproduction on the raw unified clinical cohort using leave-one-source-out evaluation. It implements second-degree polynomial expansion, mutual-information selection of the top 15 transformed features, Random Forest + Gradient Boosting + RBF-SVM soft voting, and an XGBoost meta-learner trained on the three base learners' probabilities. All preprocessing and feature selection are fitted within training partitions.

The paper pseudocode trains the XGBoost meta-learner on base-ensemble predictions made on the same training records. To avoid stacking leakage, this implementation instead trains the meta-learner on 3-fold out-of-fold probabilities from each of the three base learners within the outer training sources. This is a leakage-safe methodological adaptation and is not an exact reproduction of the pseudocode's meta-training step. The paper's stated 5-fold CV on pooled datasets also differs from this source-held-out stress test.

A direct XGBoost baseline and soft-voting-only model are evaluated on the identical held-out sources. Metrics use a 0.5 threshold for thresholded classification measures; mean and SD are across five source holdouts, not confidence intervals.

## Summary across held-out sources

| model                     | n_sources | n_total | accuracy_mean | accuracy_sd_across_sources | f1_mean | f1_sd_across_sources | roc_auc_mean | roc_auc_sd_across_sources | pr_auc_mean | brier_score_mean | log_loss_mean |
| ------------------------- | --------- | ------- | ------------- | -------------------------- | ------- | -------------------- | ------------ | ------------------------- | ----------- | ---------------- | ------------- |
| HPEM (OOF soft-vote meta) | 5         | 1918    | 0.6131        | 0.0749                     | 0.6291  | 0.1434               | 0.6107       | 0.0735                    | 0.6768      | 0.2568           | 0.7501        |
| Soft-voting base ensemble | 5         | 1918    | 0.6070        | 0.0552                     | 0.6404  | 0.1123               | 0.6132       | 0.0847                    | 0.6792      | 0.2491           | 0.7029        |
| XGBoost baseline          | 5         | 1918    | 0.7108        | 0.1132                     | 0.7490  | 0.1036               | 0.7018       | 0.1430                    | 0.7773      | 0.2050           | 0.6267        |

## Source-specific performance

| held_out_source | model                     | n_test | accuracy | sensitivity | specificity | f1     | roc_auc | pr_auc | brier_score |
| --------------- | ------------------------- | ------ | -------- | ----------- | ----------- | ------ | ------- | ------ | ----------- |
| Mendeley_India  | HPEM (OOF soft-vote meta) | 1000   | 0.5240   | 0.6138      | 0.4000      | 0.5993 | 0.4824  | 0.5617 | 0.2871      |
| Mendeley_India  | Soft-voting base ensemble | 1000   | 0.5230   | 0.5983      | 0.4190      | 0.5927 | 0.4686  | 0.5369 | 0.2993      |
| Mendeley_India  | XGBoost baseline          | 1000   | 0.5090   | 0.6397      | 0.3286      | 0.6018 | 0.4937  | 0.5703 | 0.3244      |
| UCI_Cleveland   | HPEM (OOF soft-vote meta) | 303    | 0.5941   | 0.5540      | 0.6280      | 0.5560 | 0.6551  | 0.6212 | 0.2381      |
| UCI_Cleveland   | Soft-voting base ensemble | 303    | 0.6271   | 0.6763      | 0.5854      | 0.6246 | 0.6758  | 0.6486 | 0.2319      |
| UCI_Cleveland   | XGBoost baseline          | 303    | 0.7525   | 0.8058      | 0.7073      | 0.7492 | 0.8358  | 0.8203 | 0.1722      |
| UCI_Hungary     | HPEM (OOF soft-vote meta) | 293    | 0.6075   | 0.4623      | 0.6898      | 0.4601 | 0.6158  | 0.4548 | 0.2706      |
| UCI_Hungary     | Soft-voting base ensemble | 293    | 0.5973   | 0.5472      | 0.6257      | 0.4957 | 0.6126  | 0.4558 | 0.2570      |
| UCI_Hungary     | XGBoost baseline          | 293    | 0.7747   | 0.7358      | 0.7968      | 0.7027 | 0.8370  | 0.7407 | 0.1601      |
| UCI_LongBeachVA | HPEM (OOF soft-vote meta) | 199    | 0.6080   | 0.5946      | 0.6471      | 0.6929 | 0.6548  | 0.8079 | 0.2831      |
| UCI_LongBeachVA | Soft-voting base ensemble | 199    | 0.6131   | 0.5878      | 0.6863      | 0.6932 | 0.6690  | 0.8143 | 0.2512      |
| UCI_LongBeachVA | XGBoost baseline          | 199    | 0.7538   | 0.8176      | 0.5686      | 0.8316 | 0.6848  | 0.8175 | 0.1937      |
| UCI_Switzerland | HPEM (OOF soft-vote meta) | 123    | 0.7317   | 0.7391      | 0.6250      | 0.8374 | 0.6457  | 0.9384 | 0.2050      |
| UCI_Switzerland | Soft-voting base ensemble | 123    | 0.6748   | 0.6783      | 0.6250      | 0.7959 | 0.6402  | 0.9405 | 0.2061      |
| UCI_Switzerland | XGBoost baseline          | 123    | 0.7642   | 0.7739      | 0.6250      | 0.8599 | 0.6576  | 0.9378 | 0.1748      |

![HPEM source-held-out comparison](plots/hpem_source_comparison.png)

## Interpretation

This dataset-specific reproduction cannot confirm the paper's reported performance because its cohort composition, target harmonization, and validation design differ. The unified cohort has only five source groups and marked distribution shift; do not interpret source-level estimates as stable clinical performance. The best model should be selected by the intended use and paired uncertainty analysis, not one pooled ranking.

Machine-readable source results: `hpem_source_metrics.csv`. Summary: `hpem_summary.csv`. Held-out prediction rows are retained in `hpem_heldout_predictions.csv`.
