# Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Mathematical Formulations, Generalization Audits, and Decision Curve Analysis

**Under the Guidance of:** Rinky Chhatwani (`rinkychhatwani@gmail.com`)  
**Authors:** Vansh Rawat (`vanshrawat385@gmail.com`), Drisha Chauhan (`chauhan.drisha4116@gmail.com`), Karan Bheda (`karanbheda29898@gmail.com`), and Harsh Rathva (`Harshrathvaai@gmail.com`)  
**Affiliation:** Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat, Gujarat, India  
**Code Repository:** [https://github.com/Vansh-ai406/Data-Science](https://github.com/Vansh-ai406/Data-Science)

---

## Abstract
Cardiovascular diseases (CVDs) represent the foremost cause of global mortality, accounting for approximately 17.9 million annual deaths according to the World Health Organization. While machine learning classifiers have promised enhanced risk detection, published healthcare AI literature frequently suffers from fatal methodological flaws: naive multi-center cohort pooling, severe data leakage during feature preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we formulate and validate a leakage-safe, multi-cohort tabular machine learning framework for CVD screening. Our research is grounded in two independently handled clinical datasets: a large primary-care screening cohort (Cardio70k, $N = 68,581$; 44,665 females and 23,916 males) and an international multi-center clinical cohort (Unified Clinical, $N = 1,918$ across five hospital centers: Mendeley Data India $N=1,000$, UCI Cleveland $N=303$, UCI Hungary $N=293$, UCI Long Beach VA $N=199$, and UCI Switzerland $N=123$). We establish six core mathematical pillars underpinning clinical tabular learning: 1) second-order gradient tree boosting objective and exact node split gain calculus; 2) clinical Decision Curve Analysis (DCA) and net benefit exchange rate proofs; 3) Murphy's orthogonal three-component Brier score decomposition and logistic recalibration; 4) paired non-parametric bootstrap hypothesis testing ($B = 1,000$ replicates); 5) exact Wilson score binomial confidence intervals and Hanley-McNeil AUC variance; and 6) pattern-mixture informative missingness indicator formulations. On Cardio70k, XGBoost attained champion discrimination (ROC-AUC: $0.8019 \pm 0.0027$, PR-AUC: $0.7828$, Brier score: $0.1802$), statistically outperforming deep tabular neural networks ($\Delta\text{ROC-AUC} = +0.0027$, 95% CI: $[0.0020, 0.0036]$, paired bootstrap $p < 0.001$). Under Leave-One-Source-Out (LOSO) multi-center stress testing, we uncover steep cross-border generalization decay, where models trained on Western hospital centers collapsed to near-random discrimination ($0.4937$ ROC-AUC) on the Indian cohort, demonstrating pronounced clinical covariate shift. Augmenting feature spaces with explicit missingness indicators ($m_{ij}$) boosted cross-center generalization ROC-AUC to $0.7653$ and F1 to $0.8004$. Moving beyond discrimination, Decision Curve Analysis proves substantial positive Net Clinical Benefit ($+0.3246$ at threshold probability $p_t = 0.30$ vs. $+0.2782$ for universal treatment). Ten high-resolution result figures, model-agnostic permutation feature reliance, and demographic subgroup audits provide transparent validation of clinical alignment and algorithmic equity.

**Keywords:** Cardiovascular disease, tabular machine learning, decision curve analysis, gradient boosting mathematics, probability calibration, multi-center generalization, explainable AI, algorithmic fairness.

---

## I. Introduction
Cardiovascular diseases (CVDs) account for 32% of global mortality according to the World Health Organization [1]. Clinical screening scores like Framingham [2] and SCORE2 [3] rely on linear multivariable regressions. While interpretable, they cannot model non-linear physiological couplings autonomously. Machine learning offers higher predictive sensitivity, but published literature frequently violates TRIPOD guidelines [13] via naive cohort pooling, data leakage, and unverified deep learning architectures.

This study implements a leak-free pipeline with strict cohort segregation, mathematical derivation of tree split objectives, paired bootstrap comparisons, Leave-One-Source-Out cross-validation, and Decision Curve Analysis, developed under the faculty guidance of Rinky Chhatwani at the Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat.

---

## II. Mathematical Formulations and System Architecture

### A. Gradient Boosted Tree Objective & Optimal Node Partitioning
At boosting iteration $t$, the regularized objective with tree complexity penalty is:
$$\mathcal{L}^{(t)} = \sum_{i=1}^N l\left(y_i, \hat{y}_i^{(t-1)} + f_t(\mathbf{x}_i)\right) + \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$$

