<template>
    <div style="margin-left: 10px">
        <div style="margin-top: 10px">
            <el-input
                style="width: 600px"
                placeholder="请输入配置名称"
                v-model="name"
                clearable
            >
                <template slot="prepend">配置信息录入</template>

                <el-button
                    slot="append"
                    type="success"
                    plain
                    @click="save = !save"
                >保存
                </el-button>
            </el-input>
        </div>
        <div>
            <el-input
                class="input-with-select"
                placeholder="请输入所属页面"
                v-model="basePage"
                clearable
            >
                <template slot="prepend">所属页面</template>
            </el-input>
        </div>
        <div>
            <el-input
                class="input-with-select"
                placeholder="请输入配置描述信息"
                v-model="configdesc"
                clearable
            >
                <template slot="prepend">配置描述信息</template>
            </el-input>
        </div>
        <div class="request">
            <el-tabs
                v-model="activeTag"
                style="margin-left: 20px"
            >    

                <el-tab-pane label="变量设置" name="third">
                    <variables
                        :save="save"
                        v-on:variables="handleVariables"
                        :variables="response ? response.body.variables : []"
                    >

                    </variables>
                </el-tab-pane>


            </el-tabs>
        </div>
    </div>

</template>

<script>
    // import Headers from '../../../httprunner/components/Headers'
    // import Request from '../../../httprunner/components/Request'
    import Variables from '../../../httprunner/components/Variables'
    // import Hooks from '../../../httprunner/components/Hooks'
    // import Parameters from '../../../httprunner/components/Parameters'
    import * as configpage from "../../../../restful/configpage";
    export default {
        components: {
  
            Variables,
  
        },

        props: {
            project: {
                require: false
            },
            response: {
                require: false
            }
        },

        watch: {
            response: function () {
                this.name = this.response.name;
                this.basePage = this.response.base_page;
                this.configdesc=this.response.configdesc;
                this.id = this.response.id;
            }
        },

        methods: {
  

            handleVariables(variables) {
                this.variables = variables;
                if (this.id === '') {
                    this.addConfig();
                } else {
                    this.updateConfig();
                }
            },  


            addConfig() {
                if (this.validateData()) {
                    configpage.addUiConfig({                     
                        variables: this.variables,                  
                        base_page: this.basePage,
                        configdesc:this.configdesc,
                        name: this.name,
                        project: this.project,

                    }).then(resp => {
                        if (resp.success) {
                            this.$emit("addSuccess");
                        } else {
                            this.$message.error({
                                message: resp.msg,
                                duration: 1000
                            })
                        }
                    })
                }
            },

            updateConfig() {
                if (this.validateData()) {
                    configpage.updateUiConfig(this.id, {                  
                        variables: this.variables,                   
                        base_page: this.basePage,
                        configdesc:this.configdesc,
                        name: this.name,
                    }).then(resp => {
                        if (resp.success) {
                            this.$emit("addSuccess");
                        } else {
                            this.$message.error({
                                message: resp.msg,
                                duration: 1000
                            })
                        }
                    })
                }
            },

            validateData() {
                if (this.name === '') {
                    this.$notify.error({
                        title: '参数错误',
                        message: '配置名称不能为空',
                        duration: 1500
                    });
                    return false;
                }
                return true
            },

        },

        data() {
            return {
                name: '',
                basePage: '',
                configdesc:'',
                id: '',                           
                variables: [],           
                save: false,
                activeTag: 'third',
            }
        },
        name: "ConfigBody"
    }
</script>

<style scoped>
    .el-select {
        width: 130px;
    }

    .input-with-select {
        width: 600px;
        margin-top: 10px;
    }

    .request {
        margin-top: 15px;
        border: 1px solid #ddd;
    }

</style>
