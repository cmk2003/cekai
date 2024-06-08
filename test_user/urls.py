from django.urls import path,re_path
from test_user import views

urlpatterns=[
    #注册
    path('register/',views.register),
    #登录
    path('login/',views.login_system),
    #退出登录
    path('logout/',views.logout_system),


    #获取所有权限数据
    path('permission/',views.permission),
    #获取权限组信息
    re_path(r'^group/$',views.group_view),
    re_path(r'^group/(\d+)/$', views.group_pk_view),

    #用户
    re_path(r'^userinfo/$', views.userinfo_view),
    re_path(r'^userinfo/(?P<pk>\d+)/$', views.userinfo_pk_view),

    # 修改密码
    path('updateuserpassword/', views.updateuserpassword),

    #
    path("test/",views.test)
]