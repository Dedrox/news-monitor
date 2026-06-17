import csv
import feedparser

# URL RSS-стрічки новин BBC Україна
rss_url = "https://feeds.bbci.co.uk/ukrainian/rss.xml"

# Парсимо (збираємо) дані за вказаним посиланням
feed = feedparser.parse(rss_url)

# Назва файлу таблиці, куди все збережемо
csv_filename = "news_database.csv"

print("=== Процес збору та збереження новин ===")

# Відкриваємо файл для запису (створиться автоматично в нашій папці)
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Створюємо шапку таблиці
    writer.writerow(["Заголовок", "Посилання", "Короткий опис", "Дата"])

    # Проходимося по всіх знайдених новинах
    for entry in feed.entries:
        # Перевіряємо наявність кожного поля. Якщо пусте — пишемо "--"
        title = entry.get("title", "--")
        link = entry.get("link", "--")

        summary = entry.get("summary", "--")
        if not summary or summary.isspace():
            summary = "--"

        date = entry.get("published", "--")
        if not date or date.isspace():
            date = "--"

        # Записуємо рядок із даними в таблицю
        writer.writerow([title, link, summary, date])

print(f"Готово! Всі новини успішно збережено у файл: {csv_filename}")