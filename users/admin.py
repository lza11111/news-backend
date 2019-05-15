from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'get_tags', )
    search_fields = ('username', )
    ordering = ('-id', )

admin.site.register(User, UserAdmin)