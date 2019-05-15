import datetime
import hashlib
import json

from django.core.cache import caches
from django.utils import timezone

from users.models import User
from utils.helper import int_to_utc

cache = caches['default']

username_TO_USER_ID_KEY = 'user:username:id:%s'
USER_ID_TO_OBJECT_KEY = 'user:id:obj:%s'
VERSION = 'v1.0'


class UserBundle(object):
    pass


class UserService(object):
    @classmethod
    def _get_user_bundle_by_key(cls, key):
        data = json.loads(cache.get(key))
        bundle = UserBundle()
        for key in data:
            if key == 'date_joined':
                setattr(bundle, key, int_to_utc(data[key]))
            else:
                setattr(bundle, key, data[key])
        return bundle

    @classmethod
    def _get_user_bundle_by_user_id(cls, user_id):
        key = USER_ID_TO_OBJECT_KEY % user_id
        if key not in cache:
            user = User.objects.get(id=user_id)

        bundle = cls._get_user_bundle_by_key(key)
        if bundle.version == VERSION:
            return bundle

        user = User.objects.get(id=user_id)
        return cls._get_user_bundle_by_key(key)

    @classmethod
    def _get_user_bundle_by_username(cls, username):
        key = username_TO_USER_ID_KEY % username
        if key not in cache:
            try:
                user = User.objects.get(username__iexact=username)
                return cls._get_user_bundle_by_user_id(user.id)
            except:
                # TODO: race condition
                cache.set(key, 0)
                return None
        user_id = int(cache.get(key))
        return cls._get_user_bundle_by_user_id(user_id) if user_id != 0 else None

    @classmethod
    def get_user_bundle(cls, user_id=None, username=None):
        if user_id is not None:
            return cls._get_user_bundle_by_user_id(user_id)
        if username is not None:
            return cls._get_user_bundle_by_username(username)
        return None

    @classmethod
    def get_user_bundle_by_username(cls, username):
        user_id = cls.get_user_id_by_username(username)
        return cls.get_user_bundle(user_id)

    @classmethod
    def short_url_to_username(cls, short_url):
        if not short_url:
            return ''

        if User.objects.filter(short_url=short_url).exists():
            return User.objects.get(short_url=short_url).username
        return ''


    @classmethod
    def check_user_exists(cls, username):
        return User.objects.filter(username__iexact=username).exists()

    @classmethod
    def find_by_username(cls, username):
        if not username:
            return None

        if not User.objects.filter(username__iexact=username).exists():
            return None

        return User.objects.get(username__iexact=username)

    @classmethod
    def get_or_create(cls, username):
        username = username.strip()
        if User.objects.filter(username__iexact=username).exists():
            return User.objects.get(username__iexact=username), False

        user = User.objects.create_user(username=username)
        return user, True

    @classmethod
    def create_user(cls, username, request):

        user, created = cls.get_or_create(username)
        if created:
            user.save()
        return user
