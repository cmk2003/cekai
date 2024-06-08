import json
import math
from django.core.paginator import Paginator
from django.http import JsonResponse

from cekai import settings
from test_runner import models

#实验手册7.3
def database_view(request):
    if request.method == "POST":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        project_id = request_data.get("project")
        name = request_data.get("name")

        # 验证项目是否存在
        try:
            project = models.Project.objects.get(id=project_id)
        except:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

        # 一个项目的数据库名称不能重复
        if models.DataBaseConfig.objects.filter(name=name, project=project).first():
            return JsonResponse({"code": "200", "success": False, "msg": "数据库配置已存在"})

        # 创建数据库
        try:
            if request_data.get("id") == "":
                del request_data["id"]
            request_data["project"] = project
            models.DataBaseConfig.objects.create(**request_data)
            DATABASECONFIG_ADD_SUCCESS = {
                "code": "200",
                "success": True,
                "msg": "数据库配置新增成功",
                "name": name
            }
            return JsonResponse(DATABASECONFIG_ADD_SUCCESS)
        except Exception as e:
            return JsonResponse({"success": False, "msg": str(e)})

#实验手册7.4
def database_pk_view(request, pk):
    if request.method == "GET":
        # 获取当前项目的所有数据库配置数据
        databases = models.DataBaseConfig.objects.filter(project__id=pk).order_by('-update_time').values()

        # 分页，默认展示第一页数据，每页5条
        page = 1
        per_page = 5
        pg = Paginator(databases, per_page)
        pageData = pg.page(page)

        # 设置下一页与上一页路由
        if len(databases) > per_page:
            next_url = "http://%s:%d/api/testrunner/database_paginator/%d/2/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, int(pk), per_page)
        else:
            next_url = None

        data = {
            "success": True,
            "results": list(pageData),
            "previous": None,
            "next": next_url
        }
        return JsonResponse(data)
    elif request.method == "PUT":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        project_id = request_data.get("project")

        # 判断数据库配置是否存在
        try:
            database = models.DataBaseConfig.objects.get(id=pk)
        except models.DataBaseConfig.DoesNotExist:
            return JsonResponse({"success": False, "msg": "数据库配置不存在，或已被删除"})

        # 新的名字不能重复
        if models.DataBaseConfig.objects.exclude(id=pk).filter(name=name, project__id=project_id).first():
            return JsonResponse({"success": False, "msg": "数据库配置已存在"})

        # 修改
        database.name = request_data.get("name")
        database.type = request_data.get("type")
        database.server = request_data.get("server")
        database.account = request_data.get("account")
        database.password = request_data.get("password")
        database.desc = request_data.get("desc")
        database.save()

        return JsonResponse({"success": True, "msg": "数据库配置修改成功"})
    elif request.method == "DELETE":
        try:
            database = models.DataBaseConfig.objects.get(pk=pk)
            database.delete()
            return JsonResponse({"success": True, "msg": "数据库配置删除成功"})
        except models.DataBaseConfig.DoesNotExist:
            return JsonResponse({"success": False, "msg": "数据库配置不存在，或已被删除"})

#实验手册7.5
def database_paginator(request, project_id, page, per_page):
    if request.method == "GET":
        page = int(page)
        per_page = int(per_page)
        project_id = int(project_id)

        databases = models.DataBaseConfig.objects.filter(project__id=project_id).order_by('-update_time').values()

        pg = Paginator(databases, per_page)
        pageData = pg.page(page)

        if page == 1:
            previous_url = None
            next_url = "http://%s:%d/api/testrunner/database_paginator/%d/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, project_id, page + 1, per_page)
        elif page == math.ceil(len(databases) / per_page):
            previous_url = "http://%s:%d/api/testrunner/database_paginator/%d/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, project_id, page - 1, per_page)
            next_url = None
        else:
            previous_url = "http://%s:%d/api/testrunner/database_paginator/%d/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, project_id, page - 1, per_page)
            next_url = "http://%s:%d/api/testrunner/database_paginator/%d/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, project_id, page + 1, per_page)

        data = {
            "success": True,
            "results": list(pageData),
            "previous": previous_url,
            "next": next_url
        }
        return JsonResponse(data)