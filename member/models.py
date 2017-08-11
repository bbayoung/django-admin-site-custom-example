from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Member(AbstractBaseUser):
    TYPE_PERMISSIONS = (
        ('AD', '관리자'),
        ('ET', '에디터'),
        ('MB', '일반'),
    )

    email = models.EmailField('이메일', max_length=255, unique=True)
    username = models.CharField('닉네임', max_length=30)
    permission = models.CharField('권한', max_length=2, choices=TYPE_PERMISSIONS, default='MB')
    certification_date = models.DateField('인증일', default=None, null=True, blank=True)
    is_certificated = models.BooleanField('인증여부', default=False)

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
