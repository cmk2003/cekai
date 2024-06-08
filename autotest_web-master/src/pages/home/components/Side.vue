<template>

    <el-menu
        class="common-side-bar" 
       unique-opened       
        :default-active="$store.state.routerName"
        background-color="#304056"
        text-color="#BFCBD9"
        active-text-color="#318DF1"
        @select="select"

    > 
          <template v-for="item in side_menu" >
                <template v-if="item.subs">
                    <el-submenu :index="item.index" :key="item.index" :disabled="$store.state.routerName === 'homelist'">
                        <template slot="title">                         
                            <span :class="item.code"  slot="title"></span>&nbsp;&nbsp;{{ item.title }}
                        </template>
                        <template v-for="subItem in item.subs" :disabled="$store.state.routerName === 'homelist'">
                            <el-submenu
                                v-if="subItem.subs"
                                :index="subItem.index"
                                :key="subItem.index"
                            >
                                <template slot="title">{{ subItem.title }}</template>
                                <el-menu-item
                                    v-for="(threeItem,i) in subItem.subs"
                                    :key="i"
                                    :index="threeItem.index"
                                >{{ threeItem.title }}</el-menu-item>
                            </el-submenu>
                            <el-menu-item
                                v-else
                                :index="subItem.index"
                                :key="subItem.index"
                            >{{ subItem.title }}</el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else-if="item.title=='项目概况'|| item.title=='测试资料库' ||item.title=='数据库配置'">
                    <el-menu-item :index="item.index" :key="item.index" :disabled="$store.state.routerName === 'homelist'"> 
                        <template slot="title">                         
                            <span :class="item.code"  slot="title"></span>&nbsp;&nbsp;{{ item.title }}
                        </template>
                    </el-menu-item>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index"> 
                        <template slot="title">                         
                            <span :class="item.code"  slot="title"></span>&nbsp;&nbsp;{{ item.title }}
                        </template>
                    </el-menu-item>
                </template>
            </template>
    </el-menu>
</template>

<script>
import bus from '../components/bus';
    export default {
        name: "Side",
        data() {
            return {
                side_menu: [
                    {code:'el-icon-s-tools',
                    title:'系统管理',
                    index:'homelist'},           
                    {title: "项目概况", index: "ProjectDetail", code: "el-icon-collection"},
                    {title:"数据库配置",index:"DataBase",code:"el-icon-coin"},                   
                    { 
                    code: 'el-icon-menu', 
                    index: 'api',                   
                    title: 'API自动化',
                    subs:[
                        {title: "API 模板", index: "RecordApi",},
                        {title: "测试用例", index: "AutoTest", },
                        {title: "配置管理", index: "RecordConfig",},
                        {title: "全局变量", index: "GlobalEnv", },
                        {title: "域名管理", index: "HostIP", },
                        {title: "驱动代码", index: "DebugTalk", },
                        {title: "定时任务", index: "Task",},
                        {title: "历史报告", index: "Reports", },
                     
                    ]
                    },
                    {
                    code: 'el-icon-s-order',
                    index: 'webselemium',
                    title: 'web自动化',
                    subs: [    
                        {
                            index: 'webtestcaselist',
                            title: 'UI用例管理'
                        },
                        {
                            index: 'UICaseTestPlan',
                            title: 'UI测试计划'
                        },
                        {
                            index: 'UIRecordConfig',
                            title: 'UI页面配置'
                        },
                        {
                            index: 'UiGlobalEnv',
                            title: 'UI全局变量'
                        },
                       {
                            index: 'UItasks',
                            title: 'UI定时任务'
                        },
                        {
                            index: 'UIReportList',
                            title: 'UI测试报告'
                        },        
                    ]

                },
                ],
            }
        },

    created() {
        // 通过 Event Bus 进行组件间通信，来折叠侧边栏
        bus.$on('collapse', msg => {
            this.collapse = msg;
            bus.$emit('collapse-content', msg);
        });
    },
        methods:{
            select(url) {
                this.$store.commit('setRouterName',url);
                this.$router.push({name:url});
                this.setLocalValue("routerName",url);
            }
        }
    }
</script>

<style scoped>

    .common-side-bar {
        position: fixed;
        top: 48px;
        border-right: 1px solid #ddd;
        height: 100%;
        width: 202px;
        background-color: #fff;
        display: inline-block;
    }
</style>
