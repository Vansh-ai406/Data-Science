# Additional Dataset Suitability Audit

## Inventory result

The current machine has two additional potentially relevant archives beyond the analyzed Cardio70k and unified clinical cohorts. The archives are inspected in place; no files were extracted or modified.

## ECG waveform archive

- Archive/member: `archive (3).zip` / `ecg.csv`
- Rows: 4,998
- Row widths: 141 columns: 4998 rows
- Apparent signal columns when width is consistent: 140
- Final-field value counts: `0.0`: 2079, `1.0`: 2919
- Non-numeric or non-finite cells: 0
- Header, patient ID, and source/provenance fields: not present in the observed file layout

**Suitability:** not ready to join the current CVD classification task. The final field is binary-coded, but its meaning, source, sampling protocol, patient identity, and relationship to the current `target` are not documented by the archive. It may support a separate ECG waveform task after the data dictionary and license are established. A patient-grouped split is required if multiple beats/windows can originate from the same person.

## Synthetic CT/MRI archive

- Archive/member: `archive (4).zip` / `synthetic_slices (2)/master_metadata.csv`
- Metadata rows / unique patients: 300 / 150
- Modalities: CT: 150 metadata rows, MRI: 150 metadata rows
- Image files: 30,352 (DICOM TO PNG : 50 image files, CT: 15127 image files, MRI: 15174 image files)
- Manifest-declared slices: CT: 15127 declared slices, MRI: 15174 declared slices
- Manifest patient-modality pairs matching declared file counts: 300 / 300
- Metadata fields: `Patient_ID`, `Age`, `Gender`, `Modality`, `Num_Slices`, `Folder_Path`
- Diagnosis/target-like metadata fields: none

**Suitability:** not ready for supervised CVD detection. The metadata describes age, gender, modality, and slice counts but contains no disease labels or link to either tabular cohort. Synthetic CT/MRI slices must not be presented as patient-linked clinical evidence. Establish dataset provenance, license, intended clinical task, patient-level labels, and legitimate links before modeling.

## Research decision

Use the existing Cardio70k and raw unified clinical CSVs for the current validated tabular experiments. Keep the ECG archive as a possible separate waveform classification task pending label/provenance verification. Keep the synthetic image archive out of model training until patient-level targets and data provenance are demonstrated. Additional CSVs such as credit-card fraud, spam, and unrelated assignment data are not cardiovascular cohorts and are excluded.

## Requirements to proceed with the extra assets

1. Dataset source citation, license, collection protocol, and intended target definition.
2. ECG label mapping, units/sampling rate, patient or record identifiers, and guidance on grouped train/test splitting.
3. Image diagnosis labels and valid patient-level linkage between slices, patients, and outcomes; do not infer disease labels from age/gender or filenames.
4. A predeclared evaluation protocol with independent patient-level test data and source-aware reporting.
