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
                        <el-input placeholder="请输入接口名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search" @click="getAPIList"></el-button>
                        </el-input>
                    </el-col>

                    <el-button                        
                        v-if="permissions.includes('add')"    
                        size="smail"
                        @click="exportAPI"
                    >导出</el-button>
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
                    title="运行接口"
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
                                value
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


                <div style="position: fixed; bottom: 0; right:0; left: 500px; top: 160px">
                    <el-table
                    :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                        highlight-current-row                     
                         height="600px"
                        ref="multipleTable"
                        :data="apiData.results"
                        :show-header="true"
                        stripe
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        style="width: 100%;"
                        @selection-change="handleSelectionChange"
                        v-loading="loading"
                    >
                        <el-table-column
                            type="selection"
                            width="60"
                        >
                        </el-table-column>

                        <el-table-column
                            prop="method"
                            label="接口类型"
                            width="100">
                        </el-table-column>
   
                        <el-table-column
                            label="接口路径"
                           show-overflow-tooltip
                           width=“300”
                        >
                            <template slot-scope="scope">
                                <div class="test_demo_ellipsis">{{scope.row.url}}</div>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="接口名称"                        
                           width=“300”
                           show-overflow-tooltip
                           
                        >
                            <template slot-scope="scope">                             
                                
                             <div class="test_demo_ellipsis">{{scope.row.name}}</div>
                            
                            </template>
                        </el-table-column>
          
                        <el-table-column
                            prop="create_user"
                            label="创建人"
                            width="100">
                        </el-table-column>

   
                         <el-table-column
                            label="更新时间"
                           show-overflow-tooltip
                           width="150"
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.update_time|datetimeFormat}}</div>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column
                            min-width="250"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <div class="block block_post" v-if="scope.row.method.toUpperCase() === 'POST' ">
                                    <span class="block-method block_method_post block_method_color">POST</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                                <div class="block block_get" v-if="scope.row.method.toUpperCase() === 'GET' ">
                                    <span class="block-method block_method_get block_method_color">GET</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                                <div class="block block_put" v-if="scope.row.method.toUpperCase() === 'PUT' ">
                                    <span class="block-method block_method_put block_method_color">PUT</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                                <div class="block block_delete" v-if="scope.row.method.toUpperCase() === 'DELETE' ">
                                    <span class="block-method block_method_delete block_method_color">DELETE</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                                <div class="block block_patch" v-if="scope.row.method.toUpperCase() === 'PATCH' ">
                                    <span class="block-method block_method_patch block_method_color">PATCH</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                                <div class="block block_head" v-if="scope.row.method.toUpperCase() === 'HEAD' ">
                                    <span class="block-method block_method_head block_method_color">HEAD</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                                <div class="block block_options" v-if="scope.row.method.toUpperCase()=== 'OPTIONS' ">
                                    <span class="block-method block_method_options block_method_color">OPTIONS</span>
                                    <span class="block-method block_url">{{scope.row.url}}</span>
                                    <span class="block-summary-description">{{scope.row.name}}</span>
                                </div>

                            </template>
                            
                        </el-table-column> -->

                        <el-table-column
                         width="300"
                        label="操作"
                        >
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button 
                                    v-if="permissions.includes('change')"                                  
                                        type="info"
                                        size="mini"                                     
                                        @click="handleRowClick(scope.row)"
                                    ><span>编辑</span></el-button >

                                    <el-button
                                    v-if="permissions.includes('add')"
                                        type="success"
                                        size="mini"
                                        @click="handleCopyAPI(scope.row.id)"
                                    ><span>复制</span>
                                    </el-button>

                                    <el-button
                                        v-if="permissions.includes('add')"
                                        type="primary "  
                                        size="mini"
                                        @click="handleRunAPI(scope.row.id)"
                                    ><span>运行</span></el-button>
                                    <el-button
                                    v-if="permissions.includes('delete')"
                                        type="danger"
                                        size="mini" 
                                        @click="handleDelApi(scope.row.id)"
                                    ><span>删除</span>
                                    </el-button>
                                </el-row>
                            </template>
                        </el-table-column>

                    </el-table>
                    <el-col :span="7">
                        <el-pagination
                            style="margin-top: 25px"
                            :page-size="5"
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
    import Report from '../../../reports/DebugReport'
    import * as api from '../../../../restful/apipage'
    import {getTree } from "../../../../restful/tree";
    import * as runapi from '../../../../restful/runapi'
    export default {
        components: {
            Report
        },
        name: "ApiList",
        props: {
            host: {
                require: true
            },
            config: {
                require: true
            },
            run: Boolean,
            back: Boolean,
            node: {
                require: true
            },
            project: {
                require: true
            },
            permissions:{
                require: true
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
                selectAPI: [],
                currentRow: '',
                currentPage: 1,
                apiData: {
                    count: 0,
                    results: []
                },
                defaultProps: {
                children: 'children',
                label: 'label'
                },
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
                this.getAPIList();
            },
            node() {
                this.search = '';
                this.getAPIList();
            },
            checked() {
                if (this.checked) {
                    this.toggleAll();
                } else {
                    this.toggleClear();
                }
            },

            del() {
                if (this.selectAPI.length !== 0) {
                    this.$confirm('此操作将永久删除API，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        api.delAllAPI({data: this.selectAPI}).then(resp => {
                            this.getAPIList();
                        })
                    })
                } else {
                    this.$notify.warning({
                        title: '提示',
                        message: '请至少选择一个接口',
                        duration: 1000
                    })
                }
            }
        },

        methods: {
 
            handleCopyAPI(id) {
                this.$prompt('请输入接口名称', '复制接口', {
                    confirmButtonText: '确定',
                    inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                    inputErrorMessage: '接口名称不能为空'
                }).then(({value}) => {
                    api.copyAPI(id, {
                        'name': value
                    }).then(resp => {
						this.getAPIList();
						this.currentPage = 1;
                        if (resp.success) {
							this.$message.success(resp.msg);
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
                    runapi.runAPITree({
                        "host": this.host,
                        "project": this.project,
                        "relation": relation,
                        "async": this.asyncs,
                        "name": this.reportName,
                        "config": this.config
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
                getTree(this.$route.params.id, {params: {type: 1}}).then(resp => {
                    this.dataTree = resp.tree;
                    this.dialogTreeVisible = true;
                })
            },

            handleSelectionChange(val) {
                this.selectAPI = val;
            },

            toggleAll() {
                this.$refs.multipleTable.toggleAllSelection();
            },

            toggleClear() {
                this.$refs.multipleTable.clearSelection();
            },
            // 查询api列表
            getAPIList() {
                api.apiList({
                    params: {
                        node: this.node,
                        project: this.project,
                        search: this.search
                    }
                }).then(res => {
                    this.apiData = res;
                })
            },

            exportAPI(){
                api.exportapi({
                        page: this.currentPage,
                        node: this.node,
                        project: this.project,
                        search: this.search
                    }).then(res => {                       
                   
                        const blob = new Blob([res.data], { type: "application/vnd.ms-excel" });                
                        const url = window.URL.createObjectURL(res.data);                
                        const a = document.createElement("a");                   
                        a.style.display = "none";                
                        a.download = "API.xlsx"                
                        a.href = url;                
                        a.click();

                    if (res.status==200){
                        this.$notify.success({
                        message:"导出成功"
                    })
                    } else{
                        this.$notify.error({
                            message:"导出失败"
                        })
                    }
                })
            },
            handleCurrentChange(val) {
                api.getPaginationBypage({
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

            //删除api
            handleDelApi(index) {
                this.$confirm('此操作将永久删除该API，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    api.delAPI(index).then(resp => {
						this.getAPIList();
						this.currentPage = 1;
                        if (resp.success) {
							this.$message.success(resp.msg);
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            },

            // 编辑API
            handleRowClick(row) {
                api.getAPISingle(row.id).then(resp => {
                    if (resp.success) {
                        this.$emit('api', resp);
                    } else {
                        this.$message.error(resp.msg)
                    }
                })
            },
            // 运行API
            handleRunAPI(id) {
                this.loading = true;
                runapi.runAPIByPk(id, {
                    params: {
                        host:this.host,
                        config: this.config
                    }
                }).then(resp => {
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
            this.getAPIList();
        }
    }
</script>

<style scoped>
    .test_demo_ellipsis {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;        
        text-align: left;
    }

</style>
