<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 10px">
                    <el-button
                    v-if="permissions.includes('add')"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus"
                        @click="dialogVisible = true"
                        :disabled="!addTestActivate"
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
                        type="danger"
                        size="small"
                        icon="el-icon-delete"
                        @click="deleteNode"
                        :disabled="buttonActivate"
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
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="buttonActivate=false"
                        :disabled="buttonActivate"
                    >添加用例
                    </el-button>
                    <el-button
                    v-if="permissions.includes('add')"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="opensy()"
                        :disabled="buttonActivate"
                    >同步用例
                    </el-button>
                        <el-dialog
                            title="同步目标项目用例"
                            :visible.sync="syncdialogVisible"
                            width="25%"
                            align="center"
                            center
                        >
                            <el-form
                                :model="syncForm"
                                :rules="rules"
                                ref="syncForm"
                                label-width="120px"
                                class="project">

                                <el-form-item label="项目源" prop="oldproject"                             
                                >
                                    <el-select
                                    style="float: left;"                                    
                                    size="medium"
                                    @change="getoldtree($event)"   
                                    @clear="clearid()"                                                            
                                    clearable
                                    v-model="syncForm.oldproject"
                                     placeholder="请选择">
                                    <el-option
                                        v-for="item in projectlist"
                                        :key="item.id"
                                        v-if="item.id!=excludeproject"
                                        :label="item.name"
                                        :value="item.id">
                                        </el-option>
                                    </el-select>
                                
                                </el-form-item>
                                <el-form-item label="分组源" prop="oldnodeid">
                                <el-select      
                                    style="float: left;"                               
                                    clearable
                                    v-model="syncForm.oldnodeid"
                                     placeholder="请选择">
                                        <el-option
                                        v-for="item in oldtree"
                                        :key="item.id"
                                        :label="item.label"
                                        :value="item.id">
                                        </el-option>
                                    </el-select>
                                   
                                </el-form-item>
                                <p style="color: red">同步用例会覆盖现有的所选分组下的用例和子级分组，请谨慎操作！</p>
                            </el-form>
                            <span slot="footer" class="dialog-footer" >
                            <el-button @click="synsqx()">取 消</el-button>
                            <el-button type="primary" @click="syncCaseConfirm('syncForm')">同 步</el-button>
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
                        :disabled="addTestActivate"
                    >
                        <el-option
                            v-for="item in configOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name"
                        >
                        </el-option>
                    </el-select>


                    <el-button
                  
                        v-if="addTestActivate && permissions.includes('add')"
                        style="margin-left: 20px"
                        type="primary"                    
                      
                        size="mini"
                        @click="run = !run"
                    >运行</el-button>

                    <el-button
                   
                        v-if="addTestActivate && permissions.includes('delete')"
                        style="margin-left: 20px"
                        type="danger"                   
                        size="mini"
                        @click="del = !del"
                    >批量删除</el-button>

                    <el-button
                        :disabled="addTestActivate"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="handleBackList"
                    >返回列表
                    </el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-aside
                style="margin-top: 10px;"
                v-show="addTestActivate"
            >
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
                <test-list
                    :permissions='permissions'
                    v-show="addTestActivate"
                    :project="$route.params.id"
                    :node="currentNode !== '' ? currentNode.id : '' "
                    :del="del"
                    v-on:testStep="handleTestStep"
                    :back="back"
                    :run="run"
                    :host="currentHost"
                >
                </test-list>

                <edit-test
                    :back="back"
                    v-show="!addTestActivate"
                    :project="$route.params.id"
                    :node="currentNode.id"
                    :testStepResp="testStepResp"
                    :config="currentConfig"                  
                    :host="currentHost"
                    v-on:addSuccess="handleBackList"
                >
                </edit-test>

            </el-main>
        </el-container>
    </el-container>

</template>

