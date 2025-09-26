from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from iblog.custom_site import custom_site
from django.contrib.admin.models import LogEntry
from iblog.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'post_count','created_time')
    fields = ('name', 'status', 'is_nav')
    search_fields = ['name']

    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    search_fields = ['name']


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = [
        'title', 'category', 'status',
        'get_tags', 'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category_name', 'tag_name']
    autocomplete_fields = ['category', 'tag']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'is_md',
                'content_ck',
                'content_md',
                'content',
            ),
        }),
        ('额外信息', {
            'fields': ('tag', ),
        })
    )

    form = PostAdminForm

    def get_tags(self, obj):
        return ", ".join([tags.name for tags in obj.tag.all()[:3]])  # 显示前3个标签
    get_tags.short_description = '标签'  # 设置列标题
    get_tags.allow_tags = True

    def operator(selfself, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    class Media:
        css = {
            'all': ("css/bootstrap.css",),
        }
        js = ('js/bootstrap.bundle.min.js',)



@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_repr', 'object_id', 'action_flag',
        'user', 'change_message',
    ]