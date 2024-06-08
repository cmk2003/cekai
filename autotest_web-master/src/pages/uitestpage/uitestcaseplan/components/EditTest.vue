<template>
    <el-container>
        <el-aside style="margin-top: 10px;">
            <div class="nav-api-side">
                <div class="api-tree">
                    <el-input
                        placeholder="输入关键字进行过滤"
                        v-model="filterText"
                        size="medium"
                        clearable
                        prefix-icon="el-icon-search"
                    >
                    </el-input>

                    <el-tree
                        @node-click="handleNodeClick"
                        :data="dataTree"
                        node-key="id"
                        :default-expand-all="false"
                        :expand-on-click-node="false"
                        highlight-current
                        :filter-node-method="filterNode"
                        ref="tree2"
                    >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                    </el-tree>
                </div>

            </div>

        </el-aside>

        <el-main>
            <div v-show="!editTestStepActivate">

                <el-row :gutter="20">
                        <el-col :span="7">
                        <el-input placeholder="请输入用例名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search"   @click="getUIcaseList"></el-button>
                        </el-input>
                    </el-col>   
       
                    <el-col :span="30" style="right: 145px; position: absolute;">
                        <el-input
                            style="width: 400px; text-align: center;    "
                            placeholder="请输入测试用例名称"
                            v-model="testName"
                            clearable
                            v-if="testData.length > 0"
                        >
                            <el-select v-model="testTag" slot="prepend" placeholder="请选择" style="width: 105px">

                                <el-option
                                    v-for="value in tagOptions" :key="value"
                                    :label="value"
                                    :value="value"
                                ></el-option>

                            </el-select>

                            <el-button
                                slot="append"
                                type="success"
                                plain
                                @click="handleClickSave"
                            >保存
                            </el-button>
              
                        </el-input>
                      <el-button
                            type="primary"
                            v-loading="suite_loading"
                            v-model="testName"
                            @click="handleClickRun"
                            v-if="testData.length > 0"
                        >运行
                        </el-button>
                    </el-col>

                </el-row>
                
            </div>

            <div v-show="!editTestStepActivate" style="margin-top: 10px; ">                  
                        
                <el-row :gutter="20">
                    <el-col :span="12">
                        <div
                            v-for="(item,index) in caseData.results"
                            draggable='true'
                            @dragstart="currentAPI = JSON.parse(JSON.stringify(item))"
                            style="cursor: pointer; margin-top: 10px; "
                            :key="index"

                        >
                           
                            <div class="block block_post" >
                                <span class="block-method block_method_post block_method_color">CASE</span>
                                <el-tooltip :content="item.name" placement="top">
                                    <span class="block-method block_url test_demo_ellipsis">{{item.name}}</span>
                                </el-tooltip>
                                <el-tooltip :content="item.describe" placement="top">
                                    <span class="block-summary-description test_demo_ellipsis">{{item.describe}}</span>
                                </el-tooltip>
                            </div>
                


                        </div>
                            <el-footer style="padding-top:30px ; padding-left: 0px" >
                     <el-col :span="10">
                        <el-pagination
                            :page-size="11"
                            v-show="caseData.count !== 0"
                            background
                            @current-change="handlePageChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="caseData.count"
                            style="margin-top: 5px; text-align: center"
                        >
                        </el-pagination>
                    </el-col>
        </el-footer>
                    </el-col>
   
                    <el-col :span="12">
                        <el-dialog
                            v-if="dialogTableVisible"
                            :visible.sync="dialogTableVisible"
                            width="70%"
                        >
                            <report :summary="summary"></report>
                        </el-dialog>

                        <div style="max-height: 600px; overflow: auto"
                             @drop='drop($event)'
                             @dragover='allowDrop($event)'
                        >
                            <div class='test-list'>
                                <span
                                    v-if="testData.length ===0"
                                    style="color: red">温馨提示：<br/>选择左侧相应用例节点显示可拖拽的CASE<br/>从左边拖拽CASE至此区域组成业务用例<br/>
                                    上下拖动此区域接口调整接口调用顺序
                                </span>
                                 <div
                                    v-if="isConfigExist"
                                    class="block block_test"
                                    @mousemove="currentTest = -1"
                                >
                                    <span class="block-method block_method_config block_method_color">{{testData[0].method}}</span>                                    
                                    <input class="block-test-name" v-model="testData[0].name" disabled/>
                               

                                    <el-button
                                        style="position: absolute; right: 12px; top: 8px"
                                        v-show="currentTest === -1"
                                        type="danger"
                                        icon="el-icon-delete"
                                        circle size="mini"
                                        @click="testData.splice(index, 1)"
                                    >
                                    </el-button>
                                </div>
                      
                                <draggable
                                    v-model="testData"
                                    group="test"
                                   @start="onStart" 
                                   @end="onEnd"
                                    :sort= "true" 
                                    force-fallback="true"
                                    animation="200"
                                >
                                    <div
                                        v-for="(test, index) in testData"
                                        :key="index"
                                        class="block block_test"
                                        @mousemove="currentTest = index"
                                     v-if="test.method !== 'config'"
                                    >
                                        <span
                                            class="block-method block_method_test block_method_color">CASE</span>
                                    
                                        <el-tooltip :content="test.name" placement="top">
                                        <span class="block-test-name test_demo_ellipsis"  >{{test.name}}</span>
                                        </el-tooltip>
                                        <el-tooltip :content="test.describe" placement="top">
                                        <span class="block-test-name test_demo_ellipsis" >{{test.describe}}</span>
                                        </el-tooltip>
                                        <el-button
                                            style="position: absolute; right: 84px; top: 8px"
                                            v-show="currentTest === index"
                                            type="info"
                                            icon="el-icon-edit"
                                            circle size="mini"
                                            @click="editTestStepActivate = true"
                                                                                      
                                            title="编辑"
                                        >
                                        </el-button>

                                        <el-button
                                            style="position: absolute; right: 48px; top: 8px"
                                            v-show="currentTest === index"
                                            type="success"
                                            icon="el-icon-caret-right"
                                            circle size="mini"
                                            @click="handleSingleRun"
                                            title="运行"
                                        >
                                        </el-button>

                                        <el-button
                                            style="position: absolute; right: 12px; top: 8px"
                                            v-show="currentTest === index"
                                            type="danger"
                                            icon="el-icon-delete"
                                            circle size="mini"
                                            @click="testData.splice(index, 1)"
                                            title="删除"
                                        >
                                        </el-button>
                                    </div>
                                </draggable>
                            </div>

                        </div>
                    </el-col>
                </el-row>
            </div>

            <test-body               
                v-if="editTestStepActivate"
                :response="testData[currentTest]"              
                :config="config"     
                            
                v-on:escEdit="editTestStepActivate = false"
                v-on:getNewBody="handleNewBody"
            >
            </test-body>
        </el-main>

    </el-container>


