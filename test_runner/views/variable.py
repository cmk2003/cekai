import json
import os
import shutil
import tempfile
import uuid
from pyexcel_xls import get_data as get_xls_data
from pyexcel_xlsx import get_data as get_xlsx_data

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse

from cekai import settings
from test_runner import models
from test_runner.utils.getAccessToken import GetToken
from test_runner.utils.resource import VariablesResource
#实验手册8.3
def variable_view(request):
    # 新增全局变量
    if request.method == "POST":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            project_id = request_data["project"]
            key = request_data["key"]
            value = request_data["value"]
            desc = request_data["desc"]
        except KeyError:
            return JsonResponse({"success": False, "msg": "请求数据非法"})

        # 判断项目是否存在
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

        # 验证变量名称是否可用
        # 同一个项目不允许有相同名称的变量，不同项目之间是可以有相同名称变量的
        try:
            models.Variable.objects.filter(project=project_id).get(key=key)
            # 说明已经给该项目创建过这个变量
            return JsonResponse({"success": False, "msg": "变量已存在"})
        except models.Variable.DoesNotExist as e:
            # 该变量可以创建
            models.Variable.objects.create(key=key, value=value, desc=desc, project=project,
                                           create_user=request.user.name)
            return JsonResponse({"success": True, "msg": "变量添加成功"})
 # 分页查看全局变量
    elif request.method == "GET":
        # 获取前端数据
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        page = request.GET.get("page", 1)
        per_page = 5  # 前端页面中也是明确每页5条数据

        # 获取要展示的变量信息
        vars = models.Variable.objects.all().filter(project=project_id).order_by("-update_time")
        if search != "":
            vars = vars.filter(key__contains=search)
        vars = vars.values()

        # 分页展示
        # 假设有6条数据，用户1删除一条后，用户2点击分页器第二页出现BUG的问题
        if (len(vars) <= per_page):
            page = 1
        pg = Paginator(vars, per_page)
        pageData = pg.page(page)

        data = {
            "success": True,
            "results": list(pageData),
            "count": len(list(vars))
        }
        return JsonResponse(data)
    #批量删除
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                v = models.Variable.objects.get(pk=vDict["id"])
                v.delete()
            except models.Variable.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "变量删除成功"})



#实验手册8.5
def variable_pk_view(request, pk):
    # 修改全局变量信息
    if request.method == "PATCH":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        key = request_data.get("key")
        value = request_data.get("value")
        desc = request_data.get("desc")

        try:
            v = models.Variable.objects.get(pk=pk)

            if key != v.key:  # 在当前项目的所有变量中判断新的名字是否冲突
                try:
                    models.Variable.objects.filter(project=v.project.id).get(key=key)
                    # 已被占用
                    return JsonResponse({"success": False, "msg": "变量已存在"})
                except models.Variable.DoesNotExist:
                    v.key = key
                    v.value = value
                    v.desc = desc
                    v.save()
                    return JsonResponse({"success": True, "msg": "变量修改成功"})
            else:
                v.value = value
                v.desc = desc
                v.save()
                return JsonResponse({"success": True, "msg": "变量修改成功"})
        except models.Variable.DoesNotExist:
            # 变量被删除
            return JsonResponse({"success": False, "msg": "变量不存在，或已被删除"})
   #单个删除
    elif request.method == "DELETE":
        try:
            v = models.Variable.objects.get(pk=pk)
            v.delete()
            return JsonResponse({"success": True, "msg": "变量删除成功"})
        except models.Variable.DoesNotExist:
            return JsonResponse({"success": False, "msg": "变量不存在，或已被删除"})


#实验手册9.2
def exportexcel(request):
    if request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        project_id = request_data.get("project")

        # 获取该项目对应的所有全局变量
        variable = models.Variable.objects.filter(project__id=project_id)
        # 做Excel数据映射
        variables_resource = VariablesResource()
        dataset = variables_resource.export(queryset=variable)

        # 响应数据
        project_name = models.Project.objects.get(id=project_id).name
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.xlsx"'.format(project_name, "全局变量").encode(
            "utf-8")
        return response

