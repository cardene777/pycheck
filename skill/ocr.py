import pyocr
import re
import pyocr.builders


def ocr(image_path):
    # from django.core.serializers.json import DjangoJSONEncoder
    from PIL import Image
    # OCR エンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    txt = tool.image_to_string(
        # Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}"),
        Image.open(f"/app/{image_path}"),
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


# def ocr_result(image_path):
#     from PIL import Image
#     # OCR エンジン取得
#     tools = pyocr.get_available_tools()
#     tool = tools[0]
#
#     # 原稿画像の読み込み
#     img_org = Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}")
#     img_rgb = img_org.convert("RGB")
#     pixels = img_rgb.load()
#
#     # 原稿画像加工（黒っぽい色以外は白=255,255,255にする）
#     c_max = 169
#     for j in range(img_rgb.size[1]):
#         for i in range(img_rgb.size[0]):
#             if (pixels[i, j][0] > c_max or pixels[i, j][1] > c_max or
#                     pixels[i, j][0] > c_max):
#                 pixels[i, j] = (255, 255, 255)
#
#     # ＯＣＲ実行
#     builder = pyocr.builders.TextBuilder()
#     result = tool.image_to_string(img_rgb, lang="jpn", builder=builder)
#
#     # result = tool.image_to_string(
#     #     Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}"),
#     #     # Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}"),
#     #     lang="jpn",
#     #     builder=pyocr.builders.TextBuilder()
#     # )
#
#     result = ''.join(result.split())
#     print(result)
#
#     # resultの短縮
#     point: int = re.search(r"提出数総得点平均点", result).end()
#     result: str = result[point:].replace("\"", "").replace("'", "")
#     print(result)
#
#     # 回答数
#     toi1: int = result.index("問")
#     present_number: int = int(float(result[:toi1]))
#     result: str = result[toi1+1:]
#     print(present_number)
#
#     ten1: int = result.index("点")
#     total_points: int = int(float(result[:ten1]))
#     result: str = result[ten1+1:]
#     print(total_points)
#
#     ten2: int = result.index("点")
#     average_point: int = int(float(result[:ten2]))
#     print(average_point)
#
#     # index = result.index("ーーーー")
#     # result = result[index + 4:]
#     # toi = result.index("問")
#     # present_number = result[:toi]
#     # ten1 = result.index("点")
#     # total_points = result[toi + 1:ten1]
#     # ten2 = result[ten1 + 1:].index("点")
#     # average_point = result[ten1 + 1:][:ten2]
#     return int(present_number), int(total_points), int(average_point)
