import os
import math
import json
from typing import Dict, List, Tuple
import pymorphy3
import nltk
from nltk.corpus import stopwords
import re


class VectorSearchEngine:
    def __init__(self, tfidf_dir: str, index_path: str):
        nltk.download('stopwords', quiet=True)

        self.morph = pymorphy3.MorphAnalyzer()
        self.stop_words = set(stopwords.words("russian"))

        self.tfidf_tokens = self.load_tfidf_tokens(tfidf_dir)
        self.tfidf_lemmas = self.load_tfidf_lemmas(tfidf_dir)
        self.inverted_index = self.load_inverted_index(index_path)
        self.doc_lengths_tokens = self.compute_doc_lengths(self.tfidf_tokens)
        self.doc_lengths_lemmas = self.compute_doc_lengths(self.tfidf_lemmas)
        self.doc_urls = self.load_document_urls()

    def load_document_urls(self, index_path: str = "../home work 1/index.txt") -> Dict[int, str]:
        """
        :param index_path: Путь к файлу index.txt
        :return: Словарь соответствия номера документа и URL
        """
        doc_urls = {}
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        doc_id = int(parts[0].replace('pages/', '').replace('.html', ''))
                        url = parts[1]
                        doc_urls[doc_id] = url
        except FileNotFoundError:
            print(f"Файл index.txt не найден по пути {index_path}")

        return doc_urls

    def load_tfidf_tokens(self, tfidf_dir: str) -> List[Dict[str, Tuple[float, float]]]:
        """
        :param tfidf_dir: Директория с TF-IDF файлами токенов
        :return: Список словарей TF-IDF для каждого документа
        """
        tfidf_tokens = []
        for i in range(1, 101):
            try:
                with open(os.path.join(tfidf_dir, f'tfidf-tokens-{i}.txt'), 'r', encoding='utf-8') as f:
                    doc_tfidf = {}
                    for line in f:
                        token, idf, tfidf = line.strip().split()
                        doc_tfidf[token] = (float(idf), float(tfidf))
                    tfidf_tokens.append(doc_tfidf)
            except FileNotFoundError:
                print(f"Файл tfidf-tokens-{i}.txt не найден")
                tfidf_tokens.append({})
        return tfidf_tokens

    def load_tfidf_lemmas(self, tfidf_dir: str) -> List[Dict[str, Tuple[float, float]]]:
        """
        :param tfidf_dir: Директория с TF-IDF файлами лемм
        :return: Список словарей TF-IDF для каждого документа
        """
        tfidf_lemmas = []
        for i in range(1, 101):
            try:
                with open(os.path.join(tfidf_dir, f'tfidf-lemmas-{i}.txt'), 'r', encoding='utf-8') as f:
                    doc_tfidf = {}
                    for line in f:
                        lemma, idf, tfidf = line.strip().split()
                        doc_tfidf[lemma] = (float(idf), float(tfidf))
                    tfidf_lemmas.append(doc_tfidf)
            except FileNotFoundError:
                print(f"Файл tfidf-lemmas-{i}.txt не найден")
                tfidf_lemmas.append({})
        return tfidf_lemmas

    def load_inverted_index(self, index_path: str) -> Dict[str, List[str]]:
        """
        :param index_path: Путь к JSON файлу инвертированного индекса
        :return: Словарь инвертированного индекса
        """
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл инвертированного индекса {index_path} не найден")
            return {}

    def compute_doc_lengths(self, tfidf_docs: List[Dict[str, Tuple[float, float]]]) -> List[float]:
        """
        :param tfidf_docs: Список словарей TF-IDF для документов
        :return: Список длин документов
        """
        doc_lengths = []
        for doc_tfidf in tfidf_docs:
            squared_sum = sum(tfidf_val[1] ** 2 for tfidf_val in doc_tfidf.values())
            doc_lengths.append(math.sqrt(squared_sum) if squared_sum > 0 else 0)
        return doc_lengths

    def cosine_similarity(self, query_vector: Dict[str, float], doc_tfidf: Dict[str, Tuple[float, float]],
                          doc_length: float) -> float:
        """
        Вычисление косинусной близости между запросом и документом

        :param query_vector: Вектор запроса (токен -> вес)
        :param doc_tfidf: TF-IDF документа
        :param doc_length: Длина документа
        :return: Значение косинусной близости
        """
        dot_product = 0
        query_length = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))

        for token, query_weight in query_vector.items():
            if token in doc_tfidf:
                dot_product += query_weight * doc_tfidf[token][1]

        if query_length == 0 or doc_length == 0:
            return 0

        return dot_product / (query_length * doc_length)

    def create_query_vector(self, query: str, use_lemmas: bool = False) -> Dict[str, float]:
        """
        Создание векторного представления запроса с учетом морфологических форм

        :param query: Текстовый запрос
        :param use_lemmas: Использовать леммы вместо токенов
        :return: Вектор запроса
        """

        tokens = re.findall(r'[а-яА-ЯёЁ]+', query.lower())
        tokens = [token for token in tokens if token not in self.stop_words]

        # Создаем вектор запроса
        query_vector = {}
        token_counts = {}

        for token in tokens:
            # Получаем все возможные леммы и морфологические формы
            parse_results = self.morph.parse(token)

            # Используем первую (наиболее вероятную) лемму
            lemma = parse_results[0].normal_form

            # Увеличиваем счетчик токенов
            token_counts[lemma] = token_counts.get(lemma, 0) + 1

        # Нормализация весов
        max_count = max(token_counts.values()) if token_counts else 1

        for lemma, count in token_counts.items():
            # Получаем документы с леммой из инвертированного индекса
            if use_lemmas:
                if lemma in self.inverted_index:
                    query_vector[lemma] = count / max_count
            else:
                # Ищем все формы леммы в инвертированном индексе
                for form, doc_list in self.inverted_index.items():
                    if form.startswith(lemma):
                        query_vector[form] = count / max_count

        return query_vector

    def search(self, query: str, top_k: int = 100, use_lemmas: bool = False) -> List[Tuple[str, int, float]]:
        """
        Основной метод поиска

        :param query: Текстовый запрос
        :param top_k: Количество возвращаемых результатов
        :param use_lemmas: Использовать леммы вместо токенов
        :return: Список кортежей (URL документа, номер документа, оценка близости)
        """
        # Выбираем нужные TF-IDF и длины документов
        tfidf_docs = self.tfidf_lemmas if use_lemmas else self.tfidf_tokens
        doc_lengths = self.doc_lengths_lemmas if use_lemmas else self.doc_lengths_tokens

        query_vector = self.create_query_vector(query, use_lemmas)

        if not query_vector:
            return []

        relevant_docs = set()
        for token in query_vector.keys():
            if token in self.inverted_index:
                relevant_docs.update(map(int, self.inverted_index[token]))

        # Вычисляем близость только для релевантных документов
        similarities = []
        for doc_id in relevant_docs:
            doc_tfidf = tfidf_docs[doc_id - 1]
            doc_length = doc_lengths[doc_id - 1]
            similarity = self.cosine_similarity(query_vector, doc_tfidf, doc_length)

            # Добавляем документы с ненулевой близостью
            if similarity > 0:
                # Получаем URL документа, если он есть
                url = self.doc_urls.get(doc_id, f"Документ {doc_id}")
                similarities.append((url, doc_id, similarity))

        # Сортировка по убыванию близости и возврат top_k результатов
        return sorted(similarities, key=lambda x: x[2], reverse=True)[:top_k]


def main():
    TFIDF_DIR = "../home work 4/result"  # Директория с TF-IDF файлами
    INDEX_PATH = "../home work 3/index/inverted_index.json"  # Путь к инвертированному индексу

    # Создание поисковой системы
    search_engine = VectorSearchEngine(TFIDF_DIR, INDEX_PATH)

    # Интерактивный поиск
    while True:
        query = input("Введите запрос (или 'q' для выхода): ")
        if query.lower() == 'q':
            break

        print("\n--- Поиск по токенам ---")
        token_results = search_engine.search(query, top_k=100, use_lemmas=False)
        for url, doc_id, score in token_results:
            print(f"Документ {doc_id}: URL = {url}, Близость = {score:.4f}")

        print("\n--- Поиск по леммам ---")
        lemma_results = search_engine.search(query, top_k=100, use_lemmas=True)
        for url, doc_id, score in lemma_results:
            print(f"Документ {doc_id}: URL = {url}, Близость = {score:.4f}")


if __name__ == "__main__":
    main()
