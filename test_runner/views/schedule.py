import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django_celery_beat import models as celery_models

from test_runner.utils.schedule_format import format_request


def schedule_view(request):
    # 添加定时任务
    if request.method == "POST":
        # 获取客户端数据并格式化数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            request_data = format_request(request_data)
        except Exception as e:
            return JsonResponse({"success": False, "msg": str(e)}, status=400)

        request_data.pop("tasktype")
        request_data["crontab"] = celery_models.CrontabSchedule.objects.get(pk=request_data["crontab"])
        task = celery_models.PeriodicTask.objects.create(**request_data)
        task.save()
        return JsonResponse({"success": True, "msg": "添加定时任务成功"}, status=201)

# 分页查看
    elif request.method == "GET":
        # 获取前端数据
        project_id = request.GET.get("project")
        tasktype = request.GET.get("tasktype")
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 5)

        # 获取所有的任务
        tasks = celery_models.PeriodicTask.objects.filter(description=project_id, task="test_runner.tasks_schedule.schedule_debug_suite").order_by('-date_changed').values()
        for task in tasks:
            task["summary_kwargs"] = json.loads(task["kwargs"])

        # 数据分页处理
        if (len(tasks) <= per_page):
            page = 1
        pg = Paginator(tasks, per_page)
        pageData = pg.page(page)

        # 响应数据
        data = {
            "success": True,
            "results": list(pageData),
            "count": len(list(tasks))
        }
        return JsonResponse(data)


def schedule_pk_view(request, pk):
    # 删除单个
    if request.method == "DELETE":
        project_id = request.GET["project"]
        tasktype = request.GET["tasktype"]
        # PeriodicTask
        try:
            task = celery_models.PeriodicTask.objects.get(pk=pk)
            task.delete()
            return JsonResponse({"success": True}, status=204)
        except celery_models.PeriodicTask.DoesNotExist:
            return JsonResponse({"success": False, "msg": "定时任务不存在，或已被删除"})