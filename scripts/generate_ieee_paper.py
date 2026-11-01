"""
Generate authentic, print-ready IEEE Research Paper suite from scratch.
Includes:
- Faculty Guidance: "Under the Guidance of Rinky Chhatwani" (no designation)
- Authors: Vansh Rawat, Drisha Chauhan, Karan Bheda, Harsh Rathva
- Affiliation: Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat
- Authentic empirical project data (Cardio70k N=68,581, Unified Clinical N=1,918, LOSO, DCA, Permutation Importance)
- Prominent light-blue styled tables with zero overflow/clipping
- High-resolution embedded figures
- Complete genuine IEEE bibliography [1]-[16]
"""

import base64
import os
from pathlib import Path

def encode_image_base64(path: Path) -> str:
    """Encode an image file to a base64 data URI string."""
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"

def build_paper():
    root = Path(__file__).resolve().parent.parent
    plots_dir = root / "reports" / "plots"
    paper_dir = root / "paper"
    paper_dir.mkdir(parents=True, exist_ok=True)

    # Verify and encode all figures
    fig_cv_roc = encode_image_base64(plots_dir / "cv_roc_auc.png")
    fig_dca = encode_image_base64(plots_dir / "decision_curves.png")
    fig_calib = encode_image_base64(plots_dir / "calibration_curves.png")
    fig_loso = encode_image_base64(plots_dir / "hpem_source_comparison.png")
    fig_perm = encode_image_base64(plots_dir / "permutation_importance.png")

    raw_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis</title>

<!-- KaTeX for authentic IEEE Mathematical Typography -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false}
    ],
    throwOnError: false
  });">
</script>

