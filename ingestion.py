import pymupdf


def extract_pdf(pdf_path):
    documents = []

    pdf = pymupdf.open(pdf_path)

    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text("text").strip()

        documents.append({
            "page": page_number,
            "text": text
        })

    pdf.close()

    return documents