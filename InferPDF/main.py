import os
import sys
import time
import re
import json
import logging
import traceback

from chunker import chunk_pdf_by_toc
from ranker import rank_sections
from refiner import extract_refined_snippets

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

INPUT_DIR = "input"
OUTPUT_DIR = "output"

PERSONA = os.environ.get("PERSONA", "Travel Planner")
JOB_TO_BE_DONE = os.environ.get("JOB_TO_BE_DONE", "Plan a trip of 4 days for a group of 10 college friends.")

def clean_title(title):
    title = title.strip()
    title = re.sub(r'[:,;.\-\s]+$', '', title)
    if not title:
        title = "Untitled Section"
    return title

def clean_refined_text(text, max_length=1000):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    if len(text) > max_length:
        text = text[:max_length].rstrip() + "..."
    return text

def main():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logger.info(f"Looking for PDF files in '{INPUT_DIR}'...")
    pdf_files = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")])

    if not pdf_files:
        logger.error(f"No PDF files found in '{INPUT_DIR}'. Exiting.")
        sys.exit(1)

    logger.info(f"Detected input PDFs: {pdf_files}")

    all_sections = []
    processed_docs = set()

    start_parsing = time.perf_counter()
    for filename in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, filename)
        try:
            sections = chunk_pdf_by_toc(pdf_path)
            if not sections:
                logger.warning(f"No sections extracted from '{filename}'.")
                continue
            cleaned_sections = [
                (clean_title(title), text, page_num, doc_name)
                for (title, text, page_num, doc_name) in sections
            ]
            all_sections.extend(cleaned_sections)
            processed_docs.add(filename)
            logger.info(f"Processed '{filename}' - extracted {len(sections)} sections.")
        except Exception as e:
            logger.error(f"Error processing '{filename}': {e}")
            logger.debug(traceback.format_exc())
    end_parsing = time.perf_counter()
    logger.info(f"Finished parsing PDFs in {end_parsing - start_parsing:.2f} seconds.")

    if not all_sections:
        logger.error("No sections extracted from any document. Exiting.")
        sys.exit(1)

    start_ranking = time.perf_counter()
    ranked_sections = rank_sections(all_sections, PERSONA, JOB_TO_BE_DONE)
    end_ranking = time.perf_counter()
    logger.info(f"Ranking completed in {end_ranking - start_ranking:.2f} seconds.")

    top_sections = []
    doc_counts = {}
    for idx, score in ranked_sections:
        title, text, page_num, doc_name = all_sections[idx]
        count = doc_counts.get(doc_name, 0)
        if count < 2:
            top_sections.append((title, text, page_num, doc_name))
            doc_counts[doc_name] = count + 1
        if len(top_sections) == 5:
            break

    extracted_sections = []
    subsection_analysis = []

    start_refining = time.perf_counter()
    for rank, (title, text, page_num, doc_name) in enumerate(top_sections, start=1):
        extracted_sections.append({
            "document": os.path.basename(doc_name),
            "section_title": title,
            "importance_rank": rank,
            "page_number": page_num
        })
        refined = extract_refined_snippets(title, text, PERSONA, JOB_TO_BE_DONE)
        refined = clean_refined_text(refined)
        subsection_analysis.append({
            "document": os.path.basename(doc_name),
            "refined_text": refined,
            "page_number": page_num
        })
    end_refining = time.perf_counter()
    logger.info(f"Refinement completed in {end_refining - start_refining:.2f} seconds.")

    output_json = {
        "metadata": {
            "input_documents": sorted(processed_docs),
            "persona": PERSONA,
            "job_to_be_done": JOB_TO_BE_DONE,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    output_path = os.path.join(OUTPUT_DIR, "challenge1b_output.json")
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(output_json, outfile, indent=2, ensure_ascii=False)

    logger.info(f"Output JSON generated at '{output_path}'.")
    logger.info(f"Processing completed at {time.strftime('%H:%M:%S IST on %Y-%m-%d')}.")

if __name__ == "__main__":
    main()
