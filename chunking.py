from ingestion import extract_pdf


def create_chunks(documents):
    chunks = []

    for document in documents:

        page_number = document["page"]
        text = document["text"]

        sections = text.split("\n")

        current_section = ""

        for line in sections:

            line = line.strip()

            if not line:
                continue

            # Detect numbered sections
            if line[0].isdigit() and "." in line[:3]:

                if current_section:
                    chunks.append({
                        "page": page_number,
                        "text": current_section.strip()
                    })

                current_section = line

            else:
                current_section += " " + line

        # Add final section
        if current_section:
            chunks.append({
                "page": page_number,
                "text": current_section.strip()
            })

    return chunks


if __name__ == "__main__":

    old_document = extract_pdf("data/old.pdf")
    new_document = extract_pdf("data/new.pdf")

    old_chunks = create_chunks(old_document)
    new_chunks = create_chunks(new_document)

    print("OLD CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(old_chunks):

        print(f"\nChunk {i + 1}")
        print("Page:", chunk["page"])
        print("Text:", chunk["text"])

    print("\n\nNEW CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(new_chunks):

        print(f"\nChunk {i + 1}")
        print("Page:", chunk["page"])
        print("Text:", chunk["text"])