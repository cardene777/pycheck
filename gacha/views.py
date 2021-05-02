from django.shortcuts import render, redirect
from django.views import generic
from .models import GachaTitle, GachaItem, Count
import random


class Gacha(generic.ListView):
    template_name = "gacha/gacha.html"
    model = GachaTitle
    context_object_name = "gacha_titles"


def gacha_detail(requests, username, gacha_title):
    message = "NO"
    gacha_items = GachaItem.objects.filter(title__title=gacha_title)
    counter = Count.objects.get(username=username)
    params = {
        "message": message,
        "gacha_items": gacha_items,
        "gacha_title": gacha_title,
        "counter": counter,
    }
    return render(requests, "gacha/gacha_detail.html", params)


def gacha_play(requests, username, gacha_title):
    message = "OK"
    gacha_items = GachaItem.objects.filter(title__title=gacha_title.lower())
    counter = Count.objects.get(username=username)
    counter.counter -= 1
    counter.save()
    counter = Count.objects.get(username=username)
    probability = []
    rare_probability = {
        "N": 0.6,
        "R": 0.3,
        "SR": 0.07,
        "VR": 0.03
    }
    for gacha_item in gacha_items:
        probability.append(rare_probability[gacha_item.rare])

    random_item = random.choices(gacha_items, weights=probability, k=1)

    gacha_random_item = GachaItem.objects.get(name=random_item[0].name)

    params = {
        "message": message,
        "item": gacha_random_item,
        "gacha_title": gacha_title,
        "counter": counter,
    }
    return render(requests, "gacha/gacha_detail.html", params)