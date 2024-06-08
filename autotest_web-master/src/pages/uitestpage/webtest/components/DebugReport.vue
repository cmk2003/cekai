<template>

    <div style="overflow-y: scroll; height: 800px">
        <el-table
            :data="[summary]"
            size="medium"
            style="width: 100%"
            border
            stripe
            :header-cell-style="{textAlign:'center', background: '#F8F8FA'}"
            :cell-style="{textAlign:'center'}"
        >
            <el-table-column
                label="测试时间"
                width="160"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.time.start_at|timestampToTime}}</span>
                </template>
            </el-table-column>

            <el-table-column
                label="持续时间"
                width="100"
            >
                <template slot-scope="scope">
                    <span v-text="scope.row.time.duration.toFixed(3)+' 秒'"></span>
                </template>
            </el-table-column>

            <el-table-column
                label="总数"
                width="100"
            >
                <template slot-scope="scope">
                    <el-tag>{{ scope.row.stat.testsRun }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column
                label="成功"
                width="100"
            >
                <template slot-scope="scope">
                    <el-tag type="success">{{ scope.row.stat.successes }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column
                label="失败"
                width="100"
            >
                <template slot-scope="scope">
                    <el-tag type="danger">{{ scope.row.stat.failures }}</el-tag>
                </template>
            </el-table-column>




            <el-table-column
                label="系统环境"
            >
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        
                        <p>Python: {{ scope.row.platform.python_version }}</p>
                        <div slot="reference" class="name-wrapper">
                            <el-tag size="medium">{{ scope.row.platform.platform }}</el-tag>
                        </div>
                    </el-popover>
                </template>
            </el-table-column>

        </el-table>

        <br/>
        <br/>

        <slot v-for="item in summary.details">
            <div>
                <span style="font-weight: bold; font-size: medium">{{item.name}}</span>
                <!-- <el-popover
                    placement="top-start"
                    width="400"
                    trigger="hover"
                >
                    <pre class="code-block">{{item.in_out}}</pre>
                    <el-button slot="reference" round type="text">parameters & output</el-button>
                </el-popover> -->

            </div>
            <el-table
                :data="item.detail"
                style="width: 100%"
                border
                :header-cell-style="{textAlign:'center', background: '#F8F8FA'}"
                :cell-style="{textAlign:'center'}"
            >


                <el-table-column
                    label="名 称"
                >
                    <template slot-scope="scope">
                        <span>{{ scope.row.name }}</span>
                    </template>
                </el-table-column>

 

                <el-table-column
                    label="用例描述"
                >
                    <template slot-scope="scope">
                        <span
                           >{{ scope.row.casedescribe }}</span>
                    </template>
                </el-table-column>

                <el-table-column
                    label="持续时间 (秒)"
                >
                    <template slot-scope="scope">
                        <span>{{ scope.row.time.duration.toFixed(3)+' 秒' }}</span>
                    </template>
                </el-table-column>

                <el-table-column
                    label="测试结果"
                >
                    <template slot-scope="scope">
                        <div :class="scope.row.status">{{ scope.row.status }}</div>
                    </template>
                </el-table-column>

                <el-table-column
                    type="expand"
                    
                >
                    <template slot-scope="props">
                        <el-tabs>
                            <el-tab-pane label="用例脚本信息">
                                <pre class="code-block" v-html="handleRequest(props.row.casebody)"></pre>
                            </el-tab-pane>
                            <el-tab-pane label="用例执行情况" v-if="props.row.casesteps!== null">                      
                            
                                <div   v-for="item in props.row.casesteps" :key="item.rowkeyid" >
                                    <el-collapse accordion >
                                        <el-collapse-item >
                                            <template slot="title">
                                            <div  style="width: 95%"> 

                                                <i v-if="item.status=='passed'" class="el-icon-success" style="color: green; padding-left: 100px"></i> 
                                                <i v-if="item.status=='failed'" class="el-icon-error" style="color: red;padding-left: 100px"></i> 
                                                <span style="widht: 70%">{{item.stepname}}</span>
                                                <span style="float: right; color: #999" >{{item.time.duration}} ms</span>
                                            </div>                             
                                            </template>                                   
                                            <div v-if="item.parameters!==''">                                       
                                                {{item.parameters}}
                                            </div> 
                                                <div class="demo-image__preview" v-if="item.attachments.length!==0"
                                                style="widht: 1000px"
                                                >                       
                                                    <div  v-for="im in item.attachments" :key="im.uid"  style="widht: 1000px">
                                                        <!-- <span class="demonstration">{{im.name}}</span> -->
                                                        <el-image   
                                                            style="width: 800px; height: 500px"
                                                            :src="im.path"
                                                            :preview-src-list=[im.path]>

                                                        >
                                                        <div slot="placeholder" class="image-slot">
                                                            加载中<span class="dot">...</span>
                                                        </div>
                                                        </el-image>
                                                    </div>
                                                </div>
                                        </el-collapse-item>
                                
                                    </el-collapse>
                                        
                                        
                                </div>                           
 
                            </el-tab-pane>
                     
          
                            <el-tab-pane label="异常信息" v-if="props.row.errormessage !== ''">
                                <pre class="code-block" v-text="handleResponse(props.row.errormessage)"></pre>
                            </el-tab-pane>
                        </el-tabs>

                    </template>
                </el-table-column>

            </el-table>
        </slot>
    </div>

</template>

<script>
    export default {
        name: "DebugReport",
        data() {
            return{
                srcList:[
                    'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
                    ]
                
                }
   
        },
        methods: {
            srcListtest(srcurl){
                return [
                    srcurl
                ]
            },
            handleRequest(request) {
                const keys = ["start_timestamp"];
                keys.forEach(function (item) {
                    delete request[item];
                });
                try {
                    request["body"] = JSON.parse(request["body"])
                } catch (e) {
                }
                return request
            },

            handleContent(content) {
                try {
                    content = JSON.parse(content)
                } catch (e) {
                }
                return content
            },
            handleResponse(response) {
                const keys = ["response_time_ms", "encoding", "ok", "reason", "url", "text", "json", "content_size", "content_type"];
                keys.forEach(function (item) {
                    delete response[item];
                });
                return response
            }
        },
        props: {
            summary: {
                require: true
            }
        }
    }
</script>

<style scoped>
.step__content {
    margin-left: 20px;
}
.step {
    line-height: 1.2em;
}
.step__title {
    position: relative;
    padding: 7px 15px 7px 25px;
}
.long-line {
    word-break: break-word;
}
.step__status {
    left: 7px;
    position: absolute;
}
.text_status_passed {
    color: #97cc64;
}
.fa-fw {
    width: 1.28571429em;
    text-align: center;
}
.fa {
    display: inline-block;
    font:
        normal normal normal 14px/1 FontAwesome;
        font-style: normal;
        font-variant-ligatures: normal;
        font-variant-caps: normal;
        font-variant-numeric: normal;
        font-variant-east-asian: normal;
        font-weight: normal;
        font-stretch: normal;
        font-size: inherit;
        line-height: 1;
        font-family: FontAwesome;;
        font-size: inherit;
    text-rendering: auto;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
.fa-check-circle:before {
    content: "";
}
</style>
