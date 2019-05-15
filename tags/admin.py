from django.contrib import admin

from tags.models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unique_name', )
    search_fields = ('name', 'unique_name')
    ordering = ('-id', )

admin.site.register(Tag, TagAdmin)
