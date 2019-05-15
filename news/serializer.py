from rest_framework import serializers

from .models import News

from tags.serializer import TagSerializer

class SampleNewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    liked = serializers.BooleanField(required=False)
    
    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'created_at',
            'like_count',
            'read_count',
            'liked',
            'tags',
            'cover_image',
        )

class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    liked = serializers.BooleanField(required=False)
    related_news = SampleNewsSerializer(many=True)

    class Meta:
        model = News
        fields = '__all__'
