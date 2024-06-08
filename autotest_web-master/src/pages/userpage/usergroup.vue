<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button 
                    type="primary"
                     size="small"
                    icon="el-icon-circle-plus-outline"
                    @click="dialogVisible=true"
                    >
                    新增角色
                    </el-button>
                    <el-button 
                    v-show="userGroupData.count !== 0 "
                    style="margin-left: 20px"
                    type="danger"
                     size="small"
                    icon="el-icon-delete"
                    @click="delSelectionUsers"
                    >
                    批量删除
                    </el-button>

                    <el-dialog
                        title="添加角色"
                        :visible.sync="dialogVisible"
                        width="60%"
                        center
                    >
                        <el-form
                            :model="addusergroupForm"
                            :rules="rules"
                            ref="addusergroupForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="角色名" prop="name">
                                <el-input v-model="addusergroupForm.name" clearable placeholder="请输入角色名称"></el-input>
                            </el-form-item>            
                            <el-form-item label="授权" class="edit_dev">
                            <el-transfer 
                            v-model="addusergroupForm.permissions" 
                            :data="data"                           
                            :titles="['待选择权限', '已选择权限']"
                            ></el-transfer>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('addusergroupForm')">确 定</el-button>
                      </span>
                    </el-dialog>  
                     <el-dialog
                        title="编辑角色"
                        :visible.sync="editdialogVisible"
                        width="60%"
                        center
                    >
                        <el-form
                            :model="editusergroupFrom"
                            :rules="rules"
                            ref="editusergroupFrom"
                            label-width="100px"
                            class="project">
                            <el-form-item label="角色名" prop="name">
                                <el-input v-model="editusergroupFrom.name" clearable placeholder="请输入角色名称"></el-input>
                            </el-form-item>            
                            <el-form-item label="授权" class="edit_dev">
                            <el-transfer 
                            v-model="editusergroupFrom.permissions" 
                            :data="data"                           
                            :titles="['待选择权限', '已选择权限']"
                            ></el-transfer>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="editdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleEditConfirm('editusergroupFrom')">确 定</el-button>
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
                            <el-input v-model="search" placeholder="请输入用户组名称">
                                <el-button slot="append" icon="el-icon-search" @click="GetUserGroupList">
                                </el-button>
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
                            :data="userGroupData.results"
                            :show-header="userGroupData.results.length !== 0 "
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
                                label="角色名称"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.name}}</div>
                                </template>
                            </el-table-column>



                            <el-table-column
                            label="操作">
                                <template slot-scope="scope">
                                    <el-row v-show="currentRow === scope.row">
                                        <el-button
                                            type="info"                                           
                                            size="mini"
                                            @click="handerEditUserGroup(scope.row)"
                                        >编辑</el-button>


                                        <el-button
                                            v-show="userGroupData.count !== 0"
                                            type="danger"                                  
                                            size="mini"
                                            @click="handerDelUserGroup(scope.row.id)"
                                        >删除
                                        </el-button>
                                    </el-row>
                                </template>

                            </el-table-column>

                        </el-table>
                        <el-col :span="7">
                            <el-pagination
                                :page-size="5"
                                v-show="userGroupData.count !== 0 "
                                style="padding-top:10px;"
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="userGroupData.count"
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
import * as UserGroupAPI from '../../restful/usergroup' 
export default {

    data(){

        return{
            dialogVisible:false,
            editdialogVisible:false,
            search:'',
            currentRow:'',
            currentPage:1,
            selectVariables:[],
            data:[],
            userGroupData:{
                    count: 0,
                    results: []
            },
            addusergroupForm:{
                name:'',
                permissions:[]
            },
            editusergroupFrom:{
                id:'',
                name:'',
                permissions:[]
            },
            rules:{
                name: [
                        {required: true, message: '请输入角色名称', trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ],
            }

        }

    },
    methods:{
        cellMouseEnter(row) {
                this.currentRow = row;
            },

        cellMouseLeave(row) {
                this.currentRow = '';
            },          
        
        handleSelectionChange(val) {
                this.selectVariables = val;
            },
        handleCurrentChange(val) {
                UserGroupAPI.GetusergroupBypage({page: this.currentPage,search: this.search}).then(resp => {
                    this.userGroupData = resp;
                })
            },
        handleConfirm(fromName){
            this.$refs[fromName].validate((valid)=>{
                if(valid){
                    this.dialogVisible=false;
                    UserGroupAPI.AddUserGroup(this.addusergroupForm).then(resp =>{
                        if (resp.success){
                            this.$message.success(resp.msg);
                            this.GetUserGroupList();
                            this.addusergroupForm.name='';
                            this.addusergroupForm.permissions=[];
                        }else{
                            this.$message.error(resp.msg);
                        }
                    })
                }
            })
        },

        delSelectionUsers() {
            if(this.selectVariables.length!==0){
                this.$confirm('此操作将永久删除勾选的用户，是否继续?', '提示',{
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                }).then(()=>{
                    UserGroupAPI.DeleteAllUserGroup({data: this.selectVariables}).then(resp =>{
                        if(resp.success){
                            this.$message.success(resp.msg)
                            this.GetUserGroupList();
                        }else{
                            this.$message.error(resp.msg)
                        }
                        

                    })
                })
            }

        },
        GetUserGroupList(){
            UserGroupAPI.GetUserGrouplist({params:{search: this.search}}).then(resp =>{
               this.userGroupData=resp;
            })
        },
        GerPermissionList(){
            UserGroupAPI.GetPermission().then(resp =>{                        
                       let data = [];
                       resp.data.forEach((item, index) => {                         
                            data.push({
                            key: item.id,
                            label: item.name,         
                        });
                        })                     
                    this.data=data;
            })
        },
        handerEditUserGroup(row){
            this.editusergroupFrom={
                id: row.id,
                name: row.name,
                permissions:row.permissions
            };
            this.editdialogVisible=true;
        },
        handleEditConfirm(fromName){
            this.$refs[fromName].validate(valid=>{
                if(valid){
                    this.editdialogVisible=false;
                    UserGroupAPI.UpdateUserGroup(this.editusergroupFrom).then(resp =>{
                        if (resp.success){
                            this.$message.success(resp.msg);
                            this.GetUserGroupList();
							this.currentPage = 1;
                        }else{
                            this.$message.error(resp.msg);
                        }
                    })
                }
            })
        },
        handerDelUserGroup(index){
            this.$confirm('此操作将永久删除该用户，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    UserGroupAPI.DeleteUserGroup(index).then(resp => {
						this.GetUserGroupList();
						this.currentPage = 1
                        if (resp.success) {
                            this.$message.success(resp.msg)
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
        }
        },
        name:'UserGroup',
        mounted(){
            this.GetUserGroupList();
            this.GerPermissionList();
        }
}

</script>

<style>
.edit_dev .el-transfer-panel{
    width:350px;
}

</style>