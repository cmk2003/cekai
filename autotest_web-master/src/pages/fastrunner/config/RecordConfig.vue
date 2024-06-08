<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                     v-if="permissions.includes('add')"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="initResponse = true"
                    >新增配置
                    </el-button>

                  <!--  <el-button
                        type="primary"
                        plain
                        size="small"
                        icon="el-icon-upload"
                    >导入配置
                    </el-button>

                    <el-button
                        type="info"
                        plain
                        size="small"
                        icon="el-icon-download"
                    >导出配置
                    </el-button>-->

                    <el-button
                     v-if="permissions.includes('delete')"
                        style="margin-left: 20px"
                        type="danger"            
                        size="mini"
                        icon="el-icon-delete"
                        @click="del= !del"
                    >批量删除</el-button>

                    <el-button
                        :disabled="!addConfigActivate"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="addConfigActivate=false"
                    >返回列表</el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 20px">
                <config-body
                    v-show="addConfigActivate"
                    :project="$route.params.id"
                    :response="respConfig"
                    v-on:addSuccess="handleAddSuccess"
                >
                </config-body>

                <config-list
                    :permissions="permissions"
                    v-if="!addConfigActivate"
                    :project="$route.params.id"
                    v-on:respConfig="handleRespConfig"
                    :del="del"
                    :back="back"
                >
                </config-list>
            </el-main>
        </el-container>
    </el-container>

</template>

<script>
    import ConfigBody from './components/ConfigBody'
    import ConfigList from './components/ConfigList'
    import {getpermissions} from "../../../restful/userinfo";    
    export default {
        components: {
            ConfigBody,
            ConfigList
        },

        computed: {
            initResponse: {
                get() {
                    return this.addConfigActivate;
                },
                set(value) {
                    this.addConfigActivate = value;
                    this.respConfig = {
                        id: '',
                        body: {
                            name: '',
                            base_url: '',
                            confdesc:'',
                            header: [{
                                key: "",
                                value: "",
                                desc: ""
                            }],
                            request: {
                                data: [{
                                    key: "",
                                    value: "",
                                    desc: "",
                                    type: 1
                                }],
                                params: [{
                                    key: "",
                                    value: "",
                                    desc: "",
                                    type: 1
                                }],
                                json_data: ''
                            },
                            variables: [{
                                key: "",
                                value: "",
                                desc: "",
                                type: 1
                            }],
                            hooks: [{
                                setup: "",
                                teardown: ""
                            }],
                            parameters: [{
                                key: "",
                                value: "",
                                desc: "",
                            }],

                        }
                    };
                }
            },
        },
        data() {
            return {
                permissions:[],
                back: false,
                del: false,
                addConfigActivate: false,
                respConfig: ''
            }
        },
        methods: {
            handleAddSuccess () {
                this.back = !this.back;
                this.addConfigActivate = false;
            },
            getpermissions() {
                getpermissions({app_label:"test_runner",model:"config"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            handleRespConfig(row) {
                this.respConfig = row;
                this.addConfigActivate = true;
            }
        },
        name: "RecordConfig",
        mounted() {
            this.getpermissions();
        }
    }
</script>

<style>


</style>
