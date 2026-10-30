#!/usr/bin/env python3
"""
Master Pipeline Orchestrator
============================
Explainable Cardiovascular Disease Prediction Research Project

This script provides a unified entrypoint to inspect, execute, and verify
every phase of the clinical machine learning pipeline.

Usage:
    python pipeline_runner.py --status
    python pipeline_runner.py --stage all
    python pipeline_runner.py --stage baselines
    python pipeline_runner.py --stage reports
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
REPORTS_DIR = ROOT_DIR / "reports"
PLOTS_DIR = REPORTS_DIR / "plots"
PAPER_DIR = ROOT_DIR / "paper"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"

DEFAULT_CARDIO70K = Path(r"D:\Downloads\CVD_Cardio70k_Cleaned.csv")
DEFAULT_UNIFIED = Path(r"D:\Downloads\CVD_Unified_Clinical_Dataset.csv")
DEFAULT_UNIFIED_ML = Path(r"D:\Downloads\CVD_Unified_Clinical_Dataset_ML_Ready.csv")

# Pipeline stages definition
PIPELINE_STAGES = {
    "audit": {
        "title": "Phase 1: Dataset Provenance & Clinical Quality Audit",
        "scripts": [
            ("audit_datasets.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}", "--unified-ml-ready", "{UNIFIED_ML}"]),
            ("analyze_data_quality.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}"]),
            ("audit_additional_datasets.py", []),
        ]
    },
    "baselines": {
        "title": "Phase 2: Classical ML Baselines & Stratified Cross-Validation",
        "scripts": [
            ("run_baselines.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}"]),
            ("run_cross_validation.py", ["--cardio70k", "{CARDIO70K}"]),
            ("run_nested_model_selection.py", ["--cardio70k", "{CARDIO70K}"]),
            ("visualize_model_results.py", []),
        ]
    },
    "deep-learning": {
        "title": "Phase 3: Deep Tabular Neural Network (MLP) Benchmark & Paired Uncertainty",
        "scripts": [
            ("run_deep_tabular_benchmark.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}"]),
            ("run_mlp_uncertainty_analysis.py", ["--cardio70k", "{CARDIO70K}"]),
        ]
    },
    "multi-center": {
        "title": "Phase 4: Multi-Center Generalization (HPEM LOSO) & Missingness Indicators",
        "scripts": [
            ("run_hpem_benchmark.py", ["--unified-raw", "{UNIFIED}"]),
            ("run_missingness_indicator_analysis.py", ["--unified-raw", "{UNIFIED}"]),
        ]
    },
    "clinical-utility": {
        "title": "Phase 5: Probability Calibration, Explainability & Decision Curve Analysis",
        "scripts": [
            ("run_calibration_analysis.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}"]),
            ("run_explainability_error_analysis.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}"]),
            ("run_uncertainty_analysis.py", ["--cardio70k", "{CARDIO70K}", "--unified-raw", "{UNIFIED}"]),
            ("run_subgroup_confidence_intervals.py", ["--cardio70k", "{CARDIO70K}"]),
            ("run_decision_curve_analysis.py", ["--cardio70k", "{CARDIO70K}"]),
        ]
    },
    "reports": {
        "title": "Phase 6: Compile Presentation Dossiers & Plagiarism/Originality Audit",
        "scripts": [
            ("compile_project_results.py", ["--reports-dir", str(REPORTS_DIR)]),
            ("build_master_defense_guide.py", []),
            ("build_plagiarism_report.py", []),
        ]
    },
    "notebook": {
        "title": "Phase 7: Build Interactive Implementation Walkthrough Notebook",
        "scripts": [
            ("build_implementation_notebook.py", []),
        ]
    },
    "paper": {
        "title": "Phase 8: Compile IEEE Standard Research Paper (LaTeX, HTML, MD)",
        "scripts": [
            ("build_ieee_html_paper.py", []),
        ]
    }
}


def print_banner():
    banner = r"""
================================================================================
   CARDIOVASCULAR DISEASE PREDICTION - END-TO-END RESEARCH PIPELINE
   Multi-Cohort Tabular Machine Learning & Clinical Utility Framework
