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
                    >添加用例
                    </el-button>            


                    <!-- &nbsp环境:
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
                    </el-select> -->
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
                        v-if="!addCaseFlag && permissions.includes('add')"
                        style="margin-left: 20px"
                        type="primary"          
                        size="mini"
                        @click="run = !run"
                    >运行</el-button>


                    <el-button
                        v-if="!addCaseFlag && permissions.includes('delete')"
                        type="danger"             
                        size="mini"
                        @click="del = !del"
                    >批量删除</el-button>

                    <el-button
                        :disabled="!addCaseFlag"
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
                <case-body
                    v-show="addCaseFlag"
                    :nodeId="currentNode.id"
                    :project="$route.params.id"
                    :response="response"
                    v-on:addSuccess="handleAddSuccess"
                    :config="currentConfig"
                    :host="currentHost"
                >
                </case-body>

                <case-list
                    :permissions="permissions"
                    v-show="!addCaseFlag"
                    v-on:api="handleAPI"
                    :node="currentNode !== '' ? currentNode.id : '' "
                    :project="$route.params.id"
                    :config="currentConfig"
                    :host="currentHost"
                    :del="del"
                    :back="back"
                    :run="run"
                >
                </case-list>

            </el-main>
        </el-container>
    </el-container>

</template>

<script>
    import CaseBody from './components/CaseBody'
    import CaseList from './components/CaseList'
    import {getAllHost,getAllUiConfig } from "../../../restful/configpage";    
    import {getTree,updateTree } from "../../../restful/tree";
    import { Alert, Loading } from 'element-ui';
     import {getpermissions} from "../../../restful/userinfo";
    export default {
        watch: {
            filterText(val) {
                this.$refs.tree2.filter(val);
            }
        },
        components: {
            CaseBody,
            CaseList
        },

        computed: {
            initResponse: {
                get() {
                    return this.addCaseFlag;
                },
                set(value) {
                    this.addCaseFlag = value;
                    this.response = {
                        id: '',
                        name: '',                          
                        casedescribe: '', 
                        body:  [{
                                rowkeyid: this.guid(),
                                describe: '',
                                action: '',
                                locationType: '',
                                locationValue:'',
                                CheckValueOurce:'',
                                AttributeName:'',
                                CheckType:'',
                                DataItem:''
                            }],                 
                        variables: [{
                                key: "",
                                value: "",
                                desc: "",
                                type: 1
                            }],                     
                        
                    };
                }
            },
        },
        data() {
            return {
                permissions:[],
                loading: false,
                configOptions: [],
                hostOptions: [],
                currentConfig: '请选择',
                currentHost: '请选择',
                back: false,
                del: false,
                run: false,
                response: '',
               
                nodeForm: {
                    name: '',
                },
                rules: {
                    name: [
                        {required: true, message: '请输入节点名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
           
                },
                radio: '根节点',
                addCaseFlag: false,
                treeId: '',
                maxId: '',
                rmid:'',
                dialogVisible: false,              
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
            S4() {
                return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
            },
           guid() {
                return (this.S4()+this.S4()+"-"+this.S4()+"-"+this.S4()+"-"+this.S4()+"-"+this.S4()+this.S4()+this.S4());
                              },
            handleBackList() {
                this.addCaseFlag = false;
                this.back = !this.back;
            },
            handleDragEnd() {
                this.updateTree(false);
            },
            handleAddSuccess() {
                this.back = !this.back;
                this.addCaseFlag = false;
            },

            handleAPI(response) {
                this.addCaseFlag = true;
                this.response = response;
            },

            getpermissions() {
                getpermissions({app_label:"TestRunner",model:"uicase"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            getTree() {
                getTree(this.$route.params.id, {params: {type: 3}}).then(resp => {
                    this.dataTree = resp['tree'];
                    this.treeId = resp['id'];
                    this.maxId = resp['max'];
                })
            },
            getConfig() {
                getAllUiConfig(this.$route.params.id).then(resp => {
                    this.configOptions = resp;
                    this.configOptions.push({
                        name: '请选择'
                    })
                })
            },

            getHost() {
                getAllHost(this.$route.params.id).then(resp => {
                    this.hostOptions = resp;
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
                    type: 3
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
                this.addCaseFlag = false;
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
     
            // function S4() {
            //     return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
            // }
            // function guid() {
            //     return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
            //                   }
              


                const newChild = {id: this.guid()  , label: this.nodeForm.name, children: []};
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
        name: "webtestcaselist",
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
