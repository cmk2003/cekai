import json
import os
from copy import deepcopy

from cekai.settings import BASE_DIR
from test_runner.utils import writeReportExcel
# 汇总报告
def get_summary_report(sample_summary):
    __summary = deepcopy(sample_summary)
    summary_report = __summary[0]
    for index, summary in enumerate(sample_summary):
        if index > 0:
            summary_report["success"] = summary["success"] if not summary["success"] else summary_report["success"]
            summary_report["stat"]["testsRun"] += summary["stat"]["testsRun"]
            summary_report["stat"]["failures"] += summary["stat"]["failures"]
            summary_report["stat"]["skipped"] += summary["stat"]["skipped"]
            summary_report["stat"]["successes"] += summary["stat"]["successes"]
            summary_report["stat"]["expectedFailures"] += summary["stat"]["expectedFailures"]
            summary_report["stat"]["unexpectedSuccesses"] += summary["stat"]["unexpectedSuccesses"]
            summary_report["time"]["duration"] += summary["time"]["duration"]
            summary_report["____details"].extend(summary["____details"])
    return summary_report


def control_email(sample_summary, kwargs):
    if kwargs["strategy"] == '从不发送':
        return False
    elif kwargs["strategy"] == '始终发送':
        return True
    elif kwargs["strategy"] == '仅失败发送':
        for summary in sample_summary:
            if not summary["success"]:
                return True
    elif kwargs["strategy"] == '监控邮件':
        monitor_path = os.path.join(BASE_DIR, 'logs', 'monitor.json')
        if not os.path.isfile(monitor_path):
            all_json = {
                kwargs["task_name"]: {
                    "error_count": 0,
                    "error_message": ""
                }
            }
        else:
            with open(monitor_path, 'r', encoding='utf-8') as _json:
                all_json = json.load(_json)
            if kwargs["task_name"] not in all_json.keys():
                all_json[kwargs["task_name"]] = {
                    "error_count": 0,
                    "error_message": ""
                }
        is_send_email = False
        last_json = all_json[kwargs["task_name"]]
        runresultErrorMsg = __filter_runresult(sample_summary, kwargs["self_error"])

        if runresultErrorMsg == '' and last_json["error_message"] == '':
            last_json["error_count"] = 0
            last_json["error_message"] = ""
            is_send_email = False
        elif runresultErrorMsg == '' and last_json["error_message"] != '':
            last_json["error_count"] = 0
            last_json["error_message"] = ""
            is_send_email = True
        elif runresultErrorMsg != '' and last_json["error_message"] == '':
            last_json["error_count"] = 1
            last_json["error_message"] = runresultErrorMsg
            is_send_email = True
        elif runresultErrorMsg != '' and last_json["error_message"] != '' and last_json[
            "error_message"] != runresultErrorMsg:
            last_json["error_count"] = 1
            last_json["error_message"] = runresultErrorMsg
            is_send_email = True
        elif runresultErrorMsg != '' and last_json["error_message"] != '' and last_json[
            "error_message"] == runresultErrorMsg:
            if last_json["error_count"] < int(kwargs["fail_count"]):
                is_send_email = True
            else:
                is_send_email = False
            last_json["error_count"] += 1

        all_json[kwargs["task_name"]] = last_json
        with open(monitor_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(all_json))

        return is_send_email
    else:
        return False


def __is_self_error(error_content, self_error_list):
    if error_content and self_error_list:
        for error_message in self_error_list:
            if error_message in error_content:
                return ""
    return error_content


def __filter_runresult(sample_summary, self_error_list):
    runresultErrorMsg = ''
    for summary in sample_summary:
        runresult = writeReportExcel.get_error_response_content(summary["____details"])[0]
        for testcase_result in runresult:
            for errormsg in testcase_result["error_api_content"]:
                if errormsg:
                    runresultErrorMsg += __is_self_error(errormsg[3].strip(), self_error_list)
    return runresultErrorMsg