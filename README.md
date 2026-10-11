# Explainable Cardiovascular Disease Prediction

Research implementation for a data-centric, explainable cardiovascular disease
prediction pipeline, grounded in the supplied HPEM foundation paper and the
available clinical datasets.

## Current research scope

The supplied data support two **separate tabular cohorts**:

- `CVD_Cardio70k_Cleaned.csv`: 68,581 records, 14 candidate predictors, and a
  binary target. It has no missing cells and is the primary large-cohort track.
- `CVD_Unified_Clinical_Dataset.csv`: 1,918 records from five sources in four
  countries, with substantial and source-dependent missingness. It is a
  separate heterogeneous-cohort track.

These files do not provide patient-level links to one another or to medical
images. Their feature schemas and target populations also differ, so do not
concatenate them or describe the current work as multimodal. The
`CVD_Unified_Clinical_Dataset_ML_Ready.csv` file is useful for auditing, but its
imputation was performed before the train/test split; use the raw unified CSV
and fit preprocessing only on training folds for evaluation.

## Research roadmap

1. Audit data provenance, target definitions, missingness, duplicates, ranges,
   and cohort-specific label distributions. Run `scripts/audit_datasets.py` and
   `scripts/analyze_data_quality.py`.
2. Freeze a prediction protocol for each cohort. Treat these labels as
   contemporaneous disease classification, not future-risk prediction.
3. Build leakage-safe preprocessing and patient-level train/validation/test
   splits. For the unified cohort, reserve source-held-out evaluation where
   sample size and feature availability permit it.
4. Establish simple and strong tabular baselines. The Logistic Regression,
   Random Forest, HistGradientBoosting, and XGBoost benchmarks use a stratified
   patient holdout for Cardio70k and leave-one-source-out evaluation for the
   unified cohort. Run `scripts/run_baselines.py`.
   Run `scripts/run_cross_validation.py` for the more stable 5-fold internal
   Cardio70k estimate before further model selection.
5. Compare a regularized MLP with conventional baselines under the same
   validation splits. Treat this scikit-learn MLP as an initial neural baseline,
   then benchmark the foundation-paper HPEM and other deep tabular models if
   justified. Select models based on discrimination, sensitivity/specificity,
   calibration, and uncertainty, not accuracy alone.
   The Cardio70k baseline also includes a same-split ablation without its
   deterministic BMI, pulse-pressure, and BP-category features.
6. Add SHAP/LIME analysis, subgroup and error analysis, and ablations of
   preprocessing and feature engineering.
7. Consider external validation or image fusion only after obtaining
   compatible labels, schemas, and legitimate patient-level links. Treat the
   contribution as a hypothesis until experiments establish it.

The foundation paper's HPEM uses Random Forest, Gradient Boosting, and SVM,
polynomial feature expansion, mutual-information selection, and an XGBoost
meta-learner, with SHAP/LIME explanations. It also identifies limited
real-world population diversity as a limitation and proposes deep learning and
medical imaging as future work. This project will test those directions rather
than assume a new architecture is automatically novel.

## Setup and first run

Python 3.10+ is recommended.

```powershell
python -m pip install -r requirements.txt
python scripts/audit_datasets.py `
  --cardio70k "D:\Downloads\CVD_Cardio70k_Cleaned.csv" `
  --unified-raw "D:\Downloads\CVD_Unified_Clinical_Dataset.csv" `
  --unified-ml-ready "D:\Downloads\CVD_Unified_Clinical_Dataset_ML_Ready.csv"
```

The report is written to `reports/dataset_audit.md` by default. No dataset is
copied into the repository; pass paths to the files on your machine.

Generate the data-quality and initial EDA report:

```powershell
python scripts/analyze_data_quality.py `
   --cardio70k "D:\Downloads\CVD_Cardio70k_Cleaned.csv" `
   --unified-raw "D:\Downloads\CVD_Unified_Clinical_Dataset.csv"
```

The report is written to `reports/data_quality.md`.

Run the initial baseline experiments after the audit:

```powershell
python -m pip install -r requirements.txt
python scripts/run_baselines.py `
   --cardio70k "D:\Downloads\CVD_Cardio70k_Cleaned.csv" `
   --unified-raw "D:\Downloads\CVD_Unified_Clinical_Dataset.csv"
```

This writes `reports/baseline_results.md` and `reports/baseline_metrics.csv`.

Run stratified 5-fold cross-validation on Cardio70k:

```powershell
python scripts/run_cross_validation.py `
   --cardio70k "D:\Downloads\CVD_Cardio70k_Cleaned.csv"
```

This writes fold-level metrics, pooled out-of-fold metrics, and
`reports/cross_validation_results.md`.

## Data and clinical-use note

Keep original source citations and licensing with any publication. These
public research datasets are for research/education, not clinical diagnosis or
care. The related paper named in the conversation was not present among the
local files at project start, so its claims have not yet been incorporated.
