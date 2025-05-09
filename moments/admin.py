from django.contrib import admin

from .models import WeChatUser, Status

# Register your models here.
admin.site.register(WeChatUser)
admin.site.register(Status)