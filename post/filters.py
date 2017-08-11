import datetime
from django.contrib import admin

from post.models import Post


class CreatedDateFilter(admin.SimpleListFilter):
    title = '작성일'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        result = []
        for i in range(-3, 6):
            date = datetime.date.today() + datetime.timedelta(days=i)
            display_str = '{0} [{1}개]'.format(
                date, Post.objects.filter(created_at__date=date).count()
            )
            display_str += ' - 오늘' if i == 0 else ''
            result.append((date, display_str))
        return result

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_at__date=self.value())
        else:
            return queryset.all()
