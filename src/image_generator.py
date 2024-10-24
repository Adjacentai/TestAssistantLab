from diffusers import DiffusionPipeline
import os
import logging
from utils import read_slogan_from_docx

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def gen_img(docx_path):
    slogan = read_slogan_from_docx(docx_path)
    if not slogan:
        return
    # Загружаем модель
    try:
        pipe = DiffusionPipeline.from_pretrained("stablediffusionapi/realistic-vision-v51")
    except Exception as e:
        logging.error(f"Ошибка при загрузке модели: {e}")
        return

    # Генерируем изображение
    try:
        image = pipe(slogan).images[0]
    except Exception as e:
        logging.error(f"Ошибка при генерации изображения: {e}")
        return

    # Формирование имени для сохранения изображения
    directory = "../data/genSD"
    os.makedirs(directory, exist_ok=True)

    save_path = os.path.join(directory, f"{os.path.basename(docx_path).replace('_slogan.docx', '')}_gen.png")

    # Сохранение изображения
    try:
        image.save(save_path)
        logging.info(f"Изображение сохранено в {save_path}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении изображения: {e}")
        return