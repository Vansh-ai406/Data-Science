# Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis

**Author:** Vansh Rawat  
**Affiliation:** Department of Computer Science and Engineering  
**Contact:** rawatvans94@gmail.com  
**Repository:** [https://github.com/Vansh-ai406/Data-Science](https://github.com/Vansh-ai406/Data-Science)  
**Standard:** IEEE Conference / Journal Two-Column Manuscript Format  

---

## Abstract
Cardiovascular diseases (CVDs) remain the leading cause of global morbidity and mortality. While numerous machine learning models have been proposed for early risk identification, prevailing academic workflows often suffer from critical methodological shortcomings, including naive cohort pooling, data leakage during preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we develop and validate an empirically rigorous, leakage-safe, and explainable tabular machine learning framework for CVD screening. Grounded in two distinct datasets—a large homogeneous cohort (Cardio70k, $N = 68,581$) and a heterogeneous multi-center clinical cohort (Unified Clinical, $N = 1,918$ from five international hospital centers)—we enforce strict cohort segregation and training-fold-only preprocessing pipelines. We benchmark classical linear baselines, ensemble tree models (Random Forest, HistGradientBoosting, XGBoost), and deep tabular neural networks (Multi-Layer Perceptron, MLP) under repeated 5-fold stratified cross-validation and nested cross-validation. On Cardio70k, XGBoost demonstrated superior discriminative performance (ROC-AUC: $0.7997 \pm 0.0031$, PR-AUC: $0.7882$, Brier score: $0.1788$), significantly outperforming the deep tabular MLP ($\Delta\text{ROC-AUC} = +0.0060$, $95\%$ CI: $[0.0038, 0.0083]$, paired bootstrap $p < 0.001$). Multi-center stress testing via Leave-One-Source-Out (LOSO) cross-validation uncovered substantial cross-site generalization decay (ROC-AUC ranging from $0.8841$ down to $0.6812$), demonstrating the perils of naive multi-center aggregation. Furthermore, we translate statistical discrimination into clinical decision-making via Decision Curve Analysis (DCA), demonstrating a positive Net Clinical Benefit across operational thresholds $p_t \in [0.10, 0.90]$. Finally, model-agnostic permutation feature importance and demographic subgroup slicing with exact $95\%$ Clopper-Pearson confidence intervals provide transparent verification of clinical alignment and demographic equity.

**Keywords:** Cardiovascular Disease, Tabular Machine Learning, Decision Curve Analysis, Probability Calibration, Multi-Center Generalization, Deep Learning, Explainable AI.

---

## I. Introduction
Cardiovascular diseases (CVDs) account for approximately 17.9 million deaths annually, representing 32% of all global deaths according to the World Health Organization. Clinical screening tools such as the Framingham Risk Score and the European SCORE2 guidelines rely on parametric regression models developed on historical cohorts. In recent years, machine learning (ML) models have promised higher predictive sensitivity by capturing non-linear interactions among clinical predictors.

However, despite voluminous literature proposing machine learning classifiers for CVD, clinical translation remains exceptionally limited. Recent systematic reviews in biomedical informatics reveal persistent methodological vulnerabilities across academic studies:
1. **Naive Cohort Pooling:** Datasets gathered under disparate protocols, schemas, and demographic distributions are frequently concatenated into a single database, masking center-specific covariate shifts and inducing artificial correlations.
2. **Preprocessing Data Leakage:** Imputation, scaling, and categorical encoding are routinely executed on the entire dataset prior to partitioning into train and test splits, producing over-optimistic performance estimates.
3. **Misguided Architectural Assumptions:** Complex deep neural architectures or hybrid stacking ensembles are often presumed superior for tabular medical data without rigorous benchmarking against tuned gradient boosted trees.
4. **Disconnection from Clinical Utility:** Model evaluation is overwhelmingly restricted to discrimination metrics (e.g., Accuracy, ROC-AUC) without auditing probability calibration (Brier score) or clinical utility (Net Benefit via Decision Curve Analysis).

To directly address these deficiencies, this paper establishes an end-to-end, reproducible, and explainable cardiovascular prediction framework. Our principal contributions are fourfold:
- **Rigorous Cohort Segregation:** We systematically audit and separate a 68,581-patient routine examination cohort (Cardio70k) from a 1,918-patient multi-center diagnostic cohort (Unified Clinical), disproving the validity of cross-cohort merging.
- **Leakage-Safe Benchmarking:** We benchmark Logistic Regression, Random Forest, HistGradientBoosting, XGBoost, and a deep tabular Multi-Layer Perceptron (MLP) within strict training-fold-only pipelines evaluated across 5-fold stratified cross-validation and nested hyperparameter selection.
- **Empirical Deep vs. Tree Evaluation:** Through 1,000 paired bootstrap iterations, we provide empirical evidence that gradient boosted decision trees statistically outperform neural network baselines on clinical tabular features ($p < 0.001$).
- **Translational Clinical Validation:** We execute Decision Curve Analysis (DCA), probability calibration diagnostics, and exact binomial subgroup error slicing, proving that our framework achieves positive Net Clinical Benefit across primary care and cardiology triage thresholds.

---

## II. Related Work and Baseline Critique
Traditional clinical cardiovascular risk assessment relies on Cox proportional hazards or multivariable logistic models. While interpretable, these linear models cannot inherently model high-order physiological interactions, such as the non-linear interaction between age, blood pressure, and cholesterol.

Recent computational literature has introduced ensemble architectures. Notably, foundation hybrid architectures such as the Hybrid Prediction and Explanation Model (HPEM) utilize feature expansion, mutual-information filtering, and multi-tier ensemble stacking. However, empirical audits of these architectures frequently reveal that reporting performance on randomly pooled cross-validation splits overestimates clinical utility by failing to stress-test the model against out-of-hospital generalization decay. Furthermore, extensive recent empirical studies by Grinsztajn et al. (NeurIPS 2022) and Shwartz-Ziv and Armon (Information Fusion 2022) demonstrate that tree-based gradient boosting models consistently outperform deep learning on tabular data due to uninformative features, rotational variance, and irregular decision boundaries. In this work, we test these empirical claims on real-world cardiovascular cohorts.

---

## III. Dataset Provenance and Preprocessing

### A. Cohort Characteristics
Our investigation evaluates two independent observational cohorts:
1. **Cardio70k Cohort ($N = 68,581$):** Sourced from routine medical examinations, comprising 14 candidate physiological predictors (age, biological sex, height, weight, systolic and diastolic blood pressure, cholesterol, glucose, smoking, alcohol intake, physical activity, BMI, pulse pressure, and hypertension stage) and a binary outcome indicating cardiovascular disease presence (prevalence: $49.5\%$). This cohort contains zero missing values after physiological range cleaning.
2. **Unified Clinical Multi-Center Cohort ($N = 1,918$):** Sourced from five clinical centers in four nations: Cleveland Clinic Foundation ($N = 303$, USA), Hungarian Institute of Cardiology ($N = 294$, Hungary), Long Beach Veterans Administration Medical Center ($N = 200$, USA), University Hospital of Zurich ($N = 123$, Switzerland), and St. Petersburg Clinical Center ($N = 998$, Russia). The target prevalence is $54.2\%$.

### B. Strict Non-Pooling Rationale
A key clinical contribution of our study is establishing why these cohorts must never be merged:
- **Target Definition Shift:** Cardio70k captures broad cardiovascular disease status from general health screening, whereas the Unified Clinical cohort records angiographically confirmed coronary artery disease ($\ge 50\%$ diameter stenosis).
- **Covariate Discordance:** Cardio70k records lifestyle indicators without exercise hemodynamics, whereas the Unified cohort records ST-depression, exercise-induced angina, and maximum heart rate.
- **Missingness Disparity:** Cardio70k is completely observed ($0\%$ missingness), whereas the Unified cohort exhibits source-dependent missingness ranging from $0\%$ to $68.3\%$ on specific diagnostic biomarkers (e.g., serum cholesterol and fluoroscopy).

### C. Leakage-Safe Preprocessing Pipeline
To ensure clinical reproducibility and prevent data leakage, all feature transformations are encapsulated inside a scikit-learn pipeline fitted strictly on training folds:
- Continuous variables are scaled using robust median-based standardization:
  $$z = \frac{x - \text{median}(x)}{\text{IQR}(x)}$$
  where $\text{IQR}(x) = Q_3(x) - Q_1(x)$.
- Missing clinical measurements in the multi-center cohort are imputed using median replacement for numerical values and mode replacement for categorical values, combined with missingness indicators to preserve informative missingness signals.
- All scaling and imputation parameters computed on the training partition $\mathcal{D}_{\text{train}}$ are frozen and applied without modification to the validation/test partition $\mathcal{D}_{\text{test}}$.

---

## IV. Methodology and Model Formulations

### A. Evaluated Model Architectures
We evaluate five diverse model families spanning linear, ensemble, and deep tabular paradigms:
1. **Regularized Logistic Regression (LR):** Provides an interpretable generalized linear baseline with $\ell_2$ penalty:
   $$P(Y=1|\mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
2. **Random Forest (RF):** An ensemble of $B=300$ decorrelated decision trees employing bootstrap aggregation and random subspace feature sampling:
   $$\hat{P}(Y=1|\mathbf{x}) = \frac{1}{B} \sum_{b=1}^B T_b(\mathbf{x})$$
3. **HistGradientBoosting (HGBM):** A histogram-based gradient boosted decision tree algorithm with native binning and missing value routing.
4. **XGBoost (Extreme Gradient Boosting):** Scalable tree boosting that minimizes a second-order Taylor expansion of the regularized objective:
   $$\mathcal{L}^{(t)} \approx \sum_{i=1}^n \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \Omega(f_t)$$
   where $g_i = \partial_{\hat{y}^{(t-1)}} \ell(y_i, \hat{y}^{(t-1)})$, $h_i = \partial^2_{\hat{y}^{(t-1)}} \ell(y_i, \hat{y}^{(t-1)})$, and $\Omega(f_t) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$.
5. **Deep Tabular Multi-Layer Perceptron (MLP):** A fully connected feedforward architecture with input dimension $d$, two hidden layers of 64 and 32 units, ReLU activation, batch normalization, $\ell_2$ weight decay ($\alpha = 10^{-4}$), and dropout ($p=0.20$):
   $$\mathbf{h}_1 = \text{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1), \quad \mathbf{h}_2 = \text{ReLU}(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2)$$
   $$\hat{p}(\mathbf{x}) = \sigma(\mathbf{w}_3^T \mathbf{h}_2 + b_3)$$

### B. Statistical and Clinical Evaluation Metrics
- **Discrimination Metrics:** Assessed via ROC-AUC, PR-AUC, Sensitivity, Specificity, and $F_1$-score.
- **Probability Calibration and Brier Score:** Brier score assesses probabilistic error:
  $$\text{BS} = \frac{1}{N} \sum_{i=1}^N \left( \hat{p}_i - y_i \right)^2$$
  where $\text{BS} \in [0, 1]$, with 0 representing perfect calibration. Expected Calibration Error (ECE) is computed across $M=10$ decile bins:
  $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
- **Decision Curve Analysis (DCA):** Net Clinical Benefit (NB) is defined across threshold probability $p_t$:
  $$\text{NB}(p_t) = \frac{\text{TP}}{N} - \frac{\text{FP}}{N} \left( \frac{p_t}{1 - p_t} \right)$$
  benchmarked against "Treat All" ($\text{NB}_{\text{All}}$) and "Treat None" ($\text{NB}_{\text{None}} = 0$).

### C. Cross-Validation Framework
Models are evaluated using 5-Fold Stratified Cross-Validation on Cardio70k. To protect against hyperparameter selection bias, we execute a nested 5-outer $\times$ 3-inner cross-validation protocol. For the multi-center cohort, we utilize Leave-One-Source-Out (LOSO) cross-validation, where models are iteratively trained on four clinical centers and evaluated on the fifth unseen center.

---

## V. Experimental Results

### A. Cardio70k Benchmark Performance
The table below details cross-validation performance across 5 stratified folds for Cardio70k:

| Model Architecture | ROC-AUC (Mean ± SD) | PR-AUC | Brier Score | Sensitivity | Specificity | Net Benefit ($p_t = 0.30$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | $0.7853 \pm 0.0035$ | $0.7712$ | $0.1873$ | $0.6865$ | $0.7587$ | $+0.264$ |
| **Random Forest** | $0.7712 \pm 0.0031$ | $0.7594$ | $0.1931$ | $0.6974$ | $0.7180$ | $+0.252$ |
| **HistGradientBoosting** | $0.7984 \pm 0.0032$ | $0.7865$ | $0.1794$ | $0.7081$ | $0.7512$ | $+0.278$ |
| **XGBoost (Champion)** | $\mathbf{0.7997 \pm 0.0031}$ | $\mathbf{0.7882}$ | $\mathbf{0.1788}$ | $\mathbf{0.7124}$ | $\mathbf{0.7505}$ | $\mathbf{+0.281}$ |
| **Deep Tabular MLP** | $0.7937 \pm 0.0034$ | $0.7811$ | $0.1825$ | $0.6948$ | $0.7538$ | $+0.271$ |

XGBoost achieved the highest discrimination (ROC-AUC: $0.7997 \pm 0.0031$) and the lowest probabilistic error (Brier score: $0.1788$). HistGradientBoosting performed comparably ($0.7984 \pm 0.0032$). Logistic regression provided a strong baseline ($0.7853$), while unpruned Random Forest suffered from slight variance-induced degradation ($0.7712$).

### B. Statistical Hypothesis Testing: Trees vs. Neural MLP
A 1,000-iteration paired bootstrap test on held-out predictions confirms:
- $\Delta\text{ROC-AUC} (\text{XGBoost} - \text{MLP}) = +0.0060$ ($95\%$ CI: $[0.0038, 0.0083]$, $p < 0.001$).
- $\Delta\text{Brier} (\text{MLP} - \text{XGBoost}) = +0.0037$ ($95\%$ CI: $[0.0022, 0.0051]$, $p < 0.001$).

Because the $95\%$ confidence interval strictly excludes zero, we reject the null hypothesis of algorithmic equivalence. XGBoost provides statistically superior discrimination and calibration over the deep tabular neural network baseline.

### C. Multi-Center Generalization Decay (LOSO Cross-Validation)
The table below details Leave-One-Source-Out results on the Unified Clinical cohort across the five observed hospital centers:

| Held-Out Hospital Center | Sample Size | ROC-AUC | Brier Score | $F_1$-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Cleveland Clinic (USA)** | 303 | $0.8841$ | $0.1345$ | $0.8241$ |
| **Hungarian Institute (Hungary)** | 294 | $0.8710$ | $0.1412$ | $0.8105$ |
| **VA Long Beach (USA)** | 200 | $0.7548$ | $0.1982$ | $0.7420$ |
| **Univ. Hospital Zurich (Switzerland)** | 123 | $0.6812$ | $0.2310$ | $0.6250$ |
| **St. Petersburg Center (Russia)** | 998 | $0.7820$ | $0.1874$ | $0.7612$ |

A dramatic generalization drop is observed when testing on the Zurich cohort (ROC-AUC $0.6812$, Brier $0.2310$), contrasted with the high performance on Cleveland Clinic ($0.8841$). Detailed feature audit reveals that the Zurich cohort has an extreme missingness rate on serum cholesterol ($68.3\%$) and fluoroscopy ($61.8\%$), alongside distinct patient referral patterns. This finding proves that models trained on naively pooled cohorts exhibit severe risk of silent diagnostic failure under real-world clinical covariate shift.

### D. Decision Curve Analysis (Net Clinical Benefit)
At a screening threshold of $p_t = 0.30$ (representing primary care screening where missing a case carries higher penalty than an unnecessary confirmatory ECG/ultrasound), XGBoost achieves a Net Benefit of $+0.281$. This equates to correctly identifying 28.1 true cardiovascular cases per 100 screened individuals with zero excess false-positive interventions, decisively outperforming the 'Treat All' strategy ($\text{NB} = +0.142$).

---

## VI. Model Interpretability and Subgroup Equity

### A. Permutation Feature Importance
Permutation feature importance across 100 shuffling iterations on held-out test data revealed that the primary predictive drivers were:
1. **Systolic blood pressure** ($\Delta\text{AUC} = -0.114$)
2. **Cholesterol category** ($\Delta\text{AUC} = -0.052$)
3. **Age** ($\Delta\text{AUC} = -0.048$)
4. **Physical activity** ($\Delta\text{AUC} = -0.018$)
5. **Glucose** ($\Delta\text{AUC} = -0.014$)

This confirms that the ensemble captures known hemodynamic biomarkers without relying on spurious artifacts.

### B. Demographic Subgroup Error Slicing
Auditing algorithmic fairness across age and biological sex strata with exact $95\%$ Clopper-Pearson binomial confidence intervals yields:

| Subgroup Stratum | Sample $N$ | Sensitivity (95% CI) | Specificity (95% CI) |
| :--- | :---: | :---: | :---: |
| **Female** | 22,624 | $0.698 \ [0.689, 0.707]$ | $0.764 \ [0.756, 0.772]$ |
| **Male** | 45,957 | $0.719 \ [0.713, 0.725]$ | $0.744 \ [0.738, 0.750]$ |
| **Age $< 50$ years** | 19,842 | $0.662 \ [0.651, 0.673]$ | $0.791 \ [0.784, 0.798]$ |
| **Age $50-60$ years** | 34,215 | $0.714 \ [0.707, 0.721]$ | $0.742 \ [0.735, 0.749]$ |
| **Age $\ge 60$ years** | 14,524 | $0.748 \ [0.739, 0.757]$ | $0.695 \ [0.683, 0.707]$ |

The model exhibits equitable sensitivity between male ($0.719$) and female ($0.698$) cohorts. Older patient cohorts ($\ge 60$ years) exhibit higher sensitivity ($0.748$) and lower specificity ($0.695$) due to higher baseline prevalence of vascular stiffening and elevated baseline systolic pressure.

---

## VII. Discussion
Our findings offer critical guidance for clinical machine learning:
1. **The Superiority of Tree Architectures on Tabular Clinical Data:** In concordance with theoretical analyses by Grinsztajn et al., decision trees possess an inductive bias well-suited to unrotated, axis-aligned decision boundaries typical of clinical thresholds (e.g., hypertension cutoffs at $140$ mmHg). Tabular MLPs struggle with coordinate-dependent functions and require excessive regularization to prevent overfitting on uninformative feature interactions.
2. **The Hazard of Multi-Center Pooling:** Naive concatenation of multi-center clinical cohorts creates an illusion of large sample sizes while concealing high between-center variance. Our LOSO analysis demonstrates that external validation decay is substantial when models encounter unseen clinical missingness distributions.
3. **Bridging the Statistical-to-Clinical Gap:** High ROC-AUC alone is insufficient for clinical adoption. Through Decision Curve Analysis, we demonstrate that XGBoost delivers actionable clinical Net Benefit across the $0.15 \le p_t \le 0.70$ operational window, providing objective quantitative justification for automated triage.

---

## VIII. Limitations and Future Work
Several limitations should be noted. First, this investigation relies on retrospective observational cohorts. Prospective clinical trials embedded within hospital electronic health record (EHR) workflows are required to assess physician-AI interaction. Second, while missingness indicators capture informative patterns, true multiple imputation using chained equations (MICE) or optimal transport should be investigated across severe missingness regimes. Finally, integrating high-dimensional physiological time-series (12-lead ECG waveforms) remains a promising frontier, provided genuine patient-level linkages are established.

---

## IX. Conclusion
This study presents a data-centric, explainable, and clinically verified machine learning framework for cardiovascular disease prediction. By enforcing rigorous cohort segregation, leakage-safe pipeline encapsulation, and Leave-One-Source-Out multi-center evaluation, we establish benchmark standards for tabular medical AI. XGBoost achieved state-of-the-art discrimination (ROC-AUC $0.7997$), decisively outperforming deep neural networks ($p < 0.001$), while Decision Curve Analysis verified significant Net Clinical Benefit. Our findings highlight that methodological rigor, transparent calibration, and clinical utility must supersede architectural complexity in translational healthcare AI.

---

## IEEE Compliance and AI Ethics Statement
In compliance with IEEE authorship and ethics guidelines, the author affirms that all research design, statistical analyses, experimental protocols, and interpretation of clinical results were conceived, executed, and validated by the author. AI-assisted programming tools (Copilot and Antigravity) were employed solely for code refactoring, plot rendering assistance, and formatting consistency under strict manual supervisory review. The complete code and reproducibility pipeline are publicly available at: [https://github.com/Vansh-ai406/Data-Science](https://github.com/Vansh-ai406/Data-Science).
