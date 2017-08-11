from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst


IGNORE_MODELS = (
    'auth',
    "sites",
    "sessions",
    "admin",
    "contenttypes",
)


def gnb_menus(request):
    menus = [
        {
            'name': '홈', 'url': '/admin/',
        },
        {
            'name': '회원',
            'sub_menus': [
                {'name': '관리자', 'url': '/admin/member/member/?permission__exact=AD'},
                {'name': '에디터', 'url': '/admin/member/member/?permission__exact=ET'},
                {'name': '일반', 'url': '/admin/member/member/?permission__exact=MB'},
            ]
        },
        {
            'name': ' 글 ',
            'sub_menus': [
                {'name': 'IT', 'url': '/admin/post/post/?category__name=IT'},
                {'name': 'GENDER', 'url': '/admin/post/post/?category__name=GENDER'},
                {'name': 'SOCIAL', 'url': '/admin/post/post/?category__name=SOCIAL'},
                {'name': 'POLITICS', 'url': '/admin/post/post/?category__name=POLITICS'},
                {'name': '통계', 'url': '/admin/post/post/status/'},
            ]
        },
        {
            'name': '댓글', 'url': '/admin/post/comment/'
        },
    ]
    return {'gnb_menus': menus}


def gnb_apps(request):
    user = request.user
    apps = []
    app_dict = {}
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label

        if app_label in IGNORE_MODELS:
            continue

        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            if True in perms.values():
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
                    'perms': perms,
                }
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'app_label': app_label,
                        'name': app_label.title(),
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

    for key in sorted(app_dict.keys()):
        apps.append(app_dict[key])

    return {'gnb_apps': apps}
