from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment, Account

admin.site.register((Post, Comment))

class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInLine, )
    
admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
