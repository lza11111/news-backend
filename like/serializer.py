from rest_framework import serializers
from like.models import Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = (
            'content_type',
            'object_id',
            'created_at',
        )
