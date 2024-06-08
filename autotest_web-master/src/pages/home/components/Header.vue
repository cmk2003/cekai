<template>
    <div>
        <div class="nav-header">

            <span style="color: white; font-size: 25px; margin-left: 10px">sunck测试平台</span>

            <span class="right">
                <div style="float: right; color: #d9d9d9; margin-right: 100px">

                    <a class="iconfont"  @click="editdialogVisible=true">&#xe61c;</a>                 

                    <span v-text="this.$store.state.useractualname" style="padding-left: 5px; font-size: large" ></span>           
                    <a v-if="this.$store.state.Is_superuser==true || this.$store.state.Is_superuser=='true'" style="padding-left: 10px; color:#d9d9d9; text-decoration:none;"  :href="HTurl" target="_blank" >后台管理</a>
                <a style="padding-left: 10px;" @click="editpasswordVisible=true">修改密码</a>
                    <a style="padding-left: 10px;" @click="handleLogOut">注 销</a>
                </div>
            </span>
           <el-dialog
                        title="修改用户信息"
                        :visible.sync="editdialogVisible"
                        width="30%"
                        align="center"
                    >
                        <el-form
                            :model="editVariablesForm"                     
                            ref="editVariablesForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="账号" prop="username">
                                <el-input v-model="editVariablesForm.username" :disabled="true" ></el-input>
                            </el-form-item>
                            <el-form-item label="用户名" prop="name">
                                <el-input v-model="editVariablesForm.name" clearable placeholder="请输入用户名"></el-input>
                            </el-form-item>
                            <el-form-item label="邮箱" prop="email">
                                <el-input v-model="editVariablesForm.email" clearable placeholder="请输入邮箱"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="canceltable('editVariablesForm')">取 消</el-button>
                        <el-button type="primary" @click="handleEditConfirm('editVariablesForm')">确 定</el-button>
                      </span>
            </el-dialog>
                     <el-dialog
                        title="修改密码"
                        :visible.sync="editpasswordVisible"
                        width="30%"
                        align="center"
                    >
                        <el-form
                            :model="editpasswordForm"
                            :rules="rules"
                            ref="editpasswordForm"
                            label-width="100px"
                            class="project">
                     
                            <el-form-item label="旧密码" prop="password">
                                <el-input v-model="editpasswordForm.password" clearable placeholder="请输入旧密码" type="password"></el-input>
                            </el-form-item>
                            <el-form-item label="新密码" prop="newpassword">
                                <el-input v-model="editpasswordForm.newpassword" clearable placeholder="请输入新密码" type="password"></el-input>
                            </el-form-item>
                                <el-form-item label="确认密码" prop="checkpassword">
                                <el-input v-model="editpasswordForm.checkpassword" clearable placeholder="请输入确认密码" type="password"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="canceltable('editpasswordForm')">取 消</el-button>
                        <el-button type="primary" @click="handleEditpasswordConfirm('editpasswordForm')">确 定</el-button>
                      </span>
            </el-dialog>
        </div>
    </div>


</template>

<script>
import {logout,userinfo,updatapassword} from "../../../restful/userinfo";
    export default {
        data :
            function(){
                            const validateNewPassword = (rule, value, callback) => {
                                if (!value) {
                                    return callback(new Error('新密码不能为空'));
                                } else if (value === this.editpasswordForm.password) {
                                    callback(new Error('新密码不能与原密码相同!'))
                                }else if(value.toString().length < 6){
                                    callback(new Error('密码至少六位'));
                                } else {
                                    callback();
                                }
                            };

                            const validateNewPassword2 = (rule, value, callback) => {
                                if (!value) {
                                    return callback(new Error('确认密码不能为空'));
                                } else if (value !== this.editpasswordForm.newpassword) {
                                    callback(new Error('与新密码不一致!'))
                                }else if(value.toString().length < 6){
                                    callback(new Error('密码至少六位'));
                                } else {
                                    callback();
                                }
                                  };
            
            return {
                HTurl:config.HTurl,
                editdialogVisible: false,
                editVariablesForm:{
                    username: this.$store.state.user,
                    name:this.$store.state.useractualname,          
                    email: this.$store.state.email,
                },
                editpasswordVisible:false,
                editpasswordForm:{
                    password:'',
                    newpassword:'',
                    checkpassword:''
                },
                 rules: {
                    password: [
                        {required: true, message: '请输入旧密码', trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ],          
                    newpassword:[
                     
                        { validator:validateNewPassword, required: true,  trigger: 'blur' }
     
                    ],
                    checkpassword:[
                        { validator:validateNewPassword2,required: true,  trigger: 'blur' }
       
                    ]
                }
                
            }
            },
        
        methods: {
            handleLogOut () {
                this.$store.commit("isLogin", null);
                this.setLocalValue("token", null);
				this.$store.commit("setUser", null);
				this.setLocalValue("user", null);
				this.$store.commit("setRouterName", null);
				this.setLocalValue("routerName", null);
				this.$store.commit("setUseractualname", null);
				this.setLocalValue("useractualname", null);
				this.$store.commit("setUseEmail", null);
				this.setLocalValue("email", null);
				this.$store.commit("setIs_superuser", null);
				this.setLocalValue("Is_superuser", null);
                this.$router.push({name:"Login"});
				logout({"username":this.$store.state.user});
            },   

            handleEditConfirm(formName) {
                
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.editdialogVisible = false;
                        userinfo(this.editVariablesForm).then(resp => {
                            if (!resp.success) {
                                this.$message.info({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            } else {             
           
                                this.$store.commit("setUseractualname",this.editVariablesForm.name); 
                                this.$store.commit("setUseEmail",this.editVariablesForm.email);   
                                 this.setLocalValue("useractualname", this.editVariablesForm.name);
                                 this.setLocalValue("email", this.editVariablesForm.email);
                                 this.$message.info({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            }
                        })

                    }
                });

            },
            handleEditpasswordConfirm(formName) {
                console.log(this.$refs[formName])
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.editpasswordVisible = false;
                        updatapassword(this.editpasswordForm).then(resp => {
                            if (!resp.success) {
                                this.editpasswordForm.password="",
                                this.editpasswordForm.newpassword="",
                                this.editpasswordForm.checkpassword="",
                                this.$message.success({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            } else {             
                                 this.$message.error({
                                    message: resp.msg,
                                    duration: 1000
                                })
                                this.$router.push('/testrunner/login');
                            }
                        })

                    }
                });

            },
            //点取消时初始化数据
            canceltable(value){
                if(value==='editpasswordForm'){
                    this.editpasswordVisible=false,
                    this.editpasswordForm.password="",
                    this.editpasswordForm.newpassword="",
                    this.editpasswordForm.checkpassword=""
                }else{
                    this.editdialogVisible=false,
                    this.editVariablesForm={
                    username: this.$store.state.user,
                    useractualname:this.$store.state.useractualname,          
                    email: this.$store.state.email,
                }
                }
                
            }
        },
        name: "Header",

    }
</script>

<style scoped>
    .left {
        width: 500px;
        left: 20px;
        display: inline-block;
        position: fixed;
        z-index: 900;
        top: -5px;
    }

    .right {
        position: fixed;
        left: 300px;
        right: 0;
        top: 0;

    }

    .right div a:hover {
        color: darkcyan;
    }

    .logo {
        background:white;
        height: 45px;
    }

    .nav-header {
       background: #242F42;
        margin: 0 auto;
        font-size: 14px;
        width: 100%;
        border-bottom: 1px solid #ddd;
        height: 49px;
        line-height: 49px;
    }

</style>
