from django.http import JsonResponse

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from test_user import models


def permission(request):
    if request.method == "GET":
        if request.user.is_superuser:#如果是超级管理员则有所有权限
            permission_list = Permission.objects.all().values_list('codename')
        else:# 普通用户获取权限
            try:
                # 获取前段数据
                app_label = request.GET["app_label"]
                model = request.GET["model"]
                print(app_label, model)
                content_type_id = ContentType.objects.filter(app_label=app_label, model=model).first()
                # 从用户的角色组里找到对应的权限，拿到页面对应的权限
                user = models.User.objects.get(id=request.user.id)
                permission_list = user.groups.values().filter(permissions__content_type_id=content_type_id.id).values_list("permissions__codename")
            except:
                return JsonResponse({"msg": "权限获取失败，请检查参数是否正确", "permissions": []})
        permission_list = [i[0].split("_")[0] for i in permission_list]
        return JsonResponse({"msg": "获取成功", "permissions": permission_list})