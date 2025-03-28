import os
import re
import nltk
import pymorphy3
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

morph = pymorphy3.MorphAnalyzer()
stop_words = set(stopwords.words("russian"))


def extract_text_from_html(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()


def tokenize_text(text: str) -> set[str]:
    tokens = nltk.word_tokenize(text, language="russian")
    filtered_tokens = set()

    for token in tokens:
        token = token.lower()
        if token in stop_words:
            continue
        if not re.fullmatch(r'[а-яА-ЯёЁ]+', token):
            continue
        filtered_tokens.add(token)

    return filtered_tokens


def lemmatize_tokens(tokens: set[str]) -> dict[str, list[str]]:
    lemma_dict: dict[str, list[str]] = {}

    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        lemma_dict.setdefault(lemma, []).append(token)

    return lemma_dict

def process_file(directory, filename):
    tokens: set[str] = set()
    file_path = os.path.join(directory, filename)
    text = extract_text_from_html(file_path)
    tokens = tokenize_text(text)

    lemmatized_tokens = lemmatize_tokens(tokens)

    filename = filename.replace(".html", "")
    with open("result/tokens-" + filename + ".txt", "w", encoding="utf-8") as token_file:
        token_file.writelines(f"{token}\n" for token in sorted(tokens))

    with open("result/lemmas-" + filename + ".txt", "w", encoding="utf-8") as lemma_file:
        for lemma, words in sorted(lemmatized_tokens.items()):
            unique_words = " ".join(sorted(set(words)))
            lemma_file.write(f"{lemma} {unique_words}\n")


def process_html_files(directory: str) -> None:
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            process_file(directory, filename)


if __name__ == "__main__":
    process_html_files("../home work 1/pages")
