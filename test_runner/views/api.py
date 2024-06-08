import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse

from test_runner import models
from test_runner.utils import parser, prepare, loader
from test_runner.utils.parser import parse_host
from test_runner.utils.resource import ApiResource


def api_view(request):
    # 新增
    if request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))

        # 数据格式化
        api = parser.Format(request_data)
        api.parse()

        # 判断项目是否存在
        try:
            project = models.Project.objects.get(pk=api.project)
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目已被删除"})

        # 创建API接口对象
        try:
            models.Api.objects.create(name=api.name,
                                      body=api.testcase,
                                      url=api.url,
                                      method=api.method,
                                      project=project,
                                      relation=api.relation,
                                      create_user=request.user.name)

            return JsonResponse({"success":True, "msg": "API添加成功"}, status=201)
        except:
            return JsonResponse({"success": False, "msg": "数据信息太长"})

# 分页查看
    elif request.method == "GET":
        # 获取前端数据
        node = request.GET.get("node")
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        page = request.GET.get("page", 1)
        per_page =request.GET.get("per_page", 5)

        # 获取当前项目的所有API接口数据
        apis = models.Api.objects.filter(project__id=project_id).order_by("-update_time")
        if node:#获取某个节点下的API接口
            # apis = apis.filter(relation=node)
            relation = models.Relation.objects.get(project__id=project_id, type=1)
            tree = eval(relation.tree)
            nodes = prepare.findtreenodes(tree, node)
            apis = apis.filter(relation__in=nodes)
        if search:#根据查询条件过滤API接口
            apis = apis.filter(name__contains=search)
        apis = apis.values()

        # 数据分页
        if (len(apis) <= per_page):
            page = 1
        pg = Paginator(apis, per_page)
        pageData = pg.page(page)

        # 响应
        data = {
            "success": True,
            "count": len(apis),
            "results": list(pageData)
        }
        return JsonResponse(data, status=200)
    # 批量删除
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                api = models.Api.objects.get(pk=vDict["id"])
                api.delete()
            except models.Api.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "环境API成功"})

def api_pk_view(request, pk):
    # 拷贝
    if request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")

        try:
            api = models.Api.objects.get(id=pk)
        except models.Api.DoesNotExist:
            return JsonResponse({"success": False, "msg": "API不存在，或已被删除"})

        # 拷贝主体
        body = eval(api.body)
        body["name"] = name
        api.body = body
        api.name = name
        api.id = None
        # 保存一个新的API数据
        api.save()
        return JsonResponse({"success":True, "msg": "API拷贝成功"})
        # 获取单个API信息
    elif request.method == "GET":
        try:
            # 获取API对象
            api = models.Api.objects.get(id=pk)

            # 解析API对象
            parse = parser.Parse(eval(api.body))
            parse.parse_http()

            # 响应
            data = {
                "id": api.id,
                "body": parse.testcase,
                "success": True
            }
            return JsonResponse(data)
        except models.Api.DoesNotExist:
            return JsonResponse({"success": False, "msg": "API不存在，或已被删除"})
    # 修改
    elif request.method == "PATCH":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))

        # 格式化数据
        api_format = parser.Format(request_data)
        api_format.parse()

        # 修改
        try:
            api = models.Api.objects.get(id=pk)
            api.name = api_format.name
            api.body = api_format.testcase
            api.url = api_format.url
            api.method = api_format.method
            api.save()

            return JsonResponse({"success": True, "msg": "API修改成功"})
        except models.Api.DoesNotExist:
            return JsonResponse({"success": False, "msg": "API不存在，或已被删除"})
    elif request.method == "DELETE":
        try:
            api = models.Api.objects.get(pk=pk)
            api.delete()
            return JsonResponse({"success": True, "msg": "环境API成功"})
        except models.Api.DoesNotExist:
            return JsonResponse({"success": False, "msg": "API不存在，或已被删除"})

def exportApiExcel(request):
    # 导出
    if request.method == "POST":
        # 获取数据
        node = request.GET.get("node")
        project_id = request.GET.get("project")
        search = request.GET.get("search")

        # 获取该项目的所有api接口
        apis = models.Api.objects.filter(project__id=project_id).order_by("-update_time")
        # 根据条件过滤
        if search != "":
            apis = apis.filter(Q(url__contains=search) | Q(name__contains=search))
        # 根据节点过滤
        if node != "":
            relation = models.Relation.objects.get(project_id=project_id, type=1)
            tree = eval(relation.tree)
            nodes = prepare.findtreenodes(tree, node)
            apis = apis.filter(relation__in=nodes)

        # 获取项目名称
        project_name = models.Project.objects.get(id=project_id).name

        # api接口导出资源对象
        api_resource = ApiResource()
        # 合成导出数据
        dataset = api_resource.export(queryset=apis)

        # 创建响应对象并返回
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.xlsx"'.format(project_name, "API接口").encode("utf-8")
        return response

def runApi(request, pk):
    # 运行一个API接口
    if request.method == "GET":
        # 获取API接口对象
        api = models.Api.objects.get(id=int(pk))

        # 获取前端数据
        host = request.GET.get("host")
        config = request.GET.get("config")

        # API运行主体
        test_case = eval(api.body)

        # 确定是否使用配置
        if config == "请选择":
            config = None
        else:
            config = eval(models.Config.objects.get(name=config, project=api.project).body)

        # 确定是否使用环境域名
        if host == "请选择":
            host = None
        else:
            host = models.HostIP.objects.get(name=host, project=api.project).value.splitlines()
            if not config:
                # 没有配置，则将test_case中的ip换成host的
                test_case = parse_host(host, test_case)

        # 为了运行api的，发起请求的，summary运行结果
        c = parse_host(host, config)
        summary = loader.debug_api(test_case, api.project.id, config=c)

        return JsonResponse(summary,safe=False)