from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from post.filters import CreatedDateFilter
from post.forms import MyPostAdminForm
from post.models import Category, Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    max_num = 2


class PostAdmin(admin.ModelAdmin):
    form = MyPostAdminForm
    list_per_page = 10
    list_display = ('id', 'title', 'member', 'is_deleted', 'created_at', )
    list_editable = ('is_deleted', )
    list_filter = (CreatedDateFilter, 'member__permission', 'category__name', 'is_deleted', )
    empty_value_display = '-'
    fieldsets = (
        ('기본 정보', {
            'fields': (('member', 'category', ), )
        }),
        ('제목 및 내용', {
            'fields': ('title', 'subtitle', 'content', )
        }),
        ('삭제', {
           'fields': ('is_deleted', 'deleted_at', )
        })
    )
    inlines = [
        CommentInline,
    ]

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        post_urls = [
            url(r'^status/$', self.admin_site.admin_view(self.post_status_view))
        ]
        return post_urls + urls

    def post_status_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            posts=Post.objects.all()
        )
        return TemplateResponse(request, "admin/post_status.html", context)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]


class CommentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Comment._meta.fields]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
