"""Create a reproducible inventory of the supplied CVD tabular datasets."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def inspect_dataset(label: str, path: Path) -> tuple[str, pd.DataFrame]:
    frame = pd.read_csv(path)
    lines = [
        f"## {label}",
        "",
        f"- File: `{path}`",
        f"- Shape: {len(frame):,} rows x {len(frame.columns):,} columns",
        f"- Exact duplicate rows: {int(frame.duplicated().sum()):,}",
    ]

    if "patient_id" in frame:
        lines.append(
            f"- Duplicate patient IDs: {int(frame['patient_id'].duplicated().sum()):,}"
        )
        non_id_columns = [column for column in frame.columns if column != "patient_id"]
        lines.append(
            "- Rows identical across predictors/label except ID (review; not "
            "automatically duplicates): "
            f"{int(frame.duplicated(subset=non_id_columns).sum()):,}"
        )

    if "target" in frame:
        counts = frame["target"].value_counts(dropna=False).sort_index()
        lines.extend(["", "### Target distribution", "", "| Target | Rows | Percent |", "|---:|---:|---:|"])
        for target, count in counts.items():
            lines.append(f"| {target} | {count:,} | {count / len(frame) * 100:.2f}% |")
        if frame["target"].isna().any():
            lines.append(f"| Missing | {int(frame['target'].isna().sum()):,} | |")
        if not counts.index.isin([0, 1]).all():
            lines.append("\n> Target contains values beyond binary 0/1; verify its definition.")

    lines.extend(
        [
            "",
            "### Columns and missingness",
            "",
            "| Column | Type | Missing | Missing % |",
            "|---|---|---:|---:|",
        ]
    )
    for column in frame.columns:
        missing = int(frame[column].isna().sum())
        lines.append(
            f"| {column} | {frame[column].dtype} | {missing:,} | "
            f"{missing / len(frame) * 100:.2f}% |"
        )

    if "source" in frame and "target" in frame:
        table = pd.crosstab(frame["source"], frame["target"], margins=True)
        table_text = "\n".join(line.rstrip() for line in table.to_string().splitlines())
        lines.extend(
            ["", "### Target by source", "", "```text", table_text, "```"]
        )

    if "disease_severity" in frame.columns:
        lines.extend(
            [
                "",
                "> Exclude `disease_severity` from predictors: the data dictionary "
                "states that it directly defines `target` for UCI records.",
            ]
        )

    return "\n".join(lines), frame


def compare_ready_export(raw: pd.DataFrame, ready: pd.DataFrame) -> str:
    lines = ["## Raw vs. ML-ready unified export", ""]
    lines.append(f"- Same row count: {len(raw) == len(ready)}")
    same_ids = True
    if "patient_id" in raw and "patient_id" in ready:
        same_ids = set(raw["patient_id"]) == set(ready["patient_id"])
        lines.append(
            f"- Same patient ID set: {same_ids}"
        )
        if not same_ids or len(raw) != len(ready):
            lines.append("- Value comparison skipped because rows cannot be aligned safely.")
            return "\n".join(lines)
        raw = raw.set_index("patient_id").sort_index()
        ready = ready.set_index("patient_id").sort_index()
    shared = [column for column in raw.columns if column in ready.columns]
    changed = {}
    for column in shared:
        left = raw[column]
        right = ready[column]
        if len(left) == len(right):
            equal = left.eq(right).fillna(False) | (left.isna() & right.isna())
            count = int((~equal).sum())
            if count:
                changed[column] = count
    lines.extend(
        [
            f"- Shared columns with changed values (including imputations): `{changed}`",
            "",
            "> Use the raw CSV for model development. The data dictionary says the "
            "ML-ready export uses whole-file median/mode imputation; refit all "
            "preprocessing inside each training fold to avoid leakage.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--unified-ml-ready", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/dataset_audit.md"),
        help="Markdown report path (default: reports/dataset_audit.md)",
    )
    args = parser.parse_args()

    cardio_report, _ = inspect_dataset("Cardio70k cleaned cohort", args.cardio70k)
    unified_report, unified = inspect_dataset("Unified clinical cohort (raw)", args.unified_raw)
    sections = ["# Initial Dataset Audit", "", cardio_report, "", unified_report]

    if args.unified_ml_ready:
        ready_report, ready = inspect_dataset(
            "Unified clinical cohort (ML-ready; audit only)", args.unified_ml_ready
        )
        sections.extend(
            ["", ready_report, "", compare_ready_export(unified, ready)]
        )

    sections.extend(
        [
            "",
            "## Initial analysis decisions",
            "",
            "- Keep Cardio70k and the unified clinical cohort as separate analyses; "
            "there is no patient linkage and their predictor schemas differ.",
            "- Treat `target` as contemporaneous disease classification, not future "
            "risk, unless source documentation establishes otherwise.",
            "- Do not use identifiers as predictors. Keep cohort/source metadata for "
            "grouped evaluation, not as model inputs in cross-source tests.",
            "- No linked image files were supplied with these CSVs; image fusion is "
            "out of scope until compatible paired data are available.",
            "- Identical predictor/label profiles with different IDs are flagged "
            "for review; do not remove them without evidence that they are duplicate patients.",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote audit report: {args.output}")


if __name__ == "__main__":
    main()