<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="dialogVisible=true"
                    >新增用户
                    </el-button>                    
                    <el-button
                        v-show="userData.count !== 0 "
                        style="margin-left: 20px"
                        type="danger"
                        icon="el-icon-delete"                        
                        size="small"
                        @click="delSelectionUsers"
                    >批量删除</el-button>
                    

                    <el-dialog
                        title="添加用户"
                        :visible.sync="dialogVisible"
                        width="30%"
                       center
                    >
                        <el-form
                            :model="usersForm"
                            :rules="rules"
                            ref="usersForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="姓名" prop="name">
                                <el-input v-model="usersForm.name" clearable placeholder="请输入姓名"></el-input>
                            </el-form-item>
                            <el-form-item label="账号" prop="username">
                                <el-input v-model="usersForm.username" clearable placeholder="请输入账号" ></el-input>

                            </el-form-item>
                            <el-form-item label="密码" prop="password">
                                <el-input v-model="usersForm.password" clearable placeholder="请输入密码" type="password"></el-input>
                            </el-form-item>
                            <el-form-item label="确认密码" prop="newpassword">
                                <el-input v-model="usersForm.newpassword" clearable placeholder="请输入确认密码" type="password"></el-input>                   
                            </el-form-item>
                            <el-form-item label="E-Mail" prop="email">
                                <el-input v-model="usersForm.email" clearable placeholder="请输入E-Mail"></el-input>
                            </el-form-item>
                            <el-form-item label="是否启用" prop="is_active" >
                                <el-radio v-model="usersForm.is_active" :label="true">是</el-radio>
                                <el-radio v-model="usersForm.is_active" :label="false">否</el-radio>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('usersForm')">确 定</el-button>
                      </span>
                    </el-dialog>

                    <el-dialog
                        title="编辑用户"
                        :visible.sync="editdialogVisible"
                        width="60%"
                        center
                    >
                        <el-form
                            :model="editusersForm"
                            :rules="rules"
                            ref="editusersForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="姓名" prop="name">
                                <el-input v-model="editusersForm.name" clearable placeholder="请输入姓名"></el-input>
                            </el-form-item>
                            <el-form-item label="账号" prop="username">
                                <el-input v-model="editusersForm.username" disabled placeholder="请输入账号" ></el-input>
                            </el-form-item>                     
                            <el-form-item label="E-Mail" prop="email">
                                <el-input v-model="editusersForm.email" clearable placeholder="请输入E-Mail"></el-input>
                            </el-form-item>
                            <el-form-item label="是否启用" prop="is_active" >
                                <el-radio v-model="editusersForm.is_active" :label="true">是</el-radio>
                                <el-radio v-model="editusersForm.is_active" :label="false">否</el-radio>
                            </el-form-item>
                            <el-form-item label="是否超管" prop="is_superuser" >
                                <el-radio v-model="editusersForm.is_superuser" :label="true">是</el-radio>
                                <el-radio v-model="editusersForm.is_superuser" :label="false">否</el-radio>
                            </el-form-item>
                            <el-form-item label="所属角色" class="edit_dev">
                            <el-transfer 
                            v-model="editusersForm.groups" 
                            :data="groupdata"                           
                            :titles="['待选择角色', '已选择角色']"
                            ></el-transfer>
                            </el-form-item>
                            <el-form-item label="所属项目" class="edit_dev">
                            <el-transfer 
                            v-model="editusersForm.belong_project" 
                            :data="data"                           
                            :titles="['待选择项目', '已选择项目']"
                            ></el-transfer>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="editdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleEditConfirm('editusersForm')">确 定</el-button>
                      </span>
                    </el-dialog>                   
                </div>
            </div>
        </el-header>

        <el-container>
            <el-header style="padding: 0; height: 50px;">
                <div style="padding-top: 8px; padding-left: 20px; overflow: hidden;">
                    <el-row :gutter="50">
                        <el-col :span="6">
                            <el-input placeholder="请输入用户姓名或账号"  clearable v-model="search">
                                <el-button slot="append" icon="el-icon-search" @click="GetUserlist"></el-button>
                            </el-input>
                        </el-col>

                    </el-row>
                </div>
            </el-header>

            <el-container>
                <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                    <div style="position: fixed; bottom: 0; right:0; left: 220px; top: 220px">
                        <el-table
                        :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                            highlight-current-row
                            :data="userData.results"
                            :show-header="userData.results.length !== 0 "
                            stripe
                            height="calc(75%)"
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
                                label="用户名称"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.name}}</div>
                                </template>
                            </el-table-column>

                            <el-table-column
                                label="用户账号"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div >{{scope.row.username}}</div>

                                </template>
                            </el-table-column>

                            <el-table-column
                           
                                label="E-Mail"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div >{{scope.row.email}}</div>

                                </template>
                            </el-table-column>   
                            <el-table-column
                           
                                label="是否启用"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div v-if="scope.row.is_active==true">是</div>
                                    <div v-if="scope.row.is_active==false">否</div>

                                </template>
                            </el-table-column>         
                            <el-table-column
                           
                                label="是否超管"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div v-if="scope.row.is_superuser==true">是</div>
                                    <div v-if="scope.row.is_superuser==false">否</div>

                                </template>
                            </el-table-column>                                              
                            <el-table-column
                                label="创建时间"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.date_joined|datetimeFormat}}</div>

                                </template>
                            </el-table-column>

                            <el-table-column
                            label="操作">
                                <template slot-scope="scope">
                                    <el-row v-show="currentRow === scope.row">
                                        <el-button
                                            type="info"                                           
                                            size="mini"
                                            @click="handleEditVariables(scope.row)"
                                        >编辑</el-button>


                                        <el-button
                                            v-show="userData.count !== 0"
                                            type="danger"                                  
                                            size="mini"
                                            @click="handleDelUser(scope.row.id)"
                                        >删除
                                        </el-button>
                                    </el-row>
                                </template>

                            </el-table-column>

                        </el-table>
                        <el-col :span="7">
                            <el-pagination
                                :page-size="5"
                                v-show="userData.count !== 0 "
                                style="padding-top:10px;"
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="userData.count"
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
    import * as UserApi from "../../restful/userinfo";
   import {getProjectList} from "../../restful/project";
   import {GetUserGrouplist} from '../../restful/usergroup';

    export default {


        data() {

                const validateusername=(rule, value, callback)=>{
                    const uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
                    if(!value){
                        return callback(new Error('账号不能为空'));
                    }else  if (!uPattern.test(value)) {
                        return callback(new Error('用户名4到16位,只能是字母,数字,下划线,连字符'))                  
                    }else {
                        callback();
                    }
                };
                const validatoremail=(rule,value,callback)=>{
                    const ePattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
                    if(!value){
                        return callback(new Error('邮箱不能为空'));
                    }else  if (!ePattern.test(value)) {
                        return callback(new Error('邮箱格式不正确'))                  
                    }else {
                        callback();
                    }
                }
                const validateNewPassword = (rule, value, callback) => {
                    if (!value) {
                        return callback(new Error('确认密码不能为空'));
                    } else if (value !== this.usersForm.password) {
                        callback(new Error('与密码不一致!'))
                    }else if(value.toString().length < 6){
                        callback(new Error('密码至少六位'));
                    } else {
                        callback();
                    }
                        };
            return {

                
                search: '',           
                selectVariables: [],
                currentRow: '',
                currentPage: 1,
                userData: {
                    count: 0,
                    results: []
                },            
                editdialogVisible: false,
                dialogVisible: false,
                tkdialogVisible: false,
                usersForm: {
                    name: '',
                    username: '',
                    password: '',
                    newpassword:'',
                    email:'',
                    is_active:true,
                },
                data:[],
                groupdata:[],
                projectData:[],
                editusersForm: {
                    name: '',
                    username: '',          
                    email:'',
                    is_active:'',
                    is_superuser:'',
                    belong_project:[],
                    groups:[],
                    id:''
                },

                rules: {
                    name: [
                        {required: true, message: '请输入姓名', trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ],
                    username: [
                        {validator:validateusername,required: true,  trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                        {min: 6, max: 50, message: '最少需要6个字符', trigger: 'blur'}
                    ],
                    newpassword: [
                        {validator:validateNewPassword,required: true, trigger: 'blur'},
                     
                    ],
                    is_active: [
                        {required: true, message: '请选择是否启用', trigger: 'blur'},
                     
                    ],    
                    is_superuser:[
                        {required:true,message:"请选择角色类型",trigger:'blur'},
                    ],
                    email:[
                        {validator:validatoremail ,required:true,trigger:'blur'},                     
                    ]
                }
            }
        },
        methods: {
            cellMouseEnter(row) {
                this.currentRow = row;
            },

            cellMouseLeave(row) {
                this.currentRow = '';
            },     
            clear(){
                
            },
            handleEditVariables(row) {
                this.editusersForm = {
                    name: row.name,
                    username: row.username,
                    email:row.email,
                    id: row.id,
                    is_active:row.is_active,
                    is_superuser:row.is_superuser,
                    belong_project:row.belong_project,
                    groups: row.groups,

                };

                this.editdialogVisible = true;
            },
     
            getProjectList() {
                getProjectList().then(resp => {
                    this.projectData = resp.results;
                       let data = [];
                       resp.results2.forEach((item, index) => {                         
                            data.push({
                            key: item.id,
                            label: item.name,         
                        });
                        })                     
                    this.data=data;               
                })
            },
            getUserGroupList(){
                GetUserGrouplist({params:{
                    search: ''
                }}).then(resp =>{
                    let groupdata=[];
                    resp.results2.forEach((item,index)=>{
                        groupdata.push({
                            key:item.id,
                            label:item.name,
                        });
                    })
                    this.groupdata=groupdata;
                })
            },

            handleDelUser(index) {
                this.$confirm('此操作将永久删除该用户，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    UserApi.deluser(index).then(resp => {
						this.GetUserlist();
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
                this.selectVariables = val;
            },

            handleCurrentChange(val) {
                UserApi.getuserPaginationBypage({
                    
                        page: this.currentPage,                     
                        search: this.search
                  
                }).then(resp => {
                    this.userData = resp;
                })
            },
            delSelectionUsers() {
                if (this.selectVariables.length !== 0) {
                    this.$confirm('此操作将永久删除勾选的用户，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        UserApi.delAlluser({data: this.selectVariables}).then(resp => {
                            this.GetUserlist();
							this.currentPage = 1;
                        })
                    })
                } else {
                    this.$notify.warning({
                        title: '提示',
                        message: '请至少勾选一个用户',
                        duration: 1000
                    })
                }
            },

            handleConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {                       
                        this.dialogVisible = false;
                       UserApi.adduser(this.usersForm).then(resp => {
                            if (resp.success) {
                                this.$message.success({
                                    message: resp.msg,
                                    duration: 1000
                                })
                                this.usersForm.name = '';
                                this.usersForm.username = '';
                                this.usersForm.password='';
                                this.usersForm.newpassword = '';
                                this.usersForm.is_active = true;
                                this.usersForm.email='';
                                this.GetUserlist();
								this.currentPage = 1;
                            } else {
                                  this.$message.error(resp.msg);
                            }
                        })                    
                    }
                });

            },

            handleEditConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.editdialogVisible = false;
                        UserApi.userinfo(this.editusersForm).then(resp => {
                            if (!resp.success) {
                                this.$message.error({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            } else {
                                this.$message.success(resp.msg)
                                this.GetUserlist();
                            }
							this.currentPage = 1
                        })
                    }
                });

            },

            GetUserlist() {
                UserApi.getuserlist({search: this.search}                       
                    
                ).then(resp => {
                   
                    this.userData = resp;
                })
            },
        },
        name: "UserList",
        mounted() {
            this.GetUserlist();
            this.getProjectList();
            this.getUserGroupList();
        }
    }
</script>

<style>

.edit_dev .el-transfer-panel{
    width:350px;
}
</style>
