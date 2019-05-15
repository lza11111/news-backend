# coding: utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import F

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)


class Likable(models.Model):
    like_count = models.IntegerField(default=0)
    likes = GenericRelation(Like)

    class Meta:
        abstract = True

    # return True if this user hasn't liked this item before
    # otherwise return False
    def liked_by(self, user):
        # instead of using self.likes.filter(user=user)
        # the following approach is much more faster
        # because an object can be liked million of times
        # but a user usually don't create too many likes.
        if not user.is_authenticated:
            return False

        content_type = ContentType.objects.get_for_model(self)
        if Like.objects.filter(
            user=user,
            content_type=content_type,
            object_id=self.id,
        ).exists():
            return False

        with transaction.atomic():
            Like.objects.create(content_object=self, user=user)
            self.like_count = F('like_count') + 1
            self.save()

        return True

    def like_canceled_by(self, user):
        content_type = ContentType.objects.get_for_model(self)

        with transaction.atomic():
            likable_object = Like.objects.filter(
                user=user,
                content_type=content_type,
                object_id=self.id,
            )
            if likable_object.count() > 0:
                likable_object.delete()
                self.like_count = F('like_count') - 1
                self.save()

        return True

    def get_recent_likes(self, k=5):
        return self.likes.all()[:k]

    def has_liked_by(self, user):
        # check is user liked this object
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(user=user,
                                   content_type=content_type,
                                   object_id=self.id).exists()

    @classmethod
    def get_like_id_set(cls, user):
        if not user.is_authenticated:
            return set()
        content_type = ContentType.objects.get_for_model(cls)
        return set(Like.objects.filter(
            user=user,
            content_type=content_type,
        ).values_list('object_id', flat=True))