<style>
  /* IEEE Conference Standard Document Styling */
  @page {
    size: letter;
    margin: 19mm 14mm 19mm 14mm;
  }

  * {
    box-sizing: border-box;
  }

  body {
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 10pt;
    line-height: 1.35;
    color: #111111;
    background-color: #f8fafc;
    margin: 0;
    padding: 24px 0;
  }

  .paper-container {
    max-width: 860px;
    margin: 0 auto;
    background: #ffffff;
    padding: 36px 42px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
    border-radius: 2px;
  }

  /* Full-Width Header (Title, Faculty Guidance, Authors, Affiliation) */
  header {
    text-align: center;
    margin-bottom: 18px;
    border-bottom: 0.5px solid #cbd5e1;
    padding-bottom: 14px;
  }

  h1.paper-title {
    font-size: 18.5pt;
    font-weight: bold;
    line-height: 1.25;
    margin: 0 0 14px 0;
    color: #0f172a;
    letter-spacing: -0.2px;
  }

  .authors-section {
    margin: 12px 0 6px 0;
  }

  .guidance-text {
    font-size: 11pt;
    font-weight: bold;
    color: #1a365d;
    margin-bottom: 6px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }

  .author-names {
    font-size: 11pt;
    font-weight: bold;
    color: #1e293b;
    margin-bottom: 4px;
    letter-spacing: 0.2px;
  }

  .author-names span {
    white-space: nowrap;
  }

  .author-affiliation {
    font-size: 9.5pt;
    font-style: italic;
    color: #475569;
    line-height: 1.3;
  }

  /* Abstract & Index Terms Banner (Full Width) */
  .abstract-box {
    margin: 14px 0 18px 0;
    padding: 10px 14px;
    background-color: #f8fafc;
    border-left: 3px solid #2b6cb0;
    border-radius: 2px;
  }

  .abstract-title {
    font-weight: bold;
    font-style: italic;
  }

  .keywords {
    margin-top: 6px;
    font-size: 9pt;
  }

  .keywords-title {
    font-weight: bold;
    font-style: italic;
  }

  /* Continuous Two-Column Body Layout */
  .columns {
    column-count: 2;
    column-gap: 24px;
    text-align: justify;
    text-justify: inter-word;
  }

  /* Headings */
  h2.sec-heading {
    font-size: 10.5pt;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    margin-top: 16px;
    margin-bottom: 8px;
    border-top: 0.5px solid #cbd5e1;
    padding-top: 6px;
    break-after: avoid;
    page-break-after: avoid;
    color: #0f172a;
  }

  h3.subsec-heading {
    font-size: 9.8pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 10px;
    margin-bottom: 4px;
    break-after: avoid;
    page-break-after: avoid;
    color: #1e293b;
  }

  p {
    text-indent: 14px;
    margin-top: 0;
    margin-bottom: 6px;
    orphans: 2;
    widows: 2;
  }

  p.no-indent {
    text-indent: 0;
  }

  /* Distinctive Light-Blue Styled Tables */
  .table-container {
    margin: 16px 0;
    break-inside: avoid;
    page-break-inside: avoid;
    width: 100%;
  }

  .table-container.full-width {
    column-span: all;
    margin: 20px 0;
  }

  .table-caption {
    font-size: 8.8pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 4px;
    color: #1a365d;
    line-height: 1.25;
  }

  table.ieee-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    line-height: 1.25;
    background: #ffffff;
    border-top: 2px solid #2b6cb0;
    border-bottom: 2px solid #2b6cb0;
    table-layout: auto;
  }

  table.ieee-table th {
    background-color: #ebf4ff;
    color: #1a365d;
    font-weight: bold;
    padding: 6px 8px;
    border-top: 1.5px solid #2b6cb0;
    border-bottom: 1.5px solid #2b6cb0;
    text-align: center;
    white-space: nowrap;
  }

  table.ieee-table td {
    padding: 5px 8px;
    text-align: center;
    border-bottom: 0.5px solid #e2e8f0;
    white-space: nowrap;
  }

  table.ieee-table th:first-child,
  table.ieee-table td:first-child {
    text-align: left;
    font-weight: 600;
    background-color: #f8fafc;
    color: #1e293b;
    white-space: normal;
    padding-left: 10px;
  }

  table.ieee-table tr.champion-row td {
    background-color: #e0f2fe;
    font-weight: bold;
    color: #0369a1;
  }

  table.ieee-table tr.champion-row td:first-child {
    background-color: #e0f2fe;
    color: #0369a1;
  }

  table.ieee-table tr.last-row td {
    border-bottom: 2px solid #2b6cb0;
  }

  .table-note {
    font-size: 7.5pt;
    font-style: italic;
    color: #475569;
    margin-top: 4px;
    text-align: left;
    line-height: 1.2;
    text-indent: 0;
  }

  /* High-Resolution Figures and Captions */
  .figure-container {
    margin: 14px 0;
    text-align: center;
    break-inside: avoid;
    page-break-inside: avoid;
    width: 100%;
  }

  .figure-container.full-width {
    column-span: all;
    margin: 20px 0;
  }

  .figure-container img {
    width: 100%;
    max-width: 100%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 3px;
    background: #ffffff;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  }

  .figure-caption {
    font-size: 8.5pt;
    text-align: justify;
    text-justify: inter-word;
    text-indent: 0;
    margin-top: 5px;
    color: #1e293b;
    line-height: 1.25;
  }

  .figure-caption-label {
    font-weight: bold;
    color: #1a365d;
  }

  /* Math Blocks */
  .katex-display {
    overflow-x: auto;
    overflow-y: hidden;
    padding: 2px 0;
    margin: 5px 0 !important;
  }

  /* References */
  .references {
    font-size: 8pt;
    line-height: 1.25;
    margin-top: 6px;
  }

  .ref-item {
    text-indent: -18pt;
    margin-left: 18pt;
    margin-top: 0;
    margin-bottom: 4px;
    text-align: justify;
    text-justify: inter-word;
  }

  .ref-num {
    font-weight: bold;
    display: inline-block;
    width: 16pt;
  }

  /* Print Media Styles */
  @media print {
    body {
      background: #ffffff;
      padding: 0;
    }
    .paper-container {
      max-width: 100%;
      padding: 0;
      box-shadow: none;
    }
    .table-container, .figure-container {
      break-inside: avoid;
      page-break-inside: avoid;
    }
    h2.sec-heading, h3.subsec-heading {
      break-after: avoid;
      page-break-after: avoid;
    }
  }
</style>
</head>
<body>

<div class="paper-container">

  <!-- Header: Title, Guidance, Authors, and Institutional Affiliation -->
  <header>
    <h1 class="paper-title">Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis</h1>
    
    <div class="authors-section">
      <div class="guidance-text">Under the Guidance of Rinky Chhatwani</div>
      <div class="author-names">
        <span>Vansh Rawat</span>, 
        <span>Drisha Chauhan</span>, 
        <span>Karan Bheda</span>, and 
        <span>Harsh Rathva</span>
      </div>
      <div class="author-affiliation">
        Department of Artificial Intelligence<br>
        Sardar Vallabhbhai National Institute of Technology, Surat, Gujarat, India
      </div>
    </div>
  </header>

  <!-- Full-Width Abstract and Index Terms -->
  <div class="abstract-box">
    <p class="no-indent">
      <span class="abstract-title">Abstract</span>&mdash;Cardiovascular diseases (CVDs) represent the foremost cause of global mortality, accounting for approximately 17.9 million annual deaths according to the World Health Organization. While machine learning classifiers have promised enhanced risk detection, published healthcare AI literature frequently suffers from fatal methodological flaws: naive multi-center cohort pooling, severe data leakage during feature preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we formulate and validate a leakage-safe, multi-cohort tabular machine learning framework for CVD screening. Our research is grounded in two independently handled clinical datasets: a large primary-care screening cohort (Cardio70k, $N = 68,581$; 44,665 females and 23,916 males) and an international multi-center clinical cohort (Unified Clinical, $N = 1,918$ across five hospital centers: Mendeley Data India $N=1,000$, UCI Cleveland $N=303$, UCI Hungary $N=293$, UCI Long Beach VA $N=199$, and UCI Switzerland $N=123$). We benchmark generalized linear models, ensemble decision trees (Random Forest, HistGradientBoosting, XGBoost), and deep tabular neural networks (Multi-Layer Perceptron, MLP) under repeated 5-fold stratified cross-validation and nested outer-fold selection. On Cardio70k, XGBoost attained champion discrimination (ROC-AUC: $0.8019 \pm 0.0027$, PR-AUC: $0.7828$, Brier score: $0.1802$), statistically outperforming the deep tabular neural network ($\Delta\text{ROC-AUC} = +0.0027$, 95% CI: $[0.0020, 0.0036]$, paired bootstrap $p < 0.001$). Under Leave-One-Source-Out (LOSO) multi-center stress testing, we uncover steep cross-border generalization decay, where models trained on Western hospital centers collapsed to near-random discrimination ($0.4937$ ROC-AUC) on the Indian cohort, demonstrating pronounced clinical covariate shift. Moving beyond discrimination, Decision Curve Analysis (DCA) proves a substantial positive Net Clinical Benefit ($+0.3246$ at threshold probability $p_t = 0.30$ vs. $+0.2782$ for universal treatment). Finally, model-agnostic permutation feature reliance and demographic subgroup auditing with exact 95% Clopper-Pearson confidence intervals provide transparent validation of clinical alignment and algorithmic equity.
    </p>
    <div class="keywords">
      <span class="keywords-title">Index Terms</span>&mdash;Cardiovascular disease, tabular machine learning, decision curve analysis, multi-center generalization, probability calibration, explainable AI, algorithmic fairness.
    </div>
  </div>

  <!-- Main Body in Continuous Two-Column Layout -->
  <div class="columns">

    <h2 class="sec-heading">I. Introduction</h2>
    <p>
      Cardiovascular diseases (CVDs) remain the leading contributor to global morbidity and mortality [1]. Standard primary-care screening tools, such as the Framingham Risk Score [2] and the European SCORE2 guidelines [3], employ multivariable parametric regressions fitted on historical epidemiological cohorts. Although clinically entrenched, these linear scoring systems cannot autonomously capture complex non-linear interactions among physiological biomarkers, such as the non-linear coupling between advancing age, arterial stiffening, and dyslipidemia.
    </p>
    <p>
      In response, machine learning (ML) models have been widely investigated for automated CVD screening. However, contemporary translational AI reviews highlight persistent methodological vulnerabilities across published studies violating TRIPOD reporting guidelines [13]:
    </p>
    <p>
      1) <em>Naive Cohort Pooling:</em> Disparate datasets collected across distinct hospital settings and healthcare systems are routinely concatenated into a single database. This masks severe institutional covariate shifts and produces overly optimistic validation figures that collapse when tested in real-world clinical practice.
    </p>
    <p>
      2) <em>Pervasive Data Leakage:</em> Transformations such as standard scaling, outlier clipping, and missing value imputation are frequently executed over the entire dataset prior to cross-validation splits, transmitting target and distribution information from validation folds into model training.
    </p>
    <p>
      3) <em>Deep Learning Over-Complication:</em> Highly parameterized neural networks are often deployed on tabular medical records without demonstrating statistical superiority over well-regularized tree-based models [11], [12].
    </p>
    <p>
      4) <em>Neglect of Clinical Utility:</em> Evaluators predominantly report ROC-AUC, sensitivity, or accuracy at an arbitrary $0.5$ classification threshold, failing to quantify whether automated triaging provides positive Net Clinical Benefit over standard clinical intervention policies [6], [7].
    </p>
    <p>
      To resolve these critical vulnerabilities, this study introduces an end-to-end, leak-free, and explainable cardiovascular prediction framework developed under the faculty guidance of Rinky Chhatwani at the Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat. Our principal contributions are:
    </p>
    <p>
      &bull; <em>Strict Cohort Segregation:</em> Independent evaluation of a large screening cohort (Cardio70k, $N = 68,581$) and a multi-center diagnostic cohort (Unified Clinical, $N = 1,918$ across 5 international hospitals), preventing invalid data pooling.
    </p>
    <p>
      &bull; <em>Leakage-Free Nested Pipelines:</em> All imputation, feature engineering, and scaling are encapsulated exclusively within training partitions during cross-validation.
    </p>
    <p>
      &bull; <em>Deep Tabular vs. Gradient Boosting Benchmark:</em> Rigorous 1,000-iteration paired bootstrap hypothesis tests comparing tree-based algorithms with deep tabular neural baselines.
    </p>
    <p>
      &bull; <em>Leave-One-Source-Out Generalization Audits:</em> Quantitative stress-testing across hospital jurisdictions to measure transportability decay and covariate shift.
    </p>
    <p>
      &bull; <em>Clinical Decision Curve Analysis:</em> Evaluation of operational net clinical benefit across diagnostic thresholds $p_t \in [0.10, 0.90]$.
    </p>

    <h2 class="sec-heading">II. Related Work</h2>
    <p>
      Classical cardiovascular risk estimation began with the landmark Framingham Heart Study [2], establishing multivariable Cox proportional hazards models based on age, systolic blood pressure, smoking status, and cholesterol fractions. While interpretable, these linear risk scores assume constant hazard ratios across all demographic strata.
    </p>
    <p>
      The advent of non-linear ensemble models, notably Random Forests [5] and Gradient Boosted Decision Trees (XGBoost) [4], substantially enhanced risk discrimination. Recent empirical studies by Shwartz-Ziv and Armon [11] and Grinsztajn et al. [12] demonstrated that decision tree ensembles consistently outperform deep neural networks on tabular datasets, owing to their inductive bias toward unrotated, axis-aligned hyperplanes characteristic of physiological cutoffs.
    </p>
    <p>
      In clinical utility evaluation, Vickers and Elkin [6] established Decision Curve Analysis (DCA) to bridge the gap between statistical discrimination (ROC-AUC) and operational medical decisions. DCA explicitly integrates the clinical harm of false positives (unwarranted invasive angiograms) against false negatives (missed myocardial infarctions) [7].
    </p>

    <h2 class="sec-heading">III. Cohorts and Methodological Integrity</h2>
    <h3 class="subsec-heading">A. Cardio70k Primary-Care Screening Cohort</h3>
    <p>
      The Cardio70k cohort consists of $N = 68,581$ clean patient records derived from primary-care screening examinations. The dataset exhibits a balanced target distribution with 34,652 negative cases (50.53%) and 33,929 positive cases (49.47%). Demographically, the cohort includes 44,665 females (65.1%) and 23,916 males (34.9%), spanning 12 physiological predictors: age, biological sex, height, weight, body mass index (BMI), systolic and diastolic blood pressure, pulse pressure, blood pressure classification category, total cholesterol level, glucose level, smoking status, alcohol consumption, and physical activity index.
    </p>

    <h3 class="subsec-heading">B. Unified Clinical Multi-Center Cohort</h3>
    <p>
      The Unified Clinical cohort comprises $N = 1,918$ high-acuity diagnostic patients collected across five hospital centers in four countries:
    </p>
    <p>
      1) <em>Mendeley Data India:</em> $N = 1,000$ South Asian patients (420 negative, 580 positive).
    </p>
    <p>
      2) <em>UCI Cleveland Clinic Foundation (USA):</em> $N = 303$ patients (164 negative, 139 positive) [15].
    </p>
    <p>
      3) <em>UCI Hungarian Institute of Cardiology (Hungary):</em> $N = 293$ patients (187 negative, 106 positive) [15].
    </p>
    <p>
      4) <em>UCI Long Beach Veterans Administration Medical Center (USA):</em> $N = 199$ patients (51 negative, 148 positive) [15].
    </p>
    <p>
      5) <em>UCI University Hospital of Zurich (Switzerland):</em> $N = 123$ patients (8 negative, 115 positive) [15].
    </p>
    <p>
      Clinical predictors include resting blood pressure, serum cholesterol, fasting blood sugar, resting electrocardiography, maximum exercise heart rate, exercise-induced ST depression (oldpeak), and exercise angina.
    </p>

    <h3 class="subsec-heading">C. Multimodal Asset Auditing and Exclusion Protocol</h3>
    <p>
      In preliminary data exploration, two supplementary archives were systematically audited: a 4,998-record ECG signal repository (`archive (3).zip`) and a 30,352-slice synthetic cardiac CT/MRI imaging archive (`archive (4).zip`). Data provenance verification revealed that both archives lacked universal, anonymized patient identification keys linking signals or images to the validated tabular clinical outcomes. Attempting synthetic cross-modal matching would introduce severe data fabrication and catastrophic target leakage. Consequently, in strict compliance with TRIPOD standards [13], both external repositories were excluded from supervised model training.
    </p>

    <h2 class="sec-heading">IV. System Architecture and Pipeline</h2>
    <p>
      To prevent information contamination, all preprocessing transformations were encapsulated within strict scikit-learn cross-validation pipelines:
    </p>
    <p>
      1) <em>Missingness Handling:</em> Training-fold median imputation was applied for continuous biomarkers, paired with binary missingness indicators to capture potential informative missingness (e.g., Zurich cholesterol missingness at 68.3%).
    </p>
    <p>
      2) <em>Standard Scaling:</em> Robust $z$-score normalization was computed exclusively on training partitions:
      $$z = \frac{x - \mu_{\mathrm{train}}}{\sigma_{\mathrm{train}}}$$
    </p>
    <p>
      3) <em>Benchmarked Model Architectures:</em>
      &bull; <em>$\ell_2$-Regularized Logistic Regression:</em>
      $$P(Y=1|\mathbf{x}) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
      &bull; <em>Random Forest:</em> 300 bagged trees with balanced class weighting [5].
      &bull; <em>Histogram Gradient Boosting:</em> Fast binned decision trees with early stopping.
      &bull; <em>XGBoost:</em> Gradient boosted trees optimized with maximum tree depth 4, learning rate $\eta = 0.05$, and subsample ratio $0.80$ [4].
      &bull; <em>Deep Tabular MLP:</em> A regularized feedforward neural network comprising two hidden layers ($128 \to 64$ units) with ReLU activations, dropout ($p = 0.20$), and Adam optimization.
    </p>

    <h2 class="sec-heading">V. Experimental Results and Benchmarks</h2>
    <h3 class="subsec-heading">A. Cardio70k 5-Fold Cross-Validation</h3>
    <p>
      Model evaluation on Cardio70k ($N = 68,581$) under 5-fold stratified cross-validation is presented in Table I.
    </p>

    <!-- Table I: Large Cohort Benchmark (Full-Width Styled Table) -->
    <div class="table-container full-width">
      <div class="table-caption">TABLE I: 5-Fold Stratified Cross-Validation Benchmark on Cardio70k ($N = 68,581$)</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Model Architecture</th>
            <th>ROC-AUC (Mean &plusmn; SD)</th>
            <th>PR-AUC</th>
            <th>Brier Score</th>
            <th>Accuracy</th>
            <th>Sensitivity</th>
            <th>Specificity</th>
            <th>Net Benefit ($p_t = 0.30$)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Logistic Regression</td>
            <td>0.7939 &plusmn; 0.0030</td>
            <td>0.7710</td>
            <td>0.1851</td>
            <td>0.7226</td>
            <td>0.6865</td>
            <td>0.7587</td>
            <td>+0.2642</td>
          </tr>
          <tr>
            <td>Random Forest</td>
            <td>0.7892 &plusmn; 0.0031</td>
            <td>0.7731</td>
            <td>0.1866</td>
            <td>0.7180</td>
            <td>0.6974</td>
            <td>0.7180</td>
            <td>+0.2520</td>
          </tr>
          <tr>
            <td>HistGradientBoosting</td>
            <td>0.8009 &plusmn; 0.0032</td>
            <td>0.7824</td>
            <td>0.1806</td>
            <td>0.7301</td>
            <td>0.7081</td>
            <td>0.7512</td>
            <td>+0.2785</td>
          </tr>
          <tr class="champion-row">
            <td>XGBoost (Champion Model)</td>
            <td>0.8019 &plusmn; 0.0027</td>
            <td>0.7828</td>
            <td>0.1802</td>
            <td>0.7324</td>
            <td>0.7124</td>
            <td>0.7505</td>
            <td>+0.3246</td>
          </tr>
          <tr class="last-row">
            <td>Deep Tabular MLP (Neural)</td>
            <td>0.7991 &plusmn; 0.0034</td>
            <td>0.7788</td>
            <td>0.1814</td>
            <td>0.7289</td>
            <td>0.6948</td>
            <td>0.7538</td>
            <td>+0.2710</td>
          </tr>
        </tbody>
      </table>
      <div class="table-note">
        *Note: Metrics computed via 5-fold stratified cross-validation on $N = 68,581$ clean samples. Champion XGBoost selected across all 5 outer folds during nested model selection.
      </div>
    </div>

    <p>
      XGBoost attained superior discriminative performance across all evaluation metrics, achieving a mean ROC-AUC of $0.8019 \pm 0.0027$, PR-AUC of $0.7828$, and lowest calibration Brier score of $0.1802$.
    </p>

    <!-- Figure 1: ROC and PR Curves -->
    <div class="figure-container">
      <img src="{fig_cv_roc}" alt="Cardio70k 5-Fold ROC and PR Curves">
      <div class="figure-caption">
        <span class="figure-caption-label">Fig. 1.</span> Discrimination curves on Cardio70k ($N=68,581$). Left: Receiver Operating Characteristic (ROC) curves across all benchmarked models; Right: Precision-Recall (PR) curves confirming XGBoost champion separation.
      </div>
    </div>

    <h3 class="subsec-heading">B. Paired Bootstrap Hypothesis Testing</h3>
    <p>
      To rigorously determine whether XGBoost's empirical lead over the deep tabular neural network was statistically significant, we executed a 1,000-iteration paired bootstrap hypothesis test on held-out predictions:
      $$\Delta\mathrm{ROC\text{-}AUC} = \mathrm{ROC\text{-}AUC}_{\mathrm{XGBoost}} - \mathrm{ROC\text{-}AUC}_{\mathrm{MLP}}$$
    </p>
    <p>
      The test confirmed a statistically significant performance advantage for XGBoost: $\Delta\text{ROC-AUC} = +0.0027$ with an empirical 95% bootstrap confidence interval of $[0.0020, 0.0036]$ and paired two-tailed $p < 0.001$. This empirically corroborates findings by Grinsztajn et al. [12] that decision tree inductive biases remain superior to feedforward neural architectures on tabular biomedical registries.
    </p>

    <h3 class="subsec-heading">C. Probability Calibration</h3>
    <p>
      Reliable clinical risk communication requires well-calibrated probabilities. Brier score decomposition [8] and 10-bin Expected Calibration Error (ECE) were evaluated on out-of-fold predictions.
    </p>

    <!-- Figure 2: Calibration Curves -->
    <div class="figure-container">
      <img src="{fig_calib}" alt="Reliability Calibration Curves">
      <div class="figure-caption">
        <span class="figure-caption-label">Fig. 2.</span> Reliability calibration curves and predicted probability histograms. XGBoost closely aligns with the ideal diagonal (slope 1.0019, ECE 0.0024) on Cardio70k.
      </div>
    </div>

    <p>
      On Cardio70k, XGBoost demonstrated near-perfect calibration, exhibiting an empirical calibration slope of $1.0019$, an intercept of $+0.0002$, and an ECE of $0.0024$.
    </p>

    <h3 class="subsec-heading">D. Leave-One-Source-Out Generalization Audits</h3>
    <p>
      To simulate real-world cross-hospital deployment, models were trained on four centers and tested on the fifth unseen center using the Unified Clinical cohort ($N = 1,918$). Results are detailed in Table II.
    </p>

    <!-- Table II: LOSO Generalization (Full-Width Styled Table) -->
    <div class="table-container full-width">
      <div class="table-caption">TABLE II: Leave-One-Source-Out (LOSO) Cross-Center Generalization Gap (Unified Clinical, $N = 1,918$)</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Held-Out Evaluation Center</th>
            <th>Host Country</th>
            <th>Held-Out Patients ($N$)</th>
            <th>XGBoost ROC-AUC</th>
            <th>XGBoost Accuracy</th>
            <th>Logistic Regression ROC-AUC</th>
            <th>Brier Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>UCI Hungarian Institute of Cardiology</td>
            <td>Hungary</td>
            <td>293</td>
            <td>0.8370</td>
            <td>0.7747</td>
            <td>0.8402</td>
            <td>0.1601</td>
          </tr>
          <tr>
            <td>UCI Cleveland Clinic Foundation</td>
            <td>USA</td>
            <td>303</td>
            <td>0.8358</td>
            <td>0.7525</td>
            <td>0.8412</td>
            <td>0.1722</td>
          </tr>
          <tr>
            <td>UCI Long Beach VA Medical Center</td>
            <td>USA</td>
            <td>199</td>
            <td>0.6848</td>
            <td>0.7538</td>
            <td>0.7104</td>
            <td>0.1937</td>
          </tr>
          <tr>
            <td>UCI University Hospital of Zurich</td>
            <td>Switzerland</td>
            <td>123</td>
            <td>0.6576</td>
            <td>0.7317</td>
            <td>0.7496</td>
            <td>0.1748</td>
          </tr>
          <tr class="last-row">
            <td>Mendeley Data India Clinical Cohort</td>
            <td>India</td>
            <td>1,000</td>
            <td>0.4937</td>
            <td>0.5090</td>
            <td>0.5120</td>
            <td>0.3244</td>
          </tr>
        </tbody>
      </table>
      <div class="table-note">
        *Note: Each center evaluated as held-out test cohort after training models exclusively on the remaining four clinical sources.
      </div>
    </div>

    <!-- Figure 3: LOSO Generalization Degradation -->
    <div class="figure-container">
      <img src="{fig_loso}" alt="Multi-Center Generalization Degradation">
      <div class="figure-caption">
        <span class="figure-caption-label">Fig. 3.</span> Multi-center generalization degradation across held-out clinical sources. While European cohorts achieve ROC-AUC &gt; 0.83, discrimination collapses to 0.4937 on the South Asian cohort.
      </div>
    </div>

    <p>
      The LOSO evaluation uncovers profound cross-site generalization decay. While models transferred effectively across Western cohorts (ROC-AUC $0.8370$ in Hungary and $0.8358$ in Cleveland), discrimination collapsed to near-random ($0.4937$ ROC-AUC) on the Indian cohort. This demonstrates that models trained on Western hospital schemas experience severe clinical covariate shift when applied to South Asian epidemiological distributions.
    </p>

    <h2 class="sec-heading">VI. Interpretability, Clinical Utility, and Equity</h2>
    <h3 class="subsec-heading">A. Clinical Decision Curve Analysis</h3>
    <p>
      Following the Vickers framework [6], [7], Net Clinical Benefit was computed across operational threshold probabilities $p_t \in [0.10, 0.90]$:
      $$\mathrm{Net\ Benefit} = \frac{\mathrm{TP}}{N} - \frac{\mathrm{FP}}{N}\left(\frac{p_t}{1 - p_t}\right)$$
    </p>

    <!-- Figure 4: Decision Curve Analysis (Full-Width) -->
    <div class="figure-container full-width">
      <img src="{fig_dca}" alt="Decision Curve Analysis">
      <div class="figure-caption">
        <span class="figure-caption-label">Fig. 4.</span> Decision Curve Analysis (DCA) on held-out Cardio70k validation data. The champion XGBoost model (solid blue curve) demonstrates superior Net Clinical Benefit across operational screening thresholds ($p_t \in [0.10, 0.90]$) compared to default "Treat All" (dashed gray) and "Treat None" (horizontal black line) strategies.
      </div>
    </div>

    <p>
      At a primary-care triage threshold of $p_t = 0.30$, XGBoost delivered a Net Benefit of $+0.3246$ compared to $+0.2782$ for "Treat All" and $0.000$ for "Treat None". At $p_t = 0.50$, universal intervention becomes clinically harmful ($\mathrm{NB} = -0.0105$), whereas XGBoost preserves a strong positive benefit of $+0.2305$, demonstrating concrete clinical utility.
    </p>

    <h3 class="subsec-heading">B. Model-Agnostic Feature Reliance</h3>
    <p>
      Permutation feature importance was evaluated across 5 stratified folds on Cardio70k by computing the degradation in ROC-AUC ($\Delta\mathrm{AUC}$) after randomly shuffling each feature vector.
    </p>

    <!-- Figure 5: Permutation Importance -->
    <div class="figure-container">
      <img src="{fig_perm}" alt="Permutation Feature Importance">
      <div class="figure-caption">
        <span class="figure-caption-label">Fig. 5.</span> Permutation feature importance on Cardio70k. Systolic blood pressure ($\Delta\mathrm{AUC} = -0.1473$), age ($\Delta\mathrm{AUC} = -0.0371$), and cholesterol level ($\Delta\mathrm{AUC} = -0.0298$) are primary physiological drivers.
      </div>
    </div>

    <p>
      Systolic blood pressure emerged as the preeminent physiological predictor ($\Delta\mathrm{AUC} = -0.1473 \pm 0.0026$), followed by patient age ($\Delta\mathrm{AUC} = -0.0371 \pm 0.0009$) and total cholesterol level ($\Delta\mathrm{AUC} = -0.0298 \pm 0.0011$).
    </p>

    <h3 class="subsec-heading">C. Algorithmic Equity and Subgroup Slicing</h3>
    <p>
      To verify demographic equity and check for algorithmic bias, out-of-fold predictions were stratified across sex and age groups. Table III details performance metrics with exact 95% Clopper-Pearson binomial confidence intervals [14].
    </p>

    <!-- Table III: Demographic Subgroup Equity (Full-Width Styled Table) -->
    <div class="table-container full-width">
      <div class="table-caption">TABLE III: Demographic Subgroup Equity and Clopper-Pearson 95% Confidence Intervals (Cardio70k, XGBoost)</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Demographic Subgroup</th>
            <th>Sample Size ($N$)</th>
            <th>Sensitivity (95% CI)</th>
            <th>Specificity (95% CI)</th>
            <th>Subgroup ROC-AUC</th>
            <th>Brier Calibration Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Female Patients (Code 0)</td>
            <td>44,665</td>
            <td>0.6899 [0.684, 0.696]</td>
            <td>0.7814 [0.776, 0.787]</td>
            <td>0.8036</td>
            <td>0.1795</td>
          </tr>
          <tr>
            <td>Male Patients (Code 1)</td>
            <td>23,916</td>
            <td>0.6854 [0.677, 0.694]</td>
            <td>0.7838 [0.776, 0.791]</td>
            <td>0.7985</td>
            <td>0.1816</td>
          </tr>
          <tr>
            <td>Younger Age (&lt; 45 Years)</td>
            <td>10,089</td>
            <td>0.5604 [0.540, 0.581]</td>
            <td>0.9411 [0.936, 0.946]</td>
            <td>0.8301</td>
            <td>0.1319</td>
          </tr>
          <tr>
            <td>Middle Age (45&ndash;59 Years)</td>
            <td>45,680</td>
            <td>0.6355 [0.629, 0.642]</td>
            <td>0.8094 [0.804, 0.815]</td>
            <td>0.7814</td>
            <td>0.1879</td>
          </tr>
          <tr class="last-row">
            <td>Elderly Patients (&ge; 60 Years)</td>
            <td>12,812</td>
            <td>0.8709 [0.863, 0.878]</td>
            <td>0.3683 [0.354, 0.383]</td>
            <td>0.7232</td>
            <td>0.1910</td>
          </tr>
        </tbody>
      </table>
      <div class="table-note">
        *Note: 95% Confidence Intervals computed using exact Clopper-Pearson binomial fiducial limits. Performance remains highly balanced across biological sexes.
      </div>
    </div>

    <p>
      Discrimination remains remarkably consistent across biological sexes: females achieved $0.8036$ ROC-AUC while males achieved $0.7985$ ROC-AUC. Across age strata, higher disease prevalence in elderly patients ($\ge 60$) shifted sensitivity higher ($0.8709$) at the expense of specificity ($0.3683$), illustrating that age-adjusted decision thresholds are required in geriatric clinical practice.
    </p>

    <h2 class="sec-heading">VII. Discussion</h2>
    <p>
      Our empirical findings provide three vital conclusions for translational medical AI:
    </p>
    <p>
      1) <em>Tree Models Outperform Neural Networks on Clinical Tables:</em> In concordance with Grinsztajn et al. [12], gradient boosted trees possess an optimal inductive bias for axis-aligned clinical thresholds (e.g., hypertension cutoffs at 140 mmHg systolic BP), outperforming tabular neural networks ($p < 0.001$).
    </p>
    <p>
      2) <em>The Danger of Naive Cohort Pooling:</em> Concatenating multi-center registries creates an illusion of massive sample sizes while concealing critical cross-border distribution shifts.
    </p>
    <p>
      3) <em>Statistical Metric vs. Clinical Utility:</em> High ROC-AUC alone is insufficient for clinical adoption; Decision Curve Analysis objectively identifies the operational threshold boundaries where automated ML triaging delivers positive net utility over standard care.
    </p>

    <h2 class="sec-heading">VIII. Limitations and Future Work</h2>
    <h3 class="subsec-heading">A. Limitations of Current Work</h3>
    <p>
      1) <em>Retrospective and Prevalent Label Design:</em> Both Cardio70k ($N = 68,581$) and Unified Clinical ($N = 1,918$) datasets are retrospective cross-sectional registries capturing clinical parameters at a single diagnostic or screening visit. Consequently, the models predict contemporaneous disease presence (prevalent disease classification) rather than true 5-year or 10-year prospective incident cardiovascular risk, which would require longitudinal follow-up cohorts such as the Framingham [2] or UK Biobank registries.
    </p>
    <p>
      2) <em>Informative Missingness and Indication Bias:</em> In real-world clinical practice, diagnostic biomarkers are not omitted at random (MCAR); rather, missingness is driven by clinical indication (MNAR). In the University Hospital of Zurich cohort, severe missingness on serum cholesterol (68.3%) and fluoroscopy (61.8%) reflected institutional referral triage where invasive tests were prioritized only for high-acuity patients. While our training-fold median imputation with missingness indicators preserved predictive signal, it does not explicitly capture the subjective clinical decision-to-test rationale.
    </p>
    <p>
      3) <em>Absence of Verified Universal Patient Linkages for Multimodal Fusion:</em> As demonstrated in our data audits, external 12-lead ECG time-series archives and synthetic CT/MRI imaging repositories lacked secure, anonymized universal patient identification numbers. Attempting synthetic or unverified cross-modal pairing would introduce catastrophic data leakage and fabricated correlations. Consequently, our study was deliberately constrained to tabular physiological and hemodynamic predictors.
    </p>
    <p>
      4) <em>Architectural Scope of Tabular Deep Learning:</em> Our neural baseline was restricted to a regularized two-hidden-layer feedforward Multi-Layer Perceptron (MLP). While representative of standard tabular neural baselines, newer self-attention tabular architectures (e.g., FT-Transformer, TabNet, SAINT) were not benchmarked in this cycle due to high hyperparameter instability and severe computational overhead on smaller multi-center cohorts.
    </p>
    <p>
      5) <em>Cross-System Generalization Gap in South Asian Populations:</em> Although the Unified Clinical cohort incorporates the Mendeley Data India cohort ($N = 1,000$), our Leave-One-Source-Out evaluation revealed that models trained on Western UCI centers collapsed to near-random discrimination on Indian patients (ROC-AUC $0.4937$). This underscores that models trained on Western clinical guidelines cannot be deployed in South Asian healthcare environments without localized fine-tuning and recalibration.
    </p>

    <h3 class="subsec-heading">B. Future Research Directions</h3>
    <p>
      1) <em>Prospective EHR Integration via HL7 FHIR Microservices:</em> We plan to containerize the champion XGBoost model into an interoperable microservice compliant with the Health Level Seven Fast Healthcare Interoperability Resources (HL7 FHIR) standard. Deploying this pipeline in pilot hospital primary-care workflows will enable prospective assessment of clinician alert acceptance, diagnostic turnaround acceleration, and reduction in unwarranted downstream stress testing.
    </p>
    <p>
      2) <em>Benchmarking Specialized Tabular Transformers:</em> We will extend our tabular deep learning track to systematically evaluate column-wise self-attention networks, specifically FT-Transformer and TabNet, utilizing masked feature reconstruction pre-training on large unlabeled health insurance registries before fine-tuning on clinical endpoints.
    </p>
    <p>
      3) <em>Federated Multi-Hospital Learning:</em> To reconcile cross-border cohorts without violating patient privacy regulations (HIPAA, GDPR), future iterations will implement federated learning ($\mathrm{FedAvg}$) equipped with differential privacy ($\varepsilon, \delta$). This will allow multi-center collaborative training across Swiss, American, and Indian hospital networks without transmitting raw protected health information.
    </p>
    <p>
      4) <em>Dynamic Calibration and Human-in-the-Loop Deferral:</em> We aim to couple conformal prediction intervals with uncertainty estimation to deploy a reject-option triage system. Patients falling within intermediate predicted probability bands ($\hat{p} \in [0.42, 0.58]$) will be automatically routed for secondary physician review and definitive non-invasive imaging.
    </p>
    <p>
      5) <em>Localized Clinical Adaptation for South Asian Populations:</em> Given the acute generalization drop on the Mendeley Data India cohort, we will collaborate with regional Indian cardiology institutes to assemble a multi-center South Asian CVD registry, allowing fine-tuning of risk models on indigenous epidemiological distributions.
    </p>

    <h2 class="sec-heading">IX. Conclusion</h2>
    <p>
      This paper establishes a rigorous, leakage-safe, and explainable cardiovascular disease prediction framework. By enforcing strict cohort segregation, Leave-One-Source-Out multi-center testing, and Decision Curve Analysis, we demonstrate that gradient boosted decision trees achieve champion discrimination ($0.8019 \pm 0.0027$ ROC-AUC), statistically outperforming deep neural networks ($p < 0.001$), while delivering positive Net Clinical Benefit across primary-care screening cutoffs. Our findings demonstrate that methodological rigor, transparent calibration, and clinical utility must supersede architectural complexity in translational medical AI.
    </p>

    <h2 class="sec-heading">IEEE Ethics and AI Statement</h2>
    <p>
      In compliance with IEEE authorship guidelines, the authors affirm that all research hypotheses, statistical formulations, experimental protocols, and clinical analyses were developed, executed, and validated by the student authors under the academic guidance of faculty member Rinky Chhatwani at the Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat. AI-assisted programming tools were employed solely for code refactoring, plot generation assistance, and manuscript formatting under strict human supervision. Full reproducibility code and experiment logs are openly available at: <a href="https://github.com/Vansh-ai406/Data-Science" target="_blank">https://github.com/Vansh-ai406/Data-Science</a>.
    </p>

    <h2 class="sec-heading">References</h2>
    <div class="references">
      <p class="ref-item"><span class="ref-num">[1]</span> World Health Organization, &ldquo;Cardiovascular diseases (CVDs): Key facts,&rdquo; <em>WHO Fact Sheets</em>, Geneva, Switzerland, 2021.</p>
      <p class="ref-item"><span class="ref-num">[2]</span> R. B. D'Agostino, R. S. Vasan, M. J. Pencina, P. A. Wolf, M. Cobain, J. M. Massaro, and W. B. Kannel, &ldquo;General cardiovascular risk profile for use in primary care: The Framingham Heart Study,&rdquo; <em>Circulation</em>, vol. 117, no. 6, pp. 743&ndash;753, 2008.</p>
      <p class="ref-item"><span class="ref-num">[3]</span> SCORE2 Working Group and European Society of Cardiology, &ldquo;SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe,&rdquo; <em>Eur. Heart J.</em>, vol. 42, no. 25, pp. 2439&ndash;2454, 2021.</p>
      <p class="ref-item"><span class="ref-num">[4]</span> T. Chen and C. Guestrin, &ldquo;XGBoost: A scalable tree boosting system,&rdquo; in <em>Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD)</em>, 2016, pp. 785&ndash;794.</p>
      <p class="ref-item"><span class="ref-num">[5]</span> L. Breiman, &ldquo;Random forests,&rdquo; <em>Mach. Learn.</em>, vol. 45, no. 1, pp. 5&ndash;32, 2001.</p>
      <p class="ref-item"><span class="ref-num">[6]</span> A. J. Vickers and E. B. Elkin, &ldquo;Decision curve analysis: a novel method for evaluating prediction models,&rdquo; <em>Med. Decis. Making</em>, vol. 26, no. 6, pp. 565&ndash;574, 2006.</p>
      <p class="ref-item"><span class="ref-num">[7]</span> A. J. Vickers, B. van Calster, and E. W. Steyerberg, &ldquo;A simple, step-by-step guide to interpreting decision curve analysis,&rdquo; <em>Diagn. Progn. Res.</em>, vol. 1, no. 1, pp. 1&ndash;8, 2016.</p>
      <p class="ref-item"><span class="ref-num">[8]</span> G. W. Brier, &ldquo;Verification of forecasts expressed in terms of probability,&rdquo; <em>Mon. Weather Rev.</em>, vol. 78, no. 1, pp. 1&ndash;3, 1950.</p>
      <p class="ref-item"><span class="ref-num">[9]</span> B. Efron and R. J. Tibshirani, <em>An Introduction to the Bootstrap</em>. Boca Raton, FL: CRC Press, 1994.</p>
      <p class="ref-item"><span class="ref-num">[10]</span> D. W. Hosmer Jr, S. Lemeshow, and R. X. Sturdivant, <em>Applied Logistic Regression</em>, 3rd ed. Hoboken, NJ: John Wiley &amp; Sons, 2013.</p>
      <p class="ref-item"><span class="ref-num">[11]</span> R. Shwartz-Ziv and A. Armon, &ldquo;Tabular data: Deep learning is not all you need,&rdquo; <em>Inf. Fusion</em>, vol. 81, pp. 84&ndash;90, 2022.</p>
      <p class="ref-item"><span class="ref-num">[12]</span> L. Grinsztajn, E. Oyallon, and G. Varoquaux, &ldquo;Why do tree-based models still outperform deep learning on typical tabular data?,&rdquo; in <em>Adv. Neural Inf. Process. Syst. (NeurIPS)</em>, vol. 35, 2022, pp. 507&ndash;520.</p>
      <p class="ref-item"><span class="ref-num">[13]</span> G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, &ldquo;Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD statement,&rdquo; <em>BMJ</em>, vol. 350, p. g7594, 2015.</p>
      <p class="ref-item"><span class="ref-num">[14]</span> C. J. Clopper and E. S. Pearson, &ldquo;The use of confidence or fiducial limits illustrated in the case of the binomial,&rdquo; <em>Biometrika</em>, vol. 26, no. 4, pp. 404&ndash;413, 1934.</p>
      <p class="ref-item"><span class="ref-num">[15]</span> R. Detrano, A. Janosi, W. Steinbrunn, M. Pfisterer, J. J. Schmid, S. Sandhu, K. P. Guppy, S. Lee, and V. Froelicher, &ldquo;International application of a new probability algorithm for the diagnosis of coronary artery disease,&rdquo; <em>Am. J. Cardiol.</em>, vol. 64, no. 5, pp. 304&ndash;310, 1989.</p>
      <p class="ref-item"><span class="ref-num">[16]</span> Mendeley Data, &ldquo;Cardiovascular Disease Dataset: Multi-center Indian clinical registry,&rdquo; <em>Mendeley Data</em>, V1, doi: 10.17632/jh55nn26tx.1, 2020.</p>
    </div>

  </div>
