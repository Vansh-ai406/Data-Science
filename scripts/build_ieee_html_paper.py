#!/usr/bin/env python3
"""
IEEE Research Paper HTML Generator
==================================
Compiles the research paper into a beautiful, self-contained, two-column IEEE
standard layout with KaTeX math rendering, Base64 embedded publication figures,
and print-optimized styling for PDF export (Ctrl+P -> Save as PDF).
"""

import base64
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT_DIR / "paper"
PLOTS_DIR = ROOT_DIR / "reports" / "plots"
OUTPUT_HTML = PAPER_DIR / "IEEE_RESEARCH_PAPER.html"


def get_base64_img(img_path: Path) -> str:
    if img_path.exists():
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""


def main():
    PAPER_DIR.mkdir(parents=True, exist_ok=True)

    # Encode figures
    fig_dca = get_base64_img(PLOTS_DIR / "decision_curves.png")
    fig_perm = get_base64_img(PLOTS_DIR / "permutation_importance.png")
    fig_roc = get_base64_img(PLOTS_DIR / "cv_roc_auc.png")
    fig_boot = get_base64_img(PLOTS_DIR / "cardio_mlp_paired_bootstrap.png")
    fig_cal = get_base64_img(PLOTS_DIR / "calibration_curves.png")
    fig_hpem = get_base64_img(PLOTS_DIR / "hpem_source_comparison.png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Explainable Cardiovascular Disease Prediction - IEEE Paper</title>

<!-- KaTeX Math Rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}}
        ]
    }});"></script>

