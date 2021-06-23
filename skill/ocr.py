import pyocr
import re
import pyocr.builders
import io
import requests


def ocr(image_path):
    from PIL import Image
    # OCR エンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    image_path = f"https://res.cloudinary.com/dfv9woe7f/image/upload/v1624152195/{image_path}"

    txt = tool.image_to_string(
        Image.open(io.BytesIO(requests.get(image_path).content)),
        lang="jpn",
        builder=pyocr.builders.TextBuilder()
    )

    split_txt = txt.replace("\n", "").split(" ")

    def change(text):
        new_text = re.sub("[あ-ん]", "", text)
        return new_text

    new_texts = []
    for text in split_txt:
        text = change(text)
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
    from PIL import Image
    # OCR エンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    image_path = f"https://res.cloudinary.com/dfv9woe7f/image/upload/v1624152195/{image_path}"

    # 使用する画像を指定してOCRを実行
    txt = tool.image_to_string(
        Image.open(io.BytesIO(requests.get(image_path).content)),
        lang="jpn",
        builder=pyocr.builders.TextBuilder()
    )

    split_txt = txt.replace("\n", "").split(" ")

    def change(text):
        new_text = re.sub("[あ-んa-zア-ン?A-Z※。還]+", "", text)
        new_text = re.sub("[^0-9]+", "", text)
        return new_text

    new_texts = []
    for text in split_txt:
        text = change(text)
        if text != "":
            new_texts.append(text)

    return int(new_texts[0]), int(new_texts[1]), int(new_texts[2])
