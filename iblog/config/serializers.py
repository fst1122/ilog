from rest_framework import serializers, pagination

from .models import Link, SideBar


class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )
    class Meta:
        model = Link
        fields = (
            'id', 'title', 'href',
            'owner', 'created_time',
        )

class SideBarSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )
    class Meta:
        model = SideBar
        fields = (
            'id', 'title', 'display_type',
            'owner', 'created_time',
        )