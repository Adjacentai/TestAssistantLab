from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()

API_KEY = os.getenv('NEWS_API')

# Function to search for news articles based on a query and return a list of articles.
def search_news(query, page_size):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}&pageSize={page_size}"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data['articles']
            return articles
        else:
            print(f"Ошибка при получении новостей, пробуем снова {response.status_code}")

# Function to extract the full text from a news article given its URL.
def extract_full_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = ''.join([p.get_text() for p in paragraphs])
            return article_text if article_text.strip() else None
        else:
            return None
    except Exception as e:
        print(f"Ошибка при извлечении текста из {url}: {e}")
        return None
