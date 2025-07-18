# resume_batch_processor.py

import os
import pymongo
from resume_parser import extract_text_from_pdf, analyze_resume, nlp
from LLM import parse_resume_llm  # Assuming this is the correct import path

# Configuration
FOLDER_PATH = "../resumes/part4"  # Update to your resumes directory
MONGODB_URI = "mongodb+srv://hashirayaz:jY1p6KbvePHFfWLc@cluster0.nw4lxia.mongodb.net/"  # MongoDB connection URI
DB_NAME = "ai-project"  # Database name
COLLECTION_NAME = "resumes"  # Collection name


def embed_text(text: str) -> list:
    """
    Generate an embedding for the given text using spaCy's vector representation.
    """
    doc = nlp(text)
    return doc.vector.tolist()


def process_resumes():
    """
    Iterate over all PDF resumes in FOLDER_PATH, extract and analyze each,
    generate embeddings, and store results in MongoDB.
    """
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Process each PDF in the folder
    for filename in os.listdir(FOLDER_PATH):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(FOLDER_PATH, filename)
        print(f"Processing {filename}...")

        try:
            # Extract raw text from PDF
            text = extract_text_from_pdf(file_path)

            # Parse resume structure
            # resume_data = analyze_resume(text)
            resume_data = parse_resume_llm(text)

            # Generate embedding using spaCy
            embedding = embed_text(text)

            # Construct document for MongoDB
            document = {
                "filename": filename,
                # "text": text,
                "parsed_data": resume_data,
                "embedding": embedding,
            }

            # Insert into MongoDB
            collection.insert_one(document)
            print(f"Inserted {filename} into MongoDB")

        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    process_resumes()
