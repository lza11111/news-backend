# encoding: utf-8
from django.contrib.contenttypes.models import ContentType
from like.models import Like


class LikeService:

    @classmethod
    def get_object(cls, model, object_id):
        content_type = ContentType.objects.get(model=model)
        return content_type.model_class().objects.get(id=object_id)

    @classmethod
    def get_liked_id_set(cls, model, user):
        content_type = ContentType.objects.get(model=model)
        like_set = Like.objects.filter(content_type=content_type,
                                       user=user)
        return set(like.object_id for like in like_set)

    @classmethod
    def mark_liked_objects(cls, model, objects, user):
        if not user.is_authenticated():
            return objects
        liked_id_set = cls.get_liked_id_set(model=model, user=user)
        for obj in objects:
            obj.has_liked = obj.id in liked_id_set
        return objects

    @classmethod
    def get_is_liked(cls, obj, model, user):
        if not user:
            return False

        return int(obj.id) in model.get_cached_like_id_set(user)
