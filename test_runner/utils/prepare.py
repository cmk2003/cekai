
from jsonpath import jsonpath

from test_runner import models
from test_runner.utils.parser import Format


def findtreenodes(tree,nodeid):
    if jsonpath(tree, "$..[?(@.id=='{}')]".format(nodeid)) and len(jsonpath(tree, "$..[?(@.id=='{}')]".format(nodeid))[0]['children'])>0:
        nodes=jsonpath(jsonpath(tree, "$..[?(@.id=='{}')]".format(nodeid))[0]['children'], "$..id")#获取到nodeid下面所有的id
        nodes.append(nodeid)
        return nodes
    return [nodeid]

def generate_casestep(body, case, pk):
    # 将一个api变为一个步骤
    for index in range(len(body)):
        test = body[index]#可能是一个配置，也可能是一个api
        try:
            format_http = Format(test['newBody'])
            format_http.parse()

            name = format_http.name
            new_body = format_http.testcase
            url = format_http.url
            method = format_http.method
        except KeyError:
            try:
                method = test["body"]["method"]
                name = test["body"]["name"]
                config = models.Config.objects.get(name=name, project__id=pk)
                url = config.base_url
                new_body = eval(config.body)
            except:
                api = models.Api.objects.get(id=test['id'])
                new_body = eval(api.body)
                test_body = eval(test["body"])
                name = test_body["name"]
                if api.name != name:
                    new_body["name"] = name
                url = test_body["request"]["url"]
                method = test_body["request"]["method"]

        kwargs = {
            "name": name,
            "body": new_body,
            "url": url,
            "method": method,
            "step": index,
            "case": case
        }
        models.CaseStep.objects.create(**kwargs)

def update_casestep(body,case,project):
    step_list=list(models.CaseStep.objects.filter(case=case).values("id"))
    for index in range(len(body)):
        test=body[index]
        try:
            format_http=Format(test["newBody"])
            format_http.parse()
            name=format_http.name
            new_body=format_http.testcase
            url=format_http.url
            method=format_http.method
        except KeyError:
            if isinstance(test["body"], str):
                test["body"] = eval(test["body"])

            if "case_id" in test.keys():
                case_step=models.CaseStep.objects.get(id=test['id'])
            elif test["body"].get("method")=="config":
                case_step=models.Config.objects.get(name=test['body']['name'],project__id=project)
            else:
                case_step=models.Api.objects.get(id=test["id"])

            new_body=eval(case_step.body)
            name=test["body"]["name"]

            if case_step.name != name:
                new_body["name"]=name
            if test["body"].get("method")=="config":
                url=""
                method="config"
            else:
                url=test["body"]["request"]["url"]
                method=test["body"]["request"]["method"]

        kwargs={
            "name":name,
            "body":new_body,
            "url":url,
            "method":method,
            "step":index
        }
        if "case_id" in test.keys():
            models.CaseStep.objects.filter(id=test["id"]).update(**kwargs)
            step_list.remove({"id":test["id"]})
        else:
            kwargs["case"]=case
            models.CaseStep.objects.create(**kwargs)

    #删除多余的step
    for content in step_list:
        models.CaseStep.objects.filter(id=content["id"]).delete()