from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import numpy as np
from resume_parser import nlp  # reusing the same loaded model
import os
from LLM import parse_user_query

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app)

# MongoDB configuration
MONGODB_URI = "mongodb+srv://hashirayaz:jY1p6KbvePHFfWLc@cluster0.nw4lxia.mongodb.net/"
DB_NAME = "ai-project"  # Database name
COLLECTION_NAME = "resumes"

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def embed_query(text: str) -> np.ndarray:
    """
    Generate an embedding for the query using spaCy.
    """
    return nlp(text).vector


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))


def get_skills_required_from_job_description(job_description):
    """
    Extract skills from the job description using spaCy.
    """
    doc = nlp(job_description)
    skills = []
    for token in doc:
        if token.is_alpha and len(token.text) > 1 and not token.is_stop:
            skills.append(token.text)
    return list(set(skills))


@app.route("/resume", methods=["GET"])
def get_resume():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    resume = collection.find_one({"filename": filename}, {"_id": 0})
    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    return jsonify(resume), 200


@app.route("/api/match", methods=["GET"])
def match_resumes():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    print("Query:", query)
    # Extract skills from the job description
    required_skills_json = parse_user_query(query)
    print("Required Skills JSON:", required_skills_json)
    required_skills = required_skills_json.get("skills", [])

    if not required_skills:
        return jsonify({"error": "No skills found in the job description"}), 400
    # Generate embedding for the query

    query_vec = embed_query(query)
    results = []

    for resume in collection.find(
        {}, {"filename": 1, "parsed_data": 1, "embedding": 1}
    ):
        resume_vec = np.array(resume.get("embedding", []))
        if resume_vec.size == 0:
            continue
        score = cosine_similarity(query_vec, resume_vec)
        results.append(
            {
                "filename": resume["filename"],
                "score": score,
                "parsed_data": resume["parsed_data"],
            }
        )

    top_matches = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    return (
        jsonify({"top_matches": top_matches, "required_skills": required_skills}),
        200,
    )


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    # Remember to pip install flask flask-cors pymongo spacy numpy
    app.run(debug=True)
