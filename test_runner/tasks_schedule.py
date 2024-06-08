import json
import uuid
import time

from celery import shared_task
# from django_celery_beat import task


from test_runner import models
from test_runner.utils import loader, task_manage
from test_runner.utils.parser import parse_host


@shared_task
def schedule_debug_suite(*args, **kwargs):
    global reportstoptime

    project_id = int(kwargs["project"])
    sample_summary = []

    # 检查任务列表
    if not args:
        raise ValueError("任务列表为空，请检查")

    for case in args:
        # 用例的参数
        case_kwargs = case.get("kwargs", "")
        # 获取用例执行步骤
        case_steps = models.CaseStep.objects.filter(case__id=case["id"]).order_by("step").values("body")
        if not case_steps:
            raise ValueError("用例缺失，请检查")

        report_name = case["name"]
        case_name = case["name"]
        test_case = []
        config = None
        temp_config = []
        test_data = None
        temp_baseurl = ""
        g_host_info = ""
        if case_kwargs:
            report_name = case_kwargs["testCaseName"]
            if case_kwargs.get("excelTreeData", []):
                test_data = tuple(case_kwargs["excelTreeData"])
            if case_kwargs["hostInfo"] and case_kwargs["hostInfo"] != "请选择":
                g_host_info = case_kwargs["hostInfo"]
                host = models.HostIP.objects.get(name=g_host_info, project__id=project_id)
                _host_info = json.loads(host.hostInfo)
                temp_config.extend(_host_info["variables"])
                temp_baseurl = host.base_url if host.base_url else ''

        for content in case_steps:
            body = eval(content["body"])
            if "base_url" in body["request"].keys():
                config = eval(models.Config.objects.get(name=body["name"], project__id=project_id).body)
                continue
            test_case.append(parse_host(g_host_info, body))

        if config and g_host_info not in ["请选择", '']:
            config["variables"].extend(temp_config)
            if temp_baseurl:
                config["request"]["base_url"] = temp_baseurl
        if not config and g_host_info not in ["请选择", '']:
            config = {
                "variables": temp_config,
                "request": {
                    "base_url": temp_baseurl
                }
            }

        summary = loader.debug_api(test_case, project_id, name=case_name, config=parse_host(g_host_info, config), save=False, test_data=test_data)
        reportstoptime = time.time()  # 由于运行时间计算有很大误差，重新计算运行总时间
        summary["name"] = report_name
        sample_summary.append(summary)

    if sample_summary:
        summary_report = task_manage.get_summary_report(sample_summary)
        summary_report['time']["duration"] = reportstoptime - summary_report['time']['start_at']
        report_id = str(uuid.uuid4())
        loader.save_summary(kwargs["task_name"], summary_report, project_id, type=3, report_id=report_id)

        if kwargs["iswecatsend"]:
            print("-----------发送微信------------")

        is_send_email = task_manage.control_email(sample_summary, kwargs)
        if is_send_email:
            print("-----------发送邮件------------")