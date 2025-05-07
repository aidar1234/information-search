import os
import math
from collections import defaultdict, Counter
import re
import nltk
import pymorphy3
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

NUM_DOCS = 100
HW_2_DIR = "./../home work 2/result"
OUTPUT_DIR = "result"

os.makedirs(OUTPUT_DIR, exist_ok=True)
stop_words = set(stopwords.words("russian"))
morph = pymorphy3.MorphAnalyzer()

def load_all_docs_words() -> list[list[str]]:
    all_docs_words = list()
    for i in range(1, 101):
        doc_words = load_all_words(f"{i}.html")
        all_docs_words.append(doc_words)
    return all_docs_words

def load_all_words(filename) -> list[str]:
    file_path = os.path.join("../home work 1/pages", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        text = soup.get_text()
        tokens = nltk.word_tokenize(text, language="russian")
        filtered_tokens = list()

        for token in tokens:
            token = token.lower()
            if token in stop_words:
                continue
            if not re.fullmatch(r'[а-яА-ЯёЁ]+', token):
                continue
            filtered_tokens.append(token)

        return filtered_tokens

def load_docs_tokens() -> list[list[str]]:
    docs_tokens = list()
    for i in range(1, 101):
        with open(os.path.abspath(f"{HW_2_DIR}/tokens-{i}.txt"), encoding="utf-8") as f:
            tokens = f.read().splitlines()
            docs_tokens.append(tokens)
    return docs_tokens

def compute_docs_tokens_tfs(docs_tokens, docs_all_words) -> list[dict[str, float]]:
    docs_tokens_tfs = list()
    for i in range(0, 100):
        doc_tokens = docs_tokens[i]
        doc_all_words = docs_all_words[i]

        tokens_tfs = dict()
        tokens_counts = Counter(doc_all_words)
        for doc_token in doc_tokens:
            tokens_tfs[doc_token] = tokens_counts[doc_token] / len(doc_all_words)
        docs_tokens_tfs.append(tokens_tfs)
    return docs_tokens_tfs

def compute_docs_lemmas_tfs(docs_lemmas, docs_all_words) -> list[dict[str, float]]:
    docs_lemmas_tfs = list()
    for i in range(0, 100):
        doc_lemmas = docs_lemmas[i]
        doc_all_words = docs_all_words[i]

        lemmatized_worlds = list()
        for word in doc_all_words:
            lemma = morph.parse(word)[0].normal_form
            lemmatized_worlds.append(lemma)
        lemmas_counts = Counter(lemmatized_worlds)

        lemmas_tfs = dict()
        for doc_lemma in doc_lemmas:
            lemmas_tfs[doc_lemma] = lemmas_counts[doc_lemma] / len(lemmatized_worlds)
        docs_lemmas_tfs.append(lemmas_tfs)
    return docs_lemmas_tfs


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


def merge_tf_idf(docs_tokens_tfs, docs_tokens_idfs):
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


def compute_tfidf_for_docs_tokens(docs_tokens, docs_all_words) -> list[dict[str, (float, float)]]:
    docs_tokens_tfs = compute_docs_tokens_tfs(docs_tokens, docs_all_words) # doc -> token -> tf
    docs_tokens_idfs = compute_docs_tokens_idfs(docs_tokens) # doc -> token -> idf

    return merge_tf_idf(docs_tokens_tfs, docs_tokens_idfs)


def print_tfidf(tokens_tfidfs, doc_type):
    for i in range(1, 101):
        doc_tokens_tfidfs = tokens_tfidfs[i-1]
        path = f"{OUTPUT_DIR}/tfidf-{doc_type}-{i}.txt"
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
    for doc_lemma_strings in docs_lemma_strings:
        doc_lemmas = list()
        for lemma_string in doc_lemma_strings:
            split_lemma_string = lemma_string.split(" ")
            doc_lemmas.append(split_lemma_string[0])
        docs_lemmas.append(doc_lemmas)
    return docs_lemmas


def build_token_to_lemma_map(docs_lemmas):
    token_to_lemma_map = dict()
    for doc_lemmas in docs_lemmas:
        for lemma in doc_lemmas:
            for i in range(1, len(lemma)):
                token_to_lemma_map[lemma[i]] = lemma[0]
    return token_to_lemma_map


def replace_tokens_by_lemmas(docs_tokens) -> list[set[str]]:
    replaced = list()
    for doc_tokens in docs_tokens:
        replaced_tokens = set()
        for token in doc_tokens:
            lemma = morph.parse(token)[0].normal_form
            replaced_tokens.add(lemma)
        replaced.append(replaced_tokens)
    return replaced

def compute_tfidf_for_docs_lemmas(docs_tokens, docs_all_words) -> list[dict[str, (float, float)]]:
    docs_lemmas = load_docs_lemmas()
    docs_tokens_tfs = compute_docs_lemmas_tfs(docs_lemmas, docs_all_words) # doc -> token -> tf
    docs_tokens_idfs = compute_docs_tokens_idfs(docs_lemmas) # doc -> token -> idf

    return merge_tf_idf(docs_tokens_tfs, docs_tokens_idfs)

def main():
    docs_tokens = load_docs_tokens()
    docs_all_words = load_all_docs_words()
    docs_tokens_tfidf = compute_tfidf_for_docs_tokens(docs_tokens, docs_all_words)
    docs_lemmas_tfidf = compute_tfidf_for_docs_lemmas(docs_tokens, docs_all_words)
    print_tfidf(docs_tokens_tfidf, 'tokens')
    print_tfidf(docs_lemmas_tfidf, 'lemmas')

if __name__ == '__main__':
    main()