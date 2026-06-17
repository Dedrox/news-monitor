import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from textblob import TextBlob
import pandas as pd
from datetime import datetime
from time import mktime

# Налаштування сторінки
st.set_page_config(page_title="Моніторинг новин", layout="wide")
st.title("📊 Система аналізу тональності новин")
st.write("Цей веб-додаток збирає свіжі новини, аналізує їхній емоційний фон та візуалізує результати.")

# База джерел новин
news_sources = {
    "BBC Україна": "https://feeds.bbci.co.uk/ukrainian/rss.xml",
    "ТСН": "https://tsn.ua/rss/full.rss",
    "УНІАН": "https://rss.unian.net/site/news_ukr.rss",
    "Економічна Правда": "https://epravda.com.ua/rss/"
}

# Розбиваємо меню на дві колонки
col_menu1, col_menu2 = st.columns(2)

with col_menu1:
    selected_source_name = st.selectbox("🌐 Оберіть джерело новин", list(news_sources.keys()))
    selected_rss_url = news_sources[selected_source_name]

with col_menu2:
    selected_date = st.date_input("📅 Оберіть дату для аналізу", datetime.today().date())

st.divider()

# Кнопка для запуску процесу
if st.button("Зібрати та проаналізувати новини"):
    with st.spinner(f'Шукаємо новини від {selected_source_name} за {selected_date}...'):
        
        feed = feedparser.parse(selected_rss_url)
        translator = GoogleTranslator(source='uk', target='en')
        
        results = []
        pos, neg, neu = 0, 0, 0
        
        for entry in feed.entries:
            # Спроба витягнути дату
            article_date = None
            if entry.get("published_parsed"):
                article_date = datetime.fromtimestamp(mktime(entry.published_parsed)).date()
            
            # Фільтр по даті
            if article_date and article_date != selected_date:
                continue
                
            title = entry.get("title", "--")
            link = entry.get("link", "--")
            
            if title != "--":
                try:
                    translated = translator.translate(title)
                    analysis = TextBlob(translated)
                    polarity = analysis.sentiment.polarity
                    
                    # === НАШ ПРОУКРАЇНСЬКИЙ ФІЛЬТР ===
                    title_lower = title.lower()
                    # Список слів-маркерів ворога (можеш розширювати цей список)
                    enemy_keywords = ["росія", "рф", "окупант", "ворог", "путін", "москва", "глушити", "загроза"]
                    
                    for word in enemy_keywords:
                        if word in title_lower:
                            polarity -= 0.5  # Штучно знижуємо бал емоційності, якщо є ворог
                            break
                    # =================================
                    
                    if polarity > 0.1:
                        sentiment = "Позитив 🟢"
                        pos += 1
                    elif polarity < -0.1:
                        sentiment = "Негатив 🔴"
                        neg += 1
                    else:
                        sentiment = "Нейтрально ⚪"
                        neu += 1
                except:
                    sentiment = "Помилка"
            else:
                sentiment = "--"
                
            results.append({"Заголовок": title, "Тональність": sentiment, "Посилання": link})
        
        # Візуалізація результатів
        if results:
            st.success(f"Готово! Знайдено новин: {len(results)}")
            
            col_data1, col_data2 = st.columns([2, 1])
            
            with col_data1:
                st.subheader(f"Стрічка: {selected_source_name}")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
            
            with col_data2:
                st.subheader("Інформаційний фон")
                labels = ['Позитив', 'Негатив', 'Нейтрально']
                sizes = [pos, neg, neu]
                colors = ['#4CAF50', '#F44336', '#9E9E9E']
                
                if sum(sizes) > 0:
                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
                    st.pyplot(fig)
        else:
            st.warning(f"За обрану дату ({selected_date}) новин у джерелі '{selected_source_name}' не знайдено.")