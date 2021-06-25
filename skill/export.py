from django.http import HttpResponse
import csv
from .models import SkillCheckData, Result
# from django_pandas.io import read_frame


def data_export(request):
    """
    data export csv file
    :param request:
    :return: csv file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    writer.writerow(["pk", "ユーザー名", "問題番号", "問題レベル", "回答時間", "点数"])
    for data in SkillCheckData.objects.all():
        writer.writerow(
            [data.pk, data.username, data.question_number, data.question_level,
             data.answer_time, data.score])
    return response


def result_export(request):
    """
    data export csv file
    :param request:
    :return: csv file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    writer.writerow(["pk", "ユーザー名", "提出数", "合計点", "平均点"])
    for data in Result.objects.all():
        writer.writerow(
            [data.pk, data.username, data.present_number, data.total_points, data.average_point])
    return response