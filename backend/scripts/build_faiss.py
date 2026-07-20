import os
import pickle
import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATASET_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "dataset",
        "job_postings.csv"
    )
)

FAISS_DIR = os.path.join(BASE_DIR, "faiss")

os.makedirs(FAISS_DIR, exist_ok=True)

INDEX_PATH = os.path.join(
    FAISS_DIR,
    "jobs.index"
)

DOCS_PATH = os.path.join(
    FAISS_DIR,
    "jobs.pkl"
)

# =====================================================
# Load Model
# =====================================================

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =====================================================
# Load Dataset
# =====================================================

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

df = df.fillna("")

# =====================================================
# Create Documents
# =====================================================

documents = []

for _, row in df.iterrows():

    text = f"""
Job Title:
{row.get('title', '')}

Company:
{row.get('company_name', '')}

Location:
{row.get('location', '')}

Description:
{row.get('description', '')}

Skills:
{row.get('skills_desc', '')}
"""

    documents.append(text)

print(f"Created {len(documents)} documents.")

# =====================================================
# Generate Embeddings
# =====================================================

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

# =====================================================
# Build FAISS
# =====================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# =====================================================
# Save FAISS
# =====================================================

print("Saving FAISS index...")

faiss.write_index(
    index,
    INDEX_PATH
)

# =====================================================
# Save Documents
# =====================================================

with open(DOCS_PATH, "wb") as f:
    pickle.dump(documents, f)

print("\n===================================")
print("FAISS index created successfully!")
print(INDEX_PATH)
print(DOCS_PATH)
print("===================================")