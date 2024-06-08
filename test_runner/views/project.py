import json
import math
from django.core.paginator import Paginator
from django.http import JsonResponse
from jsonpath import jsonpath

from cekai import settings
from cekai.auth import login_auth
from test_runner import models
from test_user.models import User

from django_celery_beat import models as celery_models

def project_view(request):
    # 新增项目
    if request.method == "POST":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        desc = request_data.get("desc")
        responsible = request_data.get("responsible")

        # 验证项目是否存在
        try:
            project = models.Project.objects.get(name=name)
            # 项目已存在
            return JsonResponse({"success": False, "msg": "项目已存在"})
        except models.Project.DoesNotExist:
            pro = models.Project.objects.create(name=name, desc=desc, responsible=responsible)

            # 自动生成默认的debugtalk.py
            models.Debugtalk.objects.create(project=pro)

            # 创建一个API的树结构
            models.Relation.objects.create(project=pro)
            # 创建一个测试用例的树结构
            models.Relation.objects.create(project=pro, type=2)

            # 需要对项目进行一系列的初始化操作，需要在后面的实验中补全代码

            return JsonResponse({"success": True, "msg": "项目添加成功"})

# 查看项目
    elif request.method == "GET":
        # 权限判断
        if request.user.is_superuser:#如果是超级管理员会返回所有项目
            projects = models.Project.objects.all().order_by('-create_time').values()
        else:
            # 该用户有权限的项目
            projects_id_list = User.objects.filter(id=request.user.id).values_list('belong_project', flat=True)
            # 该用户创建的项目
            create_projects_id_list = models.Project.objects.filter(responsible=request.user.name).values_list("id", flat=True)
            # 获取该用户可以访问的所有项目对象
            projects = models.Project.objects.filter(id__in=[_ for _ in projects_id_list] + [_ for _ in create_projects_id_list]).order_by('-create_time').values()

        # 分页，默认展示第一页，每页5条数据
        page = 1
        per_page = 5
        pg = Paginator(projects, per_page)
        pageData = pg.page(page)
        # 设置下一页按钮对应的请求URL
        if len(projects) > per_page:
            next_url = "http://%s:%d/api/testrunner/project_paginator/2/%d/" % (settings.SERVICE_IP, settings.SERVICE_PORT, per_page)
        else:
            next_url = None

        data = {
            "success": True,
            "results": list(pageData),   # 页面展示项目数量
            "results2": list(projects),  # 为了在修改用户时可以展示所有项目
            "previous": None,
            "next": next_url
        }
        return JsonResponse(data)

# 修改项目信息
    elif request.method == "PATCH":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        id = request_data["id"]
        name = request_data["name"]
        desc = request_data["desc"]

        try:
            # 判断项目是否存在
            pro = models.Project.objects.get(pk=id)
            if name != pro.name:
                try:
                    # 名字发生改变，需要看一看新的名字是否可用
                    models.Project.objects.get(name=name)
                    # 项目已经存在
                    return JsonResponse({"success": False, "msg": "项目已存在"})
                except models.Project.DoesNotExist:
                    # 可替换
                    pro.name = name
                    pro.desc = desc
                    pro.save()
                    return JsonResponse({"success": True, "msg": "项目修改成功"})
            else:
                pro.desc = desc
                pro.save()
                return JsonResponse({"success": True, "msg": "项目修改成功"})
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

# 删除某个项目
    elif request.method == "DELETE":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        id = request_data["id"]

        try:
            # 确认项目是否存在，存在即删除
            pro = models.Project.objects.get(pk=id)

            # 后面需实现的功能：判断是否有正在运行的测试用例，如果有则不删除项目
            # 后面需实现的功能：找到项目的测试用例，并删除测试用例，默认会删除该用例对应的用例执行步骤
            models.Case.objects.filter(project=pro.id).delete()

            # 项目其他相关内容会随着项目的删除而删除
            pro.delete()

            return JsonResponse({"success": True, "msg": "项目删除成功"})
        except models.Project.DoesNotExist:
            # 项目不存在，提示信息并刷新数据
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})



