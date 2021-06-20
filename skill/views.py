from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Image, SkillCheckData, Profile
from .ocr import ocr

import logging

logger = logging.getLogger('skill')
logger.info("log info test!")


class HomeView(generic.TemplateView):
    template_name = "skill/home.html"


def upload(request):
    if request.method == "POST":
        # form = ImageForm(request.POST, request.FILES)
        username = request.POST["username"]
        file = request.FILES["file"]
        print(username)
        image = Image(username=username, image=file)
        image.save()
        file_name = Image.objects.filter(username=username).last().image
        username, question_number, question_level, answer_time, score = ocr(file_name)
        if score == "0" or score == 0 or score == "o" or score == "O":
            score = 0
        data_list = SkillCheckData.objects.filter(username=username).values_list("question_number", flat=True)
        if question_number not in data_list:
            data = SkillCheckData(username=username, question_number=question_number, question_level=question_level,
                                  answer_time=answer_time, score=score)
            data.save()
        # try:
        #     user_count = Count.objects.get(username=username)
        #     user_count.counter += 1
        #     user_count.save()
        # except:
        #     user_count = Count(username=username, counter=1)
        #     user_count.save()
        # Image.objects.filter(image=file).delete()
    return render(request, 'skill/upload.html')


class UploadDone(generic.TemplateView):
    template_name = "skill/upload_done.html"


# def results_register(request):
#     if request.method == "POST":
#         # form = ImageForm(request.POST, request.FILES)
#         username = request.POST["username"]
#         file = request.FILES["file"]
#         name: str = str(Profile.objects.filter(username=username)[0].name)
#         name_model: int = Profile.objects.get(username=username)
#
#         image = Image(username=name, image=file)
#         image.save()
#
#         file_name = Image.objects.values_list("image", flat=True).last()
#         present_number, total_points, average_point = ocr.ocr_result(file_name)
#         name_model.result_set.create(present_number=present_number, total_points=total_points, average_point=average_point)
#         # result = Result(name=int(name_id), present_number=present_number, total_points=total_points,
#         #                 average_point=average_point)
#         # result.save()
#
#         # 画像削除
#         Image.objects.filter(image=file).delete()
#
#     return render(request, 'skill/results_register.html')


class ProfileAdd(generic.CreateView):
    model = Profile
    template_name = "skill/profile_add.html"
    success_url = reverse_lazy('skill:home')
    fields = ['username', 'name']
