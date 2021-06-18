from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Image, SkillCheckData, Result, Profile
from gacha.models import Count
import pyocr
import re

import logging

logger = logging.getLogger('skill')
logger.info("log info test!")


class HomeView(generic.TemplateView):
    template_name = "skill/home.html"


def ocr(image_path):
    # from django.core.serializers.json import DjangoJSONEncoder
    from PIL import Image
    # OCR エンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 画像パスの変換
    # from googletrans import Translatr
    # tr = Translator()
    # image_path = json.dumps(image_path, cls=DjangoJSONEncoder)
    # image_path = tr.translate(text=image_path, src="ja", dest="en").text
    # image_path = str(image_path).replace(" ", "_")
    # 使用する画像を指定してOCRを実行
    txt = tool.image_to_string(
        # Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}"),
        Image.open(image_path),
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

    # 原稿画像の読み込み
    img_org = Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}")
    img_rgb = img_org.convert("RGB")
    pixels = img_rgb.load()

    # 原稿画像加工（黒っぽい色以外は白=255,255,255にする）
    c_max = 169
    for j in range(img_rgb.size[1]):
        for i in range(img_rgb.size[0]):
            if (pixels[i, j][0] > c_max or pixels[i, j][1] > c_max or
                    pixels[i, j][0] > c_max):
                pixels[i, j] = (255, 255, 255)

    # ＯＣＲ実行
    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img_rgb, lang="jpn", builder=builder)

    # result = tool.image_to_string(
    #     Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}"),
    #     # Image.open(f"/Users/akira/Desktop/local/develop/pycheck/media/{str(image_path)}"),
    #     lang="jpn",
    #     builder=pyocr.builders.TextBuilder()
    # )

    result = ''.join(result.split())
    print(result)

    # resultの短縮
    point: int = re.search(r"提出数総得点平均点", result).end()
    result: str = result[point:].replace("\"", "").replace("'", "")
    print(result)

    # 回答数
    toi1: int = result.index("問")
    present_number: int = int(float(result[:toi1]))
    result: str = result[toi1+1:]
    print(present_number)

    ten1: int = result.index("点")
    total_points: int = int(float(result[:ten1]))
    result: str = result[ten1+1:]
    print(total_points)

    ten2: int = result.index("点")
    average_point: int = int(float(result[:ten2]))
    print(average_point)

    # index = result.index("ーーーー")
    # result = result[index + 4:]
    # toi = result.index("問")
    # present_number = result[:toi]
    # ten1 = result.index("点")
    # total_points = result[toi + 1:ten1]
    # ten2 = result[ten1 + 1:].index("点")
    # average_point = result[ten1 + 1:][:ten2]
    return int(present_number), int(total_points), int(average_point)


def upload(request):
    if request.method == "POST":
        # form = ImageForm(request.POST, request.FILES)
        username = request.POST["username"]
        file = request.FILES["file"]
        image = Image(username=username, image=file)
        image.save()
        file_name = Image.objects.last().image
        username, question_number, question_level, answer_time, score = ocr(file_name)
        if score == "0" or score == 0 or score == "o" or score == "O":
            score = 0
        data_list = SkillCheckData.objects.filter(username=username).values_list("question_number", flat=True)
        if question_number not in data_list:
            data = SkillCheckData(username=username, question_number=question_number, question_level=question_level,
                                  answer_time=answer_time, score=score)
            data.save()
        try:
            user_count = Count.objects.get(username=username)
            user_count.counter += 1
            user_count.save()
        except:
            user_count = Count(username=username, counter=1)
            user_count.save()
        Image.objects.filter(image=file).delete()
    return render(request, 'skill/upload.html')


class UploadDone(generic.TemplateView):
    template_name = "skill/upload_done.html"


def results_register(request):
    if request.method == "POST":
        # form = ImageForm(request.POST, request.FILES)
        username = request.POST["username"]
        file = request.FILES["file"]
        name: str = str(Profile.objects.filter(username=username)[0].name)
        name_model: int = Profile.objects.get(username=username)

        image = Image(username=name, image=file)
        image.save()

        file_name = Image.objects.values_list("image", flat=True).last()
        present_number, total_points, average_point = ocr_result(file_name)
        name_model.result_set.create(present_number=present_number, total_points=total_points, average_point=average_point)
        # result = Result(name=int(name_id), present_number=present_number, total_points=total_points,
        #                 average_point=average_point)
        # result.save()

        # 画像削除
        Image.objects.filter(image=file).delete()

    return render(request, 'skill/results_register.html')


class ProfileAdd(generic.CreateView):
    model = Profile
    template_name = "skill/profile_add.html"
    success_url = reverse_lazy('skill:home')
    fields = ['username', 'name']
