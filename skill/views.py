from django.shortcuts import render, redirect
from django.views import generic
from .models import Image, SkillCheckData


class HomeView(generic.TemplateView):
    template_name = "skill/home.html"


def ocr(image_path):
    from PIL import Image
    import pyocr
    import re

    # OCR エンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 画像パスの変換
    image_path = str(image_path).replace(" ", "_")
    # 使用する画像を指定してOCRを実行
    txt = tool.image_to_string(
        Image.open(f"media/images/{str(image_path)}"),
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

    print(new_texts)
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
        score = new_texts[new_texts.index("スコァ:") + 1].split("点")[0]
    except ValueError:
        score = new_texts[new_texts.index("スコアァ:") + 1].split("点")[0]
    return username, question_number, question_level, answer_time, score


def upload(request, username):
    if request.method == "POST":
        # form = ImageForm(request.POST, request.FILES)
        print(f"file: {request.FILES['file']}")
        print(username)
        print(request.FILES["file"])
        image = Image()
        image.image = request.FILES['file']
        image.username = username
        image.save()
        username, question_number, question_level, answer_time, score = ocr(request.FILES.get("file"))
        data_list = SkillCheckData.objects.filter(username=username).values_list("question_number", flat=True)
        if question_number not in data_list:
            data = SkillCheckData(username=username, question_number=question_number, question_level=question_level,
                                  answer_time=answer_time, score=score)
            data.save()
        params = {
            "username": username,
            "question_number": question_number,
            "question_level": question_level,
            "answer_time": answer_time,
            "score": score,
        }
    return render(request, 'skill/upload.html')


class UploadDone(generic.TemplateView):
    template_name = "skill/upload_done.html"
