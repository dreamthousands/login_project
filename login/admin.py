from django.contrib import admin
from .models import UserInfo, ConfirmString
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(ConfirmString)