def project_paginator_view(request, page, per_page):
    if request.method == "GET":
        page = int(page)
        per_page = int(per_page)

        # 权限判断
        if request.user.is_superuser:
            projects = models.Project.objects.all().order_by('-create_time').values()
        else:
            # 该用户有权限的项目
            projects_id_list = User.objects.filter(id=request.user.id).values_list('belong_project', flat=True)
            # 该用户创建的项目
            create_projects_id_list = models.Project.objects.filter(responsible=request.user.name).values_list("id", flat=True)
            # 获取该用户可以访问的所享有项目对象
            projects = models.Project.objects.filter(id__in=[_ for _ in projects_id_list] + [_ for _ in create_projects_id_list]).order_by('-create_time').values()

        # 分页数据
        pg = Paginator(projects, per_page)
        pageData = pg.page(page)

        # 制作上下页按钮对应路由
        if page == 1:
            previous_url = None
            next_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (settings.SERVICE_IP, settings.SERVICE_PORT, page+1, per_page)
        elif page == math.ceil(len(projects) / per_page):
            previous_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (settings.SERVICE_IP, settings.SERVICE_PORT, page-1, per_page)
            next_url = None
        else:
            previous_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (settings.SERVICE_IP, settings.SERVICE_PORT, page-1, per_page)
            next_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (settings.SERVICE_IP, settings.SERVICE_PORT, page+1, per_page)

        data = {
            "success": True,
            "results": list(pageData),
            "previous": previous_url,
            "next": next_url
        }
        return JsonResponse(data)

#实验手册6.2
def getallprojectmessage(request):
    if request.method == "GET":
        try:
            # 获取所有项目
            projects = models.Project.objects.all().values('id', 'name')
        except:
            return JsonResponse({"code": 400, "data": [], "success": False, "msg": "数据获取失败！"})

        # 用于存放每个项目的基础数据
        data = []

        # 循环处理每一个项目，获取项目统计数据
        for project in projects:
            # 项目的基本信息
            projectdetail = {
                "api_count": 10,  # api的数量，目前为假数据
                "case_count": 10,  # 测试用例的数量，目前为假数据
                "config_count": 10,  # 配置的数量，目前为假数据
                "variables_count": 10,  # 全局变量的数量，目前为假数据
                "host_count": 10,  # 环境的数量，目前为假数据
                "task_count": 10,  # 任务的数量，目前为假数据
                "report_count": 10,  # 测试报告的数量，目前为假数据
                "uitestplan": 0,
            }

            # 测试用例相关数据，目前为假数据
            urllist = []

            # 任务相关数据，目前为假数据
            plancase = []

            PlanCase_Count = len(set(plancase))
            Cove_Count = len(set(urllist))

            projectdetail['pr_id'] = project['id']
            projectdetail['pr_name'] = project['name']
            projectdetail['Cove_Count'] = Cove_Count
            projectdetail['PlanCase_Count'] = PlanCase_Count
            projectdetail["Case_Coveage"] = round((Cove_Count / projectdetail['api_count']) * 100,
                                                  2) if Cove_Count != 0 else 0
            projectdetail["Plan_Coveage"] = round((PlanCase_Count / projectdetail['case_count']) * 100,
                                                  2) if PlanCase_Count != 0 else 0
            data.append(projectdetail)

        return JsonResponse(
            {"code": 200, "data": sorted(data, key=lambda i: i['Plan_Coveage'], reverse=True), "success": True,
             "msg": "数据获取成功！"})

#实验手册6.3
@login_auth
def project_detail(request, pk):
    if request.method == "GET":
        try:
            project = models.Project.objects.get(pk=pk)

            vars_count = models.Variable.objects.filter(project=project.id).count()
            config_count = models.Config.objects.filter(project=project.id).count()
            hostip_count = models.HostIP.objects.filter(project=project.id).count()
            api_count = models.Api.objects.filter(project=project.id).count()
            case_count = models.Case.objects.filter(project=project.id).count()
            report_count = models.Report.objects.filter(project=project.id).count()
            task_count = celery_models.PeriodicTask.objects.filter(description=project.id).count()

            # 获取项目详细信息，目前使用假数据，在后面的实验中进行替换为真数据
            data = {
                "success": True,       # 请求是否成功
                "name": project.name,  # 项目名称
                "desc": project.desc,  # 项目描述
                "api_count": api_count,        # api的数量
                "case_count": case_count,       # 测试用例的数量
                "config_count": config_count,     # 配置的数量
                "variables_count": vars_count,  # 全局变量的数量
                "host_count": hostip_count,       # 环境的数量
                "task_count": task_count,       # 任务的数量
                "report_count": report_count,     # 测试报告的数量
                "uitestplan": 0,
            }

            return JsonResponse(data)
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