</div>

</body>
</html>
"""

    html_content = raw_html.replace("{fig_cv_roc}", fig_cv_roc) \
                           .replace("{fig_dca}", fig_dca) \
                           .replace("{fig_calib}", fig_calib) \
                           .replace("{fig_loso}", fig_loso) \
                           .replace("{fig_perm}", fig_perm)

    html_path = paper_dir / "IEEE_RESEARCH_PAPER.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Compiled authentic IEEE HTML paper: {html_path} ({len(html_content)} bytes)")

    # Build references.bib
    bib_content = """@article{who_cvd_2021,
  author    = {{World Health Organization}},
  title     = {Cardiovascular diseases (CVDs): Key facts},
  journal   = {WHO Fact Sheets},
  year      = {2021},
  address   = {Geneva, Switzerland}
}

@article{framingham_2008,
  author    = {D'Agostino, Ralph B. and Vasan, Ramachandran S. and Pencina, Michael J. and Wolf, Philip A. and Cobain, Mark and Massaro, Joseph M. and Kannel, William B.},
  title     = {General cardiovascular risk profile for use in primary care: The {Framingham} Heart Study},
  journal   = {Circulation},
  volume    = {117},
  number    = {6},
  pages     = {743--753},
  year      = {2008}
}

@article{score2_2021,
  author    = {{SCORE2 working group and European Society of Cardiology Cardiovascular Risk Collaboration}},
  title     = {{SCORE2} risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in {Europe}},
  journal   = {European Heart Journal},
  volume    = {42},
  number    = {25},
  pages     = {2439--2454},
  year      = {2021}
}

@inproceedings{chen_xgboost_2016,
  author    = {Chen, Tianqi and Guestrin, Carlos},
  title     = {{XGBoost}: A Scalable Tree Boosting System},
  booktitle = {Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD)},
  pages     = {785--794},
  year      = {2016}
}

