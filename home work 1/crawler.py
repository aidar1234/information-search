import time
import os
import requests

with open("urls.txt", "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file if line.strip()]

os.makedirs("pages", exist_ok=True)

index_lines = []
for index, url in enumerate(urls, start=1):
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()

        file_name = f"pages/{index}.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Скачано: {url} -> {file_name}")
        index_lines.append(f'{file_name} {url}')
        time.sleep(0.5)
    except requests.RequestException as e:
        print(f"Ошибка при скачивании {url}: {e}")

print("Скачивание страниц завершено!")

with open("index.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(index_lines))
