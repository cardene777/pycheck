from django.urls import path
from . import views

app_name = "skill"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path('upload/', views.upload, name='upload'),
    path("upload_done/", views.UploadDone.as_view(), name="upload_done"),
    path("results_register/", views.results_register, name="results_register"),

    # export
    path("export/", views.Export.as_view(), name="export"),
    path("data_export/", views.data_export, name="data_export"),
    path("result_export/", views.result_export, name="result_export")
]