#实验手册9.3
def importvariables(request):
    if request.method == "POST":
        # 获取对应项目对象
        project = models.Project.objects.get(pk=request.POST.get("project"))

        # 循环获取前端传递过来的Excel文件
        # 目前前端限制只能导入一个Excel文件，但是后端代码具有处理多个Excel文件的能力
        for key in request.FILES:
            files = request.FILES.getlist(key)
            for file in files:
                file_suffix = os.path.splitext(file.name)[-1]
                # 验证文件类型，只处理xls和xlsx类型的文件
                if file_suffix and file_suffix in [".xls", ".xlsx"]:
                    try:
                        # 创建临时保存目录
                        upload_path = os.path.join(settings.MEDIA_ROOT, 'varUploadExecl')
                        if not os.path.exists(upload_path):
                            os.makedirs(upload_path)
                        # media下的varUploadExecl目录需要提前创建
                        tempPath = tempfile.mkdtemp(prefix=str(uuid.uuid4()),
                                                    dir=os.path.join(settings.MEDIA_ROOT, 'varUploadExecl'))
                        tempFilePath = os.path.join(tempPath, file.name)

                        # 写入文件
                        with open(tempFilePath, "wb") as fp:
                            for info in file.chunks():
                                fp.write(info)

                        # 为了区别xls和xlsx两种类型的文件
                        # 处理两种格式的文件所用的方法不同
                        # 是函数的形式，所以这里需要根据文件后缀名来选择不同的函数
                        get_excel_data = None
                        if file_suffix == ".xls":
                            get_excel_data = get_xls_data
                        else:
                            get_excel_data = get_xlsx_data
                        # 读取Excel数据
                        print(tempFilePath)
                        excel_info = get_excel_data(tempFilePath)

                        # 获取每个sheet的名称
                        for sheet_name in excel_info:
                            # 根据sheet名称获取当前sheet数据
                            sheet_data = excel_info[sheet_name]
                            # 导入需要去掉头行标题
                            if len(sheet_data) > 0:
                                sheet_data.pop(0)

                            # 处理每一行数据
                            for line_data in sheet_data:
                                # 获取相关数据
                                if len(line_data) >= 3:
                                    var_key = line_data[0]
                                    var_value = line_data[1]
                                    var_desc = line_data[2]
                                elif len(line_data) == 2:
                                    var_key = line_data[0]
                                    var_value = line_data[1]
                                else:
                                    raise Exception("Excel数据异常")

                                # 如果变量存在，就删除重新创建最新的
                                var = models.Variable.objects.filter(key=var_key, project=project)
                                if var:
                                    var.delete()
                                # 添加全局变量
                                models.Variable.objects.create(key=var_key, value=var_value, desc=var_desc,
                                                               create_user=request.user.name, project=project)
                        # 删除创建的临时文件目录
                        # 删除句柄
                        del excel_info
                        shutil.rmtree(tempPath)
                        return JsonResponse({"msg": "导入成功", "success": True})
                    except Exception as e:
                        del excel_info
                        # 删除临时目录
                        shutil.rmtree(tempPath)
                        return JsonResponse({"msg": str(e), "success": False})
                else:
                    return JsonResponse({"msg": "导入的文件不是.xls或.xlsx", "success": False})


#实验手册9.4
def tokenmsg(request):
    if request.method == "POST":
        # 获取前端数据
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            project_id = request_data["project"]
            publickeyurl = request_data["publickeyurl"]
            loginurl = request_data["loginurl"]
            username = request_data["username"]
            password = request_data["password"]
        except Exception as e:
            return JsonResponse({"description": "参数错误，有必要参数未传", "traceback": str(e)}, status=400)

        # 向对方服务器获取token数据
        try:
            gettoken = GetToken(project_id, publickeyurl, loginurl, username, password)
            gettoken.login_gettoken()
            return JsonResponse({'msg': "token生成成功", 'success': True})
        except Exception as e:
            return JsonResponse({'description': '系统内部错误', 'traceback': str(e)}, status=500)