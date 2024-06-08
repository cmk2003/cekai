<template>
    <div>
        <div>
            <div>
                <el-input
                    style="width: 600px"
                    placeholder="请输入用例名称"
                    v-model="name"
                    clearable
                >
                    <template slot="prepend">用例名称</template>

                    <el-button
                        slot="append"
                        type="success"
                        plain
                        @click="save = !save"
                    >保存
                    </el-button>
                </el-input>

                <el-button
                    type="primary"
                    @click="reverseStatus"
                    v-loading="loading"
                    :disabled="loading"
                >运行
                </el-button>
            </div>

            <div>
                <el-input
                    style="width: 600px; margin-top: 10px"
                    placeholder="请输入用例描述"
                    v-model="casedescribe"
                    clearable
                >
                <template slot="prepend">用例描述</template>

                </el-input>

            </div>

        </div>

        <div class="request">

            <el-dialog
                v-if="dialogTableVisible"
                :visible.sync="dialogTableVisible"
                width="70%"
            >
                <report :summary="summary"></report>
            </el-dialog>

            <el-tabs
                style="margin-left: 20px;"
                v-model="activeTag"
            >
                <el-tab-pane label="用例步骤" name="first">
                    <testcase
                        :save="save"
                        v-on:testcase="handleHeader"
                        :testcase="response ? response.body: [] ">
                    </testcase>
                </el-tab-pane>
                <el-tab-pane label="变量设置" name="two">
                    <variables
                        :save="save"
                        v-on:variables="handleVariables"
                        :variables="response ? response.variables : []"
                    >

                    </variables>
                </el-tab-pane>
            </el-tabs>

        </div>


    </div>

</template>

<script>
    import Testcase from '../../../uitestpage/webtest/components/Testcases'
    import variables from '../../../httprunner/components/Variables'
    import Report from '../../../uitestpage/webtest/components/DebugReport'
    import * as UICASEAPI from '../../../../restful/UIcase'
    export default {
        components: {
            Testcase,      
            Report,
            variables
        },

        props: {
   
            nodeId: {
                require: false
            },
            project: {
                require: false
            },
            config: {
                require: true
            },  
            response: {
                require: false
            }
        },
        methods: {
            reverseStatus() {
                this.save = !this.save;
                this.run = true;
            },
            handleVariables(variables) {
                this.variables = variables;
                if (!this.run) {
                    if (this.id === '') {
                        this.addUICase();
                    } else {
                        this.updateUIcase();
                    }
                } else {
                    this.runuicase();
                    this.run = false;
                }
            },
            handleHeader(testcase) {
                this.testcase = testcase;

            },
        
     

            validateData() {
                
                if (this.casedescribe === '') {
                    this.$notify.error({
                        title: '用例描述错误',
                        message: '用例描述不能为空',
                        duration: 1500
                    });
                    return false;
                }

                if (this.name === '') {
                    this.$notify.error({
                        title: 'name错误',
                        message: '用例名称不能为空',
                        duration: 1500
                    });
                    return false;
                }
                return true
            },
            updateUIcase() {
                if (this.validateData()) {
                    UICASEAPI.updateuicase(this.id, {
                        testcase: this.testcase,                  
                        casedescribe: this.casedescribe,  
                        variables:this.variables,              
                        name: this.name,                    
                    }).then(resp => {
                        if (resp.success) {
                            this.$emit('addSuccess');
                        } else {
                            this.$message.error({
                                message: resp.msg,
                                duration: 1000
                            })
                        }
                    })
                }
            },
            runuicase(){
                if(this.validateData()){
                    this.loading = true;
                    UICASEAPI.runuicase({
                        project: this.$route.params.id,
                        name:this.name,
                        config:this.config,
                        casedescribe:this.casedescribe,
                        variables:this.variables,
                        testcase:this.testcase
                    }).then(resp => {
                        this.summary = resp;
                        this.dialogTableVisible = true;
                        this.loading = false;
                    }).catch(resp => {
                        this.loading = false;
                    })
                }
            },
   

            addUICase() {
                
                if (this.validateData()) {
                 
                    UICASEAPI.adduicase({
                        testcase: this.testcase,                  
                        casedescribe: this.casedescribe,
                        variables:this.variables,
                        method:"CASE",                
                        name: this.name,                  
                        nodeId: this.nodeId,
                        project: this.project,

                    }).then(resp => {
                        if (resp.success) {
                            this.$emit('addSuccess');
                        } else {
                            this.$message.error({
                                message: resp.msg,
                                duration: 1000
                            })
                        }
                    })
                }
            }
        },

        watch: {
            response: function () {
                this.name = this.response.name;           
                this.casedescribe = this.response.casedescribe;           
                this.id = this.response.id;              
                this.testcase=this.response.body;
                this.variables=this.response.variables
            }
        },
        data() {
            return {
                loading: false,              
                name: '',
                casedescribe: '',
                id: '',
                testcase: [],
                variables:[],  
                dialogTableVisible: false,
                save: false,
                run: false,
                summary: {},
                activeTag: 'first',
          
            }
        },
        name: "CaseBody"
    }
</script>

<style scoped>
    .request {
        margin-top: 15px;
        border: 1px solid #ddd;
    }


</style>
