import os
import docx2txt
import PyPDF2
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------------- CONFIGURATION ----------------
RESUME_FOLDER = "resumes"           # Folder with resumes
JOB_DESCRIPTION_FILE = "job_description.txt"
TOP_N = 2                           # Number of best resumes to select

# Load free embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast, good for semantic search

# ---------------- FUNCTIONS ----------------

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Extract text from DOCX
def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

# Read resume content
def read_resume(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return ""

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------------- MAIN LOGIC ----------------

# Read job description
with open(JOB_DESCRIPTION_FILE, "r", encoding="utf-8") as f:
    job_description = f.read()

# Generate embedding for job description
job_embedding = model.encode(job_description)

# Read all resumes and generate embeddings
resumes = []
resume_files = []
resume_embeddings = []

for file in os.listdir(RESUME_FOLDER):
    file_path = os.path.join(RESUME_FOLDER, file)
    text = read_resume(file_path)
    if text:
        resumes.append(text)
        resume_files.append(file)
        resume_embeddings.append(model.encode(text))

# Compute similarity scores
similarity_scores = [cosine_similarity(job_embedding, emb) for emb in resume_embeddings]

# Get top N resumes
top_indices = np.argsort(similarity_scores)[-TOP_N:][::-1]

print(f"Top {TOP_N} resumes:")
for idx in top_indices:
    print(f"{resume_files[idx]} - Score: {similarity_scores[idx]:.4f}")
