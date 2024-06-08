from django.urls import path, re_path
from test_app import views

urlpatterns = [
    # POST请求时增加班级信息，GET请求时获取所有班级信息
    re_path(r'grade/$', views.grade),
    # POST请求时增加学生信息，GET请求时获取所有学生信息
    re_path(r'student/$', views.student),
]