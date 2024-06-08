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
                placeholder="请输入 base_url 地址"
                v-model="baseUrl"
                clearable
            >
                <template slot="prepend">配置请求地址</template>
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
                <el-tab-pane label="请求头" name="first">
                    <headers
                        :save="save"
                        v-on:header="handleHeader"
                        :header="response ? response.body.header: [] ">
                    </headers>
                </el-tab-pane>

                <el-tab-pane label="请求体" name="second">
                    <request
                        :save="save"
                        v-on:request="handleRequest"
                        :request="response ? response.body.request: [] "
                    >
                    </request>
                </el-tab-pane>

                <el-tab-pane label="变量设置" name="third">
                    <variables
                        :save="save"
                        v-on:variables="handleVariables"
                        :variables="response ? response.body.variables : []"
                    >

                    </variables>
                </el-tab-pane>

                <el-tab-pane label="前后置方法设置" name="fourth">
                    <hooks
                        :save="save"
                        v-on:hooks="handleHooks"
                        :hooks="response ? response.body.hooks: []"
                    >
                    </hooks>
                </el-tab-pane>

                <el-tab-pane label="数据驱动参数设置" name="five">
                    <parameters
                        :save="save"
                        v-on:parameters="handleParameters"
                        :parameters="response ? response.body.parameters: []"
                    >
                    </parameters>
                </el-tab-pane>

            </el-tabs>
        </div>
    </div>

</template>

<script>
    import Headers from '../../../httprunner/components/Headers'
    import Request from '../../../httprunner/components/Request'
    import Variables from '../../../httprunner/components/Variables'
    import Hooks from '../../../httprunner/components/Hooks'
    import Parameters from '../../../httprunner/components/Parameters'
    import * as configpage from "../../../../restful/configpage";
    export default {
        components: {
            Headers,
            Request,
            Variables,
            Hooks,
            Parameters
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
                this.name = this.response.body.name;
                this.baseUrl = this.response.body.base_url;
                this.configdesc=this.response.configdesc;
                this.id = this.response.id;
            }
        },

        methods: {
            handleHeader(header) {
                this.header = header;
            },
            handleRequest(request) {
                this.request = request;
            },

            handleVariables(variables) {
                this.variables = variables;
            },
            handleHooks(hooks) {
                this.hooks = hooks;
            },
            handleParameters(parameters) {
                this.parameters = parameters;
                if (this.id === '') {
                    this.addConfig();
                } else {
                    this.updateConfig();
                }
            },

            addConfig() {
                if (this.validateData()) {
                    configpage.addConfig({
                        parameters: this.parameters,
                        header: this.header,
                        request: this.request,
                        variables: this.variables,
                        hooks: this.hooks,
                        base_url: this.baseUrl,
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
                    configpage.updateConfig(this.id, {
                        parameters: this.parameters,
                        header: this.header,
                        request: this.request,
                        variables: this.variables,
                        hooks: this.hooks,
                        base_url: this.baseUrl,
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
                baseUrl: '',
                configdesc:'',
                id: '',
                header: [],
                request: [],
                variables: [],
                hooks: [],
                parameters: [],
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
