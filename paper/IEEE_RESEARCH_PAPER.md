# Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis

**Under the Guidance of:** Rinky Chhatwani  
**Authors:** Vansh Rawat, Drisha Chauhan, Karan Bheda, and Harsh Rathva  
**Affiliation:** Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat, Gujarat, India  
**Code Repository:** [https://github.com/Vansh-ai406/Data-Science](https://github.com/Vansh-ai406/Data-Science)

---

## Abstract
Cardiovascular diseases (CVDs) represent the foremost cause of global mortality, accounting for approximately 17.9 million annual deaths according to the World Health Organization. While machine learning classifiers have promised enhanced risk detection, published healthcare AI literature frequently suffers from fatal methodological flaws: naive multi-center cohort pooling, severe data leakage during feature preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we formulate and validate a leakage-safe, multi-cohort tabular machine learning framework for CVD screening. Our research is grounded in two independently handled clinical datasets: a large primary-care screening cohort (Cardio70k, $N = 68,581$; 44,665 females and 23,916 males) and an international multi-center clinical cohort (Unified Clinical, $N = 1,918$ across five hospital centers: Mendeley Data India $N=1,000$, UCI Cleveland $N=303$, UCI Hungary $N=293$, UCI Long Beach VA $N=199$, and UCI Switzerland $N=123$). We benchmark generalized linear models, ensemble decision trees (Random Forest, HistGradientBoosting, XGBoost), and deep tabular neural networks (Multi-Layer Perceptron, MLP) under repeated 5-fold stratified cross-validation and nested outer-fold selection. On Cardio70k, XGBoost attained champion discrimination (ROC-AUC: $0.8019 \pm 0.0027$, PR-AUC: $0.7828$, Brier score: $0.1802$), statistically outperforming the deep tabular neural network ($\Delta	ext{ROC-AUC} = +0.0027$, 95% CI: $[0.0020, 0.0036]$, paired bootstrap $p < 0.001$). Under Leave-One-Source-Out (LOSO) multi-center stress testing, we uncover steep cross-border generalization decay, where models trained on Western hospital centers collapsed to near-random discrimination ($0.4937$ ROC-AUC) on the Indian cohort, demonstrating pronounced clinical covariate shift. Moving beyond discrimination, Decision Curve Analysis (DCA) proves a substantial positive Net Clinical Benefit ($+0.3246$ at threshold probability $p_t = 0.30$ vs. $+0.2782$ for universal treatment). Finally, model-agnostic permutation feature reliance and demographic subgroup auditing with exact 95% Clopper-Pearson confidence intervals provide transparent validation of clinical alignment and algorithmic equity.

**Keywords:** Cardiovascular disease, tabular machine learning, decision curve analysis, multi-center generalization, probability calibration, explainable AI, algorithmic fairness.

---

## I. Introduction
Cardiovascular diseases (CVDs) account for 32% of global mortality according to the World Health Organization [1]. Clinical screening scores like Framingham [2] and SCORE2 [3] rely on linear multivariable regressions. While interpretable, they cannot model non-linear physiological couplings autonomously. Machine learning offers higher predictive sensitivity, but published literature frequently violates TRIPOD guidelines [13] via naive cohort pooling, data leakage, and unverified deep learning architectures.

This study implements a leak-free pipeline with strict cohort segregation, paired bootstrap comparisons, Leave-One-Source-Out cross-validation, and Decision Curve Analysis, developed under the faculty guidance of Rinky Chhatwani at the Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat.

---

## II. Benchmark Results

### Table I: 5-Fold Cross-Validation on Cardio70k ($N = 68,581$)
| Model Architecture | ROC-AUC (Mean ± SD) | PR-AUC | Brier Score | Accuracy | Sensitivity | Specificity | Net Benefit ($p_t = 0.30$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.7939 ± 0.0030 | 0.7710 | 0.1851 | 0.7226 | 0.6865 | 0.7587 | +0.2642 |
| **Random Forest** | 0.7892 ± 0.0031 | 0.7731 | 0.1866 | 0.7180 | 0.6974 | 0.7180 | +0.2520 |
| **HistGradientBoosting** | 0.8009 ± 0.0032 | 0.7824 | 0.1806 | 0.7301 | 0.7081 | 0.7512 | +0.2785 |
| **XGBoost (Champion)** | **0.8019 ± 0.0027** | **0.7828** | **0.1802** | **0.7324** | **0.7124** | **0.7505** | **+0.3246** |
| **Deep Tabular MLP** | 0.7991 ± 0.0034 | 0.7788 | 0.1814 | 0.7289 | 0.6948 | 0.7538 | +0.2710 |

*Paired Bootstrap Test:* XGBoost statistically outperforms Neural MLP by $\Delta	ext{ROC-AUC} = +0.0027$ (95% CI: $[0.0020, 0.0036]$, $p < 0.001$).

### Table II: Leave-One-Source-Out Generalization Gap (Unified Clinical, $N = 1,918$)
| Held-Out Center | Host Country | Patients ($N$) | XGBoost ROC-AUC | XGBoost Accuracy | Logistic Regression ROC-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **UCI Hungarian Inst. of Cardiology** | Hungary | 293 | 0.8370 | 0.7747 | 0.8402 | 0.1601 |
| **UCI Cleveland Clinic Foundation** | USA | 303 | 0.8358 | 0.7525 | 0.8412 | 0.1722 |
| **UCI Long Beach VA Medical Center** | USA | 199 | 0.6848 | 0.7538 | 0.7104 | 0.1937 |
| **UCI Univ. Hospital of Zurich** | Switzerland | 123 | 0.6576 | 0.7317 | 0.7496 | 0.1748 |
| **Mendeley Data India Cohort** | India | 1,000 | 0.4937 | 0.5090 | 0.5120 | 0.3244 |

### Table III: Demographic Subgroup Slicing with 95% Clopper-Pearson CIs (Cardio70k, XGBoost)
| Demographic Subgroup | Sample Size ($N$) | Sensitivity (95% CI) | Specificity (95% CI) | Subgroup ROC-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Female Patients (Code 0)** | 44,665 | 0.6899 [0.684, 0.696] | 0.7814 [0.776, 0.787] | 0.8036 | 0.1795 |
| **Male Patients (Code 1)** | 23,916 | 0.6854 [0.677, 0.694] | 0.7838 [0.776, 0.791] | 0.7985 | 0.1816 |
| **Younger Age (< 45 Years)** | 10,089 | 0.5604 [0.540, 0.581] | 0.9411 [0.936, 0.946] | 0.8301 | 0.1319 |
| **Middle Age (45–59 Years)** | 45,680 | 0.6355 [0.629, 0.642] | 0.8094 [0.804, 0.815] | 0.7814 | 0.1879 |
| **Elderly Patients (≥ 60 Years)** | 12,812 | 0.8709 [0.863, 0.878] | 0.3683 [0.354, 0.383] | 0.7232 | 0.1910 |

---

## III. Limitations and Future Work

### A. Limitations of Current Work
1. **Retrospective and Prevalent Label Design:** Both Cardio70k ($N = 68,581$) and Unified Clinical ($N = 1,918$) datasets are retrospective cross-sectional registries capturing clinical parameters at a single diagnostic or screening visit. Consequently, the models predict contemporaneous disease presence (prevalent disease classification) rather than true 5-year or 10-year prospective incident cardiovascular risk, which would require longitudinal follow-up registries like Framingham [2].
2. **Informative Missingness and Indication Bias:** In real-world clinical practice, diagnostic biomarkers are not omitted at random (MCAR); rather, missingness is driven by clinical indication (MNAR). In the Zurich cohort, severe missingness on serum cholesterol (68.3%) and fluoroscopy (61.8%) reflected institutional referral triage where invasive tests were prioritized only for high-acuity patients.
3. **Absence of Verified Universal Patient Linkages for Multimodal Fusion:** Audited 12-lead ECG waveforms and synthetic CT/MRI imaging repositories lacked secure, anonymized universal patient identification numbers. Attempting synthetic pairing would introduce catastrophic data leakage and fabricated correlations.
4. **Architectural Scope of Tabular Deep Learning:** Our neural baseline was restricted to a regularized two-hidden-layer feedforward MLP. Newer column-wise self-attention tabular architectures (FT-Transformer, TabNet) were not benchmarked due to hyperparameter instability on small clinical cohorts.
5. **Cross-System Generalization Gap in South Asian Populations:** Leave-One-Source-Out evaluation revealed that models trained on Western UCI centers collapsed to near-random discrimination on Indian patients (ROC-AUC $0.4937$), demonstrating profound clinical covariate shift.

### B. Future Research Directions
1. **Prospective EHR Integration via HL7 FHIR Microservices:** Containerizing the champion XGBoost model into an interoperable microservice compliant with the Health Level Seven Fast Healthcare Interoperability Resources (HL7 FHIR) standard for real-time hospital primary-care workflows.
2. **Specialized Tabular Transformers:** Benchmarking column-wise self-attention networks (FT-Transformer, SAINT) pre-trained with masked feature reconstruction on unlabeled clinical registries.
3. **Federated Multi-Hospital Learning:** Implementing federated averaging ($	ext{FedAvg}$) equipped with differential privacy ($arepsilon, \delta$) to enable collaborative training across international hospital networks without sharing raw protected health information.
4. **Dynamic Calibration and Human-in-the-Loop Deferral:** Coupling conformal prediction intervals with uncertainty estimation to deploy a reject-option triage system routing borderline cases ($\hat{p} \in [0.42, 0.58]$) for specialist cardiologist review.
5. **Localized Clinical Adaptation for South Asian Populations:** Pre-training on indigenous South Asian CVD registries to account for the premature onset and distinct lipid profiles of coronary artery disease in the Indian subcontinent.

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
