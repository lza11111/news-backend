from django.db import models
from django.utils import timezone

from like.models import Likable
from history.models import Recordable
from tags.models import Tag

class News(Likable, Recordable):
    # basic information
    title = models.CharField(max_length=255, unique=True, db_index=True)
    cover_image = models.URLField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_tags(self):
        return "\n".join([str(tag) for tag in self.tags.all()])

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created_at',)