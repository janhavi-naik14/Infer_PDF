import os
import fitz  # PyMuPDF

def chunk_pdf_by_toc(pdf_path):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    sections = []
    basename = os.path.basename(pdf_path)

    if not toc:
        text = "".join(page.get_text() for page in doc)
        sections.append(("Full Document", text, 1, basename))
        return sections

    toc.append([9999, "END_OF_DOC", doc.page_count + 1])

    for i in range(len(toc) - 1):
        _, title, start_page = toc[i]
        _, _, next_start_page = toc[i + 1]

        text = ""
        for pagenum in range(start_page - 1, next_start_page - 1):
            text += doc.load_page(pagenum).get_text()

        clean_title = title.strip() if title.strip() else "Untitled Section"
        sections.append((clean_title, text.strip(), start_page, basename))

    return sections