Taking the second-order Taylor expansion around $\hat{y}_i^{(t-1)}$:
$$\tilde{\mathcal{L}}^{(t)} \approx \sum_{i=1}^N \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$$
where first and second gradients for log-loss are $g_i = \hat{p}_i - y_i$ and $h_i = \hat{p}_i(1 - \hat{p}_i)$.

For leaf instance assignments $I_j = \{i : q(\mathbf{x}_i) = j\}$, setting $\frac{\partial \tilde{\mathcal{L}}^{(t)}}{\partial w_j} = 0$ yields the optimal leaf weight:
$$w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}$$
and the exact node split gain is:
$$\mathcal{G}_{\text{split}} = \frac{1}{2}\left[ \frac{\left(\sum_{i \in I_L} g_i\right)^2}{\sum_{i \in I_L} h_i + \lambda} + \frac{\left(\sum_{i \in I_R} g_i\right)^2}{\sum_{i \in I_R} h_i + \lambda} - \frac{\left(\sum_{i \in I} g_i\right)^2}{\sum_{i \in I} h_i + \lambda} \right] - \gamma$$

*Clinical & Theoretical Inductive Bias:* This demonstrates why tree boosting outperforms neural networks on tabular clinical records: splits construct axis-aligned step functions $\mathbb{I}(x_j \ge \theta)$ that mirror sharp medical thresholds (e.g., hypertension at systolic BP $\ge 140$ mmHg), whereas neural MLPs use smooth sigmoidal hyperplanes that over-smooth clinical discontinuities.

### B. Decision Curve Analysis (DCA) and Clinical Net Benefit Calculus
To evaluate clinical utility across decision thresholds $p_t \in (0, 1)$, Net Clinical Benefit is calculated as:
$$\mathrm{Net\ Benefit}(p_t) = \frac{\mathrm{TP}}{N} - \frac{\mathrm{FP}}{N} \left(\frac{p_t}{1 - p_t}\right)$$

*Derivation of the Exchange Rate:* At threshold probability $p_t$, clinical indifference between intervention benefit ($\mathcal{B}$) and false-positive harm ($\mathcal{H}$) implies:
$$p_t \cdot \mathcal{B} = (1 - p_t) \cdot \mathcal{H} \iff \frac{\mathcal{H}}{\mathcal{B}} = \frac{p_t}{1 - p_t}$$
Expressing Net Benefit in true-positive equivalents per patient. The baseline comparators are:
$$\mathrm{NB}_{\text{all}}(p_t) = \pi - (1 - \pi)\left(\frac{p_t}{1 - p_t}\right), \quad \mathrm{NB}_{\text{none}}(p_t) = 0$$

### C. Probability Calibration, Brier Decomposition, and ECE
The Brier score measures mean squared probability error:
$$\mathrm{BS} = \frac{1}{N}\sum_{i=1}^N (\hat{p}_i - y_i)^2$$
Under Murphy's decomposition across $M$ probability bins, $\mathrm{BS}$ decomposes into Reliability, Resolution, and Uncertainty:
$$\mathrm{BS} = \sum_{m=1}^M \frac{|B_m|}{N} (\bar{p}_{B_m} - \bar{y}_{B_m})^2 - \sum_{m=1}^M \frac{|B_m|}{N} (\bar{y}_{B_m} - \bar{y})^2 + \bar{y}(1 - \bar{y})$$

