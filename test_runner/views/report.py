import json
import os

from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse

from cekai.settings import MEDIA_ROOT
from test_runner import models
from test_runner.utils.writeReportExcel import write_excel_log

def report_view(request):
    # 查看
    if request.method == "GET":
        # 获取客户端数据
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 5)

        # 获取当前项目的所有测试报告数据
        reports = models.Report.objects.all().filter(project=project_id).order_by('-update_time')
        # 过滤数据
        if search != "":
            reports = reports.filter(name__contains=search)
        reports = reports.values()

        # 数据分页
        if (len(reports) <= per_page):
            page = 1
        pg = Paginator(reports, per_page)
        pageData = list(pg.page(page))

        # 因测试报告对象中的create_time、update_time和summary属性无法自动序列化，需要手动转为字符串格式
        for report in pageData:
            report["create_time"] = str(report["create_time"])
            report["update_time"] = str(report["update_time"])
            report["summary"] = json.loads(report["summary"])

        # 响应
        data = {
            "count": len(reports),
            "results": pageData
        }
        return JsonResponse(data)
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                report = models.Report.objects.get(pk=vDict["id"])
                report.delete()# 会删除关联的详细测试报告数据
            except models.Report.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "报告删除成功"})

def report_pk_view(request, pk):
    # 删除单个
    if request.method == "DELETE":
        try:
            report = models.Report.objects.get(pk=pk)
            report.delete()
            return JsonResponse({"success": True, "msg": "报告删除成功"})
        except models.Report.DoesNotExist:
            return JsonResponse({"success": False, "msg": "报告不存在，或已被删除"})


def downreport(request):
    # 下载测试报告
    if request.method == "POST":
        # 获取客户端数据
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            file_type = int(request_data["fileType"])
            project_id = int(request_data["project"])
            report_id = int(request_data["id"])
        except KeyError:
            return JsonResponse({"success": False, "msg": "请求数据非法"}, status=400)

        # file_tpye=1：资料库数据
        # file_tpye=2：Excel格式测试报告数据，大部分情况均为Excel格式数据
        # file_tpye=3：HTML格式测试报告数据
        print("-----file_type----", file_type)
        try:
            if file_type == 1:
                pass
            else:
                # 获取测试报告详细信息对象
                fileObject = models.ReportDetail.objects.get(project_id=project_id, report_id=report_id)
                # 获取文件名
                filename = fileObject.name
                # 将响应信息数据解析为json字符串格式
                summary = json.loads(fileObject.summary)
                # 在服务端media目录下生成excelReport目录，用来存放待下载的Excel文件
                filepath = write_excel_log(summary)

            # 在服务器这边找到那个Excel的路径，使用FileResponse将文件返回给客户端
            fileresponse = FileResponse(open(filepath, 'rb'))
            fileresponse["Content-Type"] = "application/octet-stream"
            fileresponse["Content-Disposition"] = "attachment;filename={}".format(filename)
            return fileresponse
        except:
            return JsonResponse({"success": False, "msg": "测试文档下载失败"})