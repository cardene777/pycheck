from django.shortcuts import render, redirect
from django.views import generic, View
from .models import QuestionModel, Comment
from .forms import CommentForm, UploodImgForm
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.

class QuestionList(generic.ListView):
    template_name = 'question/list.html'
    model = QuestionModel
    context_object_name = 'questions'


# 詳細記事,コメント機能
def question_detail(request, pk):
    # 後で変える
    question = QuestionModel.objects.get(id=pk)
    # print(f"obj: {obj}")
    # print(f"obj: {obj.title}")
    # print(obj.image_2)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = question
            comment.save()
    comments = Comment.objects.filter(article=question)
    parms = {
        'question': question,
        'comments': comments,
    }
    return render(request, 'question/detail.html', parms)


class QuestionUpdate(generic.UpdateView):
    template_name = 'question/update.html'
    model = QuestionModel
    fields = ('category', 'level', 'title', 'content', 'deadline', 'idea',)
    success_url = reverse_lazy('question:list')


class QuestionDelete(generic.DeleteView):
    template_name = 'question/delete.html'
    model = QuestionModel
    context_object_name = 'question'

    success_url = reverse_lazy('question:list')


# class QuestionCreate(generic.CreateView):
#     template_name = 'question/create.html'
#     model = QuestionModel
#     fields = ('title', 'content', 'idea', 'deadline', 'category', 'level', 'image_1', 'image_2', 'image_3', 'image_4')

#     success_url = reverse_lazy('list')

# アップロード
def idea_upload(request):
    if request.method == "POST":
        form = UploodImgForm(request.POST)
        if form.is_valid():
            question = QuestionModel()
            question.title = request.POST['title']
            question.content = request.POST['content']
            question.idea = request.POST['idea']
            question.category = request.POST['category']
            question.level = request.POST['level']
            try:
                question.image_1 = request.FILES['image_1']
            except:
                pass
            try:
                question.image_2 = request.FILES['image_2']
            except:
                pass
            try:
                question.image_3 = request.FILES['image_3']
            except:
                pass
            try:
                question.image_4 = request.FILES['image_4']
            except:
                pass
            question.published_date = timezone.now()
            question.save()
            return redirect('question:detail', pk=question.pk)
    else:
        form = UploodImgForm()
    return render(request, 'question/create.html', {'form': form})


@login_required  # 追加
def post_list(request):
    return render(request, 'question/post_list.html')