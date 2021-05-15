from django.contrib import admin
from question.models import QuestionModel, Comment


class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'idea', 'create', 'category', 'level',
                    'image_1', 'image_2', 'image_3', 'image_4')


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('comment',)


admin.site.register(QuestionModel, QuestionModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
