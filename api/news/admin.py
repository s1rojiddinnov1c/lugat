from django.contrib import admin
from .models import News, Category, Tag
# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']



admin.site.register(News, NewsAdmin)
admin.site.register(Category)
admin.site.register(Tag)

