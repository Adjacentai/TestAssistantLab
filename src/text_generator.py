from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
from utils import trim_text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

OPENAI_API = os.getenv('OPENAI_API')
MODEL_URL = os.getenv('MODEL_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

# client - OpenAI API settings
client = OpenAI(
    base_url=MODEL_URL,  # Адрес локального сервера с ИИ моделью
    api_key=OPENAI_API  # Локальный API-ключ
)

# Connect to AI and send messages for text generation
def send_to_aibot(messages, max_tokens=400):
    try:
        # Request to the local model for text generation
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        # Return the generated response from the AI
        return completion.choices[0].message.content
    except Exception as e:
        # Log an error message if the connection fails
        logging.error(f"Ошибка при попытке подключения к языковой модели {MODEL_NAME}")
        return None

# Translate text to Russian using the AI model
def translate_text(text):
    messages = [
        {"role": "system", "content": "Ты переводишь текст на русский язык."},
        {"role": "user", "content": f"Переведи это на русский: {text}"}
    ]

    translation = send_to_aibot(messages)
    if translation is None:
        logging.error("Не удалось перевести текст.")
        return "Произошла ошибка при переводе текста."
    return translation

# Generate blog content based on a news article
def generate_blog_text(news_article):

    trimmed_article = trim_text(news_article, max_lenght = 1500)

    messages = [
        {"role": "system", "content": "Перепиши в блог для целевой аудитории - мамы. Помоги понять важность раннего обучения детей арифметике, скорочтению и другим предметам на основе любого текста."},
        {"role": "user", "content": f"На основе текста Напиши краткую выжимку, аудитория мамы и развитие их ребенка: {trimmed_article}."}
    ]

    blog_text = send_to_aibot(messages, max_tokens = 200)

    if blog_text is None:
        logging.error("Не удалось сгенерировать текст блога.")
        return "Произошла ошибка при генерации текста блога."
    return blog_text

# Generate a slogan based on the blog text
def generate_slogan_text(blog_text):

    messages = [
        {"role": "system", "content": "Ты должен выделить главную мысль или краткий запоминающийся лозунг из текста, который будет использоваться для инфографики или баннера. Лозунг должен быть коротким, ясным и вдохновляющим."},
        {"role": "user", "content": f"Извлеки основную мысль из текста для блога: {blog_text}"}
    ]

    slogan = send_to_aibot(messages, max_tokens=100)

    if slogan is None:
        logging.error("Не удалось сгенерировать текст слогана из блога.")
        return "Произошла ошибка при генерации текста слогана из блога."
    return slogan


