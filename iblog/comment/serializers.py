from rest_framework import serializers, pagination

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = [
            'id', 'nickname',
            'website', 'email', 'content',
            'status', 'created_time', 'target'
        ]
        read_only_fields = ['status', 'created_time']

