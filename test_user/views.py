from django.shortcuts import render
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import Permission,Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from test_user import models
from test_runner.models import Project
# Create your views here.
def register(request):
    if request.method=="POST":
        #获取注册信息
        request_data=json.loads(request.body.decode('utf-8'))
        try:
            username=request_data["username"]
            password=request_data["password"]
            email=request_data["email"]
        except KeyError:
            return JsonResponse({"success":False,"msg":"请求数据非法"})

        #验证用户账号是否存在
        try:
            models.User.objects.get(username=username)
            return JsonResponse({"success":False,"msg":"用户名已被注册"})
        except:
            pass

        #验证用户邮箱是否存在
        try:
            models.User.objects.get(email=email)
            return JsonResponse({"success":False,"msg":"邮箱已被注册"})
        except:
            pass

        #加密密码
        password=make_password(password)

        #创建用户
        try:
            models.User.objects.create(username=username,password=password,email=email,name=request_data["name"])
            return JsonResponse({"success":True,"msg":"用户注册成功"})
        except:
            return JsonResponse({"success":False,"msg":"系统错误"})



def login_system(request):
    if request.method=="POST":
        #获取登录信息
        request_data=json.loads(request.body.decode('utf-8'))
        try:
            username=request_data["username"]
            password=request_data["password"]
        except KeyError:
            return JsonResponse({"success":False,"msg":"请求数据非法"})

        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            #用户账号密码正确且用户是活跃状态
            #更新token
            token=models.UserToken.objects.filter(user=user)
            if token:
                token.delete()
            token=models.UserToken.objects.create_token(user=user)

            LOGIN_SUCCESS={
                "success":True,
                "msg":"登陆成功",
                "token":token.token,   #用户token值
                "user":username,       #用户账号
                "name":user.name,      #用户真实姓名
                "email":user.email,    #用户邮箱
                "Is_superuser":user.is_superuser   #是否为超级管理员
            }

            login(request,user)
            return JsonResponse(LOGIN_SUCCESS)
        else:
            #用户账号密码错误或用户非活跃状态
            try:
                models.User.objects.get(username=username)
                cause='密码错误'
            except:
                cause='用户不存在'
            return JsonResponse({"result":0,"msg":cause})

def logout_system(request):
    if request.method=="POST":
        logout(request)
        return JsonResponse({})


def permission(request):
    if request.method=="GET":
        permissions_list=Permission.objects.all()
        ret_list=[]
        for permi in permissions_list:
            temp_permission={
                "id":permi.id,
                "name":permi.name,
            }
            ret_list.append(temp_permission)
        return JsonResponse({"data":ret_list})

def group_view(request):
    # 获取权限组信息
    if request.method == "GET":
        # 获取客户端数据
        search = request.GET.get("search")  # 过滤条件
        page = request.GET.get("page", 1)  # 展示页码数据
        per_page = 5  # 默认每页5条数据

        # 获取所有组数据
        groups = Group.objects.all()
        if search:
            # 根据过滤字段进行过滤
            groups = groups.filter(name__contains=search)
        groups = groups.values()

        # 数据分页
        if (len(groups) <= per_page):
            page = 1
        pg = Paginator(groups, per_page)
        pageData = pg.page(page)

        data = {
            "success": True,
            "results": list(pageData),  # 用于页面展示
            "results2": list(groups),  # 用于权限处理
            "count": len(list(groups))
        }
        return JsonResponse(data)

    # 新建权限组
    elif request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            name = request_data["name"]
            permissions = request_data["permissions"]
        except:
            return JsonResponse({"code": 400, "success": False, "msg": "参数错误或必传参数缺失"})

    # 验证组名是否存在
        try:
            Group.objects.get(name=name)
            return JsonResponse({"success": False, "msg": "用户组已存在"})
        except:
            pass

    # 创建组
        try:
            group = Group.objects.create(name=name)
            permissionsobj = Permission.objects.filter(id__in=permissions)
            group.permissions.add(*permissionsobj)
            return JsonResponse({"code": 200, "success": True, "msg": "新增用户组成功"})
        except:
            return JsonResponse({"code": 500, "success": False, "msg": "新增用户组失败"})

# 修改权限组
    elif request.method == "PATCH":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            id = request_data["id"]
            name = request_data["name"]
            permissions = request_data["permissions"]
        except:
            return JsonResponse({"code": 400, "success": False, "msg": "参数错误或必传参数缺失"})

        # 获取要修改的用户组
        try:
            group = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return JsonResponse({"code": 500, "success": False, "msg": "用户组不存在"})

        # 修改组信息，如果修改后的名称已存在，则修改失败
        try:
            group.name = name
            permissionsobj = Permission.objects.filter(id__in=permissions)
            group.permissions.set(permissionsobj)
            group.save()
            return JsonResponse({"code": 200, "success": True, "msg": "用户组修改成功"})
        except:
            return JsonResponse({"code": 500, "success": False, "msg": "用户组修改失败"})

# 批量删除权限组
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                group = Group.objects.get(pk=vDict["id"])
                group.delete()
            except:
                pass
        return JsonResponse({"success": True, "msg": "权限组删除成功"})


def group_pk_view(request, pk):
    if request.method == "DELETE":
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            return JsonResponse({"success": True,"msg": "用户组删除成功"})
        except Group.DoesNotExist:
            return JsonResponse({"success": False,"msg": "用户组不存在，或已被删除"})

