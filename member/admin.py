import datetime

from django.contrib import admin, messages
from member.models import Member
from member.forms import SetCertificationDateForm
from post.models import Post


class MemberAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('id', 'email', 'username', 'permission', 'is_certificated', 'certification_date', 'post_count', )
    list_editable = ('permission', )
    list_filter = ('permission', )
    search_fields = ('username', )
    ordering = ('-id', 'email', 'permission', )
    actions = ['set_certification_date']
    action_form = SetCertificationDateForm

    def post_count(self, obj):
        return Post.objects.filter(member=obj).count()

    def set_certification_date(self, request, queryset):
        year = request.POST.get('certification_date_year')
        month = request.POST.get('certification_date_month')
        day = request.POST.get('certification_date_day')

        if year and month and day:
            date_str = '{0}-{1}-{2}'.format(year, month, day)
            date = datetime.datetime.strptime(date_str, "%Y-%d-%m").date()

            for member in queryset:
                Member.objects.filter(id=member.id).update(is_certificated=True, certification_date=date)

            messages.success(request, '{0}명의 회원을 인증했습니다.'.format(len(queryset)))
        else:
            messages.error(request, '날짜가 선택되지 않았습니다.')

    post_count.short_description = '작성한 글 수'
    set_certification_date.short_description = '선택된 유저를 해당 날짜 기준으로 인증합니다.'


admin.site.register(Member, MemberAdmin)
