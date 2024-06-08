<template>
    <el-container>
        <el-header style="padding-top: 10px; height: 50px;">
            <div style="overflow: hidden">
                <el-row :gutter="50">
         
                    <el-col :span="7"
                    style="padding-left: 25px; padding-right: 0px; width: 25%;"
                     >
                         &nbsp用例类型:                    
                      <el-select v-model="value" placeholder="请选择"
                       @change="getTestList">
                            <el-option                         
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                           
                            </el-option>
                            
                        </el-select>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="请输入用例名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search" @click="getTestList"></el-button>
                        </el-input>
                    </el-col>           
                </el-row>
            </div>
        </el-header>

     
        
        <el-container>
      

       
            <el-main style="padding: 0; margin-left: 10px; height:700px">

           
                <div style="position: fixed; bottom: 0; right:0; left: 500px; top: 160px;">
                    <el-dialog
                        v-if="dialogTableVisible"
                        :visible.sync="dialogTableVisible"
                        width="70%"
                        :modal-append-to-body="false"
                    >
                        <report :summary="summary"></report>
                    </el-dialog>

                    <el-dialog
                        title="运行测试用例集"
                        :visible.sync="dialogTreeVisible"
                        width="45%"
                        :modal-append-to-body="false"
                    >
                        <div>
                            <div>
                                <el-row :gutter="2">
                                    <el-col :span="8">
                                        <el-switch
                                            style="margin-top: 10px"
                                            v-model="asyncs"
                                            active-color="#13ce66"
                                            inactive-color="#ff4949"
                                            active-text="异步执行"
                                            inactive-text="同步执行">
                                        </el-switch>
                                    </el-col>
                                    <el-col :span="10">
                                        <el-input
                                            v-show="asyncs"
                                            clearable
                                            placeholder="请输入报告名称"
                                            v-model="reportName"
                                            :disabled="false">
                                        </el-input>

                                    </el-col>
                                </el-row>
                            </div>
                            <div style="margin-top: 20px">
                                <el-input
                                    value
                                    placeholder="输入关键字进行过滤"
                                    v-model="filterText"
                                    size="medium"
                                    clearable
                                    prefix-icon="el-icon-search"
                                >
                                </el-input>

                                <el-tree
                                    style="overflow-y: scroll;height: 400px"                                    
                                    :data="dataTree"
                                    :check-strictly="false"
                                    :filter-node-method="filterNode"
                                    show-checkbox
                                    check-on-click-node
                                    node-key="id"
                                    ref="tree"
                                    highlight-current
                                    :props="defaultProps"
                                >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                                </el-tree>
                            </div>

                        </div>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogTreeVisible = false">取 消</el-button>
                        <el-button type="primary" @click="runTree">确 定</el-button>
                        </span>
                    </el-dialog>
                    <el-table
                    :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                        highlight-current-row
                        v-loading="loading"
                        ref="multipleTable"
                        :data="testData.results"
                        :show-header="testData.count !== 0 "
                        stripe
                        height="600px"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        @selection-change="handleSelectionChange"
                    >
                        <el-table-column
                            type="selection"
                            width="55"
                        >
                        </el-table-column>

                        <el-table-column
                            label="用例名称"
                           
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.name}}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            
                            label="API个数"
                            width="100"
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.length}} 个</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            label="用例类型"
                             width="150"
                        >
                            <template slot-scope="scope">
                                <el-tag v-if="scope.row.tag===1">冒烟用例</el-tag>
                                <el-tag v-if="scope.row.tag===2" type="success">集成用例</el-tag>
                                <el-tag v-if="scope.row.tag===3" type="danger">监控脚本</el-tag>
                                <el-tag v-if="scope.row.tag===4" type="info">回归用例</el-tag>
                                <el-tag v-if="scope.row.tag===5" type="primary">系统用例</el-tag>
                                <el-tag v-if="scope.row.tag===6" type="warning">空库用例</el-tag>
                            </template>
                        </el-table-column>

                        <el-table-column
                            label="创建人"
                            width="100"
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.create_user}}</div>

                            </template>
                        </el-table-column>
                        <el-table-column
                            label="更新时间"
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.update_time|datetimeFormat}}</div>

                            </template>
                        </el-table-column>

                        <el-table-column
                            label="操作"
                             width="300"
                        >
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                    v-if="permissions.includes('change')"
                                        type="info"
                                        size="mini"
                                        @click="handleEditTest(scope.row.id)"
                                    >编辑</el-button>

                                    <el-button
                                        type="primary"
                                  v-if="permissions.includes('add')"
                                        size="mini"
                                        @click="handleRunTest(scope.row.id, scope.row.name)"
                                    >运行</el-button>

                                    <el-button
                                        type="success"
                                      v-if="permissions.includes('add')"
                                        size="mini"
                                        @click="handleCopyTest(scope.row.id)"
                                    >复制
                                    </el-button>

                                    <el-button
                                    v-if="permissions.includes('delete')"
                                        type="danger"                                     
                                       size="mini"
                                        @click="handleDelTest(scope.row.id)"
                                    >删除
                                    </el-button>
                                </el-row>
     
                            </template>

                        </el-table-column>  

                    </el-table>  
               
                    <div>    
                        <el-footer style="padding-top:10px;">
                        
                            <el-row :gutter="50">
                                <el-col :span="9">
                                    <el-pagination
                                        @current-change="handleCurrentChange"
                                        :current-page.sync="currentPage"
                                        :page-size="5"
                                        v-show="testData.count !== 0 "                                
                                        layout="total, prev, pager, next, jumper"
                                        :total="testData.count"
                                    >
                                    </el-pagination>
                                </el-col>
                            </el-row>
                        
                        </el-footer>
                    </div> 

                </div>
    
 
            </el-main>


         </el-container> 
    </el-container>
    
