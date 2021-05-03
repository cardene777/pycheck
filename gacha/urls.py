from django.urls import path
from . import views

app_name = "gacha"

urlpatterns = [
    path("gacha/<str:username>/", views.gacha, name="gacha"),
    path("gacha_detail/<str:username>/<str:gacha_title>/", views.gacha_detail, name="gacha_detail"),
    path("gacha_play/<str:username>/<str:gacha_title>/", views.gacha_play, name="gacha_play"),
]


