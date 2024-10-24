import logging
from search_engine import search_news, extract_full_text
from text_generator import generate_blog_text, translate_text, generate_slogan_text
from utils import save_slogan_to_docx, save_blog_to_docx, format_filename
from image_generator import gen_img

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_articles(articles):
    for article_count, article in enumerate(articles, start=1):
        article_url = article['url']
        article_title = article['title']
        logging.info(f"Обрабатываем статью {article_count}/{len(articles)}: {article_title}")

        # Translate the article title
        translated_title = translate_text(article_title)
        formatted_title = format_filename(translated_title)

        # Extract the full text of the article
        full_text = extract_full_text(article_url)
        if full_text:
            logging.info(f"Текст статьи успешно извлечён ({len(full_text)} символов)")

            # Generate blog content
            blog_content = generate_blog_text(full_text)
            logging.info("Текст для блога успешно сгенерирован.")
            # Save blog to .docx
            save_blog_to_docx(translated_title, blog_content)
            logging.info("Блог успешно сохранён в .docx.")
            # Generate slogan
            slogan = generate_slogan_text(blog_content)
            logging.info("Слоган успешно сгенерирован.")
            # Save slogan to .docx
            save_slogan_to_docx(translated_title, slogan)
            logging.info("Слоган успешно сохранён в .docx.")

            docx_path = f"../data/sloganDocs/{formatted_title}_slogan.docx"
            gen_img(docx_path)
        else:
            logging.warning("Не удалось извлечь полный текст статьи.")

def get_blog(page_size):
    logging.info("Запускаем поиск новостей...")
    query = (
         "early education AND (arithmetic OR math OR speed reading) AND "
         "(parents OR moms OR mothers) AND "
         "(importance OR benefits OR advantages OR strategies OR tips)"
    )
    articles = search_news(query, page_size=page_size)
    if articles:
        logging.info(f"Найдено {len(articles)} статей. Начнем обработку...")
        process_articles(articles)
    else:
        logging.warning("Не удалось найти статьи по запросу.")


if __name__ == "__main__":
    get_blog(2)  # choice of page_size