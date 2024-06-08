<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                    v-if="permissions.includes('add')"
                        :disabled="PycodedebugActivate"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="dialogVisible = true"
                    >新增文件
                    </el-button>

                    <el-button
                    v-if="permissions.includes('delete')"
                        :disabled="PycodedebugActivate"
                        style="margin-left: 20px"
                        type="danger"
                        icon="el-icon-delete"
                     
                        size="mini"
                        @click="delSelectionPycodefile"
                        title="批量删除"
                    >批量删除</el-button>

                    <el-button
                    v-if="permissions.includes('add')"
                        v-show="PycodedebugActivate"
                        type="primary"
                        size="mini"
                        icon="el-icon-lock"
                        @click="save = !save"
                        round
                    >保存
                    </el-button>

                    <el-button
                    v-if="permissions.includes('add')"
                        v-show="PycodedebugActivate"
                        icon="el-icon-caret-right"
                        type="success"
                        size="mini"
                        @click="run = !run"
                        round
                    >运行
                    </el-button>

                    <el-dialog
                        title="添加文件"
                        :visible.sync="dialogVisible"
                        width="30%"
                        align="center"
                    >
                        <el-form :model="pycodefileForm"
                                 :rules="rules"
                                 ref="pycodefileForm"
                                 label-width="100px"
                                 class="project">
                            <el-form-item label="文件名称" prop="name">
                                <el-input v-model="pycodefileForm.name" clearable></el-input>
                            </el-form-item>
                            <el-form-item label="文件描述" prop="desc">
                                <el-input v-model="pycodefileForm.desc" clearable></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('pycodefileForm')">确 定</el-button>
                      </span>
                    </el-dialog>
                    <el-dialog
                        title="编辑文件信息"
                        :visible.sync="editVisible"
                        width="30%"
                    >
                        <el-form :model="pycodefileForm"
                                 :rules="rules"
                                 ref="pycodefileForm"
                                 label-width="100px"
                                 class="project">
                            <el-form-item label="修改名称" prop="name">
                                <el-input v-model="pycodefileForm.name" clearable></el-input>
                            </el-form-item>
                            <el-form-item label="修改描述" prop="desc">
                                <el-input v-model="pycodefileForm.desc" clearable></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                            <el-button @click="handlecancle">取 消</el-button>
                            <el-button type="primary" @click="handleConfirm('pycodefileForm')">确 定</el-button>
                        </span>
                    </el-dialog>

                    <el-button
                        :disabled="!PycodedebugActivate"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="quitEditPycode"
                    >返回列表</el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px" v-if="PycodedebugActivate">
                <PycodeDebug
                    :id="pycodeid"
                    :save = "save"
                    :run="run"
                >
                </PycodeDebug>
            </el-main>
        </el-container>

        <el-container v-show="!PycodedebugActivate">
            <el-header style="padding: 0; height: 50px;">
                <div style="padding-top: 8px; padding-left: 30px; overflow: hidden">
                    <el-row :gutter="50">
                        <el-col :span="6">
                            <el-input placeholder="请输入变量名称"  clearable v-model="search">
                                <el-button slot="append" icon="el-icon-search" @click="PycodeList"></el-button>
                            </el-input>
                        </el-col>

                    </el-row>
                </div>
            </el-header>

            <el-container>
                <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                    <div style="position: fixed; bottom: 0; right:0; left: 230px; top: 150px">
                        <el-table
                        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
                            v-loading="loading"
                            element-loading-text="正在玩命加载"
                            highlight-current-row
                            :data="pycodeData.results"
                            :show-header="pycodeData.results.length !== 0 "
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
                                label="文件名"
                                width="200"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.name}}</div>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="简要描述"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.desc}}</div>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="创建人"
                                width="150"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.create_user}}</div>

                                </template>
                            </el-table-column>
                            <el-table-column
                                label="更新时间"
                                width="250"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.update_time | datetimeFormat}}</div>

                                </template>
                            </el-table-column>
                            <el-table-column
                            width="260"
                            label="操作"
                            >
                                <template slot-scope="scope">
                                    <el-row v-show="currentRow === scope.row">
                                        <el-button
                                            v-show="pycodeData.count !== 0 && scope.row.name !== 'debugtalk.py' && permissions.includes('change')"
                                            type="info"
                                            size="mini"
                                            @click="handleEditPycodeData(scope.$index, scope.row)"
                                            title="编辑基本信息"
                                        >编辑
                                        </el-button>
                                        <el-button
                                            v-show="pycodeData.count !== 0 && permissions.includes('change')"
                                            type="success"
                                            size="mini"
                                            @click="handleEditPycode(scope.row.id)"
                                            title="编辑脚本内容"
                                        >脚本
                                        </el-button>
                                        <el-button
                                            v-show="pycodeData.count !== 0 && scope.row.name !== 'debugtalk.py' && permissions.includes('delete')"
                                            type="danger"
                                            size="mini"
                                            @click="handleDelPycode(scope.row.id)"
                                            title="删除"
                                        >
                                        删除
                                        </el-button>

                                    </el-row>
                                </template>
                            </el-table-column>
                        </el-table>
                        <el-col :span="5">
                            <el-pagination
                                :page-size="5"
                                v-show="pycodeData.count !== 0 "
                              style="padding-top:10px;"
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="pycodeData.count"
                            >
                            </el-pagination>
                        </el-col>
                    </div>
                </el-main>
            </el-container>
        </el-container>
    </el-container>

