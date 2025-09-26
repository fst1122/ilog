"""
URL configuration for iblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import views as sitemap_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer, OpenAPIRenderer

from .custom_site import custom_site
from blog.views import (
    IndexView, CategoryView,
    TagView, PostDetailView,
    SearchView, AuthorView,
)
from config.views import LinkListView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.apis import PostViewSet, CategoryViewSet, TagViewSet
from comment.apis import CommentViewSet


router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')
router.register(r'tag', TagViewSet, basename='api-tag')
router.register(r'comment', CommentViewSet, basename='api-comment')

schema_view = get_schema_view(
    title="Blog API",
    description="Blog API documentation",
    version="1.0.0",
    renderer_classes=[JSONOpenAPIRenderer],
    public=True,
)

urlpatterns = [
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls, name='admin'),
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
    path('links/', LinkListView.as_view(), name='links'),
    path('search/', SearchView.as_view(), name='search'),
    path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('rss/', LatestPostFeed(), name='rss'),
    path('feed/', LatestPostFeed(), name='rss'),
    path('sitemap.xml', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include((router.urls, 'api'), namespace='api'), name='api'),
    path('api/docs/', schema_view, name='api-docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
