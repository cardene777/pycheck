from django.shortcuts import render, redirect
from django.views import generic
from .models import GachaTitle, GachaItem, Count, MyGachaItems
import random


def gacha(requests, username):
    gacha_titles = GachaTitle.objects.all()
    try:
        user_count = Count.objects.get(username=username)
    except:
        user_count = "No"
    params = {
        "gacha_titles": gacha_titles,
        "user_count": user_count,
    }
    return render(requests, "gacha/gacha.html", params)


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

    # ガチャタイトルの名前修正
    gacha_items = GachaItem.objects.filter(title__title=gacha_title.lower())

    # カウンターを１減らす
    counter = Count.objects.get(username=username)
    counter.counter -= 1
    counter.save()
    counter = Count.objects.get(username=username)
    # 確率設定
    probability = []
    rare_probability = {
        "N": 0.6,
        "R": 0.3,
        "SR": 0.07,
        "VR": 0.03
    }
    for gacha_item in gacha_items:
        probability.append(rare_probability[gacha_item.rare])

    # ランダムに１つ取得
    random_item = random.choices(gacha_items, weights=probability, k=1)
    gacha_random_item = GachaItem.objects.get(name=random_item[0].name)

    # MyGachaItemsモデルにデータ登録
    my_gach_item = MyGachaItems(username=username, item=gacha_random_item.name)
    my_gach_item.save()

    params = {
        "message": message,
        "item": gacha_random_item,
        "gacha_title": gacha_title,
        "counter": counter,
    }
    return render(requests, "gacha/gacha_detail.html", params)


def gacha_item_list(requests, username):
    # 取得したガチャアイテムを全て取得
    item_names = MyGachaItems.objects.filter(username=username)
    gacha_items = []
    for item_name in item_names:
        gacha_item = GachaItem.objects.get(name=item_name.name)
        gacha_items.append(gacha_item)

    params = {
        "gacha_items": gacha_items
    }
    return render(requests, "gacha/my_gacha_item.html", params)