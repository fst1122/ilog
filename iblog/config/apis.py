from rest_framework import viewsets

from .models import Link, SideBar
from .serializers import LinkSerializer, SideBarSerializer


class LinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    serializer_class = LinkSerializer

class SideBarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SideBar.objects.filter(status=SideBar.STATUS_SHOW)
    serializer_class = SideBarSerializer