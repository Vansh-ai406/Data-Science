# Data Quality and Initial EDA

This is a profiling report, not a cleaning recipe. Values are retained; statistical flags are not assumed to be errors.

## Integrity checks

- Cardio70k rows identical across predictors and target, excluding ID: 650; they form 858 repeated profiles, of which 374 have conflicting targets. They are not confirmed duplicate patients.
- Cardio70k BMI formula maximum absolute difference: 0.050 kg/m^2; the stored BMI is rounded to one decimal place.
- Cardio70k pulse-pressure formula mismatches: 0.
- Unified target vs. documented severity (`disease_severity >= 1`) mismatches among rows with known severity: 0 of 918.
- IDs, source metadata, and `disease_severity` are not model predictors; severity directly defines the outcome for the applicable UCI rows.

## Documented range checks

Numeric ranges come from the supplied legend and may describe observed dataset ranges rather than physiological validity limits; they are screening references, not grounds for deleting records. Categorical checks verify documented code sets.

| dataset | feature | check | expected | outside | missing |
| --- | --- | --- | --- | --- | --- |
| Cardio70k | age_years | legend range (screen only) | 29.6 to 64.9 | 0 | 0 |
| Cardio70k | height_cm | legend range (screen only) | 120 to 220 | 0 | 0 |
| Cardio70k | weight_kg | legend range (screen only) | 30 to 200 | 0 | 0 |
| Cardio70k | bmi | legend range (screen only) | 12 to 70 | 0 | 0 |
| Cardio70k | systolic_bp | legend range (screen only) | 70 to 250 | 0 | 0 |
| Cardio70k | diastolic_bp | legend range (screen only) | 40 to 150 | 0 | 0 |
| Cardio70k | pulse_pressure | legend range (screen only) | 5 to 140 | 0 | 0 |
| Cardio70k | sex | allowed codes | 0, 1 | 0 | 0 |
| Cardio70k | bp_category | allowed codes | 0, 1, 2, 3, 4 | 0 | 0 |
| Cardio70k | cholesterol_level | allowed codes | 1, 2, 3 | 0 | 0 |
| Cardio70k | glucose_level | allowed codes | 1, 2, 3 | 0 | 0 |
| Cardio70k | smoking | allowed codes | 0, 1 | 0 | 0 |
| Cardio70k | alcohol | allowed codes | 0, 1 | 0 | 0 |
| Cardio70k | physically_active | allowed codes | 0, 1 | 0 | 0 |
| Cardio70k | target | allowed codes | 0, 1 | 0 | 0 |
| Unified | age | legend range (screen only) | 20 to 80 | 0 | 0 |
| Unified | resting_bp | legend range (screen only) | 80 to 200 | 0 | 60 |
| Unified | cholesterol | legend range (screen only) | 85 to 603 | 0 | 254 |
| Unified | max_heart_rate | legend range (screen only) | 60 to 202 | 0 | 55 |
| Unified | oldpeak | legend range (screen only) | -2.6 to 6.2 | 0 | 62 |
| Unified | sex | allowed codes | 0, 1 | 0 | 0 |
| Unified | chest_pain_type | allowed codes | 0, 1, 2, 3 | 0 | 0 |
| Unified | fasting_blood_sugar | allowed codes | 0, 1 | 0 | 90 |
| Unified | resting_ecg | allowed codes | 0, 1, 2 | 0 | 2 |
| Unified | exercise_angina | allowed codes | 0, 1 | 0 | 55 |
| Unified | st_slope | allowed codes | 0, 1, 2 | 0 | 487 |
| Unified | num_major_vessels | allowed codes | 0, 1, 2, 3 | 0 | 609 |
| Unified | thalassemia | allowed codes | 0, 1, 2 | 0 | 1484 |
| Unified | disease_severity | allowed codes | 0, 1, 2, 3, 4 | 0 | 1000 |
| Unified | target | allowed codes | 0, 1 | 0 | 0 |

## IQR outlier flags

