"""Profile clinical ranges, outliers, derivations, and cohort differences."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


CARDIO_RANGES = {
    "age_years": (29.6, 64.9),
    "height_cm": (120, 220),
    "weight_kg": (30, 200),
    "bmi": (12, 70),
    "systolic_bp": (70, 250),
    "diastolic_bp": (40, 150),
    "pulse_pressure": (5, 140),
}
CARDIO_CATEGORIES = {
    "sex": {0, 1},
    "bp_category": {0, 1, 2, 3, 4},
    "cholesterol_level": {1, 2, 3},
    "glucose_level": {1, 2, 3},
    "smoking": {0, 1},
    "alcohol": {0, 1},
    "physically_active": {0, 1},
    "target": {0, 1},
}
UNIFIED_RANGES = {
    "age": (20, 80),
    "resting_bp": (80, 200),
    "cholesterol": (85, 603),
    "max_heart_rate": (60, 202),
    "oldpeak": (-2.6, 6.2),
}
UNIFIED_CATEGORIES = {
    "sex": {0, 1},
    "chest_pain_type": {0, 1, 2, 3},
    "fasting_blood_sugar": {0, 1},
    "resting_ecg": {0, 1, 2},
    "exercise_angina": {0, 1},
    "st_slope": {0, 1, 2},
    "num_major_vessels": {0, 1, 2, 3},
    "thalassemia": {0, 1, 2},
    "disease_severity": {0, 1, 2, 3, 4},
    "target": {0, 1},
}
CARDIO_NUMERIC = list(CARDIO_RANGES)
CARDIO_CATEGORICAL = list(CARDIO_CATEGORIES)
UNIFIED_NUMERIC = list(UNIFIED_RANGES)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = row.get(column, "")
            text = "" if pd.isna(value) else str(value)
            cells.append(text.replace("|", "\\|"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def range_checks(
    frame: pd.DataFrame,
    dataset: str,
    ranges: dict[str, tuple[float, float]],
    categories: dict[str, set[int]],
) -> list[dict[str, object]]:
    rows = []
    for column, (lower, upper) in ranges.items():
        invalid = frame[column].notna() & ~frame[column].between(lower, upper)
        rows.append(
            {
                "dataset": dataset,
                "feature": column,
                "check": "legend range (screen only)",
                "expected": f"{lower} to {upper}",
                "outside": int(invalid.sum()),
                "missing": int(frame[column].isna().sum()),
            }
        )
    for column, allowed in categories.items():
        invalid = frame[column].notna() & ~frame[column].isin(allowed)
        rows.append(
            {
                "dataset": dataset,
                "feature": column,
                "check": "allowed codes",
                "expected": ", ".join(map(str, sorted(allowed))),
                "outside": int(invalid.sum()),
                "missing": int(frame[column].isna().sum()),
            }
        )
    return rows


def iqr_flags(
    frame: pd.DataFrame,
    dataset: str,
    numeric_features: list[str],
    group_column: str | None = None,
) -> list[dict[str, object]]:
    groups = [("All records", frame)]
    if group_column:
        groups = list(frame.groupby(group_column, sort=True))
    rows = []
    for group_name, group in groups:
        for feature in numeric_features:
            values = group[feature].dropna()
            if values.empty:
                continue
            first_quartile = values.quantile(0.25)
            third_quartile = values.quantile(0.75)
            spread = third_quartile - first_quartile
            flagged = (values < first_quartile - 1.5 * spread) | (
                values > third_quartile + 1.5 * spread
            )
            rows.append(
                {
                    "dataset": dataset,
                    "source/group": group_name,
                    "feature": feature,
                    "n": len(values),
                    "IQR flags": int(flagged.sum()),
                    "flagged %": f"{flagged.mean() * 100:.2f}%",
                }
            )
    return rows


def cardio_target_summary(frame: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for feature in CARDIO_NUMERIC:
        for target, group in frame.groupby("target", sort=True):
            rows.append(
                {
                    "feature": feature,
                    "target": int(target),
                    "n": len(group),
                    "median": f"{group[feature].median():.2f}",
                    "IQR": (
                        f"{group[feature].quantile(0.25):.2f} - "
                        f"{group[feature].quantile(0.75):.2f}"
                    ),
                }
            )
    for feature in CARDIO_CATEGORICAL:
        if feature == "target":
            continue
        summary = frame.groupby([feature, "target"], observed=True).size().unstack(
            fill_value=0
        )
        for level, counts in summary.iterrows():
            total = int(counts.sum())
            positives = int(counts.get(1, 0))
            rows.append(
                {
                    "feature": f"{feature}={level}",
                    "target": "positive prevalence",
                    "n": total,
                    "median": f"{positives / total * 100:.2f}%",
                    "IQR": "",
                }
            )
    return rows


def unified_source_summary(frame: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for source, group in frame.groupby("source", sort=True):
        row: dict[str, object] = {
            "source": source,
            "n": len(group),
            "positive %": f"{group['target'].mean() * 100:.2f}%",
        }
        for feature in UNIFIED_NUMERIC:
            row[f"{feature} median"] = (
                "NA" if group[feature].notna().sum() == 0 else f"{group[feature].median():.1f}"
            )
            row[f"{feature} missing %"] = f"{group[feature].isna().mean() * 100:.1f}%"
        rows.append(row)
    return rows


def create_report(cardio_path: Path, unified_path: Path, output_path: Path) -> None:
    cardio = pd.read_csv(cardio_path)
    unified = pd.read_csv(unified_path)
    cardio_formula_error = (
        cardio["weight_kg"] / (cardio["height_cm"] / 100) ** 2 - cardio["bmi"]
    ).abs()
    severity_known = unified["disease_severity"].notna()
    severity_mismatches = int(
        (
            unified.loc[severity_known, "target"]
            != (unified.loc[severity_known, "disease_severity"] >= 1).astype(int)
        ).sum()
    )
    profile_duplicates = int(
        cardio.duplicated(subset=[column for column in cardio if column != "patient_id"]).sum()
    )
    features_without_id = [
        column for column in cardio if column not in {"patient_id", "target"}
    ]
    profile_labels = cardio.groupby(features_without_id, dropna=False)["target"].agg(
        ["size", "nunique"]
    )
    repeated_profile_groups = int(profile_labels["size"].gt(1).sum())
    conflicting_profile_groups = int(
        (profile_labels["size"].gt(1) & profile_labels["nunique"].gt(1)).sum()
    )

    range_rows = range_checks(
        cardio, "Cardio70k", CARDIO_RANGES, CARDIO_CATEGORIES
    ) + range_checks(
        unified, "Unified", UNIFIED_RANGES, UNIFIED_CATEGORIES
    )
    outlier_rows = iqr_flags(cardio, "Cardio70k", CARDIO_NUMERIC)
    outlier_rows.extend(iqr_flags(unified, "Unified", UNIFIED_NUMERIC, "source"))
    source_rows = unified_source_summary(unified)

    source_columns = ["source", "n", "positive %"]
    for feature in UNIFIED_NUMERIC:
        source_columns.extend([f"{feature} median", f"{feature} missing %"])

    report = [
        "# Data Quality and Initial EDA",
        "",
        "This is a profiling report, not a cleaning recipe. Values are retained; "
        "statistical flags are not assumed to be errors.",
        "",
        "## Integrity checks",
        "",
        f"- Cardio70k rows identical across predictors and target, excluding ID: {profile_duplicates:,}; "
        f"they form {repeated_profile_groups:,} repeated profiles, of which "
        f"{conflicting_profile_groups:,} have conflicting targets. They are not confirmed duplicate patients.",
        f"- Cardio70k BMI formula maximum absolute difference: {cardio_formula_error.max():.3f} kg/m^2; "
        "the stored BMI is rounded to one decimal place.",
        f"- Cardio70k pulse-pressure formula mismatches: "
        f"{int((cardio['systolic_bp'] - cardio['diastolic_bp'] != cardio['pulse_pressure']).sum()):,}.",
        f"- Unified target vs. documented severity (`disease_severity >= 1`) mismatches "
        f"among rows with known severity: {severity_mismatches:,} of {int(severity_known.sum()):,}.",
        "- IDs, source metadata, and `disease_severity` are not model predictors; "
        "severity directly defines the outcome for the applicable UCI rows.",
        "",
        "## Documented range checks",
        "",
        "Numeric ranges come from the supplied legend and may describe observed "
        "dataset ranges rather than physiological validity limits; they are "
        "screening references, not grounds for deleting records. Categorical "
        "checks verify documented code sets.",
        "",
        markdown_table(
            range_rows,
            ["dataset", "feature", "check", "expected", "outside", "missing"],
        ),
        "",
        "## IQR outlier flags",
        "",
        "Flags use the 1.5 x IQR rule. They are prompts for review, not removal "
        "criteria; unified-cohort flags are computed separately within each source.",
        "",
        markdown_table(
            outlier_rows,
            ["dataset", "source/group", "feature", "n", "IQR flags", "flagged %"],
        ),
        "",
        "## Unified cohort by source",
        "",
        "Source-specific prevalence and observed medians/missingness show that "
        "the cohorts differ. This can contribute to transfer-performance changes; "
        "it does not by itself identify the cause.",
        "",
        markdown_table(source_rows, source_columns),
        "",
        "## Cardio70k by target",
        "",
        "Numeric summaries report medians and IQRs. Categorical rows report "
        "within-level positive prevalence. These are descriptive associations, "
        "not causal effects.",
        "",
        markdown_table(
            cardio_target_summary(cardio),
            ["feature", "target", "n", "median", "IQR"],
        ),
        "",
        "## Preprocessing implications",
        "",
        "- Keep legitimate extreme measurements; investigate only documented "
        "range violations or source-specific coding anomalies.",
        "- Preserve Cardio70k's distinct patient rows even when predictor profiles "
        "match; record profile overlap in evaluation reports.",
        "- The unified cohort has strong source differences and non-random missingness. "
        "Fit imputers/encoders inside each training split and report source-held-out "
        "performance rather than relying only on pooled random splits.",
        "- Cardio70k includes deterministic derived features (BMI, pulse pressure, "
        "BP category). Add a predeclared ablation without derived fields to test "
        "whether they add value beyond their source measurements.",
        "- Cardio70k target prevalence is near 50/50; do not add SMOTE by default. "
        "For other cohorts, assess imbalance within each evaluation split before "
        "choosing class weights or resampling.",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Wrote data-quality report: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/data_quality.md"),
    )
    args = parser.parse_args()
    create_report(args.cardio70k, args.unified_raw, args.output)


if __name__ == "__main__":
    main()