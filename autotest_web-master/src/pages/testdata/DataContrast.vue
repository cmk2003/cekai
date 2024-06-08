<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                     v-if="permissions.includes('view')"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="dialogVisible=true"
                    >添加数据核对
                    </el-button>
             
                    <el-button
                     v-if="permissions.includes('delete')"
                        v-show="DataContrastData.count !== 0 "
                        style="margin-left: 20px"
                        type="danger"
                        icon="el-icon-delete"                        
                        size="small"
                        @click="delSelectionVariables"
                    >批量删除</el-button>         
                    <el-dialog
                        title="核对结果"
                        :visible.sync="resultdialogVisible"
                        width="50%"                        
                        align="center"
                    >                          
                            <div  class="outer-container">
                                <div class="inner-container"  >
                                    <div                                                                
                                    v-for="item in results"
                                     :key="item"  >
                                     <span >{{item}}</span>
                                     </div>                                 
                                                                    
                                </div>
                            </div>
          
                    
                    </el-dialog>
                  <el-dialog
                        title="请选择运行方式"
                        :visible.sync="asdialogVisible"                      
                        width="20%"
                        center
                        
                    >
                    <p style="color: red;text-align: center">部分EXCEL打开时间较长，建议使用异步执行</p>
                        <el-form                                            
                            :model="asynform"         
                            :rules="rules"                
                            ref="asynform"
                            label-width="100px"
                            class="project"
                            style="text-align: center"
                            >
                          <div style="margin-top: 20px; ">
                            <el-radio v-model="asynform.isasyncs" :label= false border size="medium" prop="isasyncs">调试</el-radio>
                            <el-radio v-model="asynform.isasyncs" :label= true border size="medium" prop="isasyncs">异步</el-radio>
                        </div>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="asdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handrunDataContrastById()">确 定</el-button>
                      </span>
                    </el-dialog>
            
                    <el-dialog
                        title="添加数据核对"
                        :visible.sync="dialogVisible"
                        width="30%"
                        center
                    >
                        <el-form
                            :model="DataContrastForm"
                            :rules="rules"
                            ref="DataContrastForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="文件一" prop="fileonename">
                                   <el-select    
                                                                                           
                                    size="medium"
                                  style="float: left;width:100%"  
                                  @change="getfileoneexceltree($event)"
                                    @clear="clearone()"                                                            
                                    clearable
                                    v-model="DataContrastForm.fileonename"
                                     placeholder="请选择文件一">
                                    <el-option
                                        v-for="item in testData"
                                        :key="item.name"                                     
                                        :label="item.name"
                                        :value="item.name">
                                        </el-option>
                                    </el-select>                        
                            </el-form-item>
                            <el-form-item label="sheet" prop="fileonesheet">
                                <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"  
                                                                                       
                                    clearable
                                    v-model="DataContrastForm.fileonesheet"
                                     placeholder="请选择sheet页">
                                    <el-option
                                        v-for="item in fileoneexceltree"
                                        :key="item.value"                                     
                                        :label="item.label"
                                        :value="item.value">
                                        </el-option>
                                    </el-select>                               
                            </el-form-item>
                            <el-form-item label="单元格范围" prop="fileoneRange">
                                <el-input v-model="DataContrastForm.fileoneRange" clearable placeholder="请输入核对的单元格范围,比如：A1:B5"></el-input>
                            </el-form-item>
                            <el-form-item label="文件二" prop="filetwoname">
                                    <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"  
                                  @change="getfiletwoexceltree($event)"
                                    @clear="cleartwo()"                                                            
                                    clearable
                                    v-model="DataContrastForm.filetwoname"
                                     placeholder="请选择文件二">
                                    <el-option
                                        v-for="item in testData"
                                        :key="item.name"                                     
                                        :label="item.name"
                                        :value="item.name">
                                        </el-option>
                                    </el-select>   
                  
                            </el-form-item>
                            <el-form-item label="sheet" prop="filetwosheet">
                                 <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"                                                                                         
                                    clearable
                                    v-model="DataContrastForm.filetwosheet"
                                     placeholder="请选择sheet页">
                                    <el-option
                                        v-for="item in filetwoexceltree"
                                        :key="item.value"                                     
                                        :label="item.label"
                                        :value="item.value">
                                        </el-option>
                                    </el-select>     
                            </el-form-item>
                            <el-form-item label="单元格范围" prop="filetwoRange">
                                <el-input v-model="DataContrastForm.filetwoRange" clearable placeholder="请输入核对的单元格范围,比如：A1:B5"></el-input>
                            </el-form-item>
                            <el-form-item label="描述" prop="desc">
                                <el-input v-model="DataContrastForm.desc" clearable placeholder="请输入简要描述"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer" >
                        <el-button @click="dialogVisible = false" >取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('DataContrastForm')">确 定</el-button>
                      </span>
                    </el-dialog>

                    <el-dialog
                        title="编辑数据核对"
                        :visible.sync="editdialogVisible"
                        width="30%"
                        center
                    >
                        <el-form
                            :model="editDataContrastForm"
                            :rules="rules"
                            ref="editDataContrastForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="文件一" prop="fileonename">             
                                   <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"  
                                  @change="getfileoneexceltree($event)"
                                    @clear="clearone()"                                                            
                                    clearable
                                    v-model="editDataContrastForm.fileonename"
                                     placeholder="请选择文件一">
                                    <el-option
                                        v-for="item in testData"
                                        :key="item.name"                                     
                                        :label="item.name"
                                        :value="item.name">
                                        </el-option>
                                    </el-select>   
                            </el-form-item>
                            <el-form-item label="sheet" prop="fileonesheet">
                                <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"                                                                                         
                                    clearable
                                    v-model="editDataContrastForm.fileonesheet"
                                     placeholder="请选择sheet页">
                                    <el-option
                                        v-for="item in fileoneexceltree"
                                        :key="item.value"                                     
                                        :label="item.label"
                                        :value="item.value">
                                        </el-option>
                                    </el-select>     
                           
                            </el-form-item>
                            <el-form-item label="单元格范围" prop="fileoneRange">
                                <el-input v-model="editDataContrastForm.fileoneRange" clearable placeholder="请输入核对的单元格范围,比如：A1:B5"></el-input>
                            </el-form-item>
                            <el-form-item label="文件二" prop="filetwoname">
                                <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"  
                                  @change="getfiletwoexceltree($event)"
                                    @clear="cleartwo()"                                                            
                                    clearable
                                    v-model="editDataContrastForm.filetwoname"
                                     placeholder="请选择文件二">
                                    <el-option
                                        v-for="item in testData"
                                        :key="item.name"                                     
                                        :label="item.name"
                                        :value="item.name">
                                        </el-option>
                                    </el-select>   
                            
                            </el-form-item>
                            <el-form-item label="sheet" prop="filetwosheet">
                            <el-select                                                               
                                    size="medium"
                                  style="float: left;width:100%"                                                                                         
                                    clearable
                                    v-model="editDataContrastForm.filetwosheet"
                                     placeholder="请选择sheet页">
                                    <el-option
                                        v-for="item in filetwoexceltree"
                                        :key="item.value"                                     
                                        :label="item.label"
                                        :value="item.value">
                                        </el-option>
                                    </el-select>    
           
                            </el-form-item>
                            <el-form-item label="单元格范围" prop="filetwoRange">
                                <el-input v-model="editDataContrastForm.filetwoRange" clearable placeholder="请输入核对的单元格范围,比如：A1:B5"></el-input>
                            </el-form-item>
                            <el-form-item label="描述" prop="desc">
                                <el-input v-model="editDataContrastForm.desc" clearable placeholder="请输入简要描述"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="editdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleEditConfirm('editDataContrastForm')">确 定</el-button>
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
                            <el-input placeholder="请输入关键字"  clearable v-model="search">
                                <el-button slot="append" icon="el-icon-search" @click="getDataContrastList"></el-button>
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
                            :data="DataContrastData.results"
                            :show-header="DataContrastData.results.length !== 0 "
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
                                label="文件一"
                                 show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.fileonename}}-{{scope.row.fileonesheet}}-[{{scope.row.fileoneRange}}]</div>
                                </template>
                            </el-table-column>      
                            <el-table-column
                                label="文件二"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div >{{scope.row.filetwoname}}-{{scope.row.filetwosheet}}-[{{scope.row.filetwoRange}}]</div>

                                </template>
                            </el-table-column>
                            <el-table-column
                                label="描述"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div >{{scope.row.desc}}</div>

                                </template>
                            </el-table-column>
                            <el-table-column
                                label="状态"
                                show-overflow-tooltip
                                width="100"
                            >
                                <template slot-scope="scope">

                                    <div v-if="scope.row.Status==0">未核对</div>
                                    <div v-if="scope.row.Status==1">核对中</div>
                                    <div v-if="scope.row.Status==2">核对完成</div>

                                </template>
                            </el-table-column>
                            <el-table-column
                            width="100"
                                label="创建人"
                                show-overflow-tooltip
                            >
                                <template slot-scope="scope">
                                    <div >{{scope.row.create_user}}</div>

                                </template>
                            </el-table-column>
                            <el-table-column
                                label="更新时间"
                                width="200"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.update_time|datetimeFormat}}</div>

                                </template>
                            </el-table-column>

                            <el-table-column
                             width="300"
                            label="操作">
                                <template slot-scope="scope">
                                    <el-row v-show="currentRow === scope.row">
                                         <el-button
                                            v-if="permissions.includes('add')"
                                            type="success"                                           
                                            size="mini"
                                            @click="showtable(scope.row.id)"
                                        >核对</el-button>
                                        <el-button
                                        v-if="permissions.includes('change')"
                                            type="info"                                           
                                            size="mini"
                                            @click="handleDataContrast(scope.row)"
                                        >编辑</el-button>
                                        <el-button
                                            v-if="permissions.includes('view')"
                                            type="warning"                                           
                                            size="mini"
                                            @click="handlerelustDataContrasts(scope.row.result)"
                                        >查看</el-button>
                                        <el-button
                                            v-if="permissions.includes('delete')"
                                            v-show="DataContrastData.count !== 0"
                                            type="danger"                                  
                                            size="mini"
                                            @click="handleDelDataContrast(scope.row.id)"
                                        >删除
                                        </el-button>
                                    </el-row>
                                </template>

                            </el-table-column>

                        </el-table>
                        <el-col :span="7">
                            <el-pagination
                                :page-size="5"
                                v-show="DataContrastData.count !== 0 "
                                style="padding-top:10px;"
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="DataContrastData.count"
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

  import *as FileAPI from "../../restful/filepage";
   import {getpermissions} from "../../restful/userinfo";
    export default {


        data() {
            return {
                resultdialogVisible:false,
                search: '',
                selectVariables: [],
                currentRow: '',
                currentPage: 1,
                permissions:[],
                fileoneexceltree:[],
                filetwoexceltree:[],
                DataContrastData:{
                    count: 0,
                    results: []
                },
                testData:[],
                results:[],
                asdialogVisible:false,
                editdialogVisible: false,
                dialogVisible: false,          
                DataContrastForm: {
                    fileonename: '',
                    fileoneid:'',
                    fileonesheet: '',
                    filetwoname: '',
                    filetwoid:'',
                    filetwosheet:'',
                    project: this.$route.params.id,
                    fileoneRange:'',
                    filetwoRange:'',
                    desc:''
                },
                asynform:{
                    isasyncs:  true,
                    project: this.$route.params.id,
                    id:'',
                },          
                editDataContrastForm: {
                    fileonename: '',
                    fileoneid:'',
                    fileonesheet: '',
                    filetwoname: '',
                    filetwoid:'',
                    filetwosheet:'',   
                    fileoneRange:'',
                    filetwoRange:'',
                    desc:'',
                    id: ''
                },

                rules: {
                    fileonename: [
                        {required: true, message: '请选择文件一', trigger: 'blur'},
                    ],
                    fileonesheet: [
                        {required: true, message: '请选择sheet页', trigger: 'blur'},               
                    ],
                    filetwoname: [
                        {required: true, message: '请选择文件二', trigger: 'blur'},
                    ],
                    filetwosheet: [
                        {required: true, message: '请选择sheet页', trigger: 'blur'},
                    ],
                    isasyncs:[{
                        required: true, message: '请选择运行方式', trigger: 'blur'
                    }],
                     fileoneRange: [
                        {required: true, message: '请输入文件一单元格范围', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                    filetwoRange: [
                        {required: true, message: '请输入文件二单元格范围', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
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

            handlerelustDataContrasts(row){
                this.results=row
                this.resultdialogVisible=true
            },
            getpermissions() {
                getpermissions({app_label:"test_runner",model:"modelwithfilefield"}).then(resp => {
                    this.permissions = resp["permissions"];
                   
                })
            },
            handleDataContrast(row) {
          
                this.editDataContrastForm = {
                    fileonename: row.fileonename,
                    fileoneid:row.fileoneid,
                    fileonesheet: row.fileonesheet,
                    filetwoname:row.filetwoname,
                    filetwoid:row.filetwoid,
                    filetwosheet:row.filetwosheet,
                    fileoneRange:row.fileoneRange,
                    filetwoRange:row.filetwoRange,
                    desc:row.desc,
                    id: row.id
                };

                this.editdialogVisible = true;
            },
            showtable(index){
                this.asynform={
                    isasyncs:  true,
                    project: this.$route.params.id,
                    id: index
                };
                this.asdialogVisible=true
            },
            handrunDataContrastById(){
                this.asdialogVisible=false
                FileAPI.RunDataContrastById(this.asynform.id,{params:{
                    project: this.$route.params.id,
                    isasyncs: this.asynform.isasyncs,
                }}).then(resp =>{
                    if (resp.success){
                        this.$message.success(resp.msg);
                        this.getDataContrastList();
                    }else{
                         this.$message.error(resp.msg);
                    }
                }) 
            },
            handleDelDataContrast(index) {
                this.$confirm('此操作将永久删除该核对记录，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    FileAPI.delDataContrast(index).then(resp => {
                        if (resp.success) {
                            this.getDataContrastList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            },
            handleSelectionChange(val) {
                this.selectVariables = val;
            },

            getfileoneexceltree(name){          
            this.DataContrastForm.fileonesheet='';
            this.editDataContrastForm.fileonesheet='';
            if(name != null && name != '' && name != undefined){
             let obj={};
                obj = this.testData.find(item =>{
                    return item.name==name;
                });
            this.DataContrastForm.fileoneid=obj.id;
            this.editDataContrastForm.fileoneid=obj.id;
            this.fileoneexceltree=obj.excel_tree.children;
        }
            },
        getfiletwoexceltree(name){          
            this.DataContrastForm.filetwosheet='';
             this.editDataContrastForm.filetwosheet='';
            if(name != null && name != '' && name != undefined){
             let obj={};
                obj = this.testData.find(item =>{
                    return item.name==name;
                });
            this.DataContrastForm.filetwoid=obj.id;
            this.editDataContrastForm.filetwoid=obj.id;
            this.filetwoexceltree=obj.excel_tree.children
        }
            },
            clearone(){
                this.DataContrastForm.fileonename="",
                this.DataContrastForm.fileoneid='',
                this.DataContrastForm.fileonesheet="",
                this.editDataContrastForm.fileonename='',
                this.editDataContrastForm.fileonesheet=''
            },
            cleartwo(){
                this.DataContrastForm.filetwoname="",
                this.DataContrastForm.filetwosheet="",
                this.DataContrastForm.filetwoid='',
                this.editDataContrastForm.filetwoname='',
                this.editDataContrastForm.filetwosheet=''
            },
            getTestdataList() {
                FileAPI.testdataList({
                    params:{
                        project: this.$route.params.id,
                        search: '',
                        node: '',
                    
                }}).then(resp => {
                    this.testData = resp.results;                 
                })
            },
            handleCurrentChange(val) {
                FileAPI.getDataContrastPaginationBypage({
                    params: {
                        page: this.currentPage,
                        project: this.$route.params.id,
                        search: this.search
                    }
                }).then(resp => {
                    this.DataContrastData = resp;
                })
            },
            delSelectionVariables() {
                if (this.selectVariables.length !== 0) {
                    this.$confirm('此操作将永久删除勾选的核对记录，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        FileAPI.delAllDataContrast({data: this.selectVariables}).then(resp => {
                            this.getDataContrastList();
                        })
                    })
                } else {
                    this.$notify.warning({
                        title: '提示',
                        message: '请至少勾选一个核对记录',
                        duration: 1000
                    })
                }
            },

            handleConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.dialogVisible = false;
                        FileAPI.addDataContrast(this.DataContrastForm).then(resp => {
                            if (!resp.success) {
                                this.$message.info({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            } else {
                                this.DataContrastForm.fileonename = '';
                                this.DataContrastForm.fileoneid='';
                                this.DataContrastForm.fileonesheet = '';
                                this.DataContrastForm.filetwoname = '';
                                this.DataContrastForm.filetwoid='';
                                this.DataContrastForm.filetwosheet = '';
                                 this.DataContrastForm.fileoneRange = '';
                                this.DataContrastForm.filetwoRange = '';                               
                                this.DataContrastForm.desc='';
                                this.getDataContrastList();
                            }
                        })

                    }
                });

            },

            handleEditConfirm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.editdialogVisible = false;
                        FileAPI.updateDataContrast(this.editDataContrastForm.id, this.editDataContrastForm).then(resp => {
                            if (!resp.success) {
                                this.$message.info({
                                    message: resp.msg,
                                    duration: 1000
                                })
                            } else {
                                this.getDataContrastList();
                            }
                        })
                    }
                });

            },

            getDataContrastList() {
                FileAPI.DataContrastList({
                    params: {
                        project: this.$route.params.id,
                        search: this.search
                    }
                }).then(resp => {
                   
                    this.DataContrastData = resp;
                })
            },
        },
        name: "DataContrast",
        mounted() {
            this.getDataContrastList();
            this.getTestdataList();
            this.getpermissions();
        }
    }
</script>

<style>

.outer-container{
   
    height: 500px;
    position: relative;
    overflow: auto ;
    border-top:1px solid rgb(143, 142, 142);
}
.inner-container{
    position: absolute;
    left: 0;
    top: 0; 
    bottom: 0;
    text-align: left;
    line-height:30px;
}
</style>
