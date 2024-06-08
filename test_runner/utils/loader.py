import datetime
import shutil
import json
import uuid

import requests
import tempfile
import os
import copy
from httprunner import HttpRunner
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup

from cekai.settings import BASE_DIR
from test_runner import models
from test_runner.utils.fileLoader import FileLoader


def parse_summary(summary):
    for detail in summary["details"]:
        for record in detail["records"]:
            for key, value in record["meta_data"]["request"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["request"][key] = value.decode("utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["request"][key] = requests.utils.dict_from_cookiejar(value)

            for key, value in record["meta_data"]["response"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["response"][key] = value.decode("utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["response"][key] = requests.utils.dict_from_cookiejar(value)

            if "text/html" in record["meta_data"]["response"]["content_type"]:
                record["meta_data"]["response"]["content"] = \
                    BeautifulSoup(record["meta_data"]["response"]["content"], features="html.parser").prettify()

    return summary


def load_debugtalk(project):
    # 创建临时运行目录
    tempfile_path = tempfile.mkdtemp(prefix='tempHttpRunner', dir=os.path.join(BASE_DIR, 'tempWorkDir'))
    debugtalk_path = os.path.join(tempfile_path, 'debugtalk.py')
    os.chdir(tempfile_path)

    try:
        # 获取当前项目的所有驱动文件
        py_files = models.Pycode.objects.filter(project__id=project)
        if py_files:
            for file in py_files:
                # file_path = os.path.join(tempfile_path, file.name)
                FileLoader.dump_python_file(debugtalk_path, file.code)
                FileLoader.load_python_module(os.path.dirname(debugtalk_path))
        else:
            code = models.Debugtalk.objects.get(project=project)
            FileLoader.dump_python_file(debugtalk_path, code.code)

        debugtalk = FileLoader.load_python_module(os.path.dirname(debugtalk_path))

        return debugtalk, debugtalk_path
    except Exception as e:
        os.chdir(BASE_DIR)  # 回到项目根目录
        shutil.rmtree(os.path.dirname(debugtalk_path))  # 递归删除临时文件
        raise SyntaxError(str(e))

def send_request(url, method, data=None, headers=None):
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers)
    elif method.upper() == 'POST':
        response = requests.post(url, json=data, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")

    return response

def parse_summary1(response):
    summary = {
        "status_code": response.status_code,
        "response_body": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text,
        "headers": response.headers
    }
    return summary

def debug_api(api, project, name=None, config=None, save=False, test_data=None, report_name=''):
    # 验证是否有需要运行的API接口
    if len(api) == 0:
        return {"success": False, "msg": "API不存在"}

    # 可能运行多个API接口，合成待运行的列表
    if isinstance(api, dict):
        api = [api]

    # 加载当前项目的驱动文件
    debugtalk = load_debugtalk(project)
    debugtalk_content = debugtalk[0] #包含变量和函数等
    debugtalk_path = debugtalk[1]    #确定运行文件路径

    # 进入该文件所在目录下工作
    os.chdir(os.path.dirname(debugtalk_path))

    try:
        # 解析api接口数据
        testcase_list = [parse_tests(api, debugtalk_content, project, name=name, config=config)]

        fail_fast = False
        if config and 'failFast' in config.keys():
            fail_fast = True if (config["failFast"] == 'true' or config["failFast"] == True) else False

        kwargs = {
            "failfast": fail_fast
        }
        if test_data != None:
            os.environ["excelName"] = test_data[0]
            os.environ["excelsheet"] = test_data[1]
        print(testcase_list)

        # 创建请求运行对象
        runner = HttpRunner(**kwargs)
        # 对API接口发起请求
        runner.run(testcase_list)

        # 解析运行结果
        summary = parse_summary(runner.summary)
        if save:# 如需要可保存运行结果
            pass# 在后续的实验中补充

        # 返回运行结果
        return summary

    except Exception as e:
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        # 删除临时运行文件
        shutil.rmtree(os.path.dirname(debugtalk_path))

def parse_tests(testcases, debugtalk, project, name=None, config=None):
    refs = {
        "env": {},
        "def-api": {},
        "def-testcase": {},
        "debugtalk": debugtalk
    }
    testset = {
        "config": {
            "name": testcases[-1]["name"],
            "variables": []
        },
        "teststeps": testcases,
    }

    if config:
        if "parameters" in config.keys():
            for content in config["parameters"]:
                for key, value in content.items():
                    try:
                        content[key] = eval(value.replace("\n", ""))
                    except:
                        content[key] = value
        if 'outParams' in config.keys():
            config["output"] = []
            out_params = config.pop('outParams')
            for params in out_params:
                config["output"].append(params["key"])
        testset["config"] = config

    if name:
        testset["config"]["name"] = name

    global_variables = []

    for variables in models.Variable.objects.filter(project__id=project).values("key", "value"):
        if testset["config"].get("variables"):
            for content in testset["config"]["variables"]:
                if variables["key"] not in content.keys():
                    global_variables.append({variables["key"]: variables["value"]})
        else:
            global_variables.append({variables["key"]: variables["value"]})

    if not testset["config"].get("variables"):
        testset["config"]["variables"] = global_variables
    else:
        testset["config"]["variables"].extend(global_variables)

    testset["config"]["refs"] = refs
    return testset

def debug_suite(suite, project, obj, config, save=True):
    if len(suite) == 0:
        return {"success": False, "msg": "API不存在"}

    case_sets = []
    debugtalk = load_debugtalk(project)#加载驱动文件
    debugtalk_content = debugtalk[0]
    debugtalk_path = debugtalk[1]

    # 进入临时工作目录
    os.chdir(os.path.dirname(debugtalk_path))
    try:
        for index in range(len(suite)):
            cases = copy.deepcopy(parse_tests(suite[index], debugtalk_content, project, name=obj[index]['name'], config=config[index]))
            case_sets.append(cases)

        kwargs = {
            "failfast": True
        }
        runner = HttpRunner(**kwargs)
        # 运行
        runner.run(case_sets)
        # 解析结果
        summary = parse_summary(runner.summary)
        if save:
            save_summary("", summary, project, type=1)
        return summary
    except Exception as e:
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        # 删除debugtalk文件
        shutil.rmtree(os.path.dirname(debugtalk_path))

def save_summary(name, summary, project_id, type=2, report_id=""):
    if "status" in summary.keys():
        return
    # 报考名称
    if name == "":
        name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 报告ID
    if report_id=="":
        report_id=str(uuid.uuid4())
    # 简化的报告信息
    simple_summary = {
        "time": summary["time"],
        "platform": summary["platform"],
        "stat": summary["stat"],
        "success": summary["success"],
    }
    project_class = models.Project.objects.get(id=project_id)
    # 创建报告信息对象
    report = models.Report.objects.create(**{
        "project": project_class,
        "name": name,
        "type": type,
        "summary": json.dumps(simple_summary),
        "report_id": report_id
    })
    report.save()
    # 创建详细报告信息对象
    report_detail = models.ReportDetail.objects.create(**{
        "project": project_class,
        "name": name,
        "report": report,
        "summary": json.dumps(summary, ensure_ascii=False)
    })
    report_detail.save()

def debug_api(api, project, name=None, config=None, save=False, test_data=None, report_name=''):
    # 验证是否有需要运行的API接口
    if len(api) == 0:
        return {"success": False, "msg": "API不存在"}

    # 可能运行多个API接口，合成待运行的列表
    if isinstance(api, dict):
        api = [api]

    # 加载当前项目的驱动文件
    debugtalk = load_debugtalk(project)
    debugtalk_content = debugtalk[0] #包含变量和函数等
    debugtalk_path = debugtalk[1]    #确定运行文件路径

    # 进入该文件所在目录下工作
    os.chdir(os.path.dirname(debugtalk_path))

    try:
        # 解析api接口数据
        testcase_list = [parse_tests(api, debugtalk_content, project, name=name, config=config)]

        fail_fast = False
        if config and 'failFast' in config.keys():
            fail_fast = True if (config["failFast"] == 'true' or config["failFast"] == True) else False

        kwargs = {
            "failfast": fail_fast
        }
        if test_data != None:
            os.environ["excelName"] = test_data[0]
            os.environ["excelsheet"] = test_data[1]

        # 创建请求运行对象
        runner = HttpRunner(**kwargs)
        # 对API接口发起请求
        runner.run(testcase_list)

        # 解析运行结果
        summary = parse_summary(runner.summary)
        # save的默认值为FALSE
        # 一般单独运行API接口不会进行保存
        # 在运行测试用例时会重新赋值save为True
        if save:
            save_summary(report_name, summary, project, type=1)

        # 返回运行结果
        return summary
    except Exception as e:
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        # 删除临时运行文件
        shutil.rmtree(os.path.dirname(debugtalk_path))