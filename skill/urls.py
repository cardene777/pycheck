from django.urls import path
from . import views

app_name = "skill"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path('upload/', views.upload, name='upload'),
    path("upload_done/", views.UploadDone.as_view(), name="upload_done"),
    path("results_register/", views.results_register, name="results_register"),
    path("export/", views.export, name="export")
]



