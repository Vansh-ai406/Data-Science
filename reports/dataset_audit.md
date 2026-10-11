# Initial Dataset Audit

## Cardio70k cleaned cohort

- File: `D:\Downloads\CVD_Cardio70k_Cleaned.csv`
- Shape: 68,581 rows x 16 columns
- Exact duplicate rows: 0
- Duplicate patient IDs: 0
- Rows identical across predictors/label except ID (review; not automatically duplicates): 650

### Target distribution

| Target | Rows | Percent |
|---:|---:|---:|
| 0 | 34,652 | 50.53% |
| 1 | 33,929 | 49.47% |

### Columns and missingness

| Column | Type | Missing | Missing % |
|---|---|---:|---:|
| patient_id | object | 0 | 0.00% |
| age_years | float64 | 0 | 0.00% |
| sex | int64 | 0 | 0.00% |
| height_cm | int64 | 0 | 0.00% |
| weight_kg | float64 | 0 | 0.00% |
| bmi | float64 | 0 | 0.00% |
| systolic_bp | int64 | 0 | 0.00% |
| diastolic_bp | int64 | 0 | 0.00% |
| pulse_pressure | int64 | 0 | 0.00% |
| bp_category | int64 | 0 | 0.00% |
| cholesterol_level | int64 | 0 | 0.00% |
| glucose_level | int64 | 0 | 0.00% |
| smoking | int64 | 0 | 0.00% |
| alcohol | int64 | 0 | 0.00% |
| physically_active | int64 | 0 | 0.00% |
| target | int64 | 0 | 0.00% |

## Unified clinical cohort (raw)

- File: `D:\Downloads\CVD_Unified_Clinical_Dataset.csv`
- Shape: 1,918 rows x 18 columns
- Exact duplicate rows: 0
- Duplicate patient IDs: 0
- Rows identical across predictors/label except ID (review; not automatically duplicates): 0

### Target distribution

| Target | Rows | Percent |
|---:|---:|---:|
| 0 | 830 | 43.27% |
| 1 | 1,088 | 56.73% |

### Columns and missingness

| Column | Type | Missing | Missing % |
|---|---|---:|---:|
| patient_id | object | 0 | 0.00% |
| source | object | 0 | 0.00% |
| country | object | 0 | 0.00% |
| age | int64 | 0 | 0.00% |
| sex | int64 | 0 | 0.00% |
| chest_pain_type | int64 | 0 | 0.00% |
| resting_bp | float64 | 60 | 3.13% |
| cholesterol | float64 | 254 | 13.24% |
| fasting_blood_sugar | float64 | 90 | 4.69% |
| resting_ecg | float64 | 2 | 0.10% |
| max_heart_rate | float64 | 55 | 2.87% |
| exercise_angina | float64 | 55 | 2.87% |
| oldpeak | float64 | 62 | 3.23% |
| st_slope | float64 | 487 | 25.39% |
| num_major_vessels | float64 | 609 | 31.75% |
| thalassemia | float64 | 1,484 | 77.37% |
| disease_severity | float64 | 1,000 | 52.14% |
| target | int64 | 0 | 0.00% |

### Target by source

```text
target             0     1   All
source
Mendeley_India   420   580  1000
UCI_Cleveland    164   139   303
UCI_Hungary      187   106   293
UCI_LongBeachVA   51   148   199
UCI_Switzerland    8   115   123
All              830  1088  1918
```

> Exclude `disease_severity` from predictors: the data dictionary states that it directly defines `target` for UCI records.

## Unified clinical cohort (ML-ready; audit only)

- File: `D:\Downloads\CVD_Unified_Clinical_Dataset_ML_Ready.csv`
- Shape: 1,918 rows x 27 columns
- Exact duplicate rows: 0
- Duplicate patient IDs: 0
- Rows identical across predictors/label except ID (review; not automatically duplicates): 0

### Target distribution

| Target | Rows | Percent |
|---:|---:|---:|
| 0 | 830 | 43.27% |
| 1 | 1,088 | 56.73% |

### Columns and missingness

| Column | Type | Missing | Missing % |
|---|---|---:|---:|
| patient_id | object | 0 | 0.00% |
| source | object | 0 | 0.00% |
| country | object | 0 | 0.00% |
| age | int64 | 0 | 0.00% |
| sex | int64 | 0 | 0.00% |
| chest_pain_type | int64 | 0 | 0.00% |
| resting_bp | int64 | 0 | 0.00% |
| cholesterol | int64 | 0 | 0.00% |
| fasting_blood_sugar | int64 | 0 | 0.00% |
| resting_ecg | int64 | 0 | 0.00% |
| max_heart_rate | int64 | 0 | 0.00% |
| exercise_angina | int64 | 0 | 0.00% |
| oldpeak | float64 | 0 | 0.00% |
| st_slope | int64 | 0 | 0.00% |
| num_major_vessels | int64 | 0 | 0.00% |
| thalassemia | int64 | 0 | 0.00% |
| target | int64 | 0 | 0.00% |
| resting_bp_missing | int64 | 0 | 0.00% |
| cholesterol_missing | int64 | 0 | 0.00% |
| max_heart_rate_missing | int64 | 0 | 0.00% |
| oldpeak_missing | int64 | 0 | 0.00% |
| fasting_blood_sugar_missing | int64 | 0 | 0.00% |
| resting_ecg_missing | int64 | 0 | 0.00% |
| exercise_angina_missing | int64 | 0 | 0.00% |
| st_slope_missing | int64 | 0 | 0.00% |
| num_major_vessels_missing | int64 | 0 | 0.00% |
| thalassemia_missing | int64 | 0 | 0.00% |

### Target by source

```text
target             0     1   All
source
Mendeley_India   420   580  1000
UCI_Cleveland    164   139   303
UCI_Hungary      187   106   293
UCI_LongBeachVA   51   148   199
UCI_Switzerland    8   115   123
All              830  1088  1918
```

## Raw vs. ML-ready unified export

- Same row count: True
- Same patient ID set: True
- Shared columns with changed values (including imputations): `{'resting_bp': 60, 'cholesterol': 254, 'fasting_blood_sugar': 90, 'resting_ecg': 2, 'max_heart_rate': 55, 'exercise_angina': 55, 'oldpeak': 62, 'st_slope': 487, 'num_major_vessels': 609, 'thalassemia': 1484}`

> Use the raw CSV for model development. The data dictionary says the ML-ready export uses whole-file median/mode imputation; refit all preprocessing inside each training fold to avoid leakage.

## Initial analysis decisions

- Keep Cardio70k and the unified clinical cohort as separate analyses; there is no patient linkage and their predictor schemas differ.
- Treat `target` as contemporaneous disease classification, not future risk, unless source documentation establishes otherwise.
- Do not use identifiers as predictors. Keep cohort/source metadata for grouped evaluation, not as model inputs in cross-source tests.
- No linked image files were supplied with these CSVs; image fusion is out of scope until compatible paired data are available.
- Identical predictor/label profiles with different IDs are flagged for review; do not remove them without evidence that they are duplicate patients.
