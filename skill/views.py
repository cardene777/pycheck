from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Image, SkillCheckData, Result
from .ocr import ocr, ocr_result
from django.contrib import messages
from django.http import HttpResponse
import csv


class HomeView(generic.TemplateView):
    template_name = "skill/home.html"


def upload(request):
    if request.method == "POST":
        username = request.POST["username"]
        file = request.FILES["file"]
        image = Image(username=username, image=file)
        image.save()
        file_name = Image.objects.filter(username=username).last().image
        _, question_number, question_level, answer_time, score = ocr(file_name)
        if score == "0" or score == 0 or score == "o" or score == "O":
            score = 0
        data_list = SkillCheckData.objects.filter(username=username).values_list("question_number", flat=True)
        if question_number not in data_list:
            data = SkillCheckData(username=username, question_number=question_number, question_level=question_level,
                                  answer_time=answer_time, score=score)
            data.save()
            Image.objects.filter(username=username).delete()
    return render(request, 'skill/upload.html')


class UploadDone(generic.TemplateView):
    template_name = "skill/upload_done.html"


def results_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        file = request.FILES["file"]
        image = Image(username=username, image=file)
        image.save()
        file_name = Image.objects.filter(username=username).last().image
        present_number, total_points, average_point = ocr_result(file_name)
        if Result.objects.filter(username=username).exists():
            Result.objects.filter(username=username).delete()
        data = Result(username=username, present_number=present_number, total_points=total_points,
                      average_point=average_point)
        data.save()
        Image.objects.filter(username=username).delete()

    return render(request, 'skill/results_register.html')


def export(request):
    """
    data export csv file
    :param request:
    :return: csv file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    writer.writerow(["pk", "ユーザ名", "問題番号", "問題レベル", "回答時間", "点数"])
    for data in SkillCheckData.objects.all():
        writer.writerow(
            [data.pk, data.username, data.question_number, data.question_level,
             data.answer_time, data.score])
    return response
