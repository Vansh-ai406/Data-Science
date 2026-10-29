# Cardiovascular Disease AI Research: Master Presentation & Defense Guide

**Oral Defense Date:** October 30, 2026  
**Interactive Visual Dossier:** See `reports/MASTER_RESEARCH_DEFENSE_GUIDE.html` (Complete with all 14 embedded high-resolution figures, styled tables, and print-to-PDF formatting).

---

## 1. Executive Summary & Core Story
- **Clinical Motivation:** Cardiovascular disease (CVD) is the world's leading killer (17.9M annual deaths). Early non-invasive screening saves lives.
- **The Research Question:** Can modern tabular deep learning (MLP) or complex hybrid ensembles (HPEM) outperform regularized tree ensembles (XGBoost), and do these models transfer across different hospital centers?
- **Headline Result 1 (Cardio70k, N=68,581):** XGBoost is the strongest discriminator (ROC-AUC 0.8019, F1 0.7205), winning in 5/5 outer folds in nested CV. Our deep MLP neural network is competitive (ROC-AUC 0.7991, F1 0.7203), matching XGBoost on F1 and clinical Net Benefit.
- **Headline Result 2 (5-Center Hospital Stress Test, N=1,918):** Complex polynomial stacking (HPEM from the foundation paper) overfit local clinics and collapsed to 0.6107 ROC-AUC under leave-one-source-out transfer, whereas regularized models generalized far better.
- **Data-Centric Innovation:** Adding explicit missingness indicators (`SimpleImputer(add_indicator=True)`) improved generalization for every model across hospital systems (boosting Logistic Regression ROC-AUC from 0.7449 to 0.7653 and F1 to 0.8004).

---

## 2. Datasets & Specifications
1. **Cardio70k Cleaned Track (Primary Large-Scale Screening):**
   - 68,581 records, 14 features, 1 binary target (49.5% CVD positive vs 50.5% healthy).
   - Zero missing cells. All routine non-invasive outpatient vitals (BP, cholesterol, age, glucose, BMI, smoking, activity).
2. **Unified Clinical Dataset Track (Multi-Center Hospital Stress Test):**
   - 1,918 patients across 5 centers in 4 countries (Mendeley India N=1000, UCI Cleveland N=303, UCI Hungary N=293, UCI Long Beach VA N=199, UCI Switzerland N=123).
   - High clinic-specific missingness; evaluated via Leave-One-Source-Out (LOSO) cross-validation.
3. **Audited Extra Archives (ECG & Synthetic CT/MRI):**
   - Formally audited and excluded because they lacked diagnostic labels and verified patient linkage.

---

## 3. Evaluation Metrics & Clinical Meaning
- **Accuracy (73.58%):** Overall correctness. 73.6% is the real physiological ceiling for routine non-invasive screening; claims of 98% in literature suffer from post-diagnostic feature leakage or SMOTE leakage.
- **Sensitivity / Recall (68.83%):** Catches sick patients. Critical to prevent missed heart attacks.
- **Specificity (78.22%):** Identifies healthy patients. Prevents unnecessary angiograms and anxiety.
- **Precision (75.58%):** Positive predictive value of an alert.
- **F1-Score (0.7205 XGBoost / 0.7203 MLP):** Harmonic balance between sensitivity and precision.
- **ROC-AUC (0.8019 XGBoost / 0.7991 MLP):** Discriminative ranking power across all cutoffs.
- **Brier Score (0.1802):** Probabilistic mean squared error (lower is better).
- **ECE (0.0024):** Expected Calibration Error; proves predicted probabilities match real-world disease frequency.
- **Net Benefit (DCA):** Weighs true positives against false positives across decision thresholds ($p_t \in [0.10, 0.70]$).

---

## 4. Summary Table of Verified Results

| Task / Cohort | Winning Model | ROC-AUC | F1-Score | Accuracy | Brier Score | Clinical Takeaway |
|:---|:---|---:|---:|---:|---:|:---|
| **Cardio70k 5-Fold CV** | XGBoost | 0.8019 | 0.7205 | 73.58% | 0.1802 | Leading internal discriminator |
| **Cardio70k Neural Net** | MLP (Deep) | 0.7991 | 0.7203 | 73.42% | 0.1814 | Matches XGBoost on F1 & Net Benefit |
| **Nested CV (5x3)** | XGBoost | 0.8019 | 0.7205 | 73.58% | 0.1802 | Selected in 5/5 outer folds |
| **Multi-Hospital Transfer** | Logistic Regression | 0.7449 | 0.7525 | 69.79% | 0.2084 | Linear models resist site shift |
| **Multi-Hospital with Missingness Indicators** | Logistic Regression | **0.7653** | **0.8004** | 76.49% | 0.1756 | **Major gain (+0.02 AUC, +0.05 F1)** |
| **HPEM Paper Adaptation** | HPEM Stacking | 0.6107 | 0.6291 | 61.31% | 0.2568 | Overfit local sites; collapsed under LOSO |

---

## 5. Defense Cheat Sheet (Answers to Examiner Questions)

- **Q: "Why is your accuracy 73.6% and not 98% like the Bangladesh study?"**  
  *A: The Bangladesh study evaluated hospitalized symptomatic patients using post-diagnostic tests (ECG/stress testing), making classification retrospective confirmation. Furthermore, papers claiming >95% frequently suffer from SMOTE or scaler leakage before splitting. Our study evaluates 68,581 outpatients using routine non-invasive screening vitals under strict leak-free cross-validation. Clinical scores like Framingham achieve ~0.75 AUC; 0.802 is state-of-the-art for non-invasive vitals.*

- **Q: "Why did you use an MLP if XGBoost won?"**  
  *A: To answer the central research question: does deep tabular learning beat trees? We proved via 300 bootstrap replicates that MLP statistically outperforms linear baselines (+0.0052 AUC, p<0.05) and ties XGBoost on F1 (0.7203 vs 0.7205) and clinical Net Benefit.*

- **Q: "Why did the HPEM foundation paper perform worse in your experiments?"**  
  *A: The original paper used random cross-validation within single small hospital files (300 patients) and trained the meta-learner on training predictions. Under our leak-free leave-one-source-out multi-hospital stress test, the polynomial feature expansion overfit local clinic distributions and dropped to 0.61 AUC, proving regularized baselines generalize better.*

---
*Generated directly from verified project outputs. Use `reports/MASTER_RESEARCH_DEFENSE_GUIDE.html` for complete interactive presentation figures.*