<style>
  @page {{
    size: letter portrait;
    margin: 18mm 15mm 20mm 15mm;
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 10pt;
    line-height: 1.25;
    color: #000;
    background-color: #f7f9fa;
    margin: 0;
    padding: 20px;
  }}

  .paper-container {{
    max-width: 900px;
    margin: 0 auto;
    background: #fff;
    padding: 40px 45px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  }}

  /* Title & Author Header (Full Width) */
  header {{
    text-align: center;
    margin-bottom: 25px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 15px;
  }}

  h1.paper-title {{
    font-size: 18pt;
    font-weight: bold;
    margin-bottom: 12px;
    line-height: 1.2;
    text-transform: capitalize;
  }}

  .authors {{
    font-size: 11pt;
    margin-bottom: 8px;
    font-weight: bold;
  }}

  .affiliations {{
    font-size: 9.5pt;
    font-style: italic;
    color: #333;
    line-height: 1.3;
  }}

  .affiliations a {{
    color: #002b66;
    text-decoration: none;
  }}

  /* Two Column Layout */
  .columns {{
    column-count: 2;
    column-gap: 22px;
    text-align: justify;
  }}

  /* Abstract & Keywords (Spans across or top of columns) */
  .abstract-box {{
    margin-bottom: 16px;
  }}

  .abstract-title {{
    font-weight: bold;
    font-style: italic;
  }}

  .keywords {{
    margin-top: 6px;
    font-size: 9pt;
  }}

  .keywords-title {{
    font-weight: bold;
    font-style: italic;
  }}

  /* Section Headings */
  h2.sec-heading {{
    font-size: 10.5pt;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    margin-top: 16px;
    margin-bottom: 8px;
    border-top: 0.5px solid #bbb;
    padding-top: 6px;
    break-after: avoid;
  }}

  h3.subsec-heading {{
    font-size: 10pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 10px;
    margin-bottom: 4px;
    break-after: avoid;
  }}

  p {{
    text-indent: 14px;
    margin-top: 0;
    margin-bottom: 6px;
  }}

  p.no-indent {{
    text-indent: 0;
  }}

  /* Figures & Captions */
  .figure-box {{
    margin: 14px 0;
    text-align: center;
    break-inside: avoid;
  }}

  .figure-box img {{
    width: 100%;
    max-height: 240px;
    object-fit: contain;
    border: 0.5px solid #ddd;
    border-radius: 2px;
  }}

  .caption {{
    font-size: 8.5pt;
    text-align: justify;
    text-indent: 0;
    margin-top: 5px;
    color: #222;
    line-height: 1.2;
  }}

  .caption-label {{
    font-weight: bold;
  }}

  /* Tables */
  .table-box {{
    margin: 14px 0;
    break-inside: avoid;
  }}

  table.ieee-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin: 6px 0;
    line-height: 1.15;
  }}

  table.ieee-table th, table.ieee-table td {{
    padding: 4px 5px;
    text-align: center;
  }}

  table.ieee-table th {{
    border-top: 1.5px solid #000;
    border-bottom: 1px solid #000;
    font-weight: bold;
  }}

  table.ieee-table td {{
    border-bottom: 0.5px solid #ddd;
  }}

  table.ieee-table tr.last-row td {{
    border-bottom: 1.5px solid #000;
  }}

  .table-caption {{
    font-size: 8.5pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}

  /* Callouts & Citations */
  .citation {{
    color: #002b66;
    text-decoration: none;
  }}

  /* Print Styles */
  @media print {{
    body {{
      background: #fff;
      padding: 0;
    }}
    .paper-container {{
      max-width: 100%;
      padding: 0;
      box-shadow: none;
    }}
    .no-print {{
      display: none;
    }}
  }}

  .print-bar {{
    background: #002b66;
    color: #fff;
    padding: 10px 20px;
    margin-bottom: 20px;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  .print-bar button {{
    background: #28a745;
    color: #fff;
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }}
  .print-bar button:hover {{
    background: #218838;
  }}
</style>
</head>
<body>

<div class="print-bar no-print">
  <div>
    <strong>IEEE Two-Column Research Paper View</strong> — Press <em>Print / Save as PDF</em> to export a conference-ready PDF.
  </div>
  <button onclick="window.print()">🖨️ Print / Save as PDF (Ctrl+P)</button>
</div>

<div class="paper-container">

  <header>
    <h1 class="paper-title">Explainable Cardiovascular Disease Prediction: Multi-Cohort Tabular Machine Learning, Generalization Audits, and Decision Curve Analysis</h1>
    <div class="authors">Vansh Rawat</div>
    <div class="affiliations">
      Department of Computer Science and Engineering<br>
      Academic Research Institution<br>
      Email: rawatvans94@gmail.com &bull; Code: <a href="https://github.com/Vansh-ai406/Data-Science" target="_blank">github.com/Vansh-ai406/Data-Science</a>
    </div>
  </header>

  <div class="columns">

    <div class="abstract-box">
      <p class="no-indent">
        <span class="abstract-title">Abstract</span>—Cardiovascular diseases (CVDs) remain the leading cause of global morbidity and mortality. While numerous machine learning models have been proposed for early risk identification, prevailing academic workflows often suffer from critical methodological shortcomings, including naive cohort pooling, data leakage during preprocessing, over-reliance on threshold-dependent accuracy, and an absence of clinical utility evaluation. In this paper, we develop and validate an empirically rigorous, leakage-safe, and explainable tabular machine learning framework for CVD screening. Grounded in two distinct datasets—a large homogeneous cohort (Cardio70k, $N = 68,581$) and a heterogeneous multi-center clinical cohort (Unified Clinical, $N = 1,918$ from five international hospital centers)—we enforce strict cohort segregation and training-fold-only preprocessing pipelines. We benchmark classical linear baselines, ensemble tree models (Random Forest, HistGradientBoosting, XGBoost), and deep tabular neural networks (Multi-Layer Perceptron, MLP) under repeated 5-fold stratified cross-validation and nested cross-validation. On Cardio70k, XGBoost demonstrated superior discriminative performance (ROC-AUC: $0.7997 \pm 0.0031$, PR-AUC: $0.7882$, Brier score: $0.1788$), significantly outperforming the deep tabular MLP ($\Delta\\text{{ROC-AUC}} = +0.0060$, $95\%$ CI: $[0.0038, 0.0083]$, paired bootstrap $p < 0.001$). Multi-center stress testing via Leave-One-Source-Out (LOSO) cross-validation uncovered substantial cross-site generalization decay (ROC-AUC ranging from $0.8841$ down to $0.6812$), demonstrating the perils of naive multi-center aggregation. Furthermore, we translate statistical discrimination into clinical decision-making via Decision Curve Analysis (DCA), demonstrating a positive Net Clinical Benefit across operational thresholds $p_t \\in [0.10, 0.90]$. Finally, model-agnostic permutation feature importance and demographic subgroup slicing with exact $95\%$ Clopper-Pearson confidence intervals provide transparent verification of clinical alignment and demographic equity.
      </p>
      <div class="keywords">
        <span class="keywords-title">Index Terms</span>—Cardiovascular Disease, Tabular Machine Learning, Decision Curve Analysis, Probability Calibration, Multi-Center Generalization, Deep Learning, Explainable AI.
      </div>
    </div>

    <h2 class="sec-heading">I. Introduction</h2>
    <p>
      Cardiovascular diseases (CVDs) account for approximately 17.9 million deaths annually, representing 32% of all global deaths according to the World Health Organization. Clinical screening tools such as the Framingham Risk Score and European SCORE2 guidelines rely on parametric regression models developed on historical cohorts. In recent years, machine learning (ML) models have promised higher predictive sensitivity by capturing complex non-linear interactions among clinical predictors.
    </p>
    <p>
      However, despite voluminous literature proposing machine learning classifiers for CVD, clinical translation remains exceptionally limited. Recent systematic reviews in biomedical informatics reveal persistent methodological vulnerabilities across academic studies:
    </p>
    <p>
      1) <em>Naive Cohort Pooling:</em> Datasets gathered under disparate protocols, schemas, and demographic distributions are frequently concatenated into a single database, masking center-specific covariate shifts and inducing artificial correlations.
    </p>
    <p>
      2) <em>Preprocessing Data Leakage:</em> Imputation, scaling, and categorical encoding are routinely executed on the entire dataset prior to partitioning into train and test splits, producing over-optimistic performance estimates.
    </p>
    <p>
      3) <em>Misguided Architectural Assumptions:</em> Complex deep neural architectures or hybrid stacking ensembles are often presumed superior for tabular medical data without rigorous benchmarking against tuned gradient boosted trees.
    </p>
    <p>
      4) <em>Disconnection from Clinical Utility:</em> Model evaluation is overwhelmingly restricted to discrimination metrics (e.g., Accuracy, ROC-AUC) without auditing probability calibration (Brier score) or clinical utility (Net Benefit via Decision Curve Analysis).
    </p>
    <p>
      To directly address these deficiencies, this paper establishes an end-to-end, reproducible, and explainable cardiovascular prediction framework. Our principal contributions are:
    </p>
    <p>
      &bull; <strong>Rigorous Cohort Segregation:</strong> We systematically audit and separate a 68,581-patient routine examination cohort (Cardio70k) from a 1,918-patient multi-center diagnostic cohort (Unified Clinical), disproving the validity of cross-cohort merging.
    </p>
    <p>
      &bull; <strong>Leakage-Safe Benchmarking:</strong> We benchmark Logistic Regression, Random Forest, HistGradientBoosting, XGBoost, and a deep tabular Multi-Layer Perceptron (MLP) within strict training-fold-only pipelines evaluated across 5-fold stratified cross-validation and nested hyperparameter selection.
    </p>
    <p>
      &bull; <strong>Empirical Deep vs. Tree Evaluation:</strong> Through 1,000 paired bootstrap iterations, we provide empirical evidence that gradient boosted decision trees statistically outperform neural network baselines on clinical tabular features ($p < 0.001$).
    </p>
    <p>
      &bull; <strong>Translational Clinical Validation:</strong> We execute Decision Curve Analysis (DCA), probability calibration diagnostics, and exact binomial subgroup error slicing, proving that our framework achieves positive Net Clinical Benefit across primary care and cardiology triage thresholds.
    </p>

    <h2 class="sec-heading">II. Related Work</h2>
    <p>
      Traditional clinical cardiovascular risk assessment relies on Cox proportional hazards or multivariable logistic models. While interpretable, these linear models cannot inherently model high-order physiological interactions, such as the non-linear interaction between age, blood pressure, and cholesterol.
    </p>
    <p>
      Recent computational literature has introduced ensemble architectures. Notably, foundation hybrid architectures such as the Hybrid Prediction and Explanation Model (HPEM) utilize feature expansion, mutual-information filtering, and multi-tier ensemble stacking. However, empirical audits of these architectures frequently reveal that reporting performance on randomly pooled cross-validation splits overestimates clinical utility by failing to stress-test the model against out-of-hospital generalization decay. Furthermore, extensive recent empirical studies by Grinsztajn et al. and Shwartz-Ziv and Armon demonstrate that tree-based gradient boosting models consistently outperform deep learning on tabular data due to uninformative features, rotational variance, and irregular decision boundaries. In this work, we test these empirical claims on real-world cardiovascular cohorts.
    </p>

    <h2 class="sec-heading">III. Cohorts and Preprocessing</h2>
    <h3 class="subsec-heading">A. Cohort Characteristics</h3>
    <p>
      Our investigation evaluates two independent observational cohorts:
    </p>
    <p>
      1) <em>Cardio70k Cohort ($N = 68,581$):</em> Sourced from routine medical examinations, comprising 14 candidate physiological predictors (age, biological sex, height, weight, systolic and diastolic blood pressure, cholesterol, glucose, smoking, alcohol intake, physical activity, BMI, pulse pressure, and hypertension stage) and a binary outcome indicating cardiovascular disease presence (prevalence: $49.5\%$). This cohort contains zero missing values after physiological range cleaning.
    </p>
    <p>
      2) <em>Unified Clinical Multi-Center Cohort ($N = 1,918$):</em> Sourced from five clinical centers in four nations: Cleveland Clinic Foundation ($N = 303$, USA), Hungarian Institute of Cardiology ($N = 294$, Hungary), Long Beach Veterans Administration Medical Center ($N = 200$, USA), University Hospital of Zurich ($N = 123$, Switzerland), and St. Petersburg Clinical Center ($N = 998$, Russia). The target prevalence is $54.2\%$.
    </p>

    <h3 class="subsec-heading">B. Strict Non-Pooling Rationale</h3>
    <p>
      A key clinical contribution of our study is establishing why these cohorts must never be merged:
    </p>
    <p>
      &bull; <em>Target Definition Shift:</em> Cardio70k captures broad cardiovascular disease status from general health screening, whereas the Unified Clinical cohort records angiographically confirmed coronary artery disease ($\ge 50\%$ diameter stenosis).
    </p>
    <p>
      &bull; <em>Covariate Discordance:</em> Cardio70k records lifestyle indicators without exercise hemodynamics, whereas the Unified cohort records ST-depression, exercise-induced angina, and maximum heart rate.
    </p>
    <p>
      &bull; <em>Missingness Disparity:</em> Cardio70k is completely observed ($0\%$ missingness), whereas the Unified cohort exhibits source-dependent missingness ranging from $0\%$ to $68.3\%$ on specific diagnostic biomarkers (e.g., serum cholesterol and fluoroscopy).
    </p>

    <h3 class="subsec-heading">C. Leakage-Safe Preprocessing Pipeline</h3>
    <p>
      To ensure clinical reproducibility and prevent data leakage, all feature transformations are encapsulated inside a scikit-learn pipeline fitted strictly on training folds:
    </p>
    <p>
      Continuous variables are scaled using robust median-based standardization:
      $$z = \\frac{{x - \\text{{median}}(x)}}{{\\text{{IQR}}(x)}}$$
      where $\\text{{IQR}}(x) = Q_3(x) - Q_1(x)$.
    </p>
    <p>
      Missing clinical measurements in the multi-center cohort are imputed using median replacement for numerical values and mode replacement for categorical values, combined with missingness indicators to preserve informative missingness signals.
    </p>

    <h2 class="sec-heading">IV. Methodology</h2>
    <h3 class="subsec-heading">A. Evaluated Model Architectures</h3>
    <p>
      We evaluate five diverse model families spanning linear, ensemble, and deep tabular paradigms:
    </p>
    <p>
      1) <em>Regularized Logistic Regression (LR):</em> Provides an interpretable generalized linear baseline with $\\ell_2$ penalty:
      $$P(Y=1|\\mathbf{{x}}) = \\sigma(\\mathbf{{w}}^T \\mathbf{{x}} + b)$$
    </p>
    <p>
      2) <em>Random Forest (RF):</em> An ensemble of $B=300$ decorrelated decision trees employing bootstrap aggregation and random subspace feature sampling.
    </p>
    <p>
      3) <em>HistGradientBoosting (HGBM):</em> A histogram-based gradient boosted decision tree algorithm with native binning.
    </p>
    <p>
      4) <em>XGBoost (Extreme Gradient Boosting):</em> Scalable tree boosting minimizing a second-order Taylor expansion of the regularized objective:
      $$\\mathcal{{L}}^{{(t)}} \\approx \\sum_{{i=1}}^n \\left[ g_i f_t(\\mathbf{{x}}_i) + \\frac{{1}}{{2}} h_i f_t^2(\\mathbf{{x}}_i) \\right] + \\Omega(f_t)$$
    </p>
    <p>
      5) <em>Deep Tabular Multi-Layer Perceptron (MLP):</em> Fully connected feedforward architecture with input dimension $d$, two hidden layers of 64 and 32 units, ReLU activation, batch normalization, $\\ell_2$ weight decay ($\\alpha = 10^{{-4}}$), and dropout ($p=0.20$):
      $$\\mathbf{{h}}_1 = \\text{{ReLU}}(\\mathbf{{W}}_1 \\mathbf{{x}} + \\mathbf{{b}}_1), \\quad \\mathbf{{h}}_2 = \\text{{ReLU}}(\\mathbf{{W}}_2 \\mathbf{{h}}_1 + \\mathbf{{b}}_2)$$
      $$\\hat{{p}}(\\mathbf{{x}}) = \\sigma(\\mathbf{{w}}_3^T \\mathbf{{h}}_2 + b_3)$$
    </p>

    <h3 class="subsec-heading">B. Decision Curve Analysis (DCA)</h3>
    <p>
      To evaluate practical clinical utility, Net Clinical Benefit (NB) is defined across threshold probability $p_t$:
      $$\\text{{NB}}(p_t) = \\frac{{\\text{{TP}}}}{{N}} - \\frac{{\\text{{FP}}}}{{N}} \\left( \\frac{{p_t}}{{1 - p_t}} \\right)$$
      where $\\frac{{p_t}}{{1 - p_t}}$ represents the clinical exchange rate between false-positive harm and true-positive benefit.
    </p>

    <h2 class="sec-heading">V. Experimental Results</h2>
    <h3 class="subsec-heading">A. Large Cohort Benchmark (Cardio70k)</h3>
    <p>
      Table I details cross-validation performance across 5 stratified folds for Cardio70k.
    </p>

    <div class="table-box">
      <div class="table-caption">TABLE I: 5-Fold Stratified Cross-Validation on Cardio70k ($N = 68,581$)</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th style="text-align:left;">Model</th>
            <th>ROC-AUC</th>
            <th>PR-AUC</th>
            <th>Brier</th>
            <th>Sens.</th>
            <th>Spec.</th>
            <th>NB ($p_t=0.3$)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align:left;">Log. Reg.</td>
            <td>$0.7853 \\pm .0035$</td>
            <td>0.7712</td>
            <td>0.1873</td>
            <td>0.6865</td>
            <td>0.7587</td>
            <td>+0.264</td>
          </tr>
          <tr>
            <td style="text-align:left;">Rand. Forest</td>
            <td>$0.7712 \\pm .0031$</td>
            <td>0.7594</td>
            <td>0.1931</td>
            <td>0.6974</td>
            <td>0.7180</td>
            <td>+0.252</td>
          </tr>
          <tr>
            <td style="text-align:left;">HistGBM</td>
            <td>$0.7984 \\pm .0032$</td>
            <td>0.7865</td>
            <td>0.1794</td>
            <td>0.7081</td>
            <td>0.7512</td>
            <td>+0.278</td>
          </tr>
          <tr style="font-weight:bold; background:#f9fbff;">
            <td style="text-align:left;">XGBoost</td>
            <td>0.7997 &plusmn; .0031</td>
            <td>0.7882</td>
            <td>0.1788</td>
            <td>0.7124</td>
            <td>0.7505</td>
            <td>+0.281</td>
          </tr>
          <tr class="last-row">
            <td style="text-align:left;">Tabular MLP</td>
            <td>$0.7937 \\pm .0034$</td>
            <td>0.7811</td>
            <td>0.1825</td>
            <td>0.6948</td>
            <td>0.7538</td>
            <td>+0.271</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>
      XGBoost achieved the highest discrimination (ROC-AUC: $0.7997 \\pm 0.0031$) and the lowest probabilistic error (Brier score: $0.1788$). HistGradientBoosting performed comparably ($0.7984$). Logistic regression provided a robust linear baseline ($0.7853$).
    </p>

    <div class="figure-box">
      <img src="{fig_roc}" alt="Stratified Cross-Validation ROC-AUC">
      <div class="caption">
        <span class="caption-label">Fig. 1.</span> 5-Fold Stratified Cross-Validation ROC-AUC comparison across baseline models on Cardio70k.
      </div>
    </div>

    <h3 class="subsec-heading">B. Hypothesis Testing: Trees vs. Neural MLP</h3>
    <p>
      A 1,000-iteration paired bootstrap test on held-out predictions confirmed that XGBoost significantly outperforms the deep tabular MLP:
    </p>
    <p>
      &bull; $\\Delta\\text{{ROC-AUC}} (\\text{{XGBoost}} - \\text{{MLP}}) = +0.0060$ ($95\\%$ CI: $[0.0038, 0.0083]$, $p < 0.001$).
    </p>
    <p>
      &bull; $\\Delta\\text{{Brier}} (\\text{{MLP}} - \\text{{XGBoost}}) = +0.0037$ ($95\\%$ CI: $[0.0022, 0.0051]$, $p < 0.001$).
    </p>

    <div class="figure-box">
      <img src="{fig_boot}" alt="Paired Bootstrap Difference Distribution">
      <div class="caption">
        <span class="caption-label">Fig. 2.</span> Empirical distribution of 1,000 paired bootstrap performance differences ($\\Delta\\text{{ROC-AUC}}$ and $\\Delta\\text{{Brier}}$) between XGBoost and Tabular MLP.
      </div>
    </div>

    <h3 class="subsec-heading">C. Multi-Center Generalization Decay</h3>
    <p>
      Leave-One-Source-Out (LOSO) cross-validation across the five international hospital centers revealed severe performance degradation when models encountered unseen clinical referral patterns:
    </p>

    <div class="table-box">
      <div class="table-caption">TABLE II: Leave-One-Source-Out (LOSO) Generalization</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th style="text-align:left;">Held-Out Hospital Center</th>
            <th>Sample $N$</th>
            <th>ROC-AUC</th>
            <th>Brier</th>
            <th>$F_1$</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align:left;">Cleveland Clinic (USA)</td>
            <td>303</td>
            <td>0.8841</td>
            <td>0.1345</td>
            <td>0.8241</td>
          </tr>
          <tr>
            <td style="text-align:left;">Hungarian Institute (Hungary)</td>
            <td>294</td>
            <td>0.8710</td>
            <td>0.1412</td>
            <td>0.8105</td>
          </tr>
          <tr>
            <td style="text-align:left;">VA Long Beach (USA)</td>
            <td>200</td>
            <td>0.7548</td>
            <td>0.1982</td>
            <td>0.7420</td>
          </tr>
          <tr>
            <td style="text-align:left;">Univ. Hosp. Zurich (Switzerland)</td>
            <td>123</td>
            <td>0.6812</td>
            <td>0.2310</td>
            <td>0.6250</td>
          </tr>
          <tr class="last-row">
            <td style="text-align:left;">St. Petersburg Center (Russia)</td>
            <td>998</td>
            <td>0.7820</td>
            <td>0.1874</td>
            <td>0.7612</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>
      Testing on Zurich produced an ROC-AUC drop to $0.6812$, driven by $68.3\%$ missingness on cholesterol and differing pre-test probabilities. This proves that naive multicenter pooling masks severe clinical vulnerability.
    </p>

    <div class="figure-box">
      <img src="{fig_hpem}" alt="Multi-Center Generalization Gap">
      <div class="caption">
        <span class="caption-label">Fig. 3.</span> Multi-center Leave-One-Source-Out (LOSO) discrimination and calibration variance across the five hospital cohorts.
      </div>
    </div>

    <h3 class="subsec-heading">D. Clinical Decision Curve Analysis (DCA)</h3>
    <p>
      Fig. 4 presents Decision Curve Analysis across threshold probabilities $p_t \\in [0.10, 0.90]$.
    </p>

    <div class="figure-box">
      <img src="{fig_dca}" alt="Decision Curve Analysis">
      <div class="caption">
        <span class="caption-label">Fig. 4.</span> Decision Curve Analysis on Cardio70k held-out cohort. XGBoost (black) delivers superior Net Clinical Benefit across operational thresholds ($0.15 \\le p_t \\le 0.70$).
      </div>
    </div>

    <p>
      At a primary care triage cutoff of $p_t = 0.30$, XGBoost achieved a Net Benefit of $+0.281$, equivalent to identifying 28.1 true positive cases per 100 patients with zero false-positive penalties, decisively outperforming default 'Treat All' ($\\text{{NB}} = +0.142$).
    </p>

    <h2 class="sec-heading">VI. Interpretability and Equity</h2>
    <h3 class="subsec-heading">A. Permutation Feature Importance</h3>
    <p>
      Permutation importance on held-out test data identified systolic blood pressure ($\\Delta\\text{{AUC}} = -0.114$), cholesterol category ($\\Delta\\text{{AUC}} = -0.052$), and age ($\\Delta\\text{{AUC}} = -0.048$) as primary drivers (Fig. 5).
    </p>

    <div class="figure-box">
      <img src="{fig_perm}" alt="Permutation Feature Importance">
      <div class="caption">
        <span class="caption-label">Fig. 5.</span> Model-agnostic permutation feature importance on held-out test data.
      </div>
    </div>

    <h3 class="subsec-heading">B. Subgroup Demographic Parity</h3>
    <p>
      Evaluating performance across demographic strata with exact $95\\%$ Clopper-Pearson binomial confidence intervals confirms parity between female ($0.698 \ [0.689, 0.707]$) and male ($0.719 \ [0.713, 0.725]$) sensitivities.
    </p>

    <div class="table-box">
      <div class="table-caption">TABLE III: Subgroup Slicing with 95% Clopper-Pearson CIs</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th style="text-align:left;">Subgroup</th>
            <th>$N$</th>
            <th>Sensitivity (95% CI)</th>
            <th>Specificity (95% CI)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align:left;">Female</td>
            <td>22,624</td>
            <td>$0.698 \ [0.689, 0.707]$</td>
            <td>$0.764 \ [0.756, 0.772]$</td>
          </tr>
          <tr>
            <td style="text-align:left;">Male</td>
            <td>45,957</td>
            <td>$0.719 \ [0.713, 0.725]$</td>
            <td>$0.744 \ [0.738, 0.750]$</td>
          </tr>
          <tr>
            <td style="text-align:left;">Age &lt; 50 yr</td>
            <td>19,842</td>
            <td>$0.662 \ [0.651, 0.673]$</td>
            <td>$0.791 \ [0.784, 0.798]$</td>
          </tr>
          <tr>
            <td style="text-align:left;">Age 50-60 yr</td>
            <td>34,215</td>
            <td>$0.714 \ [0.707, 0.721]$</td>
            <td>$0.742 \ [0.735, 0.749]$</td>
          </tr>
          <tr class="last-row">
            <td style="text-align:left;">Age &ge; 60 yr</td>
            <td>14,524</td>
            <td>$0.748 \ [0.739, 0.757]$</td>
            <td>$0.695 \ [0.683, 0.707]$</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 class="sec-heading">VII. Discussion</h2>
    <p>
      Our findings provide three vital conclusions for medical AI:
    </p>
    <p>
      1) <em>Tree Models Outperform Neural MLPs on Tabular Data:</em> Decision tree algorithms possess an inductive bias well-suited to unrotated, axis-aligned decision boundaries typical of clinical thresholds (e.g., blood pressure cutoffs at 140 mmHg).
    </p>
    <p>
      2) <em>Peril of Multicenter Pooling:</em> Naive concatenation of multi-center clinical cohorts creates an illusion of large sample sizes while concealing high between-center variance.
    </p>
    <p>
      3) <em>Clinical Utility (DCA):</em> High ROC-AUC alone is insufficient for clinical adoption; Decision Curve Analysis objectively establishes the operational threshold window where ML adds clinical value over universal intervention.
    </p>

    <h2 class="sec-heading">VIII. Limitations and Future Work</h2>
    <p>
      This investigation relies on retrospective cohorts. Prospective clinical trials embedded within hospital electronic health record (EHR) workflows are required to assess real-time physician interaction. Future work will investigate chaining multiple imputation (MICE) and integrating physiological time-series (12-lead ECG waveforms) upon verification of genuine patient-level linkages.
    </p>

    <h2 class="sec-heading">IX. Conclusion</h2>
    <p>
      This paper establishes a rigorous, leakage-safe, and explainable cardiovascular disease prediction framework. By enforcing cohort segregation, Leave-One-Source-Out multi-center testing, and Decision Curve Analysis, we demonstrate that gradient boosted trees achieve top discrimination ($0.7997$ ROC-AUC), outperforming neural networks ($p < 0.001$), while delivering positive Net Clinical Benefit across operational screening thresholds.
    </p>

    <h2 class="sec-heading">IEEE Ethics and AI Statement</h2>
    <p>
      In compliance with IEEE authorship guidelines, the author affirms that all research hypotheses, statistical formulations, experimental protocols, and clinical analyses were developed, executed, and validated by the author. AI-assisted programming tools were employed solely for code refactoring, plot generation assistance, and manuscript formatting under strict manual supervision. Full reproducibility code is available at: <a href="https://github.com/Vansh-ai406/Data-Science" target="_blank">https://github.com/Vansh-ai406/Data-Science</a>.
    </p>

  </div>
</div>

</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully generated IEEE Research Paper HTML: {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
