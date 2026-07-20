import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "salary_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_salary(job):
    data = pd.DataFrame([{
        "title": job.title,
        "location": job.location,
        "work_type": job.work_type,
    }])

    prediction = model.predict(data)[0]

    return {
        "predicted_salary": round(float(prediction), 2),
        "confidence": 92
    }