Flags use the 1.5 x IQR rule. They are prompts for review, not removal criteria; unified-cohort flags are computed separately within each source.

| dataset | source/group | feature | n | IQR flags | flagged % |
| --- | --- | --- | --- | --- | --- |
| Cardio70k | All records | age_years | 68581 | 4 | 0.01% |
| Cardio70k | All records | height_cm | 68581 | 451 | 0.66% |
| Cardio70k | All records | weight_kg | 68581 | 1727 | 2.52% |
| Cardio70k | All records | bmi | 68581 | 1982 | 2.89% |
| Cardio70k | All records | systolic_bp | 68581 | 1002 | 1.46% |
| Cardio70k | All records | diastolic_bp | 68581 | 3493 | 5.09% |
| Cardio70k | All records | pulse_pressure | 68581 | 5170 | 7.54% |
| Unified | Mendeley_India | age | 1000 | 0 | 0.00% |
| Unified | Mendeley_India | resting_bp | 1000 | 0 | 0.00% |
| Unified | Mendeley_India | cholesterol | 947 | 0 | 0.00% |
| Unified | Mendeley_India | max_heart_rate | 1000 | 0 | 0.00% |
| Unified | Mendeley_India | oldpeak | 1000 | 0 | 0.00% |
| Unified | UCI_Cleveland | age | 303 | 0 | 0.00% |
| Unified | UCI_Cleveland | resting_bp | 303 | 9 | 2.97% |
| Unified | UCI_Cleveland | cholesterol | 303 | 5 | 1.65% |
| Unified | UCI_Cleveland | max_heart_rate | 303 | 1 | 0.33% |
| Unified | UCI_Cleveland | oldpeak | 303 | 5 | 1.65% |
| Unified | UCI_Hungary | age | 293 | 0 | 0.00% |
| Unified | UCI_Hungary | resting_bp | 292 | 8 | 2.74% |
| Unified | UCI_Hungary | cholesterol | 271 | 11 | 4.06% |
| Unified | UCI_Hungary | max_heart_rate | 292 | 0 | 0.00% |
| Unified | UCI_Hungary | oldpeak | 293 | 11 | 3.75% |
| Unified | UCI_LongBeachVA | age | 199 | 7 | 3.52% |
| Unified | UCI_LongBeachVA | resting_bp | 142 | 1 | 0.70% |
| Unified | UCI_LongBeachVA | cholesterol | 143 | 5 | 3.50% |
| Unified | UCI_LongBeachVA | max_heart_rate | 146 | 0 | 0.00% |
| Unified | UCI_LongBeachVA | oldpeak | 143 | 0 | 0.00% |
| Unified | UCI_Switzerland | age | 123 | 3 | 2.44% |
| Unified | UCI_Switzerland | resting_bp | 121 | 2 | 1.65% |
| Unified | UCI_Switzerland | max_heart_rate | 122 | 0 | 0.00% |
| Unified | UCI_Switzerland | oldpeak | 117 | 1 | 0.85% |

## Unified cohort by source

Source-specific prevalence and observed medians/missingness show that the cohorts differ. This can contribute to transfer-performance changes; it does not by itself identify the cause.

| source | n | positive % | age median | age missing % | resting_bp median | resting_bp missing % | cholesterol median | cholesterol missing % | max_heart_rate median | max_heart_rate missing % | oldpeak median | oldpeak missing % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Mendeley_India | 1000 | 58.00% | 49.0 | 0.0% | 147.0 | 0.0% | 326.0 | 5.3% | 146.0 | 0.0% | 2.4 | 0.0% |
| UCI_Cleveland | 303 | 45.87% | 56.0 | 0.0% | 130.0 | 0.0% | 241.0 | 0.0% | 153.0 | 0.0% | 0.8 | 0.0% |
| UCI_Hungary | 293 | 36.18% | 49.0 | 0.0% | 130.0 | 0.3% | 243.0 | 7.5% | 140.0 | 0.3% | 0.0 | 0.0% |
| UCI_LongBeachVA | 199 | 74.37% | 60.0 | 0.0% | 130.0 | 28.6% | 228.0 | 28.1% | 120.0 | 26.6% | 1.5 | 28.1% |
| UCI_Switzerland | 123 | 93.50% | 56.0 | 0.0% | 125.0 | 1.6% | NA | 100.0% | 121.0 | 0.8% | 0.3 | 4.9% |