</template>

<script>
    import PycodeDebug from './components/PycodeDebug'
    import * as debugtalkapi from '../../restful/debugtalk'
     import {getpermissions} from "../../restful/userinfo";
    export default {
        components: {
            PycodeDebug
        },

        data() {
            return {
                 permissions:[],
                back: false,
                del: false,
                save: false,
                run: false,
                PycodedebugActivate: false,
                respConfig: '',
                dialogVisible: false,
                editVisible: false,
                pycodefileForm: {
                    name: '',
                    desc: '',
                    create_user: this.$store.state.useractualname,
                    project: this.$route.params.id,
                    id: ''
                },
                search: '',
                pycodeData: {
                    count: 0,
                    results: []
                },
                currentRow: '',
                currentPage: 1,
                selectTestData: [],
                rules: {
                    name: [
                        {required: true, message: '请输入文件全称', trigger: 'blur'},
                        {min: 1, max: 30, message: '最多不超过30个字符', trigger: 'blur'}
                    ],
                    desc: [
                        {required: false, message: '简要描述下该文件', trigger: 'blur'},
                        {min: 0, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ]
                },
                pycodeid: '',
                loading: true
            }
        },
        methods: {
            quitEditPycode(){
                this.$confirm('请确认是否已保存最新代码，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    this.PycodedebugActivate=false;
                });
            },
            cellMouseEnter(row) {
                this.currentRow = row;
            },

            cellMouseLeave(row) {
                this.currentRow = '';
            },
            getpermissions() {
                getpermissions({app_label:"test_runner",model:"pycode"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            handleSelectionChange(val) {
                this.selectTestData = val;
            },

            handleEditPycode(index){
                this.PycodedebugActivate = true;
                this.pycodeid = index;
            },
            handlecancle(){
                this.editVisible = false;
                this.pycodefileForm.name = '';
                this.pycodefileForm.desc = '';
                this.pycodefileForm.id = '';
            },
            handleDelPycode(index){
                this.$confirm('此操作将永久删除该测试文件，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    debugtalkapi.deletePycode(index, {params:{project: this.$route.params.id}}).then(resp => {
                        if (resp.data.success){
							this.$notify.success(resp.data.msg);
						} else {
							this.$notify.error(resp.data.msg);
						}
						
                        this.PycodeList();
						this.currentPage = 1
                    })
                })
            },
            delSelectionPycodefile() {
                if (this.selectTestData.length !== 0) {
                    this.$confirm('此操作将永久删除勾选的文件，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        debugtalkapi.delAllPycode(this.selectTestData,{project: this.$route.params.id}).then(resp => {
                            this.$notify.success('删除成功');
                            this.PycodeList();
                        })
                    })
                } else {
                    this.$notify.warning({
                        message: '请至少勾选一个文件'
                    })
                }
            },
            handleCurrentChange(val) {
                debugtalkapi.getPycodeListPaginationBypage({
                    params: {
                        page: this.currentPage,
                        project: this.pycodefileForm.project,
                        search: this.search
                    }
                }).then(resp => {
                    this.pycodeData = resp.data;
                })
            },
            handleConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.dialogVisible = false;
                        this.editVisible = false;
                        let obj;
                        if (this.pycodefileForm.id === '') {
                            obj = debugtalkapi.addPycode(this.pycodefileForm,{project: this.$route.params.id});
                        } else {
                            obj = debugtalkapi.updatePycode(this.pycodefileForm.id,{project: this.$route.params.id},this.pycodefileForm);
                        }
                        obj.then(resp => {
                            if (this.pycodefileForm.id === '') {
								if (resp.data.success){
									this.$notify.success(resp.data.msg);
									this.currentPage = 1
								} else {
									this.$message.error(resp.data.msg);
								}
                                
                            }else {
								if (resp.data.success){
									this.$notify.success(resp.data.msg);
									this.currentPage = 1
								} else {
									this.$notify.error(resp.data.msg);
								}
                              
                            }
                            this.PycodeList();
                            this.pycodefileForm.name = '';
                            this.pycodefileForm.desc = '';
                            this.pycodefileForm.id = '';
                        })
                    } else {
                        if (this.pycodefileForm.id !== '') {
                            this.editVisible = true;
                        } else {
                            this.dialogVisible = true;
                        }
                        return false;
                    }
                });
            },

            handleEditPycodeData(index, row){
                this.editVisible = true;
                this.pycodefileForm.name = row['name'];
                this.pycodefileForm.desc = row['desc'];
                this.pycodefileForm.id = row['id'];
            },

            PycodeList(){
                debugtalkapi.getPycodeList({
                    params: {
                        project: this.$route.params.id,
                        search: this.search
                    }
                }).then(resp => {
                    this.pycodeData = resp.data;
                    this.loading = false;
                })
            }
        },
        name: "RecordPycode",
        mounted() {
            this.$nextTick( function () {
                this.PycodeList();
                
            });
            this.getpermissions();
        }
    }
</script>

<style scoped>


</style>
