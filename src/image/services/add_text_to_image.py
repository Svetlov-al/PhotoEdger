import io
import logging

from PIL import Image as PILImage, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


def add_text_to_image(
    image_data: bytes,
    file_path: str,
    text: str,
) -> None:
    """Добавляет текст из описания к изображению"""

    image = PILImage.open(io.BytesIO(image_data))

    # => Настройка шрифта и размера текста
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        font = ImageFont.truetype(font_path, 15)
    except IOError:
        font = ImageFont.load_default(size=15)

    width, height = image.size

    # => Разделение текста на строки с переносом
    lines = []
    words = text.split()
    line = ""

    for word in words:
        test_line = line + word + " "
        if ImageDraw.Draw(image).textbbox((0, 0), test_line, font=font)[2] <= width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "

    lines.append(line)

    text_height = sum(
        ImageDraw.Draw(image).textbbox((0, 0), line, font=font)[3] for line in lines
    )
    text_image = PILImage.new("RGB", (width, text_height), color="black")
    text_draw = ImageDraw.Draw(text_image)

    y = 0
    for line in lines:
        text_draw.text((10, y), line, font=font, fill="white")
        y += text_draw.textbbox((0, 0), line, font=font)[3]

    final_image = PILImage.new("RGB", (width, height + text_image.height))
    final_image.paste(image, (0, 0))
    final_image.paste(text_image, (0, height))

    final_image.save(file_path, format="JPEG")