## Cardio70k by target

Numeric summaries report medians and IQRs. Categorical rows report within-level positive prevalence. These are descriptive associations, not causal effects.

| feature | target | n | median | IQR |
| --- | --- | --- | --- | --- |
| age_years | 0 | 34652 | 52.00 | 46.10 - 57.10 |
| age_years | 1 | 33929 | 55.80 | 50.30 - 60.00 |
| height_cm | 0 | 34652 | 165.00 | 159.00 - 170.00 |
| height_cm | 1 | 33929 | 165.00 | 159.00 - 170.00 |
| weight_kg | 0 | 34652 | 70.00 | 63.00 - 79.00 |
| weight_kg | 1 | 33929 | 75.00 | 66.00 - 85.00 |
| bmi | 0 | 34652 | 25.50 | 23.40 - 28.80 |
| bmi | 1 | 33929 | 27.40 | 24.50 - 31.50 |
| systolic_bp | 0 | 34652 | 120.00 | 110.00 - 120.00 |
| systolic_bp | 1 | 33929 | 130.00 | 120.00 - 140.00 |
| diastolic_bp | 0 | 34652 | 80.00 | 70.00 - 80.00 |
| diastolic_bp | 1 | 33929 | 80.00 | 80.00 - 90.00 |
| pulse_pressure | 0 | 34652 | 40.00 | 40.00 - 40.00 |
| pulse_pressure | 1 | 33929 | 50.00 | 40.00 - 60.00 |
| sex=0 | positive prevalence | 44665 | 49.21% |  |
| sex=1 | positive prevalence | 23916 | 49.96% |  |
| bp_category=0 | positive prevalence | 9541 | 22.13% |  |
| bp_category=1 | positive prevalence | 3107 | 32.31% |  |
| bp_category=2 | positive prevalence | 32415 | 38.47% |  |
| bp_category=3 | positive prevalence | 22546 | 77.63% |  |
| bp_category=4 | positive prevalence | 972 | 86.63% |  |
| cholesterol_level=1 | positive prevalence | 51423 | 43.54% |  |
| cholesterol_level=2 | positive prevalence | 9294 | 59.62% |  |
| cholesterol_level=3 | positive prevalence | 7864 | 76.26% |  |
| glucose_level=1 | positive prevalence | 58305 | 47.56% |  |
| glucose_level=2 | positive prevalence | 5063 | 58.84% |  |
| glucose_level=3 | positive prevalence | 5213 | 61.79% |  |
| smoking=0 | positive prevalence | 62545 | 49.73% |  |
| smoking=1 | positive prevalence | 6036 | 46.84% |  |
| alcohol=0 | positive prevalence | 64920 | 49.57% |  |
| alcohol=1 | positive prevalence | 3661 | 47.66% |  |
| physically_active=0 | positive prevalence | 13488 | 53.28% |  |
| physically_active=1 | positive prevalence | 55093 | 48.54% |  |

## Preprocessing implications

- Keep legitimate extreme measurements; investigate only documented range violations or source-specific coding anomalies.
- Preserve Cardio70k's distinct patient rows even when predictor profiles match; record profile overlap in evaluation reports.
- The unified cohort has strong source differences and non-random missingness. Fit imputers/encoders inside each training split and report source-held-out performance rather than relying only on pooled random splits.
- Cardio70k includes deterministic derived features (BMI, pulse pressure, BP category). Add a predeclared ablation without derived fields to test whether they add value beyond their source measurements.
- Cardio70k target prevalence is near 50/50; do not add SMOTE by default. For other cohorts, assess imbalance within each evaluation split before choosing class weights or resampling.