Expected Calibration Error across $M=10$ bins is:
$$\mathrm{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \bar{y}_{B_m} - \bar{p}_{B_m} \right|$$

### D. Paired Bootstrap Hypothesis Testing
Paired resampling differences $\Delta^{(b)} = \mathcal{M}_{\text{XGBoost}}(\mathcal{S}^{*(b)}) - \mathcal{M}_{\text{MLP}}(\mathcal{S}^{*(b)})$ ($B = 1,000$ replicates) yield empirical two-tailed $p$-values:
$$p = 2 \cdot \min\left( \frac{1}{B}\sum_{b=1}^B \mathbb{I}(\Delta^{(b)} \le 0), \frac{1}{B}\sum_{b=1}^B \mathbb{I}(\Delta^{(b)} \ge 0) \right)$$

### E. Exact Binomial Wilson Score Confidence Limits
To prevent small-sample distortion in demographic slicing, asymmetric Wilson score limits are computed:
$$\mathrm{CI}_{1-\alpha} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

### F. Informative Missingness Formulation & Pattern Mixture Model
Augmenting feature vectors with binary missingness indicators $m_{ij} = \mathbb{I}(x_{ij} \text{ missing})$ allows estimators to model separate conditional expectations under Missing Not At Random (MNAR) hospital referral:
$$s(\mathbf{x}_i) = \sum_{j=1}^d \left( w_j^{\text{val}} \tilde{x}_{ij} + w_j^{\text{miss}} m_{ij} \right) + b \implies \mathbb{E}[Y \mid x_j, m_j=0] \ne \mathbb{E}[Y \mid m_j=1]$$

---

## III. Benchmark Results & Visual Dossier

### Table I: 5-Fold Cross-Validation on Cardio70k ($N = 68,581$)
| Model Architecture | ROC-AUC (Mean ± SD) | PR-AUC | Brier Score | Accuracy | Sensitivity | Specificity | Net Benefit ($p_t = 0.30$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression ($\ell_2$)** | 0.7939 ± 0.0030 | 0.7710 | 0.1851 | 0.7226 | 0.6865 | 0.7587 | +0.2642 |
| **Random Forest** | 0.7892 ± 0.0031 | 0.7731 | 0.1866 | 0.7180 | 0.6974 | 0.7180 | +0.2520 |
| **HistGradientBoosting** | 0.8009 ± 0.0032 | 0.7824 | 0.1806 | 0.7301 | 0.7081 | 0.7512 | +0.2785 |
| **XGBoost (Champion)** | **0.8019 ± 0.0027** | **0.7828** | **0.1802** | **0.7324** | **0.7124** | **0.7505** | **+0.3246** |
| **Deep Tabular MLP** | 0.7991 ± 0.0034 | 0.7788 | 0.1814 | 0.7289 | 0.6948 | 0.7538 | +0.2710 |

*Paired Bootstrap Test:* XGBoost statistically outperforms Neural MLP by $\Delta\text{ROC-AUC} = +0.0027$ (95% CI: $[0.0020, 0.0036]$, $p < 0.001$).

### Key High-Resolution Result Graphs
- **Fig. 1 (Discrimination Curves):** `reports/plots/cv_roc_auc.png` (ROC and PR curves on Cardio70k).
- **Fig. 2 (Probabilistic Error Distribution):** `reports/plots/cv_brier_score.png` (Brier score distribution across folds).
- **Fig. 3 (Paired Bootstrap Differences):** `reports/plots/cardio_mlp_paired_bootstrap.png` (XGBoost vs. MLP distribution with 95% CIs).
- **Fig. 4 (Reliability Calibration):** `reports/plots/calibration_curves.png` (Calibration curves and ECE across models).
- **Fig. 5 (Multi-Center Generalization):** `reports/plots/hpem_source_comparison.png` (Leave-one-source-out transfer across 5 centers).
- **Fig. 6 (Missingness Indicator Boost):** `reports/plots/missingness_indicator_comparison.png` (Generalization gains from $m_{ij}$).
- **Fig. 7 (Decision Curve Analysis):** `reports/plots/decision_curves.png` (Net clinical benefit across threshold probabilities).
- **Fig. 8 (Operational Threshold Trade-offs):** `reports/plots/threshold_tradeoffs.png` (Sensitivity, specificity, and precision across cutoffs).
- **Fig. 9 (Permutation Feature Importance):** `reports/plots/permutation_importance.png` (Biomarker ranking with SD error bars).
- **Fig. 10 (Demographic Fairness Auditing):** `reports/plots/subgroup_performance.png` (Performance across biological sex and age brackets).

### Table II: Leave-One-Source-Out Generalization Gap (Unified Clinical, $N = 1,918$)
| Held-Out Center | Host Country | Patients ($N$) | XGBoost ROC-AUC | XGBoost Accuracy | Logistic Regression ROC-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **UCI Hungarian Inst. of Cardiology** | Hungary | 293 | 0.8370 | 0.7747 | 0.8402 | 0.1601 |
| **UCI Cleveland Clinic Foundation** | USA | 303 | 0.8358 | 0.7525 | 0.8412 | 0.1722 |
| **UCI Long Beach VA Medical Center** | USA | 199 | 0.6848 | 0.7538 | 0.7104 | 0.1937 |
| **UCI Univ. Hospital of Zurich** | Switzerland | 123 | 0.6576 | 0.7317 | 0.7496 | 0.1748 |
| **Mendeley Data India Cohort** | India | 1,000 | 0.4937 | 0.5090 | 0.5120 | 0.3244 |

### Table III: Demographic Subgroup Slicing with 95% Wilson Score CIs (Cardio70k, XGBoost)
| Demographic Subgroup | Sample Size ($N$) | Sensitivity [95% CI] | Specificity [95% CI] | Subgroup ROC-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Female Patients (Code 0)** | 44,665 | 0.6899 [0.684, 0.696] | 0.7814 [0.776, 0.787] | 0.8036 | 0.1795 |
| **Male Patients (Code 1)** | 23,916 | 0.6854 [0.677, 0.694] | 0.7838 [0.776, 0.791] | 0.7985 | 0.1816 |
| **Younger Age (< 45 Years)** | 10,089 | 0.5604 [0.540, 0.581] | 0.9411 [0.936, 0.946] | 0.8301 | 0.1319 |
| **Middle Age (45–59 Years)** | 45,680 | 0.6355 [0.629, 0.642] | 0.8094 [0.804, 0.815] | 0.7814 | 0.1879 |
| **Elderly Patients (≥ 60 Years)** | 12,812 | 0.8709 [0.863, 0.878] | 0.3683 [0.354, 0.383] | 0.7232 | 0.1910 |

---

## IV. References
[1] World Health Organization, "Cardiovascular diseases (CVDs): Key facts," *WHO Fact Sheets*, Geneva, Switzerland, 2021.  
[2] R. B. D'Agostino et al., "General cardiovascular risk profile for use in primary care: The Framingham Heart Study," *Circulation*, vol. 117, no. 6, pp. 743–753, 2008.  
[3] SCORE2 Working Group and European Society of Cardiology, "SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe," *Eur. Heart J.*, vol. 42, no. 25, pp. 2439–2454, 2021.  
[4] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD)*, 2016, pp. 785–794.  
[5] L. Breiman, "Random forests," *Mach. Learn.*, vol. 45, no. 1, pp. 5–32, 2001.  
[6] A. J. Vickers and E. B. Elkin, "Decision curve analysis: a novel method for evaluating prediction models," *Med. Decis. Making*, vol. 26, no. 6, pp. 565–574, 2006.  
[7] A. J. Vickers, B. van Calster, and E. W. Steyerberg, "A simple, step-by-step guide to interpreting decision curve analysis," *Diagn. Progn. Res.*, vol. 1, no. 1, pp. 1–8, 2016.  
[8] G. W. Brier, "Verification of forecasts expressed in terms of probability," *Mon. Weather Rev.*, vol. 78, no. 1, pp. 1–3, 1950.  
[9] B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*. Boca Raton, FL: CRC Press, 1994.  
[10] D. W. Hosmer Jr, S. Lemeshow, and R. X. Sturdivant, *Applied Logistic Regression*, 3rd ed. Hoboken, NJ: John Wiley & Sons, 2013.  
[11] R. Shwartz-Ziv and A. Armon, "Tabular data: Deep learning is not all you need," *Inf. Fusion*, vol. 81, pp. 84–90, 2022.  
[12] L. Grinsztajn, E. Oyallon, and G. Varoquaux, "Why do tree-based models still outperform deep learning on typical tabular data?," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 35, 2022, pp. 507–520.  
[13] G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, "Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD statement," *BMJ*, vol. 350, p. g7594, 2015.  
[14] C. J. Clopper and E. S. Pearson, "The use of confidence or fiducial limits illustrated in the case of the binomial," *Biometrika*, vol. 26, no. 4, pp. 404–413, 1934.  
[15] R. Detrano et al., "International application of a new probability algorithm for the diagnosis of coronary artery disease," *Am. J. Cardiol.*, vol. 64, no. 5, pp. 304–310, 1989.  
[16] Mendeley Data, "Cardiovascular Disease Dataset: Multi-center Indian clinical registry," *Mendeley Data*, V1, doi: 10.17632/jh55nn26tx.1, 2020.  
[17] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *J. Am. Stat. Assoc.*, vol. 22, no. 158, pp. 209–212, 1927.  
[18] J. A. Hanley and B. J. McNeil, "The meaning and use of the area under a receiver operating characteristic (ROC) curve," *Radiology*, vol. 143, no. 1, pp. 29–36, 1982.
