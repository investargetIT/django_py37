# 用户全部信息
from rest_framework import serializers

from user.models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser',  'createdtime', 'lastmodifytime', 'datasource')


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser',  'createdtime', 'lastmodifytime', 'datasource')