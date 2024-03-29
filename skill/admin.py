from django.contrib import admin
from .models import Image, SkillCheckData, Result


class ImageAdmin(admin.ModelAdmin):
    list_display = ('username', 'image')


class SkillCheckDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'question_number', 'question_level', 'answer_time', 'score')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('username', 'present_number', 'total_points', 'average_point')


admin.site.register(SkillCheckData, SkillCheckDataAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Result, ResultAdmin)
