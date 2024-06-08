import json

from django.core.paginator import Paginator
from django.http import JsonResponse

from test_runner import models
from test_runner.utils.runner import DebugCode


def pycode_view(request):
    # 新增
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

            # # 创建一个API的树结构
            # models.Relation.objects.create(project=pro)
            # # 创建一个测试用例的树结构
            # models.Relation.objects.create(project=pro, type=2)

            return JsonResponse({"success": True, "msg": "项目添加成功"})

# 分页查看
    elif request.method == "GET":
        # 获取数据
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 5)

        # 获取所有驱动文件库
        pys = models.Pycode.objects.filter(project__id=project_id).order_by('-update_time')
        if search:
            pys = pys.filter(name__contains=search)
        pys = pys.values()

        # 数据分页
        if (len(pys) <= per_page):
            page = 1
        pg = Paginator(pys, per_page)
        pageData = pg.page(page)

        data = {
            "count": len(list(pys)),
            "results": list(pageData),
            "success": True
        }
        return JsonResponse(data)

    # 批量删除
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                py = models.Pycode.objects.get(pk=vDict["id"])
                py.delete()
            except models.Pycode.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "驱动文件删除成功"})


def pycode_pk_view(request, pk):
    if request.method == "PATCH":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))

        # 如果存在name数据则为修改驱动文件信息，否则为修改驱动文件代码
        name = request_data.get("name")
        if name:
            # 修改驱动代码文件信息
            pycode_id = request_data.get("id")
            desc = request_data.get("desc")
            try:
                py = models.Pycode.objects.get(pk=pycode_id)
                py.name = name
                py.desc = desc
                try:
                    py.save()  # 模型中做了项目和名称的唯一，所以名称相同会抛出异常
                    return JsonResponse({"success": True, "msg": "驱动文件修改成功"})
                except:
                    return JsonResponse({"success": False, "msg": "驱动代码文件已存在"})
            except models.Pycode.DoesNotExist:
                return JsonResponse({"success": False, "msg": "驱动文件不存在，或已被删除"})
        else:
            # 修改驱动代码信息
            code = request_data.get("code")
            py = models.Pycode.objects.get(pk=pk)
            py.code = code
            py.save()
            return JsonResponse({"success": True, "msg": "代码保存成功"})
    elif request.method == "GET":
        try:
            py = models.Pycode.objects.get(pk=pk)

            data = {
                "code": py.code,
                "id": py.id,
                "success": True
            }
            return JsonResponse(data)
        except models.Pycode.DoesNotExist:
            return JsonResponse({"success": False, "msg": "驱动文件不存在，或已被删除"})
    # 单个删除
    elif request.method == "DELETE":
        try:
            py = models.Pycode.objects.get(pk=pk)
            py.delete()
            return JsonResponse({"success": True, "msg": "驱动文件删除成功"})
        except models.Pycode.DoesNotExist:
            return JsonResponse({"success": False, "msg": "驱动文件不存在，或已被删除"})


def runpycode(request, pk):
    if request.method == "GET":
        try:
            # 获取驱动文件对象
            py = models.Pycode.objects.get(pk=pk)

            # 创建debug运行对象并运行代码
            # 参数1：:代码
            # 参数2：项目ID
            # 参数3：代码名称
            debug = DebugCode(py.code, request.GET.get("project"), py.name)
            debug.run()

            return JsonResponse({"msg": debug.resp})
        except models.Pycode.DoesNotExist:
            return JsonResponse({"msg": "驱动代码文件被删除"})