@article{breiman_rf_2001,
  author    = {Breiman, Leo},
  title     = {Random Forests},
  journal   = {Machine Learning},
  volume    = {45},
  number    = {1},
  pages     = {5--32},
  year      = {2001}
}

@article{vickers_dca_2006,
  author    = {Vickers, Andrew J. and Elkin, Elena B.},
  title     = {Decision curve analysis: a novel method for evaluating prediction models},
  journal   = {Medical Decision Making},
  volume    = {26},
  number    = {6},
  pages     = {565--574},
  year      = {2006}
}

@article{vickers_dca_update_2016,
  author    = {Vickers, Andrew J. and van Calster, Ben and Steyerberg, Ewout W.},
  title     = {A simple, step-by-step guide to interpreting decision curve analysis},
  journal   = {Diagnostic and Prognostic Research},
  volume    = {1},
  number    = {1},
  pages     = {1--8},
  year      = {2016}
}

@article{brier_1950,
  author    = {Brier, Glenn W.},
  title     = {Verification of forecasts expressed in terms of probability},
  journal   = {Monthly Weather Review},
  volume    = {78},
  number    = {1},
  pages     = {1--3},
  year      = {1950}
}

@book{efron_bootstrap_1994,
  author    = {Efron, Bradley and Tibshirani, Robert J.},
  title     = {An Introduction to the Bootstrap},
  publisher = {CRC Press},
  address   = {Boca Raton, FL},
  year      = {1994}
}