def userinfo_view(request):
    if request.method == "GET":
        # 获取前端数据
        search = request.GET.get("search")#查询过滤条件
        page = request.GET.get("page", 1)#展示数据的页码
        per_page = 5#默认每页5条数据

        # 获取用户数据
        users = models.User.objects.all().order_by('-date_joined')
        if search:
            users = users.filter(Q(username__contains=search) | Q(name__contains=search))
        users = users.values()

        #分页
        if (len(users) <= per_page):
            page = 1
        pg = Paginator(users, per_page)
        pageData = pg.page(page)#获取对应页码用户数据

        data = {
            "success": True,
            "results": list(pageData),
            "count": len(list(users))
        }
        return JsonResponse(data)

# 新增用户
    elif request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            name = request_data["name"]
            username = request_data["username"]
            password = request_data["password"]
            email = request_data["email"]
            is_active = request_data["is_active"]
        except KeyError:
            return JsonResponse({"code": "0100",
                                 "success": False,
                                 "msg": "请求数据非法"})

        # 验证用户账号是否存在
        try:
            models.User.objects.get(username=username)
            return JsonResponse({"code": "0101",
                                 "success": False,
                                 "msg": "用户名已被注册"})
        except:
            pass

        # 验证用户邮箱是否存在
        try:
            models.User.objects.get(email=email)
            return JsonResponse({"code": "0101",
                                 "success": False,
                                 "msg": "邮箱已被注册"})
        except:
            pass

        # 加密密码
        password = make_password(password)

        # 创建用户
        try:
            models.User.objects.create(username=username,
                                       password=password,
                                       email=email,
                                       is_active=is_active,
                                       name=name)
            return JsonResponse({"code": "0001",
                                 "success": True,
                                 "msg": "用户注册成功"})
        except:
            return JsonResponse({"code": "9999",
                                 "success": False,
                                 "msg": "系统错误"})

    # 修改用户信息
    elif request.method == "PATCH":
        # 获取前端传递的数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        username = request_data.get("username")
        email = request_data.get("email")
        is_active = request_data.get("is_active")
        is_superuser = request_data.get("is_superuser")
        belong_project = request_data.get("belong_project", [])
        groupid_list = request_data.get("groups", [])

        # 获取用户
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return JsonResponse({"code": "0104",
                                 "success": False,
                                 "msg": "该用户未注册"})

        # 合成修改数据
        if is_active != None and is_superuser != None:
            # 获取项目信息
            projects = Project.objects.filter(id__in=belong_project)

            groups = Group.objects.filter(id__in=groupid_list)
            permissions_list = []
            permissions = groups.values('permissions__id')
            for i in permissions:
                permissions_list.append(i['permissions__id'])
            permissionsobj = Permission.objects.filter(id__in=permissions_list)

            # 重置用户关联的项目
            if projects:
                user.belong_project.set(projects)
            # 重置权限
            if groups:
                user.groups.set(groups)
            # 这里添加的用户权限会导致数据与用户组的权限不一致，取用户权限不要取这里的
            user.user_permissions.set(permissionsobj)
            data = {
                'name': name,
                'email': email,
                'is_superuser': is_superuser,
                'is_active': is_active,
            }
        else:
            data = {"name": name, "email": email}

        # 修改用户信息
        try:
            oldname = user.name
            models.User.objects.filter(username=username).update(**data)

            # 用户名发生变化需要修改对应创建的项目中的responsible
            if oldname != name:
                pros = Project.objects.filter(responsible=oldname)
                for p in pros:
                    p.responsible = name
                    p.save()

            return JsonResponse({"code": "0001", "success": True, "msg": "用户信息修改成功"})
        except:
            return JsonResponse({"code": "0001", "success": False, "msg": "用户信息修改失败"})


 # 批量删除用户
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                users = models.User.objects.get(pk=vDict["id"])
                users.delete()
            except models.User.DoesNotExist:
                pass
        return JsonResponse({"success": True,"msg": "用户删除成功"})


def userinfo_pk_view(request, pk):
    # 删除单个用户，pk即为要删除用户的主键id值
    if request.method == "DELETE":
        try:
            user = models.User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({"success": True,"msg": "用户删除成功"})
        except models.User.DoesNotExist:
            return JsonResponse({"success": False,"msg": "用户不存在，或已被删除"})

def updateuserpassword(request):
    # 修改密码
    if request.method == "POST":
        # 获取客户端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            password = request_data["password"]
            newpassword = request_data["newpassword"]
        except:
            return JsonResponse({"code": "0001",
                                 "success": False,
                                 "msg": "参数错误或有必填参数未填"})

        # 获取当前登录的用户对象
        user = models.User.objects.get(id=request.user.id)
        if not user:
            return JsonResponse({"code": "0104",
                                 "success": False,
                                 "msg": "该用户未注册"})

        # 验证密码
        if not check_password(password, user.password):
            return JsonResponse({"code": "0001",
                                 "success": False,
                                 "msg": "原密码错误"})

        # 修改密码
        try:
            user.password = make_password(newpassword)
            user.save()
            return JsonResponse({"code": "0001",
                                 "success": True,
                                 "msg": "更新密码成功"})
        except:
            return JsonResponse({"code": "0001",
                                 "success": False,
                                 "msg": "更新密码失败"})


def test(request):
    print(request.user.name)
    return JsonResponse({"code": "0001",
                         "success": False,
                         "msg": "更新密码失败"})