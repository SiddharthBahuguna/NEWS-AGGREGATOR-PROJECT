from django.contrib import admin
from userauths.models import User

class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','bio']

admin.site.register(User,UserAdmin)