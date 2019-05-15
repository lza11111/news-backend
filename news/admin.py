from django.contrib import admin

from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cover_image', 'get_tags', 'updated_at', 'created_at')
    list_filter = ('tags',)
    search_fields = ('title', )
    ordering = ('-id', )

admin.site.register(News, NewsAdmin)