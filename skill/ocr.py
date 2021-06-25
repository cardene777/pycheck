import pyocr
import re
import pyocr.builders
import io
import requests


def change_text(text):
    new_text = re.sub("[あ-ん]", "", text)
    return new_text


def ocr_py(image_path):
    from PIL import Image

    tools = pyocr.get_available_tools()
    tool = tools[0]

    txt = tool.image_to_string(
        Image.open(io.BytesIO(requests.get(image_path).content)),
        lang="jpn",
        builder=pyocr.builders.TextBuilder()
    )
    return txt


def ocr(image_path):

    image_path = f"https://res.cloudinary.com/dfv9woe7f/image/upload/v1624152195/{image_path}"

    txt = ocr_py(image_path)
    split_txt = txt.replace("\n", "").split(" ")

    new_texts = []
    for text in split_txt:
        text = change_text(text)
        if text != "":
            new_texts.append(text)

    username = new_texts[0]
    try:
        question_number = new_texts[new_texts.index("受験結果問題") + 2].split(":")[0]
    except ValueError:
        question_number = new_texts[new_texts.index("受験結果") + 2].split(":")[0]
    try:
        question_level = new_texts[new_texts.index("受験結果問題") + 2].split(":")[0][0]
    except ValueError:
        question_level = new_texts[new_texts.index("受験結果") + 2].split(":")[0][0]
    answer_time = new_texts[new_texts.index("解答時間:") + 1]
    try:
        score = new_texts[new_texts.index("スコア:") + 1].split("点")[0]
    except ValueError:
        try:
            score = new_texts[new_texts.index("スコァ:") + 1].split("点")[0]
        except ValueError:
            score = new_texts[new_texts.index("スコアァ:") + 1].split("点")[0]
    return username, question_number, question_level, answer_time, score


def ocr_result(image_path):
    image_path = f"https://res.cloudinary.com/dfv9woe7f/image/upload/v1624152195/{image_path}"

    txt = ocr_py(image_path)

    split_txt = txt.replace("\n", "").split(" ")

    new_texts = []
    for text in split_txt:
        text = change_text(text)
        if text != "":
            new_texts.append(text)

    if "受験結果問題" in new_texts or "受験結果" in new_texts or "解答時間:" in new_texts:
        class NotResultError(Exception):
            pass
        raise NotResultError('成績結果画像ではありません。')

    def change(tet):
        new_text = re.sub("[あ-んa-zア-ン?A-Z※。還]+", "", tet)
        new_text = re.sub("[^0-9.]+", "", tet)
        return new_text

    new_texts = []
    for text in split_txt:
        text = change(text)
        if text != "":
            new_texts.append(text)

    return float(new_texts[0]), float(new_texts[1]), float(new_texts[2])
