import os
import math
from collections import defaultdict, Counter

NUM_DOCS = 100
HW_2_DIR = "./../home work 2/result"
OUTPUT_DIR = "result"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# # --- Сбор TF и DF данных ---
# token_docs = []
# lemma_docs = []
#
# token_df = defaultdict(int)
# lemma_df = defaultdict(int)
#
# for i in range(1, NUM_DOCS + 1):
#     # Читаем токены
#     with open(os.path.abspath(f"{HW_2_DIR}/tokens-{i}.txt"), encoding="utf-8") as f:
#         tokens = f.read().splitlines()
#     token_counts = Counter(tokens)
#     token_docs.append((token_counts, len(tokens)))
#
#     for token in set(tokens):
#         token_df[token] += 1
#
#     # Читаем леммы
#     lemma_map = defaultdict(list)
#     with open(os.path.abspath(f"{HW_2_DIR}/lemmas-{i}.txt"), encoding="utf-8") as f:
#         for line in f:
#             parts = line.strip().split()
#             if not parts:
#                 continue
#             lemma, *lemma_tokens = parts
#             lemma_map[lemma].extend(lemma_tokens)
#
#     lemma_counts = {}
#     total_tokens = 0
#     for lemma, tokens in lemma_map.items():
#         count = len(tokens)
#         lemma_counts[lemma] = count
#         total_tokens += count
#
#     lemma_docs.append((lemma_counts, total_tokens))
#
#     for lemma in lemma_counts.keys():
#         lemma_df[lemma] += 1
#
#
# # --- IDF ---
# # def compute_idf(df_dict):
# #     return {term: math.log(NUM_DOCS / (1 + df)) for term, df in df_dict.items()}
#
#
# token_idf = compute_idf(token_df)
# lemma_idf = compute_idf(lemma_df)
#
# # --- Запись TF-IDF по токенам ---
# for i, (token_counts, total_tokens) in enumerate(token_docs):
#     path = f"{OUTPUT_DIR}/tfidf-tokens-{i}.txt"
#     with open(path, "w", encoding="utf-8") as f:
#         for token, count in token_counts.items():
#             tf = count / total_tokens
#             idf = token_idf[token]
#             tfidf = tf * idf
#             f.write(f"{token} {idf:.6f} {tfidf:.6f}\n")
#
# # --- Запись TF-IDF по леммам ---
# for i, (lemma_counts, total_tokens) in enumerate(lemma_docs):
#     path = f"{OUTPUT_DIR}/tfidf-lemmas-{i}.txt"
#     with open(path, "w", encoding="utf-8") as f:
#         for lemma, count in lemma_counts.items():
#             tf = count / total_tokens
#             idf = lemma_idf[lemma]
#             tfidf = tf * idf
#             f.write(f"{lemma} {idf:.6f} {tfidf:.6f}\n")


def load_docs_tokens() -> list[list[str]]:
    docs_tokens = list()
    for i in range(1, 101):
        with open(os.path.abspath(f"{HW_2_DIR}/tokens-{i}.txt"), encoding="utf-8") as f:
            tokens = f.read().splitlines()
            docs_tokens.append(tokens)
    return docs_tokens

def compute_docs_tokens_tfs(docs_tokens) -> list[dict[str, float]]:
    docs_tokens_tfs = list()
    for doc_tokens in docs_tokens:
        tokens_tfs = dict()
        tokens_counts = Counter(doc_tokens)
        for doc_token, token_count in tokens_counts.items():
            tokens_tfs[doc_token] = token_count / len(doc_tokens)
        docs_tokens_tfs.append(tokens_tfs)
    return docs_tokens_tfs


def compute_docs_tokens_idfs(docs_tokens) -> list[dict[str, float]]:
    all_tokens = list()
    for tokens in docs_tokens:
        tokens_set = set(tokens)
        for token in tokens_set:
            all_tokens.append(token)

    tokens_counts = Counter(all_tokens)

    docs_tokens_idfs = list()
    for doc_tokens in docs_tokens:
        tokens_idfs = dict()
        dist_tokens = set(doc_tokens)
        for token in dist_tokens:
            idf = math.log(100 / tokens_counts[token])
            tokens_idfs[token] = idf
        docs_tokens_idfs.append(tokens_idfs)
    return docs_tokens_idfs


def compute_tfidf_for_docs_tokens(docs_tokens) -> list[dict[str, (float, float)]]:
    docs_tokens_tfs = compute_docs_tokens_tfs(docs_tokens) # doc -> token -> tf
    docs_tokens_idfs = compute_docs_tokens_idfs(docs_tokens) # doc -> token -> idf

    docs_tokens_tfidfs = list()
    for i in range(0, 100):
        map = dict()
        tokens_tfs = docs_tokens_tfs[i]
        tokens_idfs = docs_tokens_idfs[i]
        for token, tf in tokens_tfs.items():
            idf = tokens_idfs[token]
            map[token] = (idf, idf * tf)
        docs_tokens_tfidfs.append(map)
    return docs_tokens_tfidfs


def print_tfidf(tokens_tfidfs, type):
    for i in range(1, 101):
        doc_tokens_tfidfs = tokens_tfidfs[i-1]
        path = f"{OUTPUT_DIR}/tfidf-{type}-{i}.txt"
        with open(os.path.abspath(path), "w", encoding="utf-8") as f:
            for token, tfidfs in doc_tokens_tfidfs.items():
                f.write(f"{token} {tfidfs[0]:.6f} {tfidfs[1]:.6f}\n")


def load_docs_lemmas() -> list[list[str]]:
    docs_lemma_strings = list()
    for i in range(1, 101):
        with open(os.path.abspath(f"{HW_2_DIR}/lemmas-{i}.txt"), encoding="utf-8") as f:
            tokens = f.read().splitlines()
            docs_lemma_strings.append(tokens)
    docs_lemmas = list()
    for lemmas in docs_lemma_strings:
        splitted_lemmas = list()
        for lemma in lemmas:
            splitted = lemma.split(" ")
            splitted_lemmas.append(splitted)
        docs_lemmas.append(splitted_lemmas)
    return docs_lemmas


def build_token_to_lemma_map(docs_lemmas):
    map = dict()
    for doc_lemmas in docs_lemmas:
        for lemma in doc_lemmas:
            for i in range(1, len(lemma)):
                map[lemma[i]] = lemma[0]
    return map


def replace_tokens_by_lemmas(docs_tokens, map) -> list[list[str]]:
    replaced = list()
    for doc_tokens in docs_tokens:
        replaced_tokens = list()
        for token in doc_tokens:
            replaced_tokens.append(map[token])
        replaced.append(replaced_tokens)
    return replaced

def compute_tfidf_for_docs_lemmas(docs_tokens) -> list[dict[str, (float, float)]]:
    docs_lemmas = load_docs_lemmas()
    map = build_token_to_lemma_map(docs_lemmas)
    docs_tokens = replace_tokens_by_lemmas(docs_tokens, map)
    return compute_tfidf_for_docs_tokens(docs_tokens)

def main():
    docs_tokens = load_docs_tokens()
    docs_tokens_tfidf = compute_tfidf_for_docs_tokens(docs_tokens)
    docs_lemmas_tfidf = compute_tfidf_for_docs_lemmas(docs_tokens)
    print_tfidf(docs_tokens_tfidf, 'tokens')
    print_tfidf(docs_lemmas_tfidf, 'lemmas')

if __name__ == '__main__':
    main()