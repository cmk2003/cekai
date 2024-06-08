<template>
    <el-container>
        <el-header style="padding: 0; height: 50px;">
            <div style=" padding-left: 10px;">
                <el-row :gutter="50">
                    <el-col :span="1">
                        <el-checkbox
                            v-if="apiData.count > 0"
                            v-model="checked"
                            style="padding-top: 14px; padding-left: 2px"
                        >
                        </el-checkbox>
                    </el-col>

                    <el-col :span="6">
                        <el-input placeholder="请输入用例名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search" @click="getUIcaseList"></el-button>
                        </el-input>
                    </el-col>


                </el-row>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px;">
                <el-dialog
                    v-if="dialogTableVisible"
                    :visible.sync="dialogTableVisible"
                    width="70%"
                    
                >
                    <report :summary="summary" ></report>
                </el-dialog>

                <el-dialog
                    title="运行用例"
                    :visible.sync="dialogTreeVisible"
                    width="45%"
                    
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
                                placeholder="输入节点名称进行过滤"
                                v-model="filterText"
                                size="medium"
                                clearable
                                prefix-icon="el-icon-search"
                            >
                            </el-input>

                            <el-tree
                                style="overflow-y: scroll;height: 400px"
                                :filter-node-method="filterNode"
                                :data="dataTree"
                                show-checkbox
                                node-key="id"
                                :expand-on-click-node="false"
                                check-on-click-node
                                :check-strictly="true"
                                :highlight-current="true"
                                ref="tree"
                                
                                
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


                <div style="position: fixed; bottom: 0; right:0; left: 500px; top: 160px">
                    <el-table
                    :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                        highlight-current-row
                        height="700px"
                        ref="multipleTable"
                        :data="apiData.results"
                        :show-header="true"
                        stripe
                        style="width: 100%;"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"                        
                        @selection-change="handleSelectionChange"
                        v-loading="loading"
                    >
                        <el-table-column
                            type="selection"
                            width="70"
                        >
                        </el-table-column>
                   
                        <el-table-column
                            label="用例名称"                            
                            prop="name"
                           show-overflow-tooltip
                        >
            
                        </el-table-column>
                   
                        <el-table-column 
                          label="用例描述"
                          prop="describe"                         
                         show-overflow-tooltip
                        >
        
                        </el-table-column>
                        <el-table-column 
                          label="创建人"
                          prop="create_user"
                          width="150"
                         show-overflow-tooltip
                        >
        
                        </el-table-column>
                        <el-table-column
                        label="更新时间"
                        width="150"                 
                    >
                        <template slot-scope="scope">
                            <span>{{ scope.row.update_time | datetimeFormat }}</span>
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
                                        @click="handleRowClick(scope.row)"
                                    >编辑</el-button>

                                    <el-button
                                    v-if="permissions.includes('add')"
                                        type="success"                                       
                                        size="mini"
                                        @click="handleCopyUIcase(scope.row.id)"
                                    >复制
                                    </el-button>

                                    <el-button
                                    v-if="permissions.includes('add')"
                                        type="primary"                                   
                                        size="mini"
                                        @click="handleRunUIcase(scope.row.id)"
                                    >运行</el-button>
                                    <el-button
                                    v-if="permissions.includes('delete')"
                                        type="danger"                                    
                                        size="mini"
                                        @click="handleDelUIcase(scope.row.id)"
                                    >删除
                                    </el-button>
                                </el-row>
                            </template>
                        </el-table-column>

                    </el-table>
                    <el-col :span="7">
                        <el-pagination
                            style="margin-top: 10px"
                            :page-size="11"
                            v-show="apiData.count !== 0 "                 
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="apiData.count"
                        >
                        </el-pagination>
                    </el-col>
                </div>

            </el-main>
        </el-container>
    </el-container>
</template>

