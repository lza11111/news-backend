from django.db import models
from django.contrib.auth.models import AbstractUser

from tags.models import Tag

class User(AbstractUser):
    # required for registeration
    tags = models.ManyToManyField(Tag, blank=True)

    def get_tags(self):
        return "\n".join([str(tag) for tag in self.tags.all()])

    class Meta:
        ordering = ('-id',)