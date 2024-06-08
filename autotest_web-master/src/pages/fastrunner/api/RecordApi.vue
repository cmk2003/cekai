<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; ">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 10px">
                    <el-button
                    v-if="permissions.includes('add')"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus"
                        @click="dialogVisible = true"
                    >
                        新建分组
                    </el-button>

                    <el-dialog
                        title="新建分组"
                        :visible.sync="dialogVisible"
                        width="30%"
                        align="center"
                    >
                        <el-form
                            :model="nodeForm"
                            :rules="rules"
                            ref="nodeForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="节点名称" prop="name">
                                <el-input v-model="nodeForm.name"></el-input>
                            </el-form-item>
                        </el-form>

                        <el-radio-group v-model="radio" size="small">
                            <el-radio-button label="根节点"></el-radio-button>
                            <el-radio-button label="子节点"></el-radio-button>
                        </el-radio-group>

                        <span slot="footer" class="dialog-footer">
                        <el-button @click="quxiao()">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('nodeForm')">确 定</el-button>
                      </span>
                    </el-dialog>

                    <el-button
                    v-if="permissions.includes('delete')"
                        :disabled="currentNode === '' "
                        type="danger"
                        size="small"
                        icon="el-icon-delete"
                        @click="deleteNode"
                    >删除分组
                    </el-button>


                    <el-button
                    v-if="permissions.includes('change')"
                        :disabled="currentNode === '' "
                        type="info"
                        size="small"
                        icon="el-icon-edit-outline"
                        @click="renameNode"
                    >重命名
                    </el-button>


                    <el-button
                    v-if="permissions.includes('add')"
                        :disabled="currentNode === '' "
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="initResponse = true"
                    >添加接口
                    </el-button>
                    <el-button
                    v-if="permissions.includes('add')"
                        :disabled="currentNode === '' "
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="opentb()"
                    >同步接口
                    </el-button>

                    <el-dialog
                    v-if="permissions.includes('add')"
                        title="同步swagger-ui接口"
                        :visible.sync="tbdialogVisible"
                        width="30%"
                        align="center"
                        center
                    >
                        <el-form
                            :model="apiForm"
                            :rules="rules"
                            ref="apiForm"
                            label-width="100px"
                            
                            class="project">
                            <el-form-item label="API地址" prop="swaggerurl">
                                <el-input v-model="apiForm.swaggerurl" clearable placeholder="请输入完整的API接口地址"></el-input>
                            </el-form-item>
                            <el-form-item label="cookie" prop="token">
                                <el-input v-model="apiForm.token" clearable placeholder="请输入接口的token信息"></el-input>
                            </el-form-item>
                            <p style="color: red">同步接口会覆盖现有的API组织架构及API接口，请谨慎操作！</p>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="tbdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="synchronizationAPIConfirm('apiForm')">同 步</el-button>
                      </span>
                    </el-dialog>


                    &nbsp环境:
                    <el-select
                        placeholder="请选择"
                        size="small"
                        tyle="margin-left: -6px"
                        v-model="currentHost"
                    >
                        <el-option
                            v-for="item in hostOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name">
                        </el-option>
                    </el-select>
                    &nbsp配置:
                    <el-select
                        placeholder="请选择"
                        size="small"
                        tyle="margin-left: -6px"
                        v-model="currentConfig"
                        filterable
                    >
                        <el-option
                            v-for="item in configOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name">
                        </el-option>
                    </el-select>

                    <el-button
                       
                        v-if="!addAPIFlag && permissions.includes('add')"
                        style="margin-left: 20px"
                        type="primary"          
                        size="mini"
                        @click="run = !run"
                    >运行</el-button>


                    <el-button
                
                        v-if="!addAPIFlag && permissions.includes('delete')"
                        type="danger"             
                        size="mini"
                        @click="del = !del"
                    >批量删除</el-button>

                    <el-button
                        :disabled="!addAPIFlag"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="handleBackList"
                    >返回列表
                    </el-button>
                </div>
            </div>
        </el-header>

        <el-container>
            <el-aside style="margin-top: 10px;">
                <div class="nav-api-side">
                    <div class="api-tree">
                        <el-input
                            placeholder="输入关键字进行过滤"
                            v-model="filterText"
                            size="medium"
                            clearable
                            prefix-icon="el-icon-search"
                        >
                        </el-input>
                        <el-tree
                            @node-click="handleNodeClick"
                            :data="dataTree"
                            node-key="id"
                            :default-expand-all="false"
                            :expand-on-click-node="false"
                            draggable
                            highlight-current
                            :filter-node-method="filterNode"
                            ref="tree2"
                            @node-drag-end="handleDragEnd"
                        >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                        </el-tree>
                    </div>

                </div>

            </el-aside>

            <el-main style="padding: 0;">
                <api-body
                    v-show="addAPIFlag"
                    :nodeId="currentNode.id"
                    :project="$route.params.id"
                    :response="response"
                    v-on:addSuccess="handleAddSuccess"
                    :config="currentConfig"
                    :host="currentHost"
                >
                </api-body>

                <api-list
                    v-show="!addAPIFlag"
                    v-on:api="handleAPI"
                    :permissions="permissions"
                    :node="currentNode !== '' ? currentNode.id : '' "
                    :project="$route.params.id"
                    :config="currentConfig"
                    :host="currentHost"
                    :del="del"
                    :back="back"
                    :run="run"
                >
                </api-list>

            </el-main>
        </el-container>
    </el-container>

