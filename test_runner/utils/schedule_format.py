import json
import re

from django_celery_beat import models as celery_models

# 格式化时间
def format_crontab(crontab_time):
    crontab_s = crontab_time.strip().split(' ')
    if len(crontab_s) > 5:
        raise Exception('请检查crontab表达式长度')
    try:
        crontab = {
            'day_of_week': crontab_s[4],
            'month_of_year': crontab_s[3],
            'day_of_month': crontab_s[2],
            'hour': crontab_s[1],
            'minute': crontab_s[0]
        }
        return crontab
    except Exception:
        raise Exception('请检查crontab表达式')


# 格式化邮箱列表
def format_email(email_str):
    email_list = []
    if email_str:
        pattern = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        email_list = [_.strip() for _ in email_str.split(';') if _]
        for temp_email in email_list:
            if temp_email and re.match(pattern, temp_email) is None:
                raise Exception(str(temp_email)+' 邮箱格式错误')
    return email_list

# 格式化请求数据
def format_request(request_data):
    # 解析客户端传递的数据
    _name = request_data.get('name', '')
    _corntab = request_data.get('crontab', '')
    _switch = request_data.get('switch', False)
    _iswecatsend=request_data.get("iswecatsend",False)
    _webhook=request_data.get("webhook",'')
    _data = request_data.get('data', [])
    _strategy = request_data.get('strategy', '')
    _receiver = request_data.get('receiver', '')
    _mail_cc = request_data.get('mail_cc', '')
    _project = request_data.get('project')
    _fail_count = request_data.get('fail_count', 1)
    _self_error = request_data.get('self_error', '')
    _sensitive_keys = request_data.get('sensitive_keys', '')
    tasktype = request_data.get("tasktype")
    receiver = format_email(_receiver)
    mail_cc = format_email(_mail_cc)
    crontab_time = format_crontab(_corntab)

    self_error = [_.strip() for _ in _self_error.split(';') if _]
    sensitive_keys = [_.strip() for _ in _sensitive_keys.split(';') if _]
    _email = {
        "strategy": _strategy,
        "mail_cc": mail_cc,
        "receiver": receiver,
        "crontab": _corntab,
        "project": _project,
        "task_name": _name,
        "fail_count": _fail_count,
        "self_error": self_error,
        "sensitive_keys": sensitive_keys,
        "iswecatsend":_iswecatsend,
        "webhook":_webhook
    }

    request_data = {
        "name": _name,
        "tasktype":tasktype,
        "task": "test_runner.tasks_schedule.schedule_debug_suite",
        "crontab": crontab_time,
        "args": json.dumps(_data, ensure_ascii=False),
        "kwargs": _email,
        "description": _project,
        "enabled": _switch
    }

    if request_data["kwargs"]["strategy"] in ['始终发送', '仅失败发送'] and request_data["kwargs"]["receiver"] == []:
        raise Exception('请填写接收邮箱')

    crontab = celery_models.CrontabSchedule.objects.filter(**request_data["crontab"]).first()
    if crontab is None:
        crontab = celery_models.CrontabSchedule.objects.create(**request_data["crontab"])
        crontab.save()
    request_data["crontab"] = crontab.id
    request_data["kwargs"] = json.dumps(request_data["kwargs"], ensure_ascii=False)

    return request_data