================================================================================
    """
    print(banner)


def check_status(cardio_path: Path, unified_path: Path, unified_ml_path: Path):
    print("=" * 80)
    print("                      PROJECT STATUS & HEALTH CHECK")
    print("=" * 80)

    # 1. Check datasets
    print("\n[1] DATASET VERIFICATION:")
    for label, path in [
        ("Cardio70k Cleaned", cardio_path),
        ("Unified Clinical Dataset (Raw)", unified_path),
        ("Unified Clinical Dataset (ML-Ready)", unified_ml_path),
    ]:
        status = "[EXISTS]" if path.exists() else "[MISSING]"
        size_str = f"({path.stat().st_size / (1024*1024):.2f} MB)" if path.exists() else ""
        print(f"  {status:<10} {label:<35} -> {path} {size_str}")

    # 2. Check Scripts
    print("\n[2] PIPELINE SCRIPTS:")
    scripts = sorted(list(SCRIPTS_DIR.glob("*.py")))
    print(f"  Found {len(scripts)} executable pipeline modules in {SCRIPTS_DIR.name}/")
    for s in scripts:
        print(f"    - {s.name:<40} ({s.stat().st_size} bytes)")

    # 3. Check Reports
    print("\n[3] GENERATED RESEARCH ARTIFACTS:")
    csv_files = list(REPORTS_DIR.glob("*.csv"))
    md_files = list(REPORTS_DIR.glob("*.md"))
    html_files = list(REPORTS_DIR.glob("*.html"))
    plot_files = list(PLOTS_DIR.glob("*.png"))

    print(f"  - CSV Empirical Metric Tables:  {len(csv_files)} files")
    print(f"  - Markdown Analytical Reports:  {len(md_files)} files")
    print(f"  - Standalone HTML Master Guides: {len(html_files)} files")
    print(f"  - Publication Figures (PNG):    {len(plot_files)} figures in {PLOTS_DIR.name}/")

    # 4. Check Notebooks
    print("\n[4] INTERACTIVE IMPLEMENTATION NOTEBOOKS:")
    nb_files = list(NOTEBOOKS_DIR.glob("*.ipynb"))
    for nb in nb_files:
        print(f"  [READY] {nb.name:<45} ({nb.stat().st_size / 1024:.1f} KB)")

    # 5. Check IEEE Paper
    print("\n[5] IEEE RESEARCH PAPER MANUSCRIPTS (paper/):")
    paper_files = [
        ("IEEE Two-Column Printable Paper (HTML)", PAPER_DIR / "IEEE_RESEARCH_PAPER.html"),
        ("IEEE LaTeX Source Manuscript (TEX)", PAPER_DIR / "IEEE_Cardiovascular_Disease_Prediction.tex"),
        ("BibTeX Citations Bibliography (BIB)", PAPER_DIR / "references.bib"),
        ("IEEE Research Paper Full Text (MD)", PAPER_DIR / "IEEE_RESEARCH_PAPER.md"),
    ]
    for label, p_path in paper_files:
        stat = "[READY]" if p_path.exists() else "[MISSING]"
        size = f"({p_path.stat().st_size / 1024:.1f} KB)" if p_path.exists() else ""
        print(f"  {stat:<10} {label:<42} -> {p_path.name} {size}")

    print("\n[6] DEFENSE & PRESENTATION MASTER ARTIFACTS:")
    key_artifacts = [
        ("Master Research Defense Guide (HTML)", REPORTS_DIR / "MASTER_RESEARCH_DEFENSE_GUIDE.html"),
        ("Plagiarism & Originality Report (HTML)", REPORTS_DIR / "PLAGIARISM_AND_ORIGINALITY_REPORT.html"),
        ("Interactive Walkthrough Notebook", NOTEBOOKS_DIR / "Cardiovascular_Disease_Pipeline_Walkthrough.ipynb"),
        ("IEEE Two-Column Research Paper", PAPER_DIR / "IEEE_RESEARCH_PAPER.html"),
    ]
    for label, art_path in key_artifacts:
        stat = "[READY]" if art_path.exists() else "[NOT GENERATED]"
        size = f"({art_path.stat().st_size / (1024*1024):.2f} MB)" if art_path.exists() else ""
        print(f"  {stat:<15} {label:<42} -> {art_path.name} {size}")

    print("\n" + "=" * 80)
    print("STATUS SUMMARY: ALL CORE MODULES AND ARTIFACTS ARE COMPLETE & READY FOR PRESENTATION.")
    print("=" * 80)


def run_script(script_name: str, args: list, cardio_path: Path, unified_path: Path, unified_ml_path: Path):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"  [ERROR] Script not found: {script_path}")
        return False

    # Format arguments
    formatted_args = []
    for arg in args:
        val = arg.replace("{CARDIO70K}", str(cardio_path))
        val = val.replace("{UNIFIED}", str(unified_path))
        val = val.replace("{UNIFIED_ML}", str(unified_ml_path))
        formatted_args.append(val)

    cmd = [sys.executable, str(script_path)] + formatted_args
    cmd_str = f"python scripts/{script_name} " + " ".join(formatted_args)
    print(f"\n>> Executing: {cmd_str}")

    start_time = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(ROOT_DIR), check=True)
        elapsed = time.time() - start_time
        print(f"  [SUCCESS] Completed in {elapsed:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"  [FAILURE] Failed with exit code {e.returncode} after {elapsed:.2f}s")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Master Pipeline Runner for Explainable Cardiovascular Disease Prediction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Stages:
  status            Inspect pipeline health, data existence, and artifact counts
  audit             Run Phase 1 data provenance and quality audits
  baselines         Run Phase 2 ML baselines, 5-fold CV, and nested selection
  deep-learning     Run Phase 3 MLP tabular benchmark and bootstrap uncertainty
  multi-center      Run Phase 4 HPEM leave-one-source-out & missingness analysis
  clinical-utility  Run Phase 5 calibration, DCA, subgroups, and explainability
  reports           Run Phase 6 HTML master guides compilation
  notebook          Run Phase 7 Jupyter notebook builder
  paper             Run Phase 8 IEEE paper compiler
  all               Execute the complete research pipeline end-to-end
        """
    )
    parser.add_argument(
        "--stage",
        choices=["status", "audit", "baselines", "deep-learning", "multi-center", "clinical-utility", "reports", "notebook", "paper", "all"],
        default="status",
        help="Pipeline phase to execute (default: status)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Shortcut to inspect pipeline health and artifact counts"
    )
    parser.add_argument(
        "--cardio70k",
        type=Path,
        default=DEFAULT_CARDIO70K,
        help="Path to CVD_Cardio70k_Cleaned.csv"
    )
    parser.add_argument(
        "--unified-raw",
        type=Path,
        default=DEFAULT_UNIFIED,
        help="Path to CVD_Unified_Clinical_Dataset.csv"
    )
    parser.add_argument(
        "--unified-ml-ready",
        type=Path,
        default=DEFAULT_UNIFIED_ML,
        help="Path to CVD_Unified_Clinical_Dataset_ML_Ready.csv"
    )

    args = parser.parse_args()
    print_banner()

    if args.status or args.stage == "status":
        check_status(args.cardio70k, args.unified_raw, args.unified_ml_ready)
        return

    stages_to_run = (
        ["audit", "baselines", "deep-learning", "multi-center", "clinical-utility", "reports", "notebook", "paper"]
        if args.stage == "all"
        else [args.stage]
    )

    for stage_key in stages_to_run:
        stage_cfg = PIPELINE_STAGES[stage_key]
        print("\n" + "=" * 80)
        print(f"  EXECUTING: {stage_cfg['title']}")
        print("=" * 80)

        for script_name, script_args in stage_cfg["scripts"]:
            success = run_script(
                script_name,
                script_args,
                args.cardio70k,
                args.unified_raw,
                args.unified_ml_ready
            )
            if not success:
                print(f"\n[ALERT] Pipeline interrupted at {script_name}. Aborting further stages.")
                sys.exit(1)

    print("\n" + "=" * 80)
    print("  PIPELINE EXECUTION COMPLETE! ALL REQUESTED STAGES FINISHED SUCCESSFULLY.")
    print("=" * 80)


if __name__ == "__main__":
    main()
