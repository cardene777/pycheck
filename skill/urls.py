from django.urls import path
from . import views

app_name = "skill"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path('upload/', views.upload, name='upload'),
    path("upload_done/", views.UploadDone.as_view(), name="upload_done"),
    # path("results_register/", views.results_register, name="results_register"),
    path("profile_add/", views.ProfileAdd.as_view(), name="profile_add"),
]


