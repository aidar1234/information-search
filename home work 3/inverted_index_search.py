import os
import re
import json


def build_inverted_index(directory):
    """
    Построение инвертированного индекса из файлов лемм
    """
    inverted_index = {}

    # Создание директории для индекса, если она не существует
    os.makedirs("index", exist_ok=True)

    for filename in os.listdir(directory):
        if filename.startswith("lemmas-") and filename.endswith(".txt"):
            doc_id = filename.replace("lemmas-", "").replace(".txt", "")

            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        lemma = parts[0]
                        tokens = parts[1:]

                        # Добавляем лемму и все токены
                        for token in [lemma] + tokens:
                            if token not in inverted_index:
                                inverted_index[token] = set()
                            inverted_index[token].add(doc_id)

    # Сохранение индекса в JSON-файл
    with open("index/inverted_index.json", "w", encoding="utf-8") as f:
        # Преобразуем множества в списки для сериализации
        serializable_index = {k: list(v) for k, v in inverted_index.items()}
        json.dump(serializable_index, f, ensure_ascii=False, indent=2)

    # Сохранение текстовой версии индекса
    with open("index/inverted_index.txt", "w", encoding="utf-8") as f:
        for token, docs in sorted(inverted_index.items()):
            f.write(f"{token}: {' '.join(sorted(docs))}\n")

    return inverted_index


def load_inverted_index(index_path="index/inverted_index.json"):
    """
    Загрузка инвертированного индекса из JSON-файла
    """
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            loaded_index = json.load(f)
        # Преобразуем списки обратно во множества
        return {k: set(v) for k, v in loaded_index.items()}
    except FileNotFoundError:
        return {}


def parse_query(query):
    """
    Преобразование инфиксного запроса в постфиксную нотацию
    """
    query = query.replace(" AND ", " & ").replace(" OR ", " | ").replace(" NOT ", " ~ ")

    def get_precedence(op):
        if op in ('~', '(', ')'):
            return 1
        elif op == '&':
            return 2
        elif op == '|':
            return 3
        return 0

    output_queue = []
    operator_stack = []
    tokens = re.findall(r'\(|\)|~|&|\||\w+', query)

    for token in tokens:
        if token.isalnum():
            output_queue.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
        else:
            while (operator_stack and get_precedence(operator_stack[-1]) >= get_precedence(token)
                   and operator_stack[-1] not in '()'):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return ' '.join(output_queue)


def evaluate_postfix(postfix_query, inverted_index):
    """
    Выполнение булева поиска по постфиксному запросу
    """
    stack = []
    tokens = postfix_query.split()
    all_docs = set(str(i) for i in range(1, len(os.listdir('../home work 1/pages')) + 1))

    for token in tokens:
        if token.isalnum():
            if token in inverted_index:
                stack.append(inverted_index.get(token, set()))
            else:
                stack.append(set())
        elif token == '~':
            top = stack.pop()
            stack.append(all_docs - top)
        elif token == '&':
            right = stack.pop()
            left = stack.pop()
            stack.append(left.intersection(right))
        elif token == '|':
            right = stack.pop()
            left = stack.pop()
            stack.append(left.union(right))

    return stack[0] if stack else set()


def search(query, inverted_index):
    """
    Выполнение поиска по запросу
    """
    postfix_query = parse_query(query)
    return sorted(list(evaluate_postfix(postfix_query, inverted_index)))


lemmas_dir = "../home work 2/result"

# Построение инвертированного индекса
inverted_index = load_inverted_index()
if not inverted_index:
        inverted_index = build_inverted_index(lemmas_dir)

while True:
    query = input("Введите запрос (или 'q' для выхода): ")
    if query.lower() == 'q':
        break

    try:
        results = search(query, inverted_index)
        print("Найдены документы:", results)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")