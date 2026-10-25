# Subgroup Metric Confidence Intervals

## Methodology

To ensure robust evaluation and prevent overinterpretation of small cohort slices, this report adds 95% confidence intervals to the subgroup error analysis:
- **Sensitivity, Specificity, and Precision:** Exact Wilson score interval (Wilson, 1927), which maintains nominal coverage even for asymmetric or small-cell strata.
- **ROC-AUC:** Hanley & McNeil (1982) standard error formulation for non-parametric area under the ROC curve.

## Subgroup Performance Table with 95% CIs

| Cohort | Group Type | Group | N | Sensitivity (95% CI) | Specificity (95% CI) | Precision (95% CI) | ROC-AUC (95% CI) | Status |
|:---|:---|:---|---:|:---:|:---:|:---:|:---:|:---|
| Cardio70k | Overall | All | 68,581 | 0.688 [0.683, 0.693] | 0.782 [0.778, 0.787] | 0.756 [0.751, 0.761] | 0.802 [0.799, 0.805] | Reviewable |
| Cardio70k | Sex | Female (code 0) | 44,665 | 0.690 [0.684, 0.696] | 0.781 [0.776, 0.787] | 0.754 [0.748, 0.759] | 0.804 [0.800, 0.808] | Reviewable |
| Cardio70k | Sex | Male (code 1) | 23,916 | 0.685 [0.677, 0.694] | 0.784 [0.776, 0.791] | 0.760 [0.752, 0.768] | 0.798 [0.793, 0.804] | Reviewable |
| Cardio70k | Age band | 45-59 | 45,680 | 0.636 [0.629, 0.642] | 0.809 [0.804, 0.814] | 0.763 [0.757, 0.769] | 0.781 [0.777, 0.786] | Reviewable |
| Cardio70k | Age band | 60+ | 12,812 | 0.871 [0.864, 0.878] | 0.368 [0.354, 0.383] | 0.734 [0.725, 0.743] | 0.723 [0.714, 0.732] | Reviewable |
| Cardio70k | Age band | <45 | 10,089 | 0.560 [0.542, 0.578] | 0.941 [0.935, 0.946] | 0.798 [0.780, 0.814] | 0.830 [0.820, 0.840] | Reviewable |
| Unified clinical | Overall | All | 1,918 | 0.709 [0.681, 0.735] | 0.527 [0.492, 0.560] | 0.662 [0.635, 0.689] | 0.667 [0.643, 0.691] | Reviewable |
| Unified clinical | Source | Mendeley_India | 1,000 | 0.640 [0.600, 0.678] | 0.329 [0.285, 0.375] | 0.568 [0.530, 0.606] | 0.494 [0.457, 0.530] | Reviewable |
| Unified clinical | Source | UCI_Cleveland | 303 | 0.806 [0.732, 0.863] | 0.707 [0.634, 0.772] | 0.700 [0.625, 0.766] | 0.836 [0.789, 0.883] | Reviewable |
| Unified clinical | Source | UCI_Hungary | 293 | 0.736 [0.645, 0.810] | 0.797 [0.733, 0.848] | 0.672 [0.583, 0.751] | 0.837 [0.786, 0.889] | Reviewable |
| Unified clinical | Source | UCI_LongBeachVA | 199 | 0.818 [0.748, 0.871] | 0.569 [0.433, 0.695] | 0.846 [0.778, 0.896] | 0.685 [0.606, 0.764] | Reviewable |
| Unified clinical | Source | UCI_Switzerland | 123 | 0.774 [0.689, 0.841] | 0.625 [0.306, 0.863] | 0.967 [0.908, 0.989] | 0.658 [0.482, 0.833] | Small cell: descriptive only |
| Unified clinical | Sex | Female (code 0) | 428 | 0.448 [0.378, 0.520] | 0.800 [0.745, 0.845] | 0.626 [0.541, 0.704] | 0.733 [0.685, 0.782] | Reviewable |
| Unified clinical | Sex | Male (code 1) | 1,490 | 0.761 [0.732, 0.788] | 0.412 [0.373, 0.452] | 0.667 [0.638, 0.695] | 0.624 [0.596, 0.653] | Reviewable |
| Unified clinical | Age band | 45-59 | 730 | 0.744 [0.700, 0.784] | 0.595 [0.540, 0.648] | 0.706 [0.662, 0.747] | 0.743 [0.708, 0.778] | Reviewable |
| Unified clinical | Age band | 60+ | 582 | 0.775 [0.730, 0.814] | 0.397 [0.333, 0.465] | 0.696 [0.651, 0.739] | 0.617 [0.571, 0.663] | Reviewable |
| Unified clinical | Age band | <45 | 606 | 0.578 [0.522, 0.633] | 0.544 [0.488, 0.599] | 0.556 [0.501, 0.610] | 0.601 [0.556, 0.646] | Reviewable |

## Clinical Interpretation for Presentation

1. **Sex Equity on Cardio70k:**
   - Female (N=44,665): Sensitivity = 0.690 [0.684, 0.696], Specificity = 0.781 [0.776, 0.787], ROC-AUC = 0.804 [0.799, 0.808].
   - Male (N=23,916): Sensitivity = 0.685 [0.677, 0.694], Specificity = 0.784 [0.776, 0.791], ROC-AUC = 0.798 [0.793, 0.804].
   - **Conclusion:** The 95% confidence intervals for sensitivity and specificity overlap closely between male and female cohorts on Cardio70k, indicating consistent discriminative accuracy across biological sex in the large cohort.

2. **Age Band Disparities:**
   - For patients under 45 (<45), specificity is very high (0.941 [0.935, 0.946]) while sensitivity is lower (0.560 [0.542, 0.578]).
   - For older patients (60+), sensitivity is high (0.871 [0.864, 0.878]) while specificity drops (0.368 [0.354, 0.383]).
   - **Clinical implication:** The model operates at different effective trade-offs across age groups due to sharp prevalence shifts (29.3% in <45 vs 66.7% in 60+), demonstrating the necessity of age-stratified decision thresholds rather than a universal 0.5 cutoff.

Machine-readable output: `subgroup_confidence_intervals.csv`.
