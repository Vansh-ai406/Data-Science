# Initial Baseline Results

Exploratory, fixed-configuration baselines. These results are not clinical claims and are not external validation.

## Cardio70k

A stratified 80/20 patient-level holdout with seed 42. Preprocessing is fitted inside each model pipeline using training data only. The file has 68,581 unique patient IDs. There are 264 identical predictor profiles appearing in both partitions; they are reported, not dropped, because IDs are distinct and identical profiles can represent different patients.

### All candidate predictors

| model | n_train | n_test | accuracy | precision | sensitivity | specificity | f1 | roc_auc | pr_auc | brier_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 54864 | 13717 | 0.728 | 0.759 | 0.658 | 0.796 | 0.705 | 0.792 | 0.775 | 0.185 |
| MLP | 54864 | 13717 | 0.732 | 0.747 | 0.694 | 0.770 | 0.719 | 0.798 | 0.782 | 0.182 |
| RandomForest | 54864 | 13717 | 0.725 | 0.733 | 0.697 | 0.752 | 0.715 | 0.787 | 0.771 | 0.188 |
| HistGradientBoosting | 54864 | 13717 | 0.729 | 0.742 | 0.695 | 0.763 | 0.718 | 0.799 | 0.784 | 0.182 |
| XGBoost | 54864 | 13717 | 0.732 | 0.748 | 0.691 | 0.772 | 0.719 | 0.799 | 0.784 | 0.182 |

### Excluding deterministic derived features

Same patient split and model settings as above; excludes stored BMI, pulse pressure, and BP category while retaining their underlying height, weight, systolic BP, and diastolic BP inputs.

| model | n_train | n_test | accuracy | precision | sensitivity | specificity | f1 | roc_auc | pr_auc | brier_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 54864 | 13717 | 0.727 | 0.752 | 0.670 | 0.783 | 0.709 | 0.790 | 0.776 | 0.187 |
| MLP | 54864 | 13717 | 0.729 | 0.748 | 0.682 | 0.775 | 0.713 | 0.798 | 0.780 | 0.182 |
| RandomForest | 54864 | 13717 | 0.724 | 0.733 | 0.696 | 0.752 | 0.714 | 0.787 | 0.771 | 0.188 |
| HistGradientBoosting | 54864 | 13717 | 0.730 | 0.743 | 0.693 | 0.766 | 0.717 | 0.799 | 0.784 | 0.182 |
| XGBoost | 54864 | 13717 | 0.733 | 0.747 | 0.694 | 0.770 | 0.720 | 0.799 | 0.785 | 0.182 |

## Unified clinical cohort

Leave one source out at a time. The held-out source is never used to fit imputation, encoding, scaling, or model parameters. `disease_severity`, IDs, country, and source are not predictors. Interpret per-source results in light of small and strongly different cohorts; this is internal cross-source evaluation, not independent external validation.