#实验手册6.4
def gettagcount(request):
    if request.method == "GET":
        project_id = request.GET.get("project")

        # 待补充业务逻辑，找到这个项目的所有测试用例，看每种类型用例各有多少个
        typename = ["冒烟", "集成", "监控", "回归", "系统", "空库"]
        countlist = [3, 4, 7, 5, 4, 6]

        data = {
            "typename": typename,
            "countlist": countlist
        }
        return JsonResponse(data)

#实验手册6.5
def getreporttail(request):
    if request.method == "GET":
        # 待补充业务逻辑，找到这个项目的所有测试用例，看运行情况的数量

        data = {
            "code": 200,
            "msg": "success",
            "successes": 10,  # 成功的用例数量，此时为假数据
            "failure": 3,  # 失败的用例数量，此时为假数据
            "error": 2,  # 异常的用例数量，此时为假数据
            "skippe": 1,  # 跳过的用例数量，此时为假数据
        }
        return JsonResponse(data)

def getallprojectmessage(request):
    if request.method == "GET":
        try:
            # 获取所有项目
            projects = models.Project.objects.all().values('id', 'name')
        except:
            return JsonResponse({"code": 400, "data": [], "success": False, "msg": "数据获取失败！"})

        # 用于存放每个项目的基础数据
        data = []

        # 循环处理每一个项目，获取项目统计数据
        for project in projects:
            vars_count = models.Variable.objects.filter(project=project.get("id")).count()
            config_count = models.Config.objects.filter(project=project.get("id")).count()
            hostip_count = models.HostIP.objects.filter(project=project.get("id")).count()
            api_count = models.Api.objects.filter(project=project.get("id")).count()
            case_count = models.Case.objects.filter(project=project.get("id")).count()
            report_count = models.Report.objects.filter(project=project.get("id")).count()
            task_count = celery_models.PeriodicTask.objects.filter(description=project.get("id")).count()

            # 项目的基本信息
            projectdetail = {
                "api_count": api_count,
                "case_count": case_count,
                "config_count": config_count,
                "variables_count": vars_count,
                "host_count": hostip_count,
                "task_count": task_count,
                "report_count": report_count,
                "uitestplan": 0,
            }

            # 测试用例相关数据，目前为假数据
            urllist = []

            # 任务相关数据，目前为假数据
            plancase = []

            PlanCase_Count = len(set(plancase))
            Cove_Count = len(set(urllist))

            projectdetail['pr_id'] = project['id']
            projectdetail['pr_name'] = project['name']
            projectdetail['Cove_Count'] = Cove_Count
            projectdetail['PlanCase_Count'] = PlanCase_Count
            projectdetail["Case_Coveage"] = round((Cove_Count / projectdetail['api_count']) * 100,2) if Cove_Count != 0 else 0
            projectdetail["Plan_Coveage"] = round((PlanCase_Count / projectdetail['case_count']) * 100,2) if PlanCase_Count != 0 else 0
            data.append(projectdetail)

        return JsonResponse({"code": 200, "data": sorted(data, key=lambda i: i['Plan_Coveage'], reverse=True), "success": True,"msg": "数据获取成功！"})


def getreporttail(request):
    if request.method == "GET":
        # 获取所有的运行结果
        summarys = models.Report.objects.filter(project__id=request.GET["project"]).values("summary")

        successes_num = 0
        failure_num = 0
        error_num = 0
        skippe_num = 0

        # 分析结果
        if summarys:
            global false, null, true
            false = null = true = ''
            statlist = []
            for summary in summarys:
                statlist.append(eval(summary['summary'])['stat'])

            successes_num = sum(jsonpath(statlist, "$..successes"))
            failure_num = sum(jsonpath(statlist, "$..failures"))
            error_num = sum(jsonpath(statlist, "$..errors"))
            skippe_num = sum(jsonpath(statlist, "$..skipped"))

        data = {
            "code": 200,
            "msg": "success",
            "successes": successes_num,
            "failure": failure_num,
            "error": error_num,
            "skippe": skippe_num,
        }
        return JsonResponse(data)
