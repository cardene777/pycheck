from django.contrib import admin
from .models import GachaTitle, GachaItem, Count, MyGachaItems


class GachaTitleDataAdmin(admin.ModelAdmin):
    list_display = ('title',)


class GachaItemDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'name')


class CountDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'counter')


class MyGachaItemsAdmin(admin.ModelAdmin):
    list_display = ('username', 'item')


admin.site.register(GachaTitle, GachaTitleDataAdmin)
admin.site.register(GachaItem, GachaItemDataAdmin)
admin.site.register(Count, CountDataAdmin)
admin.site.register(Count, MyGachaItemsAdmin)
