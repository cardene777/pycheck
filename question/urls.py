from django.urls import path
from .views import *
from question import views

app_name = 'question'
urlpatterns = [
    path('list/', QuestionList.as_view(), name='list'),
    path('detail/<int:pk>/', views.question_detail, name='detail'),
    path('update/<int:pk>/', QuestionUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', QuestionDelete.as_view(), name='delete'),
    path('create/', views.idea_upload, name='create'),
]
