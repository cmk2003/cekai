import copy
import json
import os
import shutil

from django.core.paginator import Paginator
from django.http import JsonResponse
from httprunner import HttpRunner

from cekai.settings import BASE_DIR
from test_runner import models
from test_runner.utils import prepare, loader
from test_runner.utils.loader import load_debugtalk, parse_tests, parse_summary
from test_runner.utils.parser import parse_host


def case_view(request):
    # 新增
    if request.method == "POST":
        # 获取客户端数据
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            project_id = request_data["project"]
            name = request_data["name"]
            relation = request_data["relation"]
            body = request_data["body"]
            length = request_data["length"]
            tag = request_data["tag"]
        except KeyError:
            return JsonResponse({"code": "0100", "success": False, "msg": "请求数据非法"})

        # 确保项目存在
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

        # 一个项目的同一个树目录下用例名称不能重复
        if models.Case.objects.filter(name=name, project__id=project_id, relation=relation).filter():
            return JsonResponse({"success": False, "msg": "测试用例已存在"})

        # 创建测试用例
        tag_options = {
            "冒烟用例": 1,
            "集成用例": 2,
            "监控脚本": 3,
            "回归用例": 4,
            "系统用例": 5,
            "空库用例": 6
        }
        case = models.Case.objects.create(name=name,
                                          project=project,
                                          relation=relation,
                                          length=length,
                                          tag=tag_options.get(tag),
                                          create_user=request.user.name)

        # 创建测试用例步骤，一个API对应一个步骤
        prepare.generate_casestep(body, case, project_id)

        return JsonResponse({"success": True, "msg": "测试用例添加成功"})

# 分页查看
    elif request.method == "GET":
        # 获取客户端数据
        node = request.GET.get("node")
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        tag = request.GET.get("tag")
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 5)

        # 获取当前项目的所有测试用例数据
        cases = models.Case.objects.filter(project__id=project_id).order_by("-update_time")
        # 根据节点过滤
        if node != "":
            relation = models.Relation.objects.get(project__id=project_id, type=2)
            tree = eval(relation.tree)
            nodes = prepare.findtreenodes(tree, node)
            cases = cases.filter(relation__in=nodes)
        # 根据类型过滤
        if tag != "":
            cases = cases.filter(tag__contains=tag)
        # 根据条件过滤
        if search:
            cases = cases.filter(name__contains=search)
        cases = cases.values()

        # 数据分页
        if (len(cases) <= per_page):
            page = 1
        pg = Paginator(cases, per_page)
        pageData = pg.page(page)

        # 响应json数据
        data = {
            "count": len(cases),
            "results": list(pageData),
            "success": True
        }
        return JsonResponse(data, status=200)
    # 批量删除
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                case = models.Case.objects.get(pk=vDict["id"])
                case.delete()
            except models.Case.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "测试用例删除成功"})

def case_pk_view(request, pk):
    # 拷贝
    if request.method == "POST":
        # 获取客户端数据
        reqObj = json.loads(request.body.decode('utf-8'))
        name = reqObj.get("name")

        # 获取测试用例对象，主键id修改为None后再存储即为新增一个相同的数据
        case = models.Case.objects.get(id=pk)
        case.id = None
        case.name = name
        case.save()

        # 获取原测试用例的测试步骤
        case_step = models.CaseStep.objects.filter(case__id=pk)
        # 创建新的步骤赋值给新的测试用例
        for step in case_step:
            step.id = None
            step.case = case
            step.save()

        return JsonResponse({"success": True, "msg": "测试用例拷贝成功"})
# 修改
    elif request.method == "PATCH":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        project_id = int(request_data.get("project"))
        relation = request_data.get("relation")
        body = request_data.get("body")

        # 验证修改的名称是否可用
        if models.Case.objects.exclude(id=pk).filter(name=name, project__id=project_id, relation=relation).first():
            return JsonResponse({"success": False, "msg": "测试用例已存在"})

        # 修改测试用例
        case = models.Case.objects.get(id=pk)
        prepare.update_casestep(body, case, project_id)
        tag_options = {
            "冒烟用例": 1,
            "集成用例": 2,
            "监控脚本": 3,
            "回归用例": 4,
            "系统用例": 5,
            "空库用例": 6
        }
        request_data["tag"] = tag_options[request_data["tag"]]
        request_data.pop("body")
        models.Case.objects.filter(id=pk).update(**request_data)
        return JsonResponse({"success": True,  "msg": "测试用例修改成功"})