</template>

<script>
    import ApiBody from './components/ApiBody'
    import ApiList from './components/ApiList'    
    import {getTree,updateTree } from "../../../restful/tree";
    import {getAllHost,getAllConfig } from "../../../restful/configpage";
    import * as apipage from "../../../restful/apipage";
    import { Alert, Loading } from 'element-ui';
    import {getpermissions} from "../../../restful/userinfo";
    
    export default {
        watch: {
            filterText(val) {
                this.$refs.tree2.filter(val);
            }
        },
        components: {
            ApiBody,
            ApiList
        },

        computed: {
            initResponse: {
                get() {
                    return this.addAPIFlag;
                },
                set(value) {
                    this.addAPIFlag = value;
                    this.response = {
                        id: '',
                        body: {
                            name: '',
                            times: 1,
                            url: '',
                            method: 'POST',
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
                            validate: [{
                                expect: "",
                                actual: "",
                                comparator: "equals",
                                type: 1
                            }],
                            variables: [{
                                key: "",
                                value: "",
                                desc: "",
                                type: 1
                            }],
                            extract: [{
                                key: "",
                                value: "",
                                desc: ""
                            }],
                            hooks: [{
                                setup: "",
                                teardown: ""
                            }],
                            sqlVariables:[{
                            key:'',
                            database:'',
                            databasetype:'',
                            query:{params1:"",params2:"",params3:"",params4:""},
                            desc:""
                        }]
                        },

                    };
                }
            },
        },
        data() {
            return {
                loading: false,
                configOptions: [],
                hostOptions: [],
                permissions:[],
                currentConfig: '请选择',
                currentHost: '请选择',
                back: false,
                del: false,
                run: false,
                response: '',
                apiForm:{
                    swaggerurl:'',
                    token:'',
                },
                nodeForm: {
                    name: '',
                },
                rules: {
                    name: [
                        {required: true, message: '请输入节点名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    swaggerurl:[
                        {required: true, message: '请输入API地址', trigger: 'blur'},
                    ],
                    token:[
                        {required: true, message: '请输入token信息', trigger: 'blur'},
                    ]
                },
                radio: '根节点',
                addAPIFlag: false,
                treeId: '',
                maxId: '',
                rmid:'',
                dialogVisible: false,
                tbdialogVisible:false,
                currentNode: '',
                data: '',
                filterText: '',
                expand: '&#xe65f;',
                dataTree: [],
                

            }
        },
        methods: {
            quxiao(){
              this.nodeForm.name='';
              this.dialogVisible=false
            },
            opentb(){
                this.apiForm={
                    swaggerurl:'',
                    token:'',                 
                };
                this.tbdialogVisible=true;
            },
            handleBackList() {
                this.addAPIFlag = false;
                this.back = !this.back;
            },
            handleDragEnd() {
                this.updateTree(false);
            },
            handleAddSuccess() {
                this.back = !this.back;
                this.addAPIFlag = false;
            },
            getpermissions() {
                getpermissions({app_label:"test_runner",model:"api"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            handleAPI(response) {
                this.addAPIFlag = true;
                this.response = response;
            },
            synchronizationAPIConfirm(formName) {
                this.$refs[formName].validate(valid => {
                    if (valid){
                    this.$confirm('此操作将覆盖所有分组和接口, 是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }).then(() => {     
                        let loadingInstance = Loading.service({
                            text: '加载中... 请稍后',
                           background:"rgba(0, 0, 0, 0.8)"
                        }); 
                                    
                        apipage.synchronizationapi({
                                        project: this.$route.params.id,
                                        swaggerurl: this.apiForm.swaggerurl,
                                        token: this.apiForm.token,
                                        nodeid:this.currentNode.id,
                        }).then(resp => { 
                            
                            if (resp.data.success){
                                this.tbdialogVisible = false; 
                                loadingInstance.close();
                                location.reload() 
                             
                            } else{
                                this.$message.error(resp.data.msg);
                                loadingInstance.close();
                            }
                            loadingInstance.close();
                                              
                                              
                        }) 
                                        
                   
                                                 
                    })}
                     
                })
            },

            getTree() {
                getTree(this.$route.params.id, {params: {type: 1}}).then(resp => {
                    this.dataTree = resp['tree'];
                    this.treeId = resp['id'];
                    this.maxId = resp['max'];
                })
            },
            getConfig() {
                getAllConfig(this.$route.params.id).then(resp => {
                    this.configOptions = resp["results"];
                    this.configOptions.push({
                        name: '请选择'
                    })
                })
            },

            getHost() {
                getAllHost(this.$route.params.id).then(resp => {
                    this.hostOptions = resp["results"];
                    this.hostOptions.push({
                        name: '请选择'
                    })
                })
            },

            updateTree(mode) {
                updateTree(this.treeId, {
                    body: this.dataTree,
                    node: this.currentNode.id,
                    mode: mode,
                    type: 1
                }).then(resp => {
                    if (resp['success']) {
                        this.dataTree = resp['tree'];
                        this.maxId = resp['max'];
                    } else {
                        this.$message.error(resp['msg']);
                    }
                })
            },

            deleteNode() {
                this.$confirm('此操作将永久删除该节点下所有接口, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    if (this.currentNode === '') {
                        this.$message.info('请选择一个节点');
                    } else {
                        if (this.currentNode.children.length !== 0) {
                            this.$message.warning('此节点有子节点，不可删除！');
                        } else {
                            this.remove(this.currentNode, this.data);
                            this.updateTree(true);
                        }
                    }

                })
            },

            renameNode() {
                this.$prompt('请输入节点名', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    inputPattern: /\S/,
                    inputErrorMessage: '节点名称不能为空'
                }).then(({value}) => {
                    const parent = this.data.parent;
                    const children = parent.data.children || parent.data;
                    const index = children.findIndex(d => d.id === this.currentNode.id);
                    children[index]["label"] = value
                    this.updateTree(false);
                });
            },


            handleConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.append(this.currentNode);
                        this.updateTree(false);
                        this.nodeForm.name="";
                        this.dialogVisible = false;
                    }
                });
            },

            handleNodeClick(node, data) {
                this.addAPIFlag = false;
                this.currentNode = node;
                this.data = data;
            },

            filterNode(value, data) {
                if (!value) return true;
                return data.label.indexOf(value) !== -1;
            },

            remove(data, node) {
                const parent = node.parent;
                const children = parent.data.children || parent.data;
                const index = children.findIndex(d => d.id === data.id);
                children.splice(index, 1);
            },

            append(data) {
     
            function S4() {
                return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
            }
            function guid() {
                return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
                              }
              


                const newChild = {id: guid()  , label: this.nodeForm.name, children: []};
                if (data === '' || this.dataTree.length === 0 || this.radio === '根节点') {
                    this.dataTree.push(newChild);
                    return
                }
                if (!data.children) {
                    this.$set(data, 'children', []);
                }
                data.children.push(newChild);
            },

        },
        name: "RecordApi",
        mounted() {
            this.getTree();
            this.getConfig();
            this.getHost();
            this.getpermissions();
        }
    }
</script>

<style scoped>


</style>
