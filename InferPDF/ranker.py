from sentence_transformers import SentenceTransformer, util

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def rank_sections(sections, persona, job):
    query = f"{persona} {job}"
    query_emb = MODEL.encode(query, convert_to_tensor=True)

    scored = []
    for i, (title, text, page_num, doc_name) in enumerate(sections):
        emb = MODEL.encode(f"{title} {text}", convert_to_tensor=True)
        sim = util.cos_sim(query_emb, emb).item()
        scored.append((i, sim))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
