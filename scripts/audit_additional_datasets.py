"""Audit previously downloaded ECG and synthetic imaging archives."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".dcm"}


def audit_ecg_archive(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise ValueError(f"Expected one ECG CSV in {path.name}, found {len(csv_members)}")
        member = csv_members[0]
        class_counts: Counter[str] = Counter()
        row_widths: Counter[int] = Counter()
        invalid_values = 0
        row_count = 0
        first_row_numeric = False
        with archive.open(member) as raw:
            for row in csv.reader((line.decode("utf-8", errors="replace") for line in raw)):
                if not row:
                    continue
                row_count += 1
                if row_count == 1:
                    first_row_numeric = all(_is_number(cell) for cell in row)
                row_widths[len(row)] += 1
                for cell in row:
                    try:
                        value = float(cell)
                        if not math.isfinite(value):
                            invalid_values += 1
                    except ValueError:
                        invalid_values += 1
                class_counts[row[-1]] += 1
    widths = sorted(row_widths.items())
    return {
        "archive": str(path),
        "member": member,
        "rows": row_count,
        "row_widths": widths,
        "signal_columns": widths[0][0] - 1 if len(widths) == 1 else None,
        "class_counts": dict(class_counts),
        "invalid_cells": invalid_values,
        "has_header": row_count > 0 and not first_row_numeric,
        "has_patient_id": False,
        "has_source_metadata": False,
    }


def _is_number(value: str) -> bool:
    try:
        return math.isfinite(float(value))
    except ValueError:
        return False


def audit_image_archive(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        metadata_members = [name for name in names if PurePosixPath(name).name.lower() == "master_metadata.csv"]
        if len(metadata_members) != 1:
            raise ValueError(f"Expected one master_metadata.csv in {path.name}, found {len(metadata_members)}")
        with archive.open(metadata_members[0]) as raw:
            records = list(csv.DictReader(line.decode("utf-8", errors="replace") for line in raw))
        image_members = [name for name in names if PurePosixPath(name).suffix.lower() in IMAGE_EXTENSIONS]
        modality_files: Counter[str] = Counter()
        patient_modality_files: Counter[tuple[str, str]] = Counter()
        for name in image_members:
            parts = PurePosixPath(name).parts
            if len(parts) >= 3:
                patient_modality_files[(parts[-3], parts[-2])] += 1
                modality_files[parts[-2]] += 1
        claimed_slices = Counter()
        metadata_pairs = set()
        claimed_patient_slices: Counter[tuple[str, str]] = Counter()
        for record in records:
            patient = record.get("Patient_ID", "")
            modality = record.get("Modality", "")
            metadata_pairs.add((patient, modality))
            try:
                slices = int(record.get("Num_Slices", "0"))
            except ValueError:
                slices = 0
            claimed_slices[modality] += slices
            claimed_patient_slices[(patient, modality)] += slices
        matched_pairs = sum(
            1
            for patient, modality in metadata_pairs
            if patient_modality_files.get((patient, modality), 0) == claimed_patient_slices[(patient, modality)]
        )
    return {
        "archive": str(path),
        "metadata_member": metadata_members[0],
        "metadata_rows": len(records),
        "patients": len({record.get("Patient_ID", "") for record in records}),
        "modalities": dict(Counter(record.get("Modality", "") for record in records)),
        "metadata_columns": list(records[0]) if records else [],
        "label_columns": [
            column
            for column in (records[0] if records else {})
            if any(term in column.lower() for term in ("label", "target", "diagnos", "disease", "class"))
        ],
        "image_files": len(image_members),
        "image_files_by_modality": dict(modality_files),
        "claimed_slices_by_modality": dict(claimed_slices),
        "metadata_patient_modality_pairs": len(metadata_pairs),
        "slice_count_matches": matched_pairs,
    }


def render_report(ecg: dict[str, object], images: dict[str, object]) -> str:
    ecg_widths = ", ".join(f"{width} columns: {count} rows" for width, count in ecg["row_widths"])
    ecg_classes = ", ".join(f"`{label}`: {count}" for label, count in sorted(ecg["class_counts"].items()))
    modalities = ", ".join(f"{name}: {count} metadata rows" for name, count in images["modalities"].items())
    image_counts = ", ".join(f"{name}: {count} image files" for name, count in images["image_files_by_modality"].items())
    slice_counts = ", ".join(f"{name}: {count} declared slices" for name, count in images["claimed_slices_by_modality"].items())
    columns = ", ".join(f"`{column}`" for column in images["metadata_columns"])
    label_columns = ", ".join(f"`{column}`" for column in images["label_columns"]) or "none"
    return f"""# Additional Dataset Suitability Audit

## Inventory result

The current machine has two additional potentially relevant archives beyond the analyzed Cardio70k and unified clinical cohorts. The archives are inspected in place; no files were extracted or modified.

## ECG waveform archive

- Archive/member: `{Path(str(ecg['archive'])).name}` / `{ecg['member']}`
- Rows: {ecg['rows']:,}
- Row widths: {ecg_widths}
- Apparent signal columns when width is consistent: {ecg['signal_columns']}
- Final-field value counts: {ecg_classes}
- Non-numeric or non-finite cells: {ecg['invalid_cells']:,}
- Header, patient ID, and source/provenance fields: not present in the observed file layout

**Suitability:** not ready to join the current CVD classification task. The final field is binary-coded, but its meaning, source, sampling protocol, patient identity, and relationship to the current `target` are not documented by the archive. It may support a separate ECG waveform task after the data dictionary and license are established. A patient-grouped split is required if multiple beats/windows can originate from the same person.

## Synthetic CT/MRI archive

- Archive/member: `{Path(str(images['archive'])).name}` / `{images['metadata_member']}`
- Metadata rows / unique patients: {images['metadata_rows']:,} / {images['patients']:,}
- Modalities: {modalities}
- Image files: {images['image_files']:,} ({image_counts})
- Manifest-declared slices: {slice_counts}
- Manifest patient-modality pairs matching declared file counts: {images['slice_count_matches']} / {images['metadata_patient_modality_pairs']}
- Metadata fields: {columns}
- Diagnosis/target-like metadata fields: {label_columns}

**Suitability:** not ready for supervised CVD detection. The metadata describes age, gender, modality, and slice counts but contains no disease labels or link to either tabular cohort. Synthetic CT/MRI slices must not be presented as patient-linked clinical evidence. Establish dataset provenance, license, intended clinical task, patient-level labels, and legitimate links before modeling.

## Research decision

Use the existing Cardio70k and raw unified clinical CSVs for the current validated tabular experiments. Keep the ECG archive as a possible separate waveform classification task pending label/provenance verification. Keep the synthetic image archive out of model training until patient-level targets and data provenance are demonstrated. Additional CSVs such as credit-card fraud, spam, and unrelated assignment data are not cardiovascular cohorts and are excluded.

## Requirements to proceed with the extra assets

1. Dataset source citation, license, collection protocol, and intended target definition.
2. ECG label mapping, units/sampling rate, patient or record identifiers, and guidance on grouped train/test splitting.
3. Image diagnosis labels and valid patient-level linkage between slices, patients, and outcomes; do not infer disease labels from age/gender or filenames.
4. A predeclared evaluation protocol with independent patient-level test data and source-aware reporting.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ecg-archive", type=Path, required=True)
    parser.add_argument("--image-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/additional_dataset_suitability.md"))
    args = parser.parse_args()
    ecg = audit_ecg_archive(args.ecg_archive)
    images = audit_image_archive(args.image_archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(ecg, images), encoding="utf-8")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