# 修改
    elif request.method == "PATCH":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        project_id = int(request_data.get("project"))
        relation = request_data.get("relation")
        body = request_data.get("body")

        # 验证修改的名称是否可用
        if models.Case.objects.exclude(id=pk).filter(name=name, project__id=project_id, relation=relation).first():
            return JsonResponse({"success": False, "msg": "测试用例已存在"})

        # 修改测试用例
        case = models.Case.objects.get(id=pk)
        prepare.update_casestep(body, case, project_id)
        tag_options = {
            "冒烟用例": 1,
            "集成用例": 2,
            "监控脚本": 3,
            "回归用例": 4,
            "系统用例": 5,
            "空库用例": 6
        }
        request_data["tag"] = tag_options[request_data["tag"]]
        request_data.pop("body")
        models.Case.objects.filter(id=pk).update(**request_data)
        return JsonResponse({"success": True,  "msg": "测试用例修改成功"})

def getstep(request, pk):
    # 获取某个测试用例的相关测试步骤
    if request.method == "GET":
        # 获取测试用例对象
        try:
            case = models.Case.objects.get(pk=pk)
        except models.Case.DoesNotExist:
            return JsonResponse({"success": False, "msg": "测试用例不存在或已被删除"})

        tag_options = {
            1: "冒烟用例",
            2: "集成用例",
            3: "监控脚本",
            4: "回归用例",
            5: "系统用例",
            6: "空库用例"
        }
        case_dict = {
            "id": case.id,
            "apicaseid": case.apicaseid,
            "name": case.name,
            "relation": case.relation,
            "length": case.length,
            "tag": tag_options[case.tag],
            "create_user": case.create_user,
            "project": case.project.id
        }
        steps = models.CaseStep.objects.filter(case__id=pk).order_by("step")
        data = {
            "success": True,
            "case": case_dict,
            "step": list(steps.values())
        }
        return JsonResponse(data)


def run_case(request, pk):
    # 运行一个测试用例
    if request.method == "GET":
        # 获取客户端数据
        project = request.GET.get("project")
        name = request.GET.get("name")
        host = request.GET.get("host")

        # 获取当前测试用例的所有测试步骤对象
        casestep_list = models.CaseStep.objects.filter(case__id=pk).order_by("step").values("body")

        case_list = []
        config = None

        # 是否使用环境
        if host != "请选择":
            host = models.HostIP.objects.get(name=host, project=project).value.splitlines()

        for casestep in casestep_list:
            body = eval(casestep['body'])
            if "base_url" in body["request"].keys():
                config = eval(models.Config.objects.get(name=body["name"], project__id=project).body)
                continue
            case_list.append(parse_host(host, body))

        summary = loader.debug_api(case_list, project, name=name, config=parse_host(host, config), save=True)
        return JsonResponse(summary)



def run_tree_case(request):
    # 运行某分组下所有测试用例
    if request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        project_id = request_data.get("project")
        relation = request_data.get("relation")
        back_async = request_data.get("async")
        report = request_data.get("name")
        host = request_data.get("host")

        # 验证是否使用环境
        if host != "请选择":
            host = models.HostIP.objects.get(name=host, project=project_id).value.splitlines()

        case_sets = []
        suite_list = []
        config_list = []

        # 循环处理每一个分组节点
        for relation_id in relation:
            # 获取当前项目relation_id分组下的所有测试用例
            suite = list(models.Case.objects.filter(project__id=project_id, relation=relation_id).order_by("id").values("id", "name"))

            # 循环处理每一个测试用例对象
            for case in suite:
                # 获取该测试用例的所有测试步骤
                casestep_list = models.CaseStep.objects.filter(case__id=case["id"]).order_by("step").values('body')
                case_list = []
                config = None
                # 处理每一个测试步骤
                for casestep in casestep_list:
                    body = eval(casestep['body'])
                    if "base_url" in body["request"].keys():
                        config = eval(models.Config.objects.get(name=body["name"], project__id=project_id).body)
                        continue
                    # 插入主体信息
                    case_list.append(parse_host(host, body))
                config_list.append(parse_host(host, config))
                # 插入每个测试用例的运行主体列表
                case_sets.append(case_list)
                suite_list = suite_list + suite
        if back_async:
            # 异步
            return JsonResponse({"success": True, "msg": "功能未实现"})
        else:
            # 同步
            summary = loader.debug_suite(case_sets, project_id, suite_list, config_list)
        return JsonResponse(summary)