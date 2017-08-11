from django.db import models
from member.models import Member


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField('카테고리 이름', max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    member = models.ForeignKey(Member, verbose_name='작성자')
    category = models.ForeignKey(Category, verbose_name='카테고리')
    title = models.CharField('제목', max_length=255)
    subtitle = models.CharField('부제목', max_length=255)
    content = models.TextField('내용')
    is_deleted = models.BooleanField('삭제된 글', default=False)
    deleted_at = models.DateTimeField('삭제일시', default=None, null=True)
    created_at = models.DateTimeField('작성일', auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    유저가 작성한 글에 대한 댓글입니다.
    댓글은 :model:`post.Post` 와 :model:`member.Member`. 모델과 관계가 있습니다.
    """
    member = models.ForeignKey(Member, verbose_name='작성자')
    post = models.ForeignKey(Post, verbose_name='원본글')
    content = models.TextField(verbose_name='내용', help_text='댓글 내용입니다.')
    report_count = models.IntegerField('신고수')
    created_at = models.DateTimeField('작성일', auto_now_add=True)

    def __str__(self):
        return self.content