<script>
    import EditTest from './components/EditTest'
    import TestList from './components/TestList'
    import {getTree,updateTree } from "../../../restful/tree";
    import {getAllHost,getAllConfig } from "../../../restful/configpage";
    import { Alert, Loading } from 'element-ui';
    import {getProjectList} from "../../../restful/project";
    import {getOneLevelTree} from "../../../restful/tree";
    import {generateCase} from "../../../restful/apicase";
    import {getpermissions} from "../../../restful/userinfo";
    export default {
        computed: {
            buttonActivate: {
                get: function () {
                    return !this.addTestActivate || this.currentNode === '';
                },
                set: function (value) {
                    this.addTestActivate = value;
                    this.testStepResp = [];
                }
            }
        },
        watch: {
            filterText(val) {
                this.$refs.tree2.filter(val);
            }
        },
        components: {
            EditTest,
            TestList,
        },
        data() {
            return {
                permissions:[],
                loading: false,
                excludeproject:this.$route.params.id,
                testStepResp: [],
                syncdialogVisible:false,
                syncForm:{
                    oldproject:"",
                    oldnodeid:"",
                },
                nodeForm: {
                    name: '',
                },
                rules: {
                    name: [
                        {required: true, message: '请输入节点名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    oldproject:[
                        {required:true,message:"请选择用例项目源",trigger:'blur'}
                    ],
                    oldnodeid:[
                        {required:true,message:"请选择用例分组源",trigger:'blur'}
                    ]
                },
                hostOptions:[],
                back: false,
                del: false,
                run: false,
                radio: '根节点',
                addTestActivate: true,
                currentConfig: '请选择',
                currentHost:'请选择',            
                treeId: '',
                maxId: '',
                dialogVisible: false,
                currentNode: '',
                data: '',
                filterText: '',
                expand: '&#xe65f;',
                oldtree:[],
                projectlist:[],
                dataTree: [],
                configOptions: []
            }
        },
        methods: {
            clearid(){
                this.syncForm.oldproject="",
                this.syncForm.oldnodeid=""
            },
            synsqx(){
                this.clearid()
                this.syncdialogVisible=false
            },
            opensy(){
                this.clearid()
                this.syncdialogVisible=true,
                this.getpojectlsit()
            },
            getpojectlsit(){
                getProjectList().then(resp =>{
                        this.projectlist=resp.results
                })
            },
            getoldtree(val){
                if(val != null && val != '' && val != undefined){
                getOneLevelTree({params:{
                    project: val,
                    type:2
                }}).then(resp =>{
                    this.oldtree=resp.tree
                })}
            },
            getpermissions() {
                getpermissions({app_label:"test_runner",model:"case"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            syncCaseConfirm(formName) {
                this.$refs[formName].validate(valid => {
                    if (valid){
                    this.$confirm('此操作将覆盖所选分组的用例和组织, 是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }).then(() => {     
                        let loadingInstance = Loading.service({
                            text: '加载中... 请稍后',
                           background:"rgba(0, 0, 0, 0.8)"
                        });                 
                        generateCase({
                                        project: this.$route.params.id,                                            
                                        nodeid:this.currentNode.id,
                                        oldproject:this.syncForm.oldproject,
                                        oldnodeid:this.syncForm.oldnodeid
                        }).then(resp => {
                            if (resp.success){
                                this.clearid()                                
                                this.syncdialogVisible = false;  
                                loadingInstance.close()
                                this.$message.info({
                                    message: resp.msg,
                                    duration: 1000
                                })
                                location.reload() 
                             
                            }
                            else{
                                loadingInstance.close()
                                this.$message.info({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            } 
                                     
                                                    
                        })  
                        loadingInstance.close()
                      
                                        
                    })}
                })
            },
            handleDragEnd() {
                this.updateTree(false);
            },
            getConfig() {
                getAllConfig(this.$route.params.id).then(resp => {
                    this.configOptions = resp["results"];
                    this.configOptions.push({
                        name: '请选择'
                    })
                })
            },

            handleBackList() {
                this.addTestActivate = true;
                this.back = !this.back;
            },
            quxiao(){
                 this.nodeForm.name='';
                 this.dialogVisible=false
            },              
            
            handleTestStep(resp) {
				console.log("-----------handleTestStep----------------")
				console.log(resp)
                this.testStepResp = resp;
                this.addTestActivate = false;
            },
            getTree() {
                getTree(this.$route.params.id, {params: {type: 2}}).then(resp => {
                    this.dataTree = resp['tree'];
                    this.treeId = resp['id'];
                    this.maxId = resp['max'];
                })
            },

            updateTree(mode) {
                updateTree(this.treeId, {
                    mode: mode,
                    body: this.dataTree,
                    node: this.currentNode.id,
                    type: 2
                }).then(resp => {
                    if (resp['success']) {
                        this.dataTree = resp['tree'];
                        this.maxId = resp['max'];
                    } else {
                        this.$message.error(resp['msg']);
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

            deleteNode() {
                this.$confirm('此操作将永久删除该节点下所有用例, 是否继续?', '提示', {
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

            handleConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.append(this.currentNode);
                        this.updateTree(false);
                        this.dialogVisible = false;
                        this.nodeForm.name='';
                    }
                });
            },

            handleNodeClick(node, data) {
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
                const newChild = {id:  guid(), label: this.nodeForm.name, children: []};
                if (data === '' || this.dataTree.length === 0 || this.radio === '根节点') {
                    this.dataTree.push(newChild);
                    return
                }
                if (!data.children) {
                    this.$set(data, 'children', []);
                }
                data.children.push(newChild);
            },
            getHost() {
                getAllHost(this.$route.params.id).then(resp => {
                    this.hostOptions = resp["results"];
                    this.hostOptions.push({
                        name: '请选择'
                    })
                })
            },

        },
        name: "AutoTest",
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