| cohort | evaluation | feature_set | source | model | n_train | n_test | accuracy | precision | sensitivity | specificity | f1 | roc_auc | pr_auc | brier_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unified clinical | leave-one-source-out | Original clinical predictors | Mendeley_India | LogisticRegression | 918 | 1000 | 0.586 | 0.606 | 0.819 | 0.264 | 0.696 | 0.629 | 0.704 | 0.277 |
| Unified clinical | leave-one-source-out | Original clinical predictors | Mendeley_India | MLP | 918 | 1000 | 0.597 | 0.602 | 0.903 | 0.174 | 0.722 | 0.611 | 0.695 | 0.292 |
| Unified clinical | leave-one-source-out | Original clinical predictors | Mendeley_India | RandomForest | 918 | 1000 | 0.522 | 0.585 | 0.605 | 0.407 | 0.595 | 0.522 | 0.605 | 0.263 |
| Unified clinical | leave-one-source-out | Original clinical predictors | Mendeley_India | HistGradientBoosting | 918 | 1000 | 0.533 | 0.588 | 0.648 | 0.374 | 0.617 | 0.518 | 0.596 | 0.332 |
| Unified clinical | leave-one-source-out | Original clinical predictors | Mendeley_India | XGBoost | 918 | 1000 | 0.509 | 0.568 | 0.640 | 0.329 | 0.602 | 0.494 | 0.570 | 0.324 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Cleveland | LogisticRegression | 1615 | 303 | 0.749 | 0.696 | 0.806 | 0.701 | 0.747 | 0.849 | 0.841 | 0.169 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Cleveland | MLP | 1615 | 303 | 0.776 | 0.748 | 0.770 | 0.780 | 0.759 | 0.865 | 0.860 | 0.151 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Cleveland | RandomForest | 1615 | 303 | 0.696 | 0.624 | 0.849 | 0.567 | 0.720 | 0.818 | 0.821 | 0.193 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Cleveland | HistGradientBoosting | 1615 | 303 | 0.726 | 0.675 | 0.777 | 0.683 | 0.722 | 0.808 | 0.793 | 0.196 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Cleveland | XGBoost | 1615 | 303 | 0.752 | 0.700 | 0.806 | 0.707 | 0.749 | 0.836 | 0.820 | 0.172 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Hungary | LogisticRegression | 1625 | 293 | 0.795 | 0.677 | 0.830 | 0.775 | 0.746 | 0.855 | 0.773 | 0.159 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Hungary | MLP | 1625 | 293 | 0.792 | 0.677 | 0.811 | 0.781 | 0.738 | 0.851 | 0.766 | 0.158 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Hungary | RandomForest | 1625 | 293 | 0.782 | 0.659 | 0.821 | 0.759 | 0.731 | 0.845 | 0.751 | 0.166 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Hungary | HistGradientBoosting | 1625 | 293 | 0.751 | 0.632 | 0.745 | 0.754 | 0.684 | 0.814 | 0.713 | 0.185 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Hungary | XGBoost | 1625 | 293 | 0.775 | 0.672 | 0.736 | 0.797 | 0.703 | 0.837 | 0.741 | 0.160 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_LongBeachVA | LogisticRegression | 1719 | 199 | 0.709 | 0.821 | 0.777 | 0.510 | 0.799 | 0.712 | 0.849 | 0.193 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_LongBeachVA | MLP | 1719 | 199 | 0.729 | 0.826 | 0.804 | 0.510 | 0.815 | 0.709 | 0.854 | 0.193 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_LongBeachVA | RandomForest | 1719 | 199 | 0.734 | 0.832 | 0.804 | 0.529 | 0.818 | 0.711 | 0.839 | 0.181 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_LongBeachVA | HistGradientBoosting | 1719 | 199 | 0.724 | 0.821 | 0.804 | 0.490 | 0.812 | 0.648 | 0.813 | 0.211 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_LongBeachVA | XGBoost | 1719 | 199 | 0.754 | 0.846 | 0.818 | 0.569 | 0.832 | 0.685 | 0.817 | 0.194 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Switzerland | LogisticRegression | 1795 | 123 | 0.650 | 0.974 | 0.643 | 0.750 | 0.775 | 0.679 | 0.949 | 0.244 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Switzerland | MLP | 1795 | 123 | 0.602 | 0.971 | 0.591 | 0.750 | 0.735 | 0.679 | 0.951 | 0.251 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Switzerland | RandomForest | 1795 | 123 | 0.691 | 0.964 | 0.696 | 0.625 | 0.808 | 0.673 | 0.938 | 0.205 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Switzerland | HistGradientBoosting | 1795 | 123 | 0.740 | 0.956 | 0.757 | 0.500 | 0.845 | 0.638 | 0.942 | 0.179 |
| Unified clinical | leave-one-source-out | Original clinical predictors | UCI_Switzerland | XGBoost | 1795 | 123 | 0.764 | 0.967 | 0.774 | 0.625 | 0.860 | 0.658 | 0.938 | 0.175 |

## Metrics and limits

Metrics use a fixed probability threshold of 0.5 for threshold-dependent scores; ROC-AUC and PR-AUC use probabilities. Brier score measures probability error (lower is better). No hyperparameter tuning was done, and no confidence intervals are included yet. Because multiple fixed models and feature sets were compared on this same holdout, it is exploratory and is not an untouched final test set. Before model selection or final performance claims, use nested/repeated validation or reserve a fresh final test set. Then assess calibration, uncertainty, and explainability.

Machine-readable metrics: `reports/baseline_metrics.csv`.
