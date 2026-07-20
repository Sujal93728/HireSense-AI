import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FAISS_DIR = os.path.join(BASE_DIR, "faiss")

INDEX_PATH = os.path.join(
    FAISS_DIR,
    "jobs.index"
)

DOCS_PATH = os.path.join(
    FAISS_DIR,
    "jobs.pkl"
)

# =====================================================
# Global Objects
# =====================================================

model = None
index = None
documents = None


# =====================================================
# Load Everything (Only Once)
# =====================================================

def load_rag():
    global model
    global index
    global documents

    # Load embedding model
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load FAISS index
    if index is None:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(
                f"FAISS index not found:\n{INDEX_PATH}\n\n"
                "Run build_faiss.py first."
            )

        print("Loading FAISS index...")
        index = faiss.read_index(INDEX_PATH)

    # Load documents
    if documents is None:
        if not os.path.exists(DOCS_PATH):
            raise FileNotFoundError(
                f"Document file not found:\n{DOCS_PATH}\n\n"
                "Run build_faiss.py first."
            )

        print("Loading documents...")

        with open(DOCS_PATH, "rb") as f:
            documents = pickle.load(f)

        print(f"Loaded {len(documents)} documents.")


# =====================================================
# Retrieve Context
# =====================================================

def retrieve_context(query: str, top_k: int = 3):
    load_rag()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    contexts = []

    for idx in indices[0]:
        if 0 <= idx < len(documents):
            contexts.append(documents[idx])

    return contexts