</template>

<script>
    import Report from '../../../reports/DebugReport'
    import * as apicase from '../../../../restful/apicase'
    import {getTree } from "../../../../restful/tree";
    import * as runapi from '../../../../restful/runapi'
    export default {

        name: "TestList",
        components: {
            Report
        },

        props: {
            run: Boolean,
            back: Boolean,
            project: {
                require: true
            },
            host: {
                require: true
            },
            node: {
                require: false
            },
            permissions:{
                require: true
            },
            del: Boolean
        },

        watch: {
            filterText(val) {
                this.$refs.tree.filter(val);
            },

            run() {
                this.asyncs = false;
                this.reportName = "";
                this.getTree();
            },
            node() {
                this.search = '';
                this.getTestList();
            },

            back() {
                this.getTestList();
            },

            del() {
                if (this.selectTest.length !== 0) {
                    this.$confirm('此操作将永久删除测试用例集，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        apicase.delAllTest({data: this.selectTest}).then(resp => {
                            this.getTestList();
                        })
                    })
                } else {
                    this.$notify.warning({
                        title: '提示',
                        message: '请至少选择一个用例集',
                        duration: 1000
                    })
                }
            }
        },
        data() {
            return {
                search: '',
                options: [
                    {
                    value: '',
                    label: '全部'
               },{
                    value: '1',
                    label: '冒烟用例'
               },
               {
                    value: '2',
                    label: '集成用例'
               },
                {
                    value: '3',
                    label: '监控脚本'
               },
                {
                    value: '4',
                    label: '回归用例'
               },
               {
                    value: '5',
                    label: '系统用例'
               },
               {
                    value: '6',
                    label: '空库用例'
               },
                ],
                
                value:'',
                reportName: '',
                asyncs: false,
                filterText: '',
                expand: '&#xe65f;',
                dialogTreeVisible: false,
                dataTree: {},
                loading: false,
                dialogTableVisible: false,
                selectTest: [],
                summary: {},
                currentRow: '',
                testData: {
                    count: 0,
                    results: []
                },
                currentPage: 1,
                defaultProps: {
                children: 'children',
                label: 'label'
                },
            }
            
        },

        methods: {
            getTree() {
                getTree(this.$route.params.id, {params: {type: 2}}).then(resp => {
                    this.dataTree = resp.tree;
                    this.dialogTreeVisible = true;
                })
            },

            filterNode(value, data) {
                if (!value) return true;
                return data.label.indexOf(value) !== -1;
            },

            runTree() {
                this.dialogTreeVisible = false;
                const relation = this.$refs.tree.getCheckedKeys();
                if (relation.length === 0) {
                    this.$notify.error({
                        title: '提示',
                        message: '请至少选择一个节点',
                        duration: 1500
                    });
                } else {
                    runapi.runSuiteTree({
                        "host":this.host,
                        "project": this.project,
                        "relation": relation,
                        "async": this.asyncs,
                        "name": this.reportName
                    }).then(resp => {
                        if (resp.hasOwnProperty("status")) {
                            this.$message.info({
                                message: resp.msg,
                                duration: 1500
                            });
                        } else {
                            this.summary = resp;
                            this.dialogTableVisible = true;
                        }
                    })
                }
            },

            handleRunTest(id, name) {
                this.loading = true;
                runapi.runTestByPk(id, {params: {project: this.project, name: name,host:this.host}}).then(resp => {
                    this.summary = resp;
                    this.dialogTableVisible = true;
                    this.loading = false;
                }).catch(resp => {
                    this.loading = false;
                })
            },
            handleCurrentChange(val) {
                apicase.getTestPaginationBypage({
                    params: {
                        page: this.currentPage,
                        project: this.project,
                        tag:this.value,
                        node: this.node,
                        search: this.search
                    }
                }).then(resp => {
                    this.testData = resp;
                })
            },

            handleEditTest(id) {
                apicase.editTest(id).then(resp => {
                    this.$emit('testStep', resp);
                })
            },

            handleCopyTest(id) {
                this.$prompt('请输入用例集名称', '提示', {
                    confirmButtonText: '确定',
                    inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                    inputErrorMessage: '用例集不能为空'
                }).then(({value}) => {
                    apicase.coptTest(id, {
                        'name': value,
                        'relation': this.node,
                        'project': this.project
                    }).then(resp => {
						this.getTestList();
						this.currentPage = 1;
                        if (resp.success) {
                            this.$message.success(resp.msg);
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            },

            handleSelectionChange(val) {
                this.selectTest = val;
            },

            handleDelTest(id) {
                this.$confirm('此操作将永久删除该测试用例集，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    apicase.deleteTest(id).then(resp => {
						this.getTestList();
						this.currentPage = 1;
                        if (resp.success) {
                            this.$message.success(resp.msg)
                        } else {
                            this.$message.error(resp.msg)
                        }
                    })
                })
            },
            getTestList() {
                apicase.testList({
                    params: {
                        project: this.project,
                        node: this.node,                        
                        search: this.search,
                        tag:this.value
                    }
                }).then(resp => {
                    this.testData = resp;
                })
            },
            cellMouseEnter(row) {
                this.currentRow = row;
            },

            cellMouseLeave(row) {
                this.currentRow = '';
            }
        },
        mounted() {
           this.getTestList()
        }
    }
</script>

<style scoped>

</style>
