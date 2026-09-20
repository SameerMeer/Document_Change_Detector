import difflib

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from ingestion import extract_pdf
from chunking import create_chunks
from llm_explainer import explain_change


MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.80


# --------------------------------
# Load embedding model
# --------------------------------

model = SentenceTransformer(MODEL_NAME)


# --------------------------------
# Find text differences
# --------------------------------

def find_difference(old_text, new_text):

    old_words = old_text.split()
    new_words = new_text.split()

    differences = difflib.ndiff(
        old_words,
        new_words
    )

    removed = []
    added = []

    for word in differences:

        if word.startswith("- "):
            removed.append(word[2:])

        elif word.startswith("+ "):
            added.append(word[2:])

    return removed, added


# --------------------------------
# Create normalized embeddings
# --------------------------------

def create_embeddings(texts):

    embeddings = model.encode(texts)

    embeddings = np.array(
        embeddings
    ).astype("float32")

    faiss.normalize_L2(embeddings)

    return embeddings


# --------------------------------
# Compare two documents
# --------------------------------

def compare_documents(old_pdf, new_pdf):

    # -----------------------------
    # 1. Extract PDF text
    # -----------------------------

    old_document = extract_pdf(old_pdf)
    new_document = extract_pdf(new_pdf)


    # -----------------------------
    # 2. Create chunks
    # -----------------------------

    old_chunks = create_chunks(old_document)
    new_chunks = create_chunks(new_document)

    # Remove document metadata chunk
    old_chunks = old_chunks[1:]
    new_chunks = new_chunks[1:]


    # -----------------------------
    # 3. Extract chunk text
    # -----------------------------

    old_texts = [
        chunk["text"]
        for chunk in old_chunks
    ]

    new_texts = [
        chunk["text"]
        for chunk in new_chunks
    ]


    # -----------------------------
    # 4. Create embeddings
    # -----------------------------

    old_embeddings = create_embeddings(
        old_texts
    )

    new_embeddings = create_embeddings(
        new_texts
    )


    # -----------------------------
    # 5. Create FAISS indexes
    # -----------------------------

    new_index = faiss.IndexFlatIP(
        new_embeddings.shape[1]
    )

    new_index.add(new_embeddings)


    old_index = faiss.IndexFlatIP(
        old_embeddings.shape[1]
    )

    old_index.add(old_embeddings)


    # -----------------------------
    # 6. Find semantic matches
    # -----------------------------

    old_scores, old_indices = new_index.search(
        old_embeddings,
        1
    )

    new_scores, new_indices = old_index.search(
        new_embeddings,
        1
    )


    # -----------------------------
    # 7. Store results
    # -----------------------------

    results = []

    matched_new_chunks = set()


    # -----------------------------
    # 8. Compare OLD sections
    # -----------------------------

    for i, old_chunk in enumerate(old_chunks):

        similarity = float(
            old_scores[i][0]
        )

        matched_index = int(
            old_indices[i][0]
        )

        section_name = (
            old_chunk["text"]
            .split(" ", 2)[0]
        )


        # -------------------------
        # REMOVED
        # -------------------------

        if similarity < SIMILARITY_THRESHOLD:

            results.append({
                "section": section_name,
                "status": "REMOVED",
                "old_page": old_chunk["page"],
                "new_page": None,
                "similarity": similarity,
                "old_text": old_chunk["text"],
                "new_text": None,
                "removed": [],
                "added": [],
                "explanation": None
            })

            continue


        # -------------------------
        # Matching NEW section
        # -------------------------

        new_chunk = new_chunks[
            matched_index
        ]

        matched_new_chunks.add(
            matched_index
        )


        # -------------------------
        # UNCHANGED
        # -------------------------

        if old_chunk["text"] == new_chunk["text"]:

            results.append({
                "section": section_name,
                "status": "UNCHANGED",
                "old_page": old_chunk["page"],
                "new_page": new_chunk["page"],
                "similarity": similarity,
                "old_text": old_chunk["text"],
                "new_text": new_chunk["text"],
                "removed": [],
                "added": [],
                "explanation": None
            })

            continue


        # -------------------------
        # MODIFIED
        # -------------------------

        removed, added = find_difference(
            old_chunk["text"],
            new_chunk["text"]
        )


        try:

            explanation = explain_change(
                old_chunk["text"],
                new_chunk["text"]
            )

        except Exception as error:

            explanation = (
                f"LLM explanation failed: {error}"
            )


        results.append({
            "section": section_name,
            "status": "MODIFIED",
            "old_page": old_chunk["page"],
            "new_page": new_chunk["page"],
            "similarity": similarity,
            "old_text": old_chunk["text"],
            "new_text": new_chunk["text"],
            "removed": removed,
            "added": added,
            "explanation": explanation
        })


    # -----------------------------
    # 9. Find ADDED sections
    # -----------------------------

    for i, new_chunk in enumerate(new_chunks):

        if i in matched_new_chunks:
            continue


        similarity = float(
            new_scores[i][0]
        )


        if similarity < SIMILARITY_THRESHOLD:

            section_name = (
                new_chunk["text"]
                .split(" ", 2)[0]
            )

            results.append({
                "section": section_name,
                "status": "ADDED",
                "old_page": None,
                "new_page": new_chunk["page"],
                "similarity": similarity,
                "old_text": None,
                "new_text": new_chunk["text"],
                "removed": [],
                "added": [],
                "explanation": None
            })


    return results