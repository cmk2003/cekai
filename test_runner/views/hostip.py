import json
from django.core.paginator import Paginator
from django.http import JsonResponse

from test_runner import models


def hostip_view(request):
    if request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        project_id = request_data.get("project")
        name = request_data.get("name")
        value = request_data.get("value")

        # 判断项目是否存在
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist as e:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

        # 验证环境名称是否可用(同一个项目不允许有相同名称的环境，不同项目之间是可以有相同名称环境)
        try:
            models.HostIP.objects.filter(project=project_id).get(name=name)
            # 说明已经给该项目创建过这个环境
            return JsonResponse({"success": False, "msg": "环境已存在"})
        except models.HostIP.DoesNotExist as e:
            # 该变量可以创建
            models.HostIP.objects.create(name=name, value=value, project=project, create_user=request.user.name)
            return JsonResponse({"success": True, "msg": "环境添加成功"})

    #分页查看
    elif request.method == "GET":
        project_id = request.GET.get("project")
        hosts = models.HostIP.objects.all().filter(project=project_id).order_by("-update_time").values()
        page = request.GET.get("page", 1)
        per_page = 5  # 前端页面中也是明确每页5条数据

        # 假设有6条数据，用户1删除一条后，用户2点击分页器第二页出现BUG的问题
        if (len(hosts) <= per_page):
            page = 1

        pg = Paginator(hosts, per_page)
        pageData = pg.page(page)

        data = {
            "success": True,
            "results": list(pageData),
            "count": len(list(hosts))
        }
        return JsonResponse(data)


def hostip_pk_view(request, pk):
    if request.method == "PATCH":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        value = request_data.get("value")

        try:
            hostip = models.HostIP.objects.get(pk=pk)
            # 在当前项目的所有变量中判断新的名字是否冲突
            if name != hostip.name:
                try:
                    models.HostIP.objects.filter(project=hostip.project.id).get(name=name)
                    # 已被占用
                    return JsonResponse({"success": False, "msg": "环境已存在"})
                except models.HostIP.DoesNotExist as e:
                    hostip.name = name
                    hostip.value = value
                    hostip.save()
                    return JsonResponse({"success": True, "msg": "环境修改成功"})
            else:
                hostip.value = value
                hostip.save()
                return JsonResponse({"success": True, "msg": "环境修改成功"})
        except models.HostIP.DoesNotExist:
            # 环境被删除
            return JsonResponse({"success": False, "msg": "环境不存在，或已被删除"})

    elif request.method == "DELETE":
        try:
            hostip = models.HostIP.objects.get(pk=pk)
            hostip.delete()
            return JsonResponse({"success": True, "msg": "环境删除成功"})
        except models.HostIP.DoesNotExist:
            return JsonResponse({"success": False, "msg": "环境不存在，或已被删除"})
    # 获取当前pk项目的所有环境数据
    elif request.method == "GET":
        hosts = models.HostIP.objects.filter(project=pk).values()
        data = {
            "success": True,
            "results": list(hosts)
        }
        return JsonResponse(data)