<script>
    import Report from '../../../uitestpage/webtest/components/DebugReport'
    import {getTree } from "../../../../restful/tree";
    import * as UICASEAPI from '../../../../restful/UIcase'
    export default {
        components: {
            Report
        },
        name: "CaseList",
        props: {
      
            run: Boolean,
            back: Boolean,
            node: {
                require: true
            },
            project: {
                require: true
            },
            config: {
                require: true
            },
            permissions:{
                require:true
            },
            del: Boolean
        },
        data() {
            return {
                
                checked:false,
                search: '',
                reportName: '',
                asyncs: false,
                filterText: '',
                loading: false,
                expand: '&#xe65f;',
                dataTree: {},
                dialogTreeVisible: false,
                dialogTableVisible: false,
                summary: {},
                selectUIcase: [],
                currentRow: '',
                currentPage: 1,
                apiData: {
                    count: 0,
                    results: []
                }
            }
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
            back() {
                this.getUIcaseList();
            },
            node() {
                this.search = '';
                this.getUIcaseList();
            },
            checked() {
                if (this.checked) {
                    this.toggleAll();
                } else {
                    this.toggleClear();
                }
            },

            del() {
                if (this.selectUIcase.length !== 0) {
                    this.$confirm('此操作将永久删除用例，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        UICASEAPI.delAlluicase({data: this.selectUIcase}).then(resp => {
                            this.getUIcaseList();
                        })
                    })
                } else {
                    this.$notify.warning({
                        title: '提示',
                        message: '请至少选择一个用例',
                        duration: 1000
                    })
                }
            }
        },

        methods: {
            handleCopyUIcase(id) {
                this.$prompt('请输入用例名称', '提示', {
                    confirmButtonText: '确定',
                    inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                    inputErrorMessage: '用例名称不能为空'
                }).then(({value}) => {
                    UICASEAPI.copyuicase(id, {
                        'name': value
                    }).then(resp => {
                        if (resp.success) {
                            this.getUIcaseList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
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
                    UICASEAPI.runUIcaseTree({
                        "config":this.config,
                        "project": this.project,
                        "relation": relation,
                        "async": this.asyncs,
                        "name": this.reportName,                     
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
            getTree() {
               getTree(this.$route.params.id, {params: {type: 3}}).then(resp => {
                    this.dataTree = resp.tree;
                    this.dialogTreeVisible = true;
                })
            },

            handleSelectionChange(val) {
                this.selectUIcase = val;
            },

            toggleAll() {
                this.$refs.multipleTable.toggleAllSelection();
            },

            toggleClear() {
                this.$refs.multipleTable.clearSelection();
            },
    
            // 查询UIcase列表
            getUIcaseList() {
                UICASEAPI.getuicase({
                    params: {
                        node: this.node,
                        project: this.project,
                        search: this.search
                    }
                }).then(res => {
                    this.apiData = res;
                })
            },

            handleCurrentChange(val) {
                UICASEAPI.geuicasePaginationBypage({
                    params: {
                        page: this.currentPage,
                        node: this.node,
                        project: this.project,
                        search: this.search
                    }
                }).then(res => {
                    this.apiData = res;
                })
            },

            //删除用例
            handleDelUIcase(index) {
                this.$confirm('此操作将永久删除该用例，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    UICASEAPI.deluicase(index).then(resp => {
                        if (resp.success) {
                            this.getUIcaseList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            },

            // 编辑用例
            handleRowClick(row) {
                UICASEAPI.getuicaseSingle(row.id).then(resp => {
                    if (resp.success) {
                        this.$emit('api', resp);
                    } else {
                        this.$message.error(resp.msg)
                    }
                })
            },
            // // 运行API
            // handleRunAPI(id) {
            //     this.loading = true;
            //     UICASEAPI.runAPIByPk(id, {
            //         params: {
            //             host:this.host,
            //             config: this.config
            //         }
            //     }).then(resp => {
            //         this.summary = resp;
            //         this.dialogTableVisible = true;
            //         this.loading = false;
            //     }).catch(resp => {
            //         this.loading = false;
            //     })
            // },
            handleRunUIcase(id) {
                this.loading = true;
                UICASEAPI.runUIcaseByPk(
                    id,
                    {params:{project:this.$route.params.id,
                    config: this.config}  }                  
                
                ).then(resp => {
                    this.summary = resp;
                    this.dialogTableVisible = true;
                    this.loading = false;
                }).catch(resp => {
                    this.loading = false;
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
           
            this.getUIcaseList();
        }
    }
</script>

<style scoped>


</style>
