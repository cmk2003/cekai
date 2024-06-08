import json
from django.core.paginator import Paginator
from django.http import JsonResponse

from test_runner import models
from test_runner.utils import parser


def config_view(request):
    # 新增
    if request.method == "POST":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            name = request_data["name"]
            base_url = request_data["base_url"]
            configdesc = request_data["configdesc"]
            project_id = request_data["project"]
        except:
            return JsonResponse({"success": False, "msg": "请求数据非法"})

        # 验证项目是否存在
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

        # 同一个项目中不同存在相同名称的配置
        try:
            models.Config.objects.filter(project=project_id).get(name=name)
            return JsonResponse({"success": False, "msg": "配置已存在"})
        except:
            pass

        config_data = parser.Format(request_data, level="config")
        config_data.parse()

        # 可创建配置
        models.Config.objects.create(name=name, base_url=base_url, configdesc=configdesc,
                                     project=models.Project.objects.get(pk=project_id), body=config_data.testcase,
                                     create_user=request.user.name)
        return JsonResponse({"success": True, "msg": "配置添加成功"})

    elif request.method == "GET":
        # 获取数据
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        page = request.GET.get("page", 1)
        per_page = 5  # 前端页面中也是明确每页5条数据

        # 获取当前项目的所有配置数据
        cons = models.Config.objects.filter(project=project_id).order_by("-update_time")
        if search != "":
            cons = cons.filter(name__contains=search)
        cons = cons.values()

        # 分页
        if (len(cons) <= per_page):
            page = 1
        pg = Paginator(cons, per_page)
        pageData = pg.page(page)

        data = {
            "success": True,
            "results": list(pageData),
            "count": len(list(cons))
        }
        return JsonResponse(data)
#批量删除
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                config = models.Config.objects.get(pk=vDict["id"])
                config.delete()
            except models.Config.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "配置删除成功"})


def config_pk_view(request, pk):
    # 拷贝
    if request.method == "POST":
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            config = models.Config.objects.get(pk=pk)
        except models.Config.DoesNotExist:
            return JsonResponse({"success": False, "msg": "配置不存在，或已被删除"})

        name = request_data.get("name")
        try:  # 验证新的名称是否可用
            models.Config.objects.filter(project=config.project.id).get(name=name)
            # 说明该项目由这个名字的配置，所以拷贝失败
            return JsonResponse({"success": False, "msg": "配置已存在"})
        except models.Config.DoesNotExist:
            config.id = None
            body = eval(config.body)
            body["name"] = name
            config.name = name
            config.body = body
            config.save()
            return JsonResponse({"success": True, "msg": "配置拷贝成功"})
    #修改
    elif request.method == "PATCH":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))

        # 判断配置是否存在
        try:
            config = models.Config.objects.get(pk=pk)
        except models.Config.DoesNotExist:
            return JsonResponse({"success": False, "msg": "配置不存在，或已被删除"})

        # 配置解析
        config_data = parser.Format(request_data, level="config")
        config_data.parse()

        # 修改的名称要看项目之前是否存在该配置
        if config.name != config_data.name:
            try:
                models.Config.objects.filter(project=config.project.id).get(name=config_data.name)
                # 有值表示不能修改，说明该项目已经存在该名称配置
                return JsonResponse({"success": False, "msg": "配置已存在"})
            except:
                pass

        # 修改测试用例步骤中的配置，需要在后面的实验中补充代码
        case_step = models.CaseStep.objects.filter(method="config", name=config.name)
        for case in case_step:
            case.name = config_data.name
            case.body = config_data.testcase
            case.save()


        # 自身对象改变
        config.name = config_data.name
        config.body = config_data.testcase
        config.base_url = config_data.base_url
        config.configdesc = request_data.get("configdesc")
        config.save()

        return JsonResponse({"success": True, "msg": "配置修改成功"})
    elif request.method == "DELETE":
        try:
            config = models.Config.objects.get(pk=pk)
            config.delete()
            return JsonResponse({"success": True, "msg": "配置删除成功"})
        except models.Config.DoesNotExist:
            return JsonResponse({"success": False, "msg": "配置不存在，或已被删除"})

    # 获取当前pk项目的所有配置数据
    elif request.method == "GET":
        configs = models.Config.objects.filter(project=pk).values()
        data = {
            "success": True,
            "results": list(configs)
        }
        return JsonResponse(data)
