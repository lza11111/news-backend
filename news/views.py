import random

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import detail_route, list_route
from .models import News
from .serializer import NewsSerializer, SampleNewsSerializer


# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsSerializer
        
        return SampleNewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        user = self.request.user
        type = self.request.query_params.get('type', '')

        if type == 'hot':
            queryset = queryset.order_by('-like_count')

        elif type == 'rcmd':
            if not user.is_authenticated or user.tags.count() == 0:
                queryset = queryset.order_by('-like_count')
            else:
                queryset = queryset.filter(tags__in=user.tags.all())
        elif type:
            queryset = queryset.filter(tags__unique_name=type)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_authenticated:
            obj.liked = False
        else: 
            obj.liked = obj.has_liked_by(request.user)
            obj.read_by(request.user)

        related_news = News.objects.filter(tags__in=obj.tags.all())

        obj.related_news = random.sample(list(related_news), min(related_news.count(), 3))

        return Response(self.get_serializer(obj).data)
    
    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        news = self.get_object()
        user = request.user
        cancel = request.data.get('cancel')
        if cancel == 'true' or cancel is True:
            news.like_canceled_by(request.user)
            user.tags.remove(*news.tags.values_list('id', flat=True))
        else:
            news.liked_by(request.user)
            user.tags.add(*news.tags.values_list('id', flat=True))

            
        return Response({'success': True})
    
    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated], url_path='delete-read')
    def delete_read(self, request, pk=None):
        news = self.get_object()        
        news.read_canceled_by(request.user)
 
        return Response({'success': True})

    @list_route(methods=['GET'], permission_classes=[IsAuthenticated], url_path='like-list')
    def like_list(self, request):
        liked_news_list = News.get_like_id_set(request.user)
        queryset = News.objects.all().filter(id__in=liked_news_list)

        return Response(self.get_serializer(queryset, many=True).data)
    
    @list_route(methods=['GET'], permission_classes=[IsAuthenticated], url_path='recent-read')
    def recent_read(self, request):
        recent_read_list = News.get_record_ids(request.user)
        results = []
        for record in recent_read_list:
            results.append(News.objects.get(id=record))

        return Response(self.get_serializer(results, many=True).data)


