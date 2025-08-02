import nltk
from nltk.tokenize import sent_tokenize

# Ensure nltk 'punkt' is downloaded in your environment or Docker image:
# nltk.download('punkt')

def extract_refined_snippets(title, text, persona, job):
    sentences = sent_tokenize(text)
    keywords = set((persona + " " + job).lower().split())

    scored = []
    for s in sentences:
        word_set = set(s.lower().split())
        score = len(word_set.intersection(keywords))
        scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)

    top_sents = [s for score, s in scored if score > 0]
    if not top_sents:
        top_sents = sentences[:3]

    snippet = " ".join(top_sents).strip()
    max_len = 1000
    if len(snippet) > max_len:
        snippet = snippet[:max_len - 3] + "..."
    return snippet
