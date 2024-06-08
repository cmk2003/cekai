import json

from django.http import JsonResponse

from test_runner import models

def tree_pk_view(request, pk):
    # 获取
    if request.method == "GET":
        # 获取树结构类型
        tree_type = request.GET.get("type")

        # 获取该项目对应树结构信息
        rm = models.Relation.objects.filter(project=pk).get(type=tree_type)

        # 將字符串转为列表或者字典
        body = eval(rm.tree)
        data = {
            "tree": body,
            "id": rm.id,
            "success": True
        }
        return JsonResponse(data)
    elif request.method == "PATCH":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        body = request_data.get("body")# 树结构体
        mode = request_data.get("mode")

        # 获取并修改
        rm = models.Relation.objects.get(pk=pk)
        rm.tree = body
        rm.save()

        if mode:
            # 删除该节点下的所有的API与CASE
            models.Api.objects.filter(relation=request_data.get("node")).delete()
            models.Case.objects.filter(relation=request_data.get("node")).delete()

        data = {
            "tree": body,
            "success": True,
            "msg": "树形结构更新成功"
        }
        return JsonResponse(data)