from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(
        widget=forms.Textarea,
        label='摘要',
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='分类',
        required=True
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='标签',
        required=False
    )
    content_ck = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label='正文',
        required=False
    )
    content_md = forms.CharField(
        widget=forms.Textarea(),
        label='正文',
        required=False
    )
    content = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc',
            'title', 'is_md', 'content',
            'content_md', 'content_ck', 'status',
        )

    def __init__(self, *args ,**kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content
            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '内容不能为空')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'js/post_editor.js',
        )
