from django.contrib import admin
from learning_logs.models import Topic, Entry


# Register your models here.
class TopicAdmin(admin.ModelAdmin):
    """显示更多字段"""

    search_fields = ['text']  # 搜索栏


class EnteryAdmin(admin.ModelAdmin):
    """显示更多字段"""
    search_fields = ['text']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EnteryAdmin)
