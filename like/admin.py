from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Like

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'object_id', 'content_object')

admin.site.register(Like, LikeAdmin)