</template>

<script>
    import draggable from 'vuedraggable'
    import TestBody from '../components/TestBody'
    import Report from '../../../uitestpage/webtest/components/DebugReport'
    import * as UICASEAPI from '../../../../restful/UIcase'
     import {getTree,updateTree } from "../../../../restful/tree";

    export default {
        components: {
            draggable,
            TestBody,
            Report
                
        },
        computed: {

            isConfigExist: {
                get() {
                    if (this.testData.length > 0 && this.testData[0].method === "config" && this.testData[0].name !== '请选择') {
                        return true;
                    }
                    return false;
                }
            }
        },
        props: {
                  
       
            project: {
                require: true
            },
            config: {
                require: true
            },  
            node: {
                require: true
            },
            testStepResp: {
                require: false
            },
            back: Boolean
        },

        name: "EditTest",
        watch: {
            config() {
               
                const temp = {body: {name: this.config, method: 'config'},method:'config',name:this.config};
                if ((this.testData.length === 0 || this.testData[0].body.method !== 'config') && this.config !== '请选择') {
                    this.testData.splice(0, 0, temp)
                } else {
                    if (this.config !== '请选择') {
                        this.testData.splice(0, 1, temp)
                    }

                }

            },
            back() {
                this.editTestStepActivate = false;
              
            },


            filterText(val) {
                this.$refs.tree2.filter(val);
            },
            testStepResp() {

                try {
                    this.testName = this.testStepResp.case.name;
                    this.testId = this.testStepResp.case.id;
                    this.testTag = this.testStepResp.case.tag;
                    this.relation = this.testStepResp.case.relation;
                    this.testData = JSON.parse(JSON.stringify(this.testStepResp.step))
                } catch (e) {
                    this.testName = '';
                    this.testId = '';
                    this.testTag = '集成用例';
                    this.testData = JSON.parse(JSON.stringify(this.testStepResp))
                }
            }
        },

        data() {
            return {
                tagOptions: {
                    1: '冒烟用例',
                    2: '集成用例',
                    3: '监控脚本',
                    4: '回归用例',
                    5: '系统用例',
                    6: '空库用例'
                },
                suite_loading: false,
                loading: false,
                dialogTableVisible: false,
                editTestStepActivate: false,
                currentPage: 1,
                length: 0,
                testId: '',
                search:"",
                testName: '',
                relation: '',
                testTag: '集成用例',
                currentTest: '',
                currentNode: '',
                currentAPI: '',
                data: '',
                filterText: '',
                expand: '&#xe65f;',
                dataTree: [],
                summary: {},
                caseData: {
                    count: 0,
                    results: []
                },

                testData: []
            }
        },
        methods: {

            handleNewBody(body, newBody) {              
                this.editTestStepActivate = false;
                const step = this.testData[this.currentTest].testplan;                
                const id = this.testData[this.currentTest].id;                
                this.testData[this.currentTest] = {
                    body: newBody.body,
                    newBody: newBody,
                    testplan: step,
                    describe:newBody.describe,
                    id: id,
                    name: newBody.name,                  
                    method:newBody.method,
                    variables:body.variables                

                };
            },
              onStart() {
                    this.drag = true;
                },
                onEnd() {
                    this.drag = false;
                },
            validateData() {
                if (this.testName === '' || this.testName.length > 100) {
                    this.$notify.warning({
                        title: '提示',
                        duration: 1000,
                        message: '用例集名称必填，不能超过100个字符'
                    });
                    return false
                }

                if (this.testData.length === 0) {
                    this.$notify.warning({
                        title: '提示',
                        duration: 1000,
                        message: '测试用例集至少包含一个用例'
                    });
                    return false
                }

        


                return true;
            },

            addTestSuite() {
                var length = this.testData.length;   
             if (this.testData[0].method === "config") {
                    length -= 1;
                }           
                UICASEAPI.addUITestPlan({
                    length: length,
                    project: this.project,
                    relation: this.node,
                    name: this.testName,
                    body: this.testData,
                    tag: this.testTag
                }).then(resp => {
                    if (resp.success) {
                        this.$emit("addSuccess");
                    } else {
                        this.$message({
                            message: resp.msg,
                            type: 'error',
                            duration: 1000
                        });
                    }
                })
            },

            updateTestSuite() {
                var length = this.testData.length;
                if (this.testData[0].method === "config") {
                    length -= 1;
                }
                UICASEAPI.updateUITestPlan(this.testId, {
                    length: length,
                    name: this.testName,
                    tag: this.testTag,
                    body: this.testData,
                    project: this.project,
                    relation: this.relation
                }).then(resp => {
                    if (resp.success) {
                        this.$emit("addSuccess");
                    } else {
                        this.$message({
                            message: resp.msg,
                            type: 'error',
                            duration: 1000
                        });
                    }
                })
            },

            handleClickSave() {
                if (this.validateData()) {
                    if (this.testId === '') {
                        this.addTestSuite();
                    } else {
                        this.updateTestSuite();
                    }
                }
            },

            handleClickRun() {
                if (this.validateData()) {
                    this.suite_loading = true;
                    UICASEAPI.runSingleTestPlanSuite({
                        config:this.config,                      
                        name: this.testName,
                        body: this.testData,
                        project: this.project
                    }).then(resp => {
                        this.suite_loading = false;
                        this.summary = resp;
                        this.dialogTableVisible = true;
                    }).catch(resp => {
                        this.suite_loading = false;
                    })
                }
            },

            handleSingleRun() {
                this.loading = true;   
                var config = this.config;           
                 if (this.testData.length > 0 && this.testData[0].method === "config") {
                    config = this.testData[0].name;
                }
                UICASEAPI.runSingleTestPlanSuite({                   
                    body: this.testData[this.currentTest],
                    config:config,
                    project: this.project
                }).then(resp => {
                    this.loading = false;
                    this.summary = resp;
                    this.dialogTableVisible = true;
                }).catch(resp => {
                    this.loading = false;
                })
            },

            handlePageChange(val) {
                UICASEAPI.geuicasePaginationBypage({
                    params: {
                        page: this.currentPage,
                        node: this.currentNode,
                        project: this.project,
                        search: this.search
                    }
                }).then(res => {
                    this.caseData = res;
                })
            },

            getUIcaseList() {
                UICASEAPI.getuicase({
                    params: {
                        node: this.currentNode,
                        project: this.project,
                        search: this.search
                    }
                }).then(res => {
                    this.caseData = res;
                })
            },

            getTree() {
                getTree(this.$route.params.id, {
                    params: {
                        type: 3
                    }
                }).then(resp => {
                    this.dataTree = resp['tree'];
                })
            },

            handleNodeClick(node, data) {
                this.currentNode = node.id;
                this.data = data;
                this.getUIcaseList();

            },

            filterNode(value, data) {
                if (!value) return true;
                return data.label.indexOf(value) !== -1;
            },

            dragEnd(event) {
                if (this.testData.length > this.length) {
                    this.testData.splice(this.length, 1)
                }
            },

            drop(event) {
                event.preventDefault();
                this.testData.push(this.currentAPI);
            },
            allowDrop(event) {
                event.preventDefault();
            },

        },
        mounted() {
            this.getTree();
            this.getUIcaseList();
        }
    }
</script>

<style scoped>

    .test-list {
        height: 590px;
    }

    .block_test {
        margin-top: 10px;
        border: 1px solid #49cc90;
        background-color: rgba(236, 248, 238, .4)
    }

    .block_method_test {
        background-color: darkcyan;
    }

    .block_method_config {
        background-color: red;
    }

    .block-test-name {
        width: 350px;
        padding-left: 10px;
        -webkit-box-flex: 1;
        -ms-flex: 1;
        font-family: Open Sans, sans-serif;
        color: #3b4151;
        border: none;
        outline: none;
        background: rgba(236, 248, 238, .4)

    }

    .test_demo_ellipsis {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        
        text-align: left;
    }

</style>
