<template>
    <el-container>
        <el-header style="background: #F7F7F7; padding: 0; height: 50px">
            <div class="apiData">
                <div style="padding-top: 10px; margin-left: 10px">
                    <el-button 
                        v-if="permissions.includes('add')"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus"
                        @click="dialogVisible = true">
                        添加数据库
                    </el-button>

                    <el-button style="margin-left: 50px"
                               type="info"
                               round
                               size="small"
                               icon="el-icon-d-arrow-left"
                               :disabled="dataBaseData.previous === null "
                               @click="getPagination(dataBaseData.previous)"
                    >
                        上一页
                    </el-button>

                    <el-button type="info"
                               round
                               size="small"
                               :disabled="dataBaseData.next === null"
                               @click="getPagination(dataBaseData.next)"
                    >
                        下一页
                        <i class="el-icon-d-arrow-right"></i>
                    </el-button>


                    <el-dialog
                        title="添加数据库"
                        :visible.sync="dialogVisible"
                        width="40%"
                        align="center"
                    >
                        <div style="padding-bottom: 10px; cursor: pointer" id="db_type">
                            <el-radio-group v-model="dataBaseForm.type">
                                <el-radio v-for="item in tags"
                                          :key="item.value"
                                          :label="item.value"
                                >{{item.name}}
                                </el-radio>
                            </el-radio-group>
                        </div>

                        <el-form :model="dataBaseForm"
                                 :rules="rules"
                                 ref="dataBaseForm"
                                 label-width="100px"
                        >

                            <el-form-item label="数据库名称" prop="name">
                                <el-input v-model="dataBaseForm.name"></el-input>
                            </el-form-item>

                            <el-form-item label="访问地址" prop="server">
                                <el-input v-model="dataBaseForm.server"></el-input>
                            </el-form-item>

                            <el-form-item label="登陆账号" prop="account">
                                <el-input v-model="dataBaseForm.account"></el-input>
                            </el-form-item>

                            <el-form-item label="登陆密码" prop="password">
                                <el-input v-model="dataBaseForm.password"></el-input>
                            </el-form-item>

                            <el-form-item label="简要描述" prop="desc">
                                <el-input v-model="dataBaseForm.desc"></el-input>
                            </el-form-item>

                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="cancelaction()">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('dataBaseForm')">确 定</el-button>
                      </span>
                    </el-dialog>
                </div>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px">
                <el-table
                :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                    :data="dataBaseData.results"
                    border
                    stripe
                    highlight-current-row
                    style="width: 100%;"
                    :show-header="dataBaseData.results.length > 0"
                >
                    <el-table-column
                        label="数据库名称"
                        width="250"
                        align="center"
                    >
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.type===1" type="">PA</el-tag>
                            <el-tag v-if="scope.row.type===2" type="success">MySQL</el-tag>                       
                            <span
                                style="margin-left: 10px; font-size: 18px; font-weight: bold">{{ scope.row.name }}</span>
                        </template>
                    </el-table-column>

                    <el-table-column
                        label="访问地址"
                        width="300"
                        align="center">
                        <template slot-scope="scope">
                            <div slot="reference" class="name-wrapper">
                                <el-tag type="info" style="font-size: 16px;">{{ scope.row.server }}</el-tag>
                            </div>
                        </template>
                    </el-table-column>


                    <el-table-column
                        label="用户名/密码"
                        width="250"
                        align="center">
                        <template slot-scope="scope">
                            <div slot="reference" class="name-wrapper">
                                <el-tag type="info" style="font-size: 16px;">{{ scope.row.account }} / {{ scope.row.password }}</el-tag>
                            </div>
                        </template>
                    </el-table-column>

                    <el-table-column
                        label="描述"
                        width="300"
                        align="center">
                        <template slot-scope="scope">
                            <div slot="reference" class="name-wrapper">
                                <el-tag type="info" style="font-size: 16px;">{{ scope.row.desc }}</el-tag>
                            </div>
                        </template>
                    </el-table-column>

                    <el-table-column
                        label="操作"
                        align="center">
                        <template slot-scope="scope">
                            <el-button
                                v-if="permissions.includes('change')"
                                size="medium"
                                @click="handleEdit(scope.$index, scope.row)">编辑
                            </el-button>

                            <el-dialog
                                title="编辑数据库"
                                :visible.sync="editVisible"
                                width="40%"
                                align="center"
                            >

                                <el-form :model="dataBaseForm"
                                         :rules="rules"
                                         ref="formName"
                                         label-width="100px"
                                >

                                    <el-form-item label="数据库名称" prop="name">
                                        <el-input v-model="dataBaseForm.name"></el-input>
                                    </el-form-item>

                                    <el-form-item label="访问地址" prop="server">
                                        <el-input v-model="dataBaseForm.server"></el-input>
                                    </el-form-item>

                                    <el-form-item label="登陆账号" prop="account">
                                        <el-input v-model="dataBaseForm.account"></el-input>
                                    </el-form-item>

                                    <el-form-item label="登陆密码" prop="password">
                                        <el-input v-model="dataBaseForm.password"></el-input>
                                    </el-form-item>

                                    <el-form-item label="简要描述" prop="desc">
                                        <el-input v-model="dataBaseForm.desc"></el-input>
                                    </el-form-item>

                                </el-form>
                                <span slot="footer" class="dialog-footer">
                        <el-button @click="cancelaction()">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('formName')">确 定</el-button>
                      </span>
                            </el-dialog>


                            <el-button
                                v-if="permissions.includes('delete')"
                                size="medium"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)">删除
                            </el-button>
                        </template>
                    </el-table-column>

                </el-table>
            </el-main>
        </el-container>
    </el-container>


