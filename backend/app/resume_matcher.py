import os
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ======================================================
# Global Variables
# ======================================================

_model = None
_jobs = None

# ======================================================
# Lazy Load SentenceTransformer
# ======================================================

def get_model():
    global _model

    if _model is None:
        print("Loading SentenceTransformer model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


# ======================================================
# Dataset Path
# ======================================================

def get_dataset_path():
    current = os.path.dirname(os.path.abspath(__file__))

    possible_paths = [
        os.path.join(current, "..", "dataset", "job_postings.csv"),
        os.path.join(current, "..", "..", "dataset", "job_postings.csv"),
    ]

    for path in possible_paths:
        path = os.path.abspath(path)

        if os.path.exists(path):
            print(f"Using dataset: {path}")
            return path

    raise FileNotFoundError("job_postings.csv not found.")


DATASET_PATH = get_dataset_path()


# ======================================================
# Lazy Load Dataset
# ======================================================

def get_jobs():
    global _jobs

    if _jobs is None:
        print("Loading jobs dataset...")

        jobs = pd.read_csv(
            DATASET_PATH,
            low_memory=False
        )

        jobs = jobs.fillna("")
        jobs = jobs[
            jobs["description"].str.strip() != ""
        ]

        # Reduce memory usage
        jobs = jobs.head(5000)

        _jobs = jobs

    return _jobs


# ======================================================
# Resume Matching
# ======================================================

def match_resume(resume_text: str):

    model = get_model()

    jobs = get_jobs().copy()

    descriptions = jobs["description"].tolist()

    print("Encoding resume...")

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=False
    )

    print("Encoding job descriptions...")

    job_embeddings = model.encode(
        descriptions,
        convert_to_tensor=False,
        show_progress_bar=False
    )

    similarities = cosine_similarity(
        [resume_embedding],
        job_embeddings
    )[0]

    jobs["match_score"] = similarities * 100

    top_jobs = (
        jobs.sort_values(
            by="match_score",
            ascending=False
        )
        .head(10)
    )

    return top_jobs[
        [
            "job_id",
            "title",
            "location",
            "description",
            "match_score"
        ]
    ].to_dict(orient="records")