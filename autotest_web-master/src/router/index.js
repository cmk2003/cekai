import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/pages/home/Home'
import Register from '@/pages/auth/Register'
import Login from '@/pages/auth/Login'
import ProjectList from '@/pages/project/ProjectList'
import ProjectDetail from '@/pages/project/ProjectDetail'
import DebugTalk from '@/pages/pycode/RecordPycode'
import RecordApi from '@/pages/fastrunner/api/RecordApi'
import AutoTest from '@/pages/fastrunner/case/AutoTest'
import GlobalEnv from '@/pages/variables/GlobalEnv'
import ReportList from '@/pages/reports/ReportList'
import RecordConfig from '@/pages/fastrunner/config/RecordConfig'
import Tasks from '@/pages/task/Tasks'
import HostAddress from '@/pages/variables/HostAddress'
import DataBase from '@/pages/project/DataBase';
import webtestcaselist from "@/pages/uitestpage/webtest/webtestcaselist"
import UICaseTestPlan from "@/pages/uitestpage/uitestcaseplan/UICaseTestPlan"
import UIReportList from "@/pages/reports/UIReportList"
import UITasks from '@/pages/uitestpage/task/Tasks'
import UiGlobalEnv from '@/pages/uitestpage/uivariables/UiGlobalEnv';
import UIRecordConfig from '@/pages/uitestpage/config/UIRecordConfig';
import DataStatistics from '@/pages/project/DataStatistics';
import homelist from '@/pages/project/index';
import UserList from '@/pages/userpage/users';
import UserGroup from '@/pages/userpage/usergroup';
Vue.use(Router);

export default new Router({
    mode: 'history',
    routes: [{
            path: '/testrunner/register',
            name: 'Register',
            component: Register,
            meta: {
                title: '用户注册'
            }
        }, {
            path: '/testrunner/login',
            name: 'Login',
            component: Login,
            meta: {
                title: '用户登录'
            }
        }, {

            path: '/testrunner',
            name: 'Index',
            component: Home,
            meta: {
                title: '首页',
                requireAuth: true
            },

            children: [{
                    name: 'homelist',
                    path: 'index_list',
                    component: homelist,
                    meta: {
                        title: '系统管理',
                        requireAuth: true,
                    }
                },
                {
                    name: 'UserList',
                    path: 'UserList',
                    component: UserList,
                    meta: {
                        title: '用户管理',
                        requireAuth: true,
                    }
                },
                {
                    name: 'UserGroup',
                    path: 'UserGroup',
                    component: UserGroup,
                    meta: {
                        title: '权限管理',
                        requireAuth: true,
                    }
                },
                {
                    name: 'ProjectList',
                    path: 'project_list',
                    component: ProjectList,
                    meta: {
                        title: '项目列表',
                        requireAuth: true,
                    }
                },
                {
                    name: 'DataStatistics',
                    path: 'Data_Statistics/:id',
                    component: DataStatistics,
                    meta: {
                        title: '数据统计',
                        requireAuth: true,
                    }
                },
                {
                    name: 'DataBase',
                    path: 'DataBase_list/:id',
                    component: DataBase,
                    meta: {
                        title: '数据库配置',
                        requireAuth: true,
                    }
                },
                {
                    name: 'ProjectDetail',
                    path: 'project/:id/dashbord',
                    component: ProjectDetail,
                    meta: {
                        title: '项目预览',
                        requireAuth: true,
                    }

                },
                {
                    name: 'DebugTalk',
                    path: 'debugtalk/:id',
                    component: DebugTalk,
                    meta: {
                        title: '编辑驱动',
                        requireAuth: true,
                    }

                },
                {
                    name: 'RecordApi',
                    path: 'api_record/:id',
                    component: RecordApi,
                    meta: {
                        title: '接口模板',
                        requireAuth: true
                    }

                },
                {
                    name: 'AutoTest',
                    path: 'auto_test/:id',
                    component: AutoTest,
                    meta: {
                        title: '自动化测试',
                        requireAuth: true
                    }

                },
                {
                    name: 'RecordConfig',
                    path: 'record_config/:id',
                    component: RecordConfig,
                    meta: {
                        title: '配置管理',
                        requireAuth: true
                    }

                },
                {
                    name: 'GlobalEnv',
                    path: 'global_env/:id',
                    component: GlobalEnv,
                    meta: {
                        title: '全局变量',
                        requireAuth: true
                    }

                },
                {
                    name: 'Reports',
                    path: 'reports/:id',
                    component: ReportList,
                    meta: {
                        title: '历史报告',
                        requireAuth: true
                    }

                },

                {
                    name: 'Task',
                    path: 'tasks/:id',
                    component: Tasks,
                    meta: {
                        title: '定时任务',
                        requireAuth: true
                    }

                },
                {
                    name: 'HostIP',
                    path: 'host_ip/:id',
                    component: HostAddress,
                    meta: {
                        title: 'HOST配置',
                        requireAuth: true
                    }

                },
                {
                    name: "webtestcaselist",
                    path: 'webtestcaselist/:id',
                    component: webtestcaselist,
                    meta: {
                        title: 'Web测试用例',
                        requireAuth: true
                    }
                },
                {
                    name: "UICaseTestPlan",
                    path: 'UICaseTestPlan/:id',
                    component: UICaseTestPlan,
                    meta: {
                        title: 'UI测试计划',
                        requireAuth: true
                    }
                },
                {
                    name: "UIRecordConfig",
                    path: 'UIRecordConfig/:id',
                    component: UIRecordConfig,
                    meta: {
                        title: 'UI页面配置',
                        requireAuth: true
                    }
                },
                {
                    name: "UiGlobalEnv",
                    path: 'UiGlobalEnv/:id',
                    component: UiGlobalEnv,
                    meta: {
                        title: 'UI全局变量',
                        requireAuth: true
                    }
                },
                {
                    name: "UIReportList",
                    path: 'UIReportList/:id',
                    component: UIReportList,
                    meta: {
                        title: 'UI测试报告',
                        requireAuth: true
                    }
                }, {
                    name: "UItasks",
                    path: 'uitasks/:id',
                    component: UITasks,
                    meta: {
                        title: 'UI定时任务',
                        requireAuth: true
                    }
                }
            ]
        },

    ]
})