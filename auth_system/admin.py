from django.contrib import admin
from django.contrib.auth import get_user_model

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','account_created','last_login']

admin.site.register(get_user_model(),UserAdmin)
