import fitz

def extract_text_from_pdf(pdf_path: str, max_pages: int | None = None):
    document = fitz.open(pdf_path)

    page_count = document.page_count
    if max_pages is not None and page_count > max_pages:
        document.close()
        raise ValueError(
            f"PDF has {page_count} pages; maximum is {max_pages}"
        )

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    document.close()
    return pages