</template>

<script>
   import * as databaseapi from '../../restful/databasepage'
   import {getpermissions} from "../../restful/userinfo";
    export default {
        name: "DataBase",
        data() {
            return {
                editVisible:false,
                dialogVisible: false,
                dataBaseData: {
                    results:[]
                },
                permissions:[],
                dataBaseForm: {
                    name: '',
                    desc: '',
                    server: '',
                    account: '',
                    password: '',
                    type: 1,
                    id: '',
                    project:this.$route.params.id
                },
                tags: [
                    {name: 'PA', value: 1},
                    {name: 'MySQL', value: 2},
              
                ],
                rules: {
                    name: [
                        {required: true, message: '请输入数据库名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    server: [
                        {required: true, message: '请输入数据库访问地址', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    account: [
                        {required: true, message: '请输入登陆账号', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '请输入登陆密码', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    desc: [
                        {required: true, message: '请简要描述下该数据库', trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ]
                }
            }
        }
        ,
        methods: {
            handleEdit(index, row) {
                this.editVisible = true;
                this.dataBaseForm.name = row['name'];
                this.dataBaseForm.desc = row['desc'];
                this.dataBaseForm.id = row['id'];
                this.dataBaseForm.server = row['server'];
                this.dataBaseForm.type = row['type'];
                this.dataBaseForm.account = row['account'];
                this.dataBaseForm.password = row['password'];
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除该数据库, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    databaseapi.deleteDataBase(row["id"]).then(resp => {
						if (resp.success){
							this.success('数据库删除成功');
						} else {
							this.$message.error(resp.msg)
						}
                        
                        this.getDataBaseList();
                    }).catch(resp => {
                        this.failure(resp)
                    });
                })
            },
            cancelaction(){
                if (this.dataBaseForm.id !== '') {
                            this.editVisible = false;
                        }else {
                            this.dialogVisible = false;
                        }      
                this.dataBaseForm.name = '';
                this.dataBaseForm.desc = '';
                this.dataBaseForm.id = '';
                this.dataBaseForm.account = '';
                this.dataBaseForm.password = '';
                this.dataBaseForm.server = '';
                this.dataBaseForm.type = 1;
                this.getDataBaseList();
            },
            getpermissions() {
                getpermissions({app_label:"test_runner",model:"databaseconfig"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            handleConfirm(formName) {
                this.$refs[formName].validate((valid) => {
					if (valid) {
                        this.dialogVisible = false;
                        this.editVisible = false;
                        let obj;

                        if (this.dataBaseForm.id === '') {
                            obj =databaseapi.addDataBase(this.dataBaseForm);
                        } else {
                            obj = databaseapi.updateDataBase(this.dataBaseForm.id, this.dataBaseForm);
                        }
                        obj.then(resp => {
                            console.log(resp["name"])
                            if (resp["name"] === this.dataBaseForm.name) {
                                this.success(resp["name"] + '数据库操作成功');
                            } else {
								if (!resp.success){
									this.$message.error(resp.msg)
								} else {
									this.$message.success(resp.msg)
								}
							}
							

                            this.dataBaseForm.name = '';
                            this.dataBaseForm.desc = '';
                            this.dataBaseForm.id = '';
                            this.dataBaseForm.account = '';
                            this.dataBaseForm.password = '';
                            this.dataBaseForm.server = '';
                            this.dataBaseForm.type = 1;
                            this.getDataBaseList();
                        }).catch(resp => {
                            this.failure(resp);
                        });
                    } else {
                        if (this.dataBaseForm.id !== '') {
                            this.editVisible = true;
                        }else {
                            this.dialogVisible = true;
                        }
                        return false;
                    }
                });

            },
            success(resp) {
                this.$notify({
                    message: resp,
                    type: 'success',
                    duration: 1000
                });
            },
            failure(resp) {
                this.$notify.error({
                    message: resp,
                    duration: 1000
                });
            },
            getDataBaseList() {
               databaseapi.getDataBaseList(this.$route.params.id).then(resp => {
                    this.dataBaseData = resp;
                })
            },
            getPagination(url) {
               databaseapi.getPagination(url).then(resp => {
                    this.dataBaseData = resp;
                })
            },
        },
        mounted() {
            this.getDataBaseList();
            this.getpermissions();
        },
        
    }
</script>

<style scoped>

</style>
