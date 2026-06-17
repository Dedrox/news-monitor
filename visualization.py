import csv
import matplotlib.pyplot as plt

input_file = "news_analyzed.csv"

# Лічильники для новин
positive = 0
negative = 0
neutral = 0

print("=== Розрахунок індексу настрою ===")

# Читаємо проаналізований файл
with open(input_file, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader) # Пропускаємо шапку
    
    for row in reader:
        if len(row) < 5: 
            continue
            
        sentiment = row[4] # Беремо п'яту колонку з оцінкою
        if "Позитив" in sentiment:
            positive += 1
        elif "Негатив" in sentiment:
            negative += 1
        elif "Нейтрально" in sentiment:
            neutral += 1

# Математичний розрахунок індексу (відсотки)
total = positive + negative + neutral
if total > 0:
    print(f"Всього проаналізовано новин: {total}")
    print(f"Позитивних: {round((positive/total)*100, 1)}%")
    print(f"Негативних: {round((negative/total)*100, 1)}%")
    print(f"Нейтральних: {round((neutral/total)*100, 1)}%")
else:
    print("Не знайдено новин для аналізу.")

# Побудова та збереження графіка
labels = ['Позитив', 'Негатив', 'Нейтрально']
sizes = [positive, negative, neutral]
colors = ['#4CAF50', '#F44336', '#9E9E9E'] # Зелений, Червоний, Сірий

# Створюємо кругову діаграму
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Інформаційний фон стрічки новин (Індекс настрою)')

# Зберігаємо графік як картинку в папку
plt.savefig("sentiment_chart.png")
print("\nУСПІХ! Графік успішно збережено у файл: sentiment_chart.png")