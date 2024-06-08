from django.urls import path, re_path

from test_runner.views import userpermission, pycode, tree, api, case, report, schedule
from test_runner.views import project
from test_runner.views import database
from test_runner.views import variable
from test_runner.views import hostip
from test_runner.views import config
urlpatterns = [
    # 获取用户权限列表
    re_path(r'^getpermissionslist/$', userpermission.permission),

    # 项目的增删改查
    re_path(r'^project/$', project.project_view),

    # 分页
    re_path(r'^project_paginator/(?P<page>\d+)/(?P<per_page>\d+)/$', project.project_paginator_view),

    #统计项目数据
    re_path(r'^getallprojectmessage/$', project.getallprojectmessage),

    # 查看单个项目信息-项目概况页面
    re_path(r'^project/(?P<pk>\d+)/$', project.project_detail),
    re_path(r'^gettagcount/$', project.gettagcount),
    re_path(r'^getreporttail/$', project.getreporttail),

    #数据库
    re_path(r'^databaseconfig/\d*$', database.database_view),
    re_path(r'^databaseconfig/(?P<pk>\d+)/$', database.database_pk_view),

    #分页
    re_path(r'^database_paginator/(?P<project_id>\d+)/(?P<page>\d+)/(?P<per_page>\d+)/$', database.database_paginator),

    #全局变量
    re_path(r'^variables/$', variable.variable_view),
    re_path(r'^variables/(?P<pk>\d+)/$', variable.variable_pk_view),

    # 导出全局变量
    re_path(r'^exportVariables/$', variable.exportexcel),
    # 导入全局变量
    re_path(r'^importvariables/$', variable.importvariables),

    #创建token变量
    re_path(r'^gettokenmsg/$', variable.tokenmsg),

    #环境配置
    re_path(r'^host_ip/$', hostip.hostip_view),
    re_path(r'^host_ip/(?P<pk>\d+)/$', hostip.hostip_pk_view),

    #配置信息
    re_path(r'^config/$', config.config_view),
    re_path(r'^config/(?P<pk>\d+)/$', config.config_pk_view),

   	# 驱动代码
    re_path(r'^pycode/$', pycode.pycode_view),
    re_path(r'^pycode/(?P<pk>\d+)/$', pycode.pycode_pk_view),
    re_path(r'^runpycode/(?P<pk>\d+)/$', pycode.runpycode),

   	# 树结构
    re_path(r'^tree/(?P<pk>\d+)/$', tree.tree_pk_view),
   	# API 接口
    re_path(r'^api/$', api.api_view),
    re_path(r'^api/(?P<pk>\d+)/$', api.api_pk_view),
    re_path(r'^exportApi/$', api.exportApiExcel),
   	# 运行一个api接口
    re_path(r'^run_api_pk/(?P<pk>\d+)/$', api.runApi),
   	# 测试用例
    re_path(r'^test/$', case.case_view),
    re_path(r'^test/(?P<pk>\d+)/$', case.case_pk_view),
    re_path(r'^teststep/(?P<pk>\d+)/$', case.getstep),

   	# 运行一个测试用例
    re_path(r'^run_testsuite_pk/(?P<pk>\d+)/$', case.run_case),
    # 运行某些分组下的所有用例
    re_path(r'^run_suite_tree/$', case.run_tree_case),
   	# 测试报告
    re_path(r'^reports/$', report.report_view),
    re_path(r'^reports/(?P<pk>\d+)/$', report.report_pk_view),
    # 下载测试报告
    re_path(r'^download/$', report.downreport),

   	# 定时任务
    re_path(r'^schedule/$', schedule.schedule_view),
    re_path(r'^schedule/(?P<pk>\d+)/$', schedule.schedule_pk_view),
]