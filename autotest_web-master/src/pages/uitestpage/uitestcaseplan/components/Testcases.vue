<template>
 <!-- @cell-mouse-enter="cellMouseEnter"这几个是鼠标放上去才会出 现按钮的方法
        @cell-mouse-leave="cellMouseLeave"
        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}" -->
    <el-table
        highlight-current-row
        :data="tableData"
        row-key="rowkeyid"
        :height="height"
        style='width: 100%;'
        :border="false"
       ref="table"
        
    > 
        <el-table-column
                    width="60px"
                    label="顺序"
                    type="index"
            
                    >
        </el-table-column>

        <el-table-column
            label="步骤描述"
            width="300px">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.describe" placeholder="请输入步骤描述"></el-input>
            </template>
        </el-table-column>

        <el-table-column label="动作" width="150px">
            <template slot-scope="scope">
                <el-select v-model="scope.row.action" filterable placeholder="请选择" clearable
                
                >
                    <el-option
                    v-for="item in actionOptions"
                    :key="item.value"                    
                    :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
        <el-table-column label="定位方式" width="150px">
            <template slot-scope="scope">
                <el-select v-model="scope.row.locationType" 
                filterable 
                placeholder="请选择" 
                clearable
                :disabled="scope.row.action===''"
                >
                    <el-option
                    v-for="item in locationTypeOptions"
                    :key="item.value"                    
                    :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
   
        <el-table-column
            label="定位值"
            width="400px">
            <template slot-scope="scope">
                <el-input clearable 
                v-model="scope.row.locationValue" 
                placeholder="请输入定位值"
               :disabled="scope.row.locationType===''"
                ></el-input>
            </template>
        </el-table-column>
        <el-table-column label="校验值来源" width="150px">
            <template slot-scope="scope">
                <el-select 
                v-model="scope.row.CheckValueOurce" 
                filterable 
                placeholder="请选择" 
                clearable
                :disabled="scope.row.action!=='断言'"
                >
                    <el-option
                    v-for="item in CheckValueOurceOptions"
                    :key="item.value"                    
                    :value="item.value"
                    
                    >
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
  
        <el-table-column
            label="属性名"
            width="200">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.AttributeName" placeholder="请输入属性名"
                :disabled="scope.row.CheckValueOurce!=='属性值'"
                
                ></el-input>

            </template>
        </el-table-column>
        <el-table-column label="校验方式" width="150px">
            <template slot-scope="scope">
                <el-select v-model="scope.row.CheckType" 
                filterable 
                placeholder="请选择" 
                clearable
                :disabled="scope.row.action!=='断言'"
                >
                    <el-option
                    v-for="item in CheckTypeOptions"
                    :key="item.value"                    
                    :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
  
        <el-table-column
            label="数据项"
            width="300px">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.DataItem" placeholder="请输入数据项"></el-input>
            </template>
        </el-table-column>
        <el-table-column
        fixed="right"
        label="操作"
        width="150px"
        >
            <template slot-scope="scope">
                <el-row >
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
  import Sortable from 'sortablejs';
    export default {
        props: {
            save: Boolean,
            testcase: {
                require: false
            }
        },

        methods: {
            S4() {
                return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
            },
           guid() {
                return (this.S4()+this.S4()+"-"+this.S4()+"-"+this.S4()+"-"+this.S4()+"-"+this.S4()+this.S4()+this.S4());
                              },
            // 行拖拽
            rowDrop () {
               // 此时找到的元素是要拖拽元素的父容器
                const tbody = this.$refs.table.$el.querySelector('.el-table__body-wrapper tbody');
                const _this = this;
                Sortable.create(tbody, {
           //  指定父元素下可被拖拽的子元素
                  draggable: ".el-table__row",
                   onEnd ({ newIndex, oldIndex }) {
                        const currRow = _this.tableData.splice(oldIndex, 1)[0];
                        _this.tableData.splice(newIndex, 0, currRow);
                    }
                });
            },
            // 列拖拽
            columnDrop () {
                const wrapperTr = document.querySelector('.el-table__header-wrapper tr');
                this.sortable = Sortable.create(wrapperTr, {
                    animation: 180,
                    delay: 0,
                    onEnd: evt => {
                        const oldItem = this.dropCol[evt.oldIndex];
                        this.dropCol.splice(evt.oldIndex, 1);
                        this.dropCol.splice(evt.newIndex, 0, oldItem);
                    }
                });
            },
          
            cellMouseEnter(row) {
                this.currentRow = row;
            },

            cellMouseLeave(row) {
                this.currentRow = '';
            },
 
            handleEdit(index, row) {
     
                
                this.tableData.push({
                        rowkeyid: this.guid(),
                        describe: '',
                        action: '',
                        locationType: '',
                        locationValue:'',
                        CheckValueOurce:'',
                        AttributeName:'',
                        CheckType:'',
                        DataItem:''
                });
           
            },

            handleDelete(index, row) {
         
                this.tableData.splice(index, 1);
            },

            // 头部信息格式化
            parsetestcase() {
                console.log(this.tableData)
                let testcase = this.tableData    
               
                return testcase;
            }
        },
        watch: {
            save: function () {
                
                this.$emit('testcase', this.parsetestcase(), this.tableData);
            },

            testcase: function () {
             
                if (this.testcase.length !== 0) {
                    this.tableData = this.testcase;
                    
                }
            }
        },
        mounted () {
           
            this.rowDrop();
            this.columnDrop();
        },
        computed:{
           
            height() {
                return window.screen.height -440
            }
        },
        data() {
            return {           
               
                actionOptions: [
                    {value:'地址栏跳转'},
                {
                    value: '跳转窗口'
                },{
                    value: '点击'
                }, {
                    value: '等待'
                }, {
                    value: '输入'
                }, {
                    value: '截图'
                }, {
                    value: '断言'
                }, 
                {
                    value: '跳转iframe'
                }, 
                  {
                    value: '返回父iframe'
                }, 
                        ],
                locationTypeOptions: [
                    {
                    value: 'XPATH'
                },{
                    value: 'ID'
                }, {
                    value: 'NAME'
                }, {
                    value: 'CLASS_NAME'
                }, {
                    value: 'CSS'
                }, {
                    value: 'LINK_TEXT'
                }, 
                {
                    value: 'PARTIAL_LINK_TEXT'
                }, 
                  {
                    value: 'TAG_NAME'
                }, 
                        ],
                CheckValueOurceOptions: [
                    {
                    value: '普通文本'
                },{
                    value: '属性值'
                }, 
                        ],
                CheckTypeOptions: [
                    {
                    value: '等于'
                },{
                    value: '小于'
                }, 
                {
                    value: '小于或等于'
                },{
                    value: '大于'
                }, 
                {
                    value: '大于或等于'
                },{
                    value: '不等于'
                }, 
                {
                    value: '字符串相等'
                },{
                    value: '长度相等'
                }, 
                {
                    value: '长度大于或相等'
                }, 
                {
                    value: '长度小于'
                }, 
                {
                    value: '长度小于或相等'
                }, 
                {
                    value: '列表相等'
                }, 
                        ],

                currentRow: '',
                tableData: [{    
                        
                        rowkeyid: this.guid(),                  
                        describe: '',
                        action: '',
                        locationType: '',
                        locationValue:'',
                        CheckValueOurce:'',
                        AttributeName:'',
                        CheckType:'',
                        DataItem:''
                    },]
            }
        },
        name: "Testcases"
    }
</script>

<style scoped>
</style>
