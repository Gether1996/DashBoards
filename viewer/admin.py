from django.contrib import admin
from .models import Statistic, DataItem, ChatRoom, ChatMessage

admin.site.register(Statistic)
admin.site.register(DataItem)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
