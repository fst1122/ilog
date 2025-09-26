from rest_framework import viewsets

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(status=Comment.STATUS_NORMAL)
    serializer_class = CommentSerializer

    def get_queryset(self):
        target = self.request.query_params.get('target', None)
        if target:
            return Comment.objects.filter(status=Comment.STATUS_NORMAL, target=target)
        return Comment.objects.filter(status=Comment.STATUS_NORMAL)


