import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# ----------------------------
# Correct Dataset Path
# ----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "job_postings.csv"
)

print("Loading dataset...")
print(DATASET_PATH)

df = pd.read_csv(DATASET_PATH)

print(f"Total Jobs: {len(df)}")

# Keep only jobs with salary
df = df[df["med_salary"].notna()]

print(f"Jobs with Salary: {len(df)}")

FEATURES = [
    "title",
    "location",
    "work_type"
]

TARGET = "med_salary"

X = df[FEATURES]
y = df[TARGET]

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_pipeline, FEATURES)
    ]
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

print("Training AI Salary Model...")

pipeline.fit(X, y)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "salary_model.pkl"
)

joblib.dump(pipeline, MODEL_PATH)

print("\n=================================")
print("✅ Salary Model Trained Successfully")
print("Saved to:")
print(MODEL_PATH)
print("=================================")