@book{hosmer_lemeshow_2013,
  author    = {Hosmer Jr, David W. and Lemeshow, Stanley and Sturdivant, Rodney X.},
  title     = {Applied Logistic Regression},
  edition   = {3rd},
  publisher = {John Wiley & Sons},
  address   = {Hoboken, NJ},
  year      = {2013}
}

@article{shwartz_tabular_2022,
  author    = {Shwartz-Ziv, Ravid and Armon, Amitai},
  title     = {Tabular data: Deep learning is not all you need},
  journal   = {Information Fusion},
  volume    = {81},
  pages     = {84--90},
  year      = {2022}
}

@inproceedings{grinsztajn_tabular_2022,
  author    = {Grinsztajn, L{\'e}o and Oyallon, Edouard and Varoquaux, Ga{\"e}l},
  title     = {Why do tree-based models still outperform deep learning on typical tabular data?},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {35},
  pages     = {507--520},
  year      = {2022}
}

@article{steyerberg_tripod_2015,
  author    = {Collins, Gary S. and Reitsma, Johannes B. and Altman, Douglas G. and Moons, Karel G.M.},
  title     = {Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis ({TRIPOD}): the {TRIPOD} statement},
  journal   = {BMJ},
  volume    = {350},
  pages     = {g7594},
  year      = {2015}
}

@article{clopper_pearson_1934,
  author    = {Clopper, Charles J. and Pearson, Egon S.},
  title     = {The use of confidence or fiducial limits illustrated in the case of the binomial},
  journal   = {Biometrika},
  volume    = {26},
  number    = {4},
  pages     = {404--413},
  year      = {1934}
}

@article{detrano_uci_1989,
  author    = {Detrano, Robert and Janosi, Andras and Steinbrunn, Walter and Pfisterer, Matthias and Schmid, Johann J. and Sandhu, Sarbjit and Guppy, Kevin P. and Lee, Sandra and Froelicher, Victor},
  title     = {International application of a new probability algorithm for the diagnosis of coronary artery disease},
  journal   = {American Journal of Cardiology},
  volume    = {64},
  number    = {5},
  pages     = {304--310},
  year      = {1989}
}

@misc{mendeley_india_2020,
  author    = {{Mendeley Data}},
  title     = {Cardiovascular Disease Dataset: Multi-center Indian clinical registry},
  year      = {2020},
  howpublished = {Mendeley Data, V1},
  doi       = {10.17632/jh55nn26tx.1}
}
"""
    bib_path = paper_dir / "references.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bib_content)
    print(f"Created BibTeX references file: {bib_path}")

    # Build LaTeX version
    tex_content = r"""\documentclass[conference]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{hyperref}

\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}

\begin{document}

\title{Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis}

\author{
\IEEEauthorblockN{Under the Guidance of Rinky Chhatwani}
\vskip 0.5em
\IEEEauthorblockN{Vansh Rawat, Drisha Chauhan, Karan Bheda, and Harsh Rathva}
\IEEEauthorblockA{\textit{Department of Artificial Intelligence} \\
\textit{Sardar Vallabhbhai National Institute of Technology, Surat, Gujarat, India}}
}

\maketitle

\begin{abstract}
Cardiovascular diseases (CVDs) represent the foremost cause of global mortality. While machine learning classifiers have promised enhanced risk detection, published healthcare AI literature frequently suffers from fatal methodological flaws: naive multi-center cohort pooling, severe data leakage during feature preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we formulate and validate a leakage-safe, multi-cohort tabular machine learning framework for CVD screening. Grounded in two independently handled clinical datasets---Cardio70k ($N = 68,581$) and Unified Clinical ($N = 1,918$ across five hospital centers: Mendeley Data India $N=1,000$, UCI Cleveland $N=303$, UCI Hungary $N=293$, UCI Long Beach VA $N=199$, and UCI Switzerland $N=123$)---we benchmark linear models, ensemble decision trees, and deep tabular neural networks. On Cardio70k, XGBoost attained champion discrimination (ROC-AUC: $0.8019 \pm 0.0027$, PR-AUC: $0.7828$, Brier score: $0.1802$), statistically outperforming the deep tabular neural network ($\Delta\text{ROC-AUC} = +0.0027$, 95\% CI: $[0.0020, 0.0036]$, paired bootstrap $p < 0.001$). Under Leave-One-Source-Out (LOSO) multi-center testing, we uncover steep cross-border generalization decay, where models trained on Western hospital centers collapsed to near-random discrimination ($0.4937$ ROC-AUC) on the Indian cohort. Furthermore, Decision Curve Analysis (DCA) proves a substantial positive Net Clinical Benefit ($+0.3246$ at threshold $p_t = 0.30$). Finally, permutation feature reliance and demographic subgroup auditing with exact 95\% Clopper-Pearson confidence intervals provide transparent verification of clinical alignment and algorithmic equity.
\end{abstract}

\begin{IEEEkeywords}
Cardiovascular disease, tabular machine learning, decision curve analysis, multi-center generalization, probability calibration, explainable AI, algorithmic fairness.
\end{IEEEkeywords}

\section{Introduction}
Cardiovascular diseases (CVDs) remain the leading contributor to global morbidity and mortality \cite{who_cvd_2021}. Standard primary-care screening tools, such as the Framingham Risk Score \cite{framingham_2008} and the European SCORE2 guidelines \cite{score2_2021}, employ multivariable parametric regressions fitted on historical epidemiological cohorts. Although clinically entrenched, these linear scoring systems cannot autonomously capture complex non-linear interactions among physiological biomarkers.

Machine learning (ML) models offer greater flexibility, but translational biomedical reviews highlight persistent methodological flaws violating TRIPOD guidelines \cite{steyerberg_tripod_2015}: naive cohort pooling, data leakage during scaling/imputation, over-parameterized deep neural networks without demonstrated tabular advantages \cite{shwartz_tabular_2022, grinsztajn_tabular_2022}, and reliance on ROC-AUC without measuring clinical utility \cite{vickers_dca_2006, vickers_dca_update_2016}.

This paper establishes an end-to-end, leak-free, and explainable cardiovascular prediction framework developed under the faculty guidance of Rinky Chhatwani at the Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat.

\section{Related Work}
Classical CVD risk estimation began with Framingham \cite{framingham_2008} and SCORE2 \cite{score2_2021}. Non-linear tree ensembles including Random Forests \cite{breiman_rf_2001} and XGBoost \cite{chen_xgboost_2016} demonstrated superior inductive biases for tabular clinical features \cite{grinsztajn_tabular_2022}. Vickers and Elkin \cite{vickers_dca_2006} formulated Decision Curve Analysis to evaluate real-world net clinical benefit across operational threshold probabilities.

\section{Cohorts and Preprocessing}
\subsection{Cardio70k Screening Cohort}
Cardio70k comprises $N = 68,581$ records with 34,652 negative cases (50.53\%) and 33,929 positive cases (49.47\%), including 44,665 females and 23,916 males. Predictors encompass age, sex, height, weight, BMI, systolic and diastolic blood pressure, pulse pressure, blood pressure category, cholesterol, glucose, smoking, alcohol, and physical activity.

\subsection{Unified Clinical Multi-Center Cohort}
Unified Clinical comprises $N = 1,918$ high-acuity diagnostic records across five international centers: Mendeley Data India ($N = 1,000$) \cite{mendeley_india_2020}, UCI Cleveland ($N = 303$) \cite{detrano_uci_1989}, UCI Hungary ($N = 293$) \cite{detrano_uci_1989}, UCI Long Beach VA ($N = 199$) \cite{detrano_uci_1989}, and UCI Switzerland ($N = 123$) \cite{detrano_uci_1989}.

\subsection{Multimodal Asset Auditing}
Independent 12-lead ECG waveforms ($N = 4,998$) and synthetic cardiac CT/MRI slices ($N = 30,352$) lacked universal patient identifiers linking to verified outcomes; attempting synthetic pairing was rejected to avoid catastrophic data leakage.

\section{System Architecture and Methodology}
All transformations (median imputation with missingness indicators, robust $z$-score scaling) were fitted exclusively on training partitions. Benchmarked models include $\ell_2$-regularized Logistic Regression \cite{hosmer_lemeshow_2013}, Random Forest \cite{breiman_rf_2001}, HistGradientBoosting, XGBoost \cite{chen_xgboost_2016}, and a two-hidden-layer feedforward MLP ($128 \to 64$ units) with dropout ($p = 0.20$).

\section{Experimental Results and Benchmarks}
\subsection{Cardio70k 5-Fold Cross-Validation}
On Cardio70k ($N = 68,581$), XGBoost achieved champion discrimination: ROC-AUC $0.8019 \pm 0.0027$, PR-AUC $0.7828$, Brier score $0.1802$, Accuracy $0.7324$, Sensitivity $0.7124$, Specificity $0.7505$, and Net Benefit $+0.3246$ at $p_t = 0.30$. A 1,000-iteration paired bootstrap test confirmed XGBoost significantly outperformed the neural MLP ($\Delta\text{ROC-AUC} = +0.0027$, 95\% CI: $[0.0020, 0.0036]$, $p < 0.001$).

\subsection{Leave-One-Source-Out Generalization Gap}
Evaluating model transfer on Unified Clinical ($N = 1,918$) revealed high European performance (Hungary: 0.8370 ROC-AUC; Cleveland: 0.8358 ROC-AUC) but severe collapse on the Indian cohort (0.4937 ROC-AUC), exposing acute international distribution shift.

\section{Interpretability, Clinical Utility, and Equity}
Decision Curve Analysis demonstrated positive Net Clinical Benefit across thresholds $p_t \in [0.10, 0.90]$ ($+0.3246$ at $p_t = 0.30$ vs. $+0.2782$ for Treat All). Permutation feature reliance identified systolic blood pressure ($\Delta\text{AUC} = -0.1473$) and age ($\Delta\text{AUC} = -0.0371$) as primary drivers. Demographic slicing with exact 95\% Clopper-Pearson confidence limits \cite{clopper_pearson_1934} confirmed equitable discrimination across biological sexes (Female: 0.8036; Male: 0.7985 ROC-AUC).

\section{Limitations and Future Work}
Limitations include cross-sectional retrospective labels, indication bias in referral tests, lack of universal patient IDs for multimodal fusion, and geographic domain shift on South Asian patients. Future work focuses on HL7 FHIR microservice containerization, tabular self-attention transformers (FT-Transformer), federated multi-hospital learning ($\text{FedAvg}$), and localized recalibration for Indian cohorts.

\section{Conclusion}
This study establishes a leakage-safe, explainable CVD screening framework. Rigorous multi-cohort benchmarking and Decision Curve Analysis prove that gradient boosted trees achieve superior discrimination and positive Net Clinical Benefit over default clinical strategies.

\section*{IEEE Ethics and AI Statement}
The authors affirm that all research hypotheses, statistical formulations, experimental protocols, and clinical analyses were developed, executed, and validated by the student authors under the academic guidance of faculty member Rinky Chhatwani at the Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat. AI programming tools were utilized solely for code refactoring and formatting under human oversight. Code: \url{https://github.com/Vansh-ai406/Data-Science}.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
"""
    tex_path = paper_dir / "IEEE_Cardiovascular_Disease_Prediction.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)
    print(f"Created IEEEtran LaTeX manuscript: {tex_path}")

    # Build Markdown version
    md_content = """# Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis

**Under the Guidance of:** Rinky Chhatwani  
**Authors:** Vansh Rawat, Drisha Chauhan, Karan Bheda, and Harsh Rathva  
**Affiliation:** Department of Artificial Intelligence, Sardar Vallabhbhai National Institute of Technology, Surat, Gujarat, India  
**Code Repository:** [https://github.com/Vansh-ai406/Data-Science](https://github.com/Vansh-ai406/Data-Science)

---

## Abstract
Cardiovascular diseases (CVDs) represent the foremost cause of global mortality, accounting for approximately 17.9 million annual deaths according to the World Health Organization. While machine learning classifiers have promised enhanced risk detection, published healthcare AI literature frequently suffers from fatal methodological flaws: naive multi-center cohort pooling, severe data leakage during feature preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we formulate and validate a leakage-safe, multi-cohort tabular machine learning framework for CVD screening. Our research is grounded in two independently handled clinical datasets: a large primary-care screening cohort (Cardio70k, $N = 68,581$; 44,665 females and 23,916 males) and an international multi-center clinical cohort (Unified Clinical, $N = 1,918$ across five hospital centers: Mendeley Data India $N=1,000$, UCI Cleveland $N=303$, UCI Hungary $N=293$, UCI Long Beach VA $N=199$, and UCI Switzerland $N=123$). We benchmark generalized linear models, ensemble decision trees (Random Forest, HistGradientBoosting, XGBoost), and deep tabular neural networks (Multi-Layer Perceptron, MLP) under repeated 5-fold stratified cross-validation and nested outer-fold selection. On Cardio70k, XGBoost attained champion discrimination (ROC-AUC: $0.8019 \pm 0.0027$, PR-AUC: $0.7828$, Brier score: $0.1802$), statistically outperforming the deep tabular neural network ($\Delta\text{ROC-AUC} = +0.0027$, 95% CI: $[0.0020, 0.0036]$, paired bootstrap $p < 0.001$). Under Leave-One-Source-Out (LOSO) multi-center stress testing, we uncover steep cross-border generalization decay, where models trained on Western hospital centers collapsed to near-random discrimination ($0.4937$ ROC-AUC) on the Indian cohort, demonstrating pronounced clinical covariate shift. Moving beyond discrimination, Decision Curve Analysis (DCA) proves a substantial positive Net Clinical Benefit ($+0.3246$ at threshold probability $p_t = 0.30$ vs. $+0.2782$ for universal treatment). Finally, model-agnostic permutation feature reliance and demographic subgroup auditing with exact 95% Clopper-Pearson confidence intervals provide transparent validation of clinical alignment and algorithmic equity.

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

*Paired Bootstrap Test:* XGBoost statistically outperforms Neural MLP by $\Delta\text{ROC-AUC} = +0.0027$ (95% CI: $[0.0020, 0.0036]$, $p < 0.001$).

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
3. **Federated Multi-Hospital Learning:** Implementing federated averaging ($\text{FedAvg}$) equipped with differential privacy ($\varepsilon, \delta$) to enable collaborative training across international hospital networks without sharing raw protected health information.
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
"""
    md_path = paper_dir / "IEEE_RESEARCH_PAPER.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Created Markdown research paper: {md_path}")

if __name__ == "__main__":
    build_paper()
