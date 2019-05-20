from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status, permissions
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ViewSet

from .models import User
from .service import UserService
from .serializer import UserSerializer, LoginSerializer
from .form import SignupForm

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        data = UserSerializer(request.user).data
        data.update({'is_authenticated': request.user.is_authenticated})
        return Response(data)

    @list_route(methods=['POST'])
    def login(self, request):
        '''
        handle user's login when POST to /api/accounts/login/
        '''
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        remember = serializer.validated_data['remember']
        if not UserService.check_user_exists(username):
            return Response({u'detail': u'您输入的账号不存在，请重新输入', u'field': u'username'}, status=status.HTTP_401_UNAUTHORIZED)

        user = UserService.find_by_username(username)
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is None:
            return Response({u'detail': u'您的密码有误，请重新输入', u'field': 'password'}, status.HTTP_401_UNAUTHORIZED)

        if not authenticated_user.is_active:
            return Response({u'detail': u"账号%s被冻结" % username, u'field': 'username'}, status=status.HTTP_403_FORBIDDEN)

        django_login(request, authenticated_user)
        if remember:
            request.session.set_expiry(60 * 60 * 24 * 60)
        else:
            request.session.set_expiry(0)

        return Response(UserSerializer(request.user).data)

    @list_route(methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        '''
        handle user's logout when POST to /api/accounts/logout/
        '''
        django_logout(request)
        return Response(status=status.HTTP_200_OK)

    def create(self, request):
        '''
        handle user's register when POST to /api/accounts/
        '''
        form = SignupForm(request.data)
        if not form.is_valid():
            errors = form.errors.as_data()

            if 'username' in errors:
                return Response(
                    {u'detail': errors['username'][0].message, u'field': 'username'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if 'confirm_password' in errors:
                return Response(
                    {u'detail': errors['confirm_password'][0].message}, 
                    status.HTTP_400_BAD_REQUEST
                )
        username = form.cleaned_data['username']
        user, created = UserService.get_or_create(username)
        if created:
            user.last_login = timezone.now()
        else:
            return Response(
                    {u'detail': '账号已存在，请检查！'}, 
                    status.HTTP_400_BAD_REQUEST
                )

        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        django_login(request, new_user)

        return Response({u'message': u'注册成功'}, status=status.HTTP_201_CREATED)
    
    @list_route(methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def nickname(self, request):
        user = request.user
        nickname = request.data.get('nickname')

        if not nickname or len(nickname) <= 3:
            return Response({u'message': u'昵称过短，请重新输入！'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.nickname = nickname
        user.save()

        return Response({u'message': u'修改成功'}, status=status.HTTP_200_OK)