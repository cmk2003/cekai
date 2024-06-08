<template>

    <div >
        <ul class="title-project">
            <li class="title-li" title="Test API Project">
                <b>{{projectInfo.name}}</b>
                <b class="desc-li">{{projectInfo.desc}}</b>

            </li>
        </ul>

        <ul class="project_detail">
            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe74a;</i> &nbsp;{{projectInfo.api_count}} 个接口</p>
                <p class="desc-p">接口总数</p>
            </li>

            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe6da;</i> &nbsp;{{projectInfo.case_count}} 个用例</p>
                <p class="desc-p">用例集总数</p>
            </li>

            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xee32;</i> &nbsp;{{projectInfo.config_count}} 套配置</p>
                <p class="desc-p">配置总数</p>
            </li>

            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe692;</i> &nbsp;{{projectInfo.variables_count}} 对变量</p>
                <p class="desc-p">全局变量对数</p>
            </li>
        </ul>

        <ul class="project_detail">
            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe609;</i> &nbsp;{{projectInfo.host_count}} 套环境</p>
                <p class="desc-p">环境总数</p>
            </li>

            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe61e;</i> &nbsp;{{projectInfo.task_count}} 项任务</p>
                <p class="desc-p">定时任务个数</p>
            </li>

            <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe66e;</i> &nbsp;{{projectInfo.report_count}} 个报告</p>
                <p class="desc-p">测试报告总数</p>
            </li>
                <li class="pull-left">
                <p class="title-p"><i class="iconfont">&#xe66e;</i> &nbsp;{{projectInfo.uitestplan}} 个UI测试计划</p>
                <p class="desc-p">UI测试计划总数</p>
            </li>

          
        </ul>
        <div style="display:table;height: 400px;
        width: 1000px; margin-top: 30px;">
          
            <div id='casetable'></div>
            <div id='runcasetable'></div>
        </div>
        
    </div>

</template>

<script>
 import {getProjectDetail,gettagcount,getreporttail } from "../../restful/project";
  
    export default {
        name: "ProjectDetail",
        data() {
            return {
                projectInfo: {},
                option:{
                    title: {
                            text: '用例类型分布'
                        },
                    tooltip: {},
                    xAxis: {
                       
                    },
                    yAxis: {},
                    series: []
                },
                runcasepotion:{
                    title: {
                            text: '用例运行情况'
                        },
                    tooltip: {},
                    xAxis: {},
                    yAxis: {},
                    series: []
                }
            }

        },
        methods: {
            gettagcount(){
                gettagcount({
                    project: this.$route.params.id
                }).then(res =>{            
                    this.option.xAxis={ data: res.typename},
                    this.option.series= [{
                        name: '',
                        type: 'bar',                      
                        barWidth:'35%',
                        data: res.countlist
                    }]
                    let myChart = this.$echarts.init(document.getElementById("casetable"));
                    myChart.setOption(this.option)
                })
            },
            getreporttail(){
                getreporttail({
                    project:this.$route.params.id
                }).then(resp =>{
                    this.runcasepotion.xAxis={
                       data:["通过","失败","异常","跳过"]
                    }
                    this.runcasepotion.series=[{
                        name: '',
                        type: 'bar',         
                        color:'lightgreen',                     
                        barWidth:'25%',
                        data: [resp.successes,resp.failure,resp.error,resp.skippe]
                    }]
                    let runChart = this.$echarts.init(document.getElementById("runcasetable"));
                    runChart.setOption(this.runcasepotion)
                })
            },
            success(resp) {
                this.$notify({
                    message: resp["msg"],
                    type: 'success',
                    duration: 1000
                });
            },
            failure(resp) {
                this.$notify.error({
                    message: resp.msg,
                    duration: 1000
                });
            },

            getProjectDetail() {
                console.log(this.$route.params.id)
                const pk = this.$route.params.id;
                getProjectDetail(pk).then(res => {
                    this.projectInfo = res
                })
            }
        },
        mounted() {
            this.gettagcount();
            this.getProjectDetail();          
            this.getreporttail();
        }
    }

</script>

<style scoped>


    .desc-p {
        padding-top: 10px;
        font-size: 12px;
        color: #b6b6b6;
    }

    .title-p {
        font-size: 18px;
        margin-top: 10px;
    }

    .title-project li a {
        font-size: 12px;
        text-decoration: none;
        color: #a3a3a3;
        margin-left: 20px;

    }

    .pull-left {
        float: left;
        margin-left: 10px;
    }

    .project_detail li {
        margin-top: 10px;
        text-indent: 20px;
        display: inline-block;
        height: 90px;
        width: calc(20% - 1.5px);
        border: 1px solid #ddd;
    }

    .project_detail {
        height: 100px;
        margin-top: 20px;
    }

    .title-project {
        margin-top: 40px;
        margin-left: 10px;
    }

    ul li {
        list-style: none;
    }

    .title-li {
        font-size: 24px;
        color: #607d8b;
    }

    .desc-li {
        margin-top: 10px;
        color: #b6b6b6;
        font-size: 14px;
    }
    #casetable {
      
        height: 400px;
        width: 500px;
        display:table-cell;
    }
    #runcasetable {
 
        height: 400px;
        width: 500px;
      
        display:table-cell;
    }

</style>
