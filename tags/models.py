from django.db import models

from .constants import Type, TYPE_CHOICES


class Tag(models.Model):
    name = models.CharField(max_length=200)
    unique_name = models.SlugField(max_length=200, unique=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ('name',)
