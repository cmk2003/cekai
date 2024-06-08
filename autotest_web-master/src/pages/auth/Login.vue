<template>

    <el-container class="login login-wrap-nighttime">
                <div class="login-box ">
                <div class="login-box-left">
                    <img src="~@/assets/images/login-left-night.f43356b5.png" alt="">
                <div class="box-left-content">
                    <!-- <img src="~@/assets/images/1.png" alt=""> -->
                    <div class="line"></div>
                    <div class="slogan">sunck自动化平台</div>
                </div>
                
                </div>
                <div class="login-box-right">
                
                <div class="login-box-content">
                    <div class="login-box-inp">
                        <form id="submit-form">
                            
                                <div id="form-msg" style="text-align: center">登录账号</div>
                                <div id="form-inputs">
                                    <div class="form-input-div">
                                        <i class="iconfont"
                                           style="position: absolute; bottom: 215px; padding-left: 10px">&#xe61c;</i>
                                        <input placeholder="用户名" type="text" id="username" v-model="loginForm.username">
                                        <div class="err_msg" id="username_err" v-html="usernameInvalid" @mouseover="usernameInvalid=''"></div>
                                    </div>
                                    <div class="form-input-div">
                                        <i class="iconfont"
                                           style="position: absolute; bottom: 155px; padding-left: 10px">&#xe652;</i>
                                        <input placeholder="密码" type="password" id="pwd" v-model="loginForm.password">
                                        <div class="err_msg" id="pwd_err" v-html="passwordInvalid" @mouseover="passwordInvalid= ''"></div>
                                    </div>
                                    <div class="form-submit">
                                        <button type="button" class="btn btn-primary" id="submitBtn" style="border-radius: 5px!important;"
                                                @click="submitForm">立即登录
                                        </button>
                                    </div>
                                </div>
                                <div class="form-foot">
                                    <span>没有账户，<router-link to="/testrunner/register">立即注册</router-link></span>
                                </div>

                        
                        </form>
                        </div>
                   </div>

           
                </div>
                </div>
        <el-footer class="copyright">
            <span>©Copyright 2022 sunck</span>
        </el-footer>
    </el-container>
    
</template>

<script>
 import {login} from "../../restful/userinfo";
    export default {
        name: "Login",

        data() {
            return {
                loginForm: {
                    username: '',
                    password: '',
                },
                usernameInvalid: '',
                passwordInvalid: ''
            };
        },

        methods: {
            validateUserName() {
                if (this.loginForm.username.replace(/(^\s*)/g, "") === '') {
                    this.usernameInvalid = "用户名不能为空";
                    return false;
                }
                return true
            },
            validatePassword() {
                if (this.loginForm.password.replace(/(^\s*)/g, "") === '') {
                    this.passwordInvalid = "密码不能为空";
                    return false;
                }
                return true;
            },
            handleLoginSuccess(resp) {
                if (resp.success) {
                    this.$router.push({name: 'homelist'});
                    this.$store.commit("isLogin", resp.token);
                    this.$store.commit("setUser", resp.user);
                    this.$store.commit("setUseractualname",resp.name);
                    this.$store.commit("setUseEmail",resp.email);      
                    this.$store.commit("setIs_superuser",resp.Is_superuser);                
                    this.$store.commit("setRouterName",'homelist');
                    this.setLocalValue("token", resp.token);
                    this.setLocalValue("user", resp.user);
                    this.setLocalValue("routerName", 'homelist');
                    this.setLocalValue("useractualname", resp.name);
                    this.setLocalValue("email", resp.email);
                    this.setLocalValue("Is_superuser", resp.Is_superuser);
                } else {
                    this.$message.error({
                        message: resp.msg,
                        duration: 2000,
                        center: true
                    })
                }
            },
            submitForm() {
                if (this.validateUserName() && this.validatePassword()) {
                    login(this.loginForm).then(resp => {
                        this.handleLoginSuccess(resp)
                    })
                }
            }
        }
    }
</script>

<style scoped>

</style>
