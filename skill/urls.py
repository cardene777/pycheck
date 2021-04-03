from django.urls import path
from . import views

app_name = "skill"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path('upload/<str:username>/', views.upload, name='upload'),
    path("upload_done/", views.UploadDone.as_view(), name="upload_done")
]


