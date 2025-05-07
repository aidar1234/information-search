from flask import Flask, request, render_template
from home_work_5.search_engine import VectorSearchEngine


def create_app():
    app = Flask(__name__)

    # Укажите тут правильные пути к вашим файлам:
    TFIDF_DIR = "../home work 4/result"
    INDEX_JSON = "../home work 3/index/inverted_index.json"

    # Создаём экземпляр поискового движка
    search_engine = VectorSearchEngine(TFIDF_DIR, INDEX_JSON)

    @app.route("/", methods=["GET", "POST"])
    def index():
        token_results = None
        lemma_results = None

        if request.method == "POST":
            query = request.form.get("query", "").strip()
            if query:
                # Поиск по токенам
                token_results = search_engine.search(query, top_k=100, use_lemmas=False)
                # Поиск по леммам
                lemma_results = search_engine.search(query, top_k=100, use_lemmas=True)

        return render_template(
            "index.html",
            token_results=token_results,
            lemma_results=lemma_results
        )

    return app


if __name__ == "__main__":
    app = create_app()
    # debug=True позволяет видеть детальную трассировку ошибок
    app.run(debug=True, host="0.0.0.0", port=5000)