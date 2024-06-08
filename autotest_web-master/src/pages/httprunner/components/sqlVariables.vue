<template>

    <el-table
        highlight-current-row
        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
        strpe
        :height="height"
        :data="tableData"
     
        style="width: 100%;"
        @cell-mouse-enter="cellMouseEnter"
        @cell-mouse-leave="cellMouseLeave"
    >
        <el-table-column
            label="变量名"
            width="150">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.key" placeholder="Key"></el-input>
            </template>
        </el-table-column>

        <el-table-column        
            label="数据库"
            width="150">
            <template slot-scope="scope">

                <el-select 
                v-model="scope.row.database"
                clearable="true"
                @clear="clearrowtype(scope.row)"
                @change="changedatabasetype(scope.row)"
                >
                    <el-option
                        v-for="item in dataBaseDataOptions"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"                        
                        >
                    </el-option>
                </el-select>

            </template>
        </el-table-column>
   
        <el-table-column         
            label="参数一"
            width="400">
            <template slot-scope="scope">
                <el-input  
                v-if="scope.row.databasetype==1"
                type="textarea"
                :rows="1"
                 clearable 
                 v-model="scope.row.query.params1"
                  placeholder="请输入MDX语句"></el-input>
        <el-select 
                placeholder="请选择操作类型"        
                v-if="scope.row.databasetype==2"
                v-model="scope.row.query.params1"                   
                >
                    <el-option
                        v-for="item in querytypeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"                        
                        >
                    </el-option>
        </el-select>
        </template>
        </el-table-column>
             <el-table-column    
            label="参数二"
            width="250">
            <template slot-scope="scope">
                <el-input 
                v-if="scope.row.databasetype==1"             
                type="textarea"
                :rows="1"
                 clearable v-model="scope.row.query.params2"
                  placeholder='精度处理：{"ride":100,"expect":1000,"around":0}'></el-input>
                <el-input 
                v-if="scope.row.databasetype==2"             
                type="textarea"
                :rows="1"
                 clearable v-model="scope.row.query.params2"
                  placeholder='请输入sql语句'></el-input>
            </template>
        </el-table-column>
        <el-table-column    
            label="参数三"
            width="200">
            <template slot-scope="scope">
                <el-select 
                placeholder="请选择返回数值类型"
                v-if="scope.row.databasetype==1"
                v-model="scope.row.query.params3"                   
                >
                    <el-option
                        v-for="item in valuetypeoptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"                        
                        >
                    </el-option>
                 </el-select>
                <el-input  v-if="scope.row.databasetype==2"
                type="textarea"
                :rows="1"
                 clearable v-model="scope.row.query.params3"
                  placeholder="请输入需要返回字段，未必填"></el-input>
            </template>
        </el-table-column>
        <el-table-column
               
            label="参数四"
            width="400">
            <template slot-scope="scope"> 
                <el-input  v-if="scope.row.databasetype==1"
                type="textarea"
                :rows="1"
                 clearable v-model="scope.row.query.params4"
                  placeholder="请输入字典key列表,[key1,key2]"></el-input>
            </template>
        </el-table-column>

        <el-table-column
            label="内容"
            width="200">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.desc" placeholder="变量简要描述"></el-input>
            </template>
        </el-table-column>

        <el-table-column
        label="操作"
        width="150"
        >
            <template slot-scope="scope">
                <el-row v-show="scope.row === currentRow">
                    <el-button
                        icon="el-icon-circle-plus-outline"
                        size="mini"
                        type="info"
                        @click="handleEdit(scope.$index, scope.row)">
                    </el-button>

                    <el-button
                        icon="el-icon-delete"
                        size="mini"
                        type="danger"
                        v-show="scope.$index !== 0"
                        @click="handleDelete(scope.$index, scope.row)">
                    </el-button>
                </el-row>

            </template>
        </el-table-column>
    </el-table>

</template>

<script>
 import {getDataBaseList} from '../../../restful/databasepage'
    export default {
        name: "sqlVariables",

        props: {
            save: Boolean,
            sqlVariables: {
                require: false
            }
        },
        computed:{
            height() {
                return window.screen.height - 440
            }
        },

        watch: {
            save: function () {
                this.$emit('sqlVariables',this.parsesqlVariables(), this.tableData);
            },

            sqlVariables: function () {
                
                if (this.sqlVariables.length !== 0) {
                    this.tableData = this.sqlVariables;
                }
            }
        },
        mounted() {
            this.getDataBaseList();
        },
        methods: {
            cellMouseEnter(row) {
                this.currentRow = row;
            },

            cellMouseLeave(row) {
                this.currentRow = '';
            },

            handleEdit(index, row) {
                this.tableData.push({
                    key: '',
                    database: '',
                    databasetype:'',
                    query:{params1:"",params2:"",params3:"",params4:""},
                    desc: ''
                });
            },
            clearrowtype(id){
                id.databasetype=''
            },
            changedatabasetype(id){    
                let obj={};
                obj = this.dataBaseDataOptions.find(item =>{
                    return item.id==id.database;
                });
               
                id.databasetype=obj.type;
            },
            // 信息格式化
            parsesqlVariables() {              
                let sqlVariables = this.tableData                  
                return sqlVariables;
            },
            handleDelete(index, row) {
                this.tableData.splice(index, 1);
            },
            getDataBaseList() {
               getDataBaseList(this.$route.params.id).then(resp => {
                    this.dataBaseDataOptions = resp.results;
                })
            },     



        },
        data() {
            return {
                currentRow: '',
                tableData: [{
                    key: '',
                    database: '',
                    databasetype:"",
                    query:{params1:"",params2:"",params3:"",params4:""},
                    desc: ''
                }],
                dataBaseDataOptions:[],    
                querytypeOptions:
                                                    [{value:"select",lable:"select"},
                                                    {value:"update",lable:"update"},
                                                    {value:"insert",lable:"insert"},
                                                    {value:"delete",lable:"delete"}],
                valuetypeoptions:[
                    {value:"str",lable:"str"},
                     {value:"float",lable:"float"},
                      {value:"int",lable:"int"},
                ],
                dataType: 'data'
            }
        }
    }

</script>


<style scoped>

</style>
