"""Run initial leakage-safe baselines on the two separate clinical cohorts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier


RANDOM_SEED = 42
TEST_SIZE = 0.2
THRESHOLD = 0.5

CARDIO_CATEGORICAL = [
    "sex",
    "bp_category",
    "cholesterol_level",
    "glucose_level",
    "smoking",
    "alcohol",
    "physically_active",
]
CARDIO_NUMERICAL = [
    "age_years",
    "height_cm",
    "weight_kg",
    "bmi",
    "systolic_bp",
    "diastolic_bp",
    "pulse_pressure",
]
UNIFIED_CATEGORICAL = [
    "sex",
    "chest_pain_type",
    "fasting_blood_sugar",
    "resting_ecg",
    "exercise_angina",
    "st_slope",
    "num_major_vessels",
    "thalassemia",
]
UNIFIED_NUMERICAL = ["age", "resting_bp", "cholesterol", "max_heart_rate", "oldpeak"]


def make_preprocessor(
    categorical: list[str], numerical: list[str], scale_numerical: bool
) -> ColumnTransformer:
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numerical:
        numeric_steps.append(("scaler", StandardScaler()))
    return ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(numeric_steps),
                numerical,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                categorical,
            ),
        ],
        remainder="drop",
    )


def make_models(categorical: list[str], numerical: list[str]) -> dict[str, Pipeline]:
    estimators = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
        "MLP": MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation="relu",
            solver="adam",
            alpha=0.001,
            batch_size=256,
            learning_rate_init=0.001,
            max_iter=200,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=15,
            random_state=RANDOM_SEED,
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=250,
            min_samples_leaf=2,
            n_jobs=-1,
            random_state=RANDOM_SEED,
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=150,
            learning_rate=0.08,
            l2_regularization=1.0,
            random_state=RANDOM_SEED,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            eval_metric="logloss",
            tree_method="hist",
            n_jobs=-1,
            random_state=RANDOM_SEED,
        ),
    }
    models = {}
    for name, estimator in estimators.items():
        models[name] = Pipeline(
            [
                (
                    "preprocessor",
                    make_preprocessor(
                        categorical,
                        numerical,
                        scale_numerical=name in {"LogisticRegression", "MLP"},
                    ),
                ),
                ("model", estimator),
            ]
        )
    return models


def calculate_metrics(
    y_true: pd.Series, probabilities: pd.Series | list[float]
) -> dict[str, float]:
    predictions = (pd.Series(probabilities, index=y_true.index) >= THRESHOLD).astype(int)
    true_negative, false_positive, false_negative, true_positive = confusion_matrix(
        y_true, predictions, labels=[0, 1]
    ).ravel()
    return {
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "sensitivity": recall_score(y_true, predictions, zero_division=0),
        "specificity": true_negative / (true_negative + false_positive),
        "f1": f1_score(y_true, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probabilities),
        "pr_auc": average_precision_score(y_true, probabilities),
        "brier_score": brier_score_loss(y_true, probabilities),
    }


def evaluate_split(
    cohort: str,
    split_name: str,
    features: pd.DataFrame,
    target: pd.Series,
    categorical: list[str],
    numerical: list[str],
) -> list[dict[str, object]]:
    output = []
    for model_name, model in make_models(categorical, numerical).items():
        model.fit(features, target)
        probabilities = model.predict_proba(features)[:, 1]
        row: dict[str, object] = {
            "cohort": cohort,
            "evaluation": split_name,
            "source": "",
            "model": model_name,
            "n_train": len(target),
            "n_test": len(target),
        }
        row.update(calculate_metrics(target, probabilities))
        output.append(row)
    return output


def run_cardio70k(path: Path) -> tuple[list[dict[str, object]], int, int]:
    frame = pd.read_csv(path)
    excluded = {"patient_id", "target"}
    features = frame.drop(columns=list(excluded))
    target = frame["target"].astype(int)
    train_x, test_x, train_y, test_y = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=target,
    )
    shared_profiles = set(
        pd.util.hash_pandas_object(train_x, index=False).tolist()
    ).intersection(pd.util.hash_pandas_object(test_x, index=False).tolist())
    results = []
    engineered_features = ["bmi", "pulse_pressure", "bp_category"]
    feature_sets = [
        (
            "All candidate predictors",
            train_x,
            test_x,
            CARDIO_CATEGORICAL,
            CARDIO_NUMERICAL,
        ),
        (
            "Exclude BMI, pulse pressure, BP category",
            train_x.drop(columns=engineered_features),
            test_x.drop(columns=engineered_features),
            [column for column in CARDIO_CATEGORICAL if column not in engineered_features],
            [column for column in CARDIO_NUMERICAL if column not in engineered_features],
        ),
    ]
    for feature_set, fit_x, evaluate_x, categorical, numerical in feature_sets:
        for model_name, model in make_models(categorical, numerical).items():
            model.fit(fit_x, train_y)
            probabilities = model.predict_proba(evaluate_x)[:, 1]
            row: dict[str, object] = {
                "cohort": "Cardio70k",
                "evaluation": "stratified 80/20 patient holdout",
                "feature_set": feature_set,
                "source": "",
                "model": model_name,
                "n_train": len(train_y),
                "n_test": len(test_y),
            }
            row.update(calculate_metrics(test_y, probabilities))
            results.append(row)
    return results, len(shared_profiles), int(frame["patient_id"].nunique())


def run_unified_source_holdout(path: Path) -> list[dict[str, object]]:
    frame = pd.read_csv(path)
    feature_columns = UNIFIED_CATEGORICAL + UNIFIED_NUMERICAL
    results = []
    for held_out_source in sorted(frame["source"].unique()):
        train = frame.loc[frame["source"] != held_out_source]
        test = frame.loc[frame["source"] == held_out_source]
        train_x = train[feature_columns]
        test_x = test[feature_columns]
        train_y = train["target"].astype(int)
        test_y = test["target"].astype(int)
        if train_y.nunique() != 2 or test_y.nunique() != 2:
            raise ValueError(f"Both target classes are required for {held_out_source}.")
        for model_name, model in make_models(
            UNIFIED_CATEGORICAL, UNIFIED_NUMERICAL
        ).items():
            model.fit(train_x, train_y)
            probabilities = model.predict_proba(test_x)[:, 1]
            row: dict[str, object] = {
                "cohort": "Unified clinical",
                "evaluation": "leave-one-source-out",
                "feature_set": "Original clinical predictors",
                "source": held_out_source,
                "model": model_name,
                "n_train": len(train_y),
                "n_test": len(test_y),
            }
            row.update(calculate_metrics(test_y, probabilities))
            results.append(row)
    return results


def render_markdown_table(
    frame: pd.DataFrame, metric_columns: list[str]
) -> str:
    columns = list(frame.columns)
    rows = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        cells = [
            f"{value:.3f}" if column in metric_columns else str(value)
            for column, value in zip(columns, values)
        ]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def write_report(
    results: pd.DataFrame,
    profile_overlap: int,
    unique_cardio_ids: int,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    results_path = output_dir / "baseline_metrics.csv"
    report_path = output_dir / "baseline_results.md"
    results.to_csv(results_path, index=False)

    metric_columns = [
        "accuracy",
        "precision",
        "sensitivity",
        "specificity",
        "f1",
        "roc_auc",
        "pr_auc",
        "brier_score",
    ]
    display = results.copy()
    cardio = display.loc[display["cohort"] == "Cardio70k"]
    cardio_full = cardio.loc[cardio["feature_set"] == "All candidate predictors"]
    cardio_ablated = cardio.loc[
        cardio["feature_set"] == "Exclude BMI, pulse pressure, BP category"
    ]
    unified = display.loc[display["cohort"] == "Unified clinical"]
    metric_display_columns = [
        "model",
        "n_train",
        "n_test",
        *metric_columns,
    ]
    report = [
        "# Initial Baseline Results",
        "",
        "Exploratory, fixed-configuration baselines. These results are not clinical "
        "claims and are not external validation.",
        "",
        "## Cardio70k",
        "",
        "A stratified 80/20 patient-level holdout with seed 42. Preprocessing is "
        "fitted inside each model pipeline using training data only. The file has "
        f"{unique_cardio_ids:,} unique patient IDs. There are {profile_overlap:,} "
        "identical predictor profiles appearing in both partitions; they are "
        "reported, not dropped, because IDs are distinct and identical profiles "
        "can represent different patients.",
        "",
        "### All candidate predictors",
            "",
            render_markdown_table(cardio_full[metric_display_columns], metric_columns),
            "",
            "### Excluding deterministic derived features",
            "",
            "Same patient split and model settings as above; excludes stored BMI, "
            "pulse pressure, and BP category while retaining their underlying height, "
            "weight, systolic BP, and diastolic BP inputs.",
            "",
            render_markdown_table(cardio_ablated[metric_display_columns], metric_columns),
        "",
        "## Unified clinical cohort",
        "",
        "Leave one source out at a time. The held-out source is never used to fit "
        "imputation, encoding, scaling, or model parameters. `disease_severity`, "
        "IDs, country, and source are not predictors. Interpret per-source results "
        "in light of small and strongly different cohorts; this is internal "
        "cross-source evaluation, not independent external validation.",
        "",
        render_markdown_table(unified, metric_columns),
        "",
        "## Metrics and limits",
        "",
        "Metrics use a fixed probability threshold of 0.5 for threshold-dependent "
        "scores; ROC-AUC and PR-AUC use probabilities. Brier score measures "
        "probability error (lower is better). No hyperparameter tuning was done, "
        "and no confidence intervals are included yet. Because multiple fixed "
        "models and feature sets were compared on this same holdout, it is "
        "exploratory and is not an untouched final test set. Before model "
        "selection or final performance claims, use nested/repeated validation "
        "or reserve a fresh final test set. Then assess calibration, uncertainty, "
        "and explainability.",
        "",
        f"Machine-readable metrics: `{results_path.as_posix()}`.",
    ]
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Wrote {report_path} and {results_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cardio70k", type=Path, required=True)
    parser.add_argument("--unified-raw", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()

    cardio_results, profile_overlap, unique_ids = run_cardio70k(args.cardio70k)
    unified_results = run_unified_source_holdout(args.unified_raw)
    results = pd.DataFrame(cardio_results + unified_results)
    write_report(results, profile_overlap, unique_ids, args.output_dir)


if __name__ == "__main__":
    main()