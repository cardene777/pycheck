from django.contrib import admin
from .models import Image, SkillCheckData

admin.site.register(Image)


class SkillCheckDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'question_number', 'question_level', 'answer_time', 'score')


admin.site.register(SkillCheckData, SkillCheckDataAdmin)
