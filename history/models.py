# coding: utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import F


class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)


class Recordable(models.Model):
    read_count = models.IntegerField(default=0)
    reads = GenericRelation(Record)

    class Meta:
        abstract = True

    def read_by(self, user):
        if not user.is_authenticated:
            return False

        content_type = ContentType.objects.get_for_model(self)

        if Record.objects.filter(
            user=user,
            content_type=content_type,
            object_id=self.id,
        ).exists():
            Record.objects.filter(
                user=user,
                content_type=content_type,
                object_id=self.id,
            ).delete()

        with transaction.atomic():
            Record.objects.create(content_object=self, user=user)
            self.read_count = F('read_count') + 1
            self.save()
            self.refresh_from_db()

        return True

    def read_canceled_by(self, user):
        content_type = ContentType.objects.get_for_model(self)

        with transaction.atomic():
            recordable_object = Record.objects.filter(
                user=user,
                content_type=content_type,
                object_id=self.id,
            )
            if recordable_object.count() > 0:
                recordable_object.delete()
                self.save()

        return True

    @classmethod
    def get_record_ids(cls, user):
        if not user.is_authenticated:
            return []
        content_type = ContentType.objects.get_for_model(cls)
        return list(Record.objects.filter(
            user=user,
            content_type=content_type,
        ).values_list('object_id', flat=True))
