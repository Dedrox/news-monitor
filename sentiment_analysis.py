import csv
from deep_translator import GoogleTranslator
from textblob import TextBlob

# Назви наших файлів
input_file = "news_database.csv"
output_file = "news_analyzed.csv"

print("=== Запуск алгоритму аналізу тональності ===")
print("Це може зайняти кілька секунд, аналізуємо текст...")

# Відкриваємо зібрану базу і створюємо нову для результатів
with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Читаємо стару шапку і додаємо нову колонку "Тональність"
    header = next(reader)
    header.append("Тональність")
    writer.writerow(header)

    # Підключаємо перекладач
    translator = GoogleTranslator(source='uk', target='en')

    # Проходимося по кожному рядку з нашої бази
    for row in reader:
        if not row:
            continue

        title = row[0] # Беремо заголовок

        # Якщо замість заголовка порожнє значення, пропускаємо аналіз
        if title == "--":
            sentiment_label = "--"
        else:
            try:
                # 1. Перекладаємо текст для точної роботи алгоритму
                translated_text = translator.translate(title)

                # 2. Визначаємо тональність за допомогою TextBlob
                analysis = TextBlob(translated_text)

                # 3. Приймаємо рішення (Полярність від -1 до 1)
                if analysis.sentiment.polarity > 0.1:
                    sentiment_label = "Позитив 🟢"
                elif analysis.sentiment.polarity < -0.1:
                    sentiment_label = "Негатив 🔴"
                else:
                    sentiment_label = "Нейтрально ⚪"
            except Exception:
                sentiment_label = "Помилка"

        # Записуємо рядок з новою оцінкою у фінальний файл
        row.append(sentiment_label)
        writer.writerow(row)
        
        # Виводимо прогрес на екран (перші 40 символів)
        print(f"{title[:40]}... -> {sentiment_label}")

print(f"\nГотово! Проаналізовані новини збережено у файл: {output_file}")