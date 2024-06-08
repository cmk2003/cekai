<template>
<el-card class="box-card">
  <!-- <div slot="header" class="clearfix">
    <span class="title-li">数据统计</span>
  
  </div> -->
  <div >
       <el-table
       :header-cell-style="{background:'#eef0f4',color:'#606266','text-align':'center'}"
      :data="projectMessage"
      
      stripe
      border
      style="width: 100%">
      <el-table-column 
        width="60"
        label="序号"
        type="index"
      >
      </el-table-column>
      <el-table-column
        prop="pr_name"
        label="项目名称"
        >
      </el-table-column>
      <el-table-column
        prop="api_count"
        label="接口数量"
        align="right"
       >
      </el-table-column>
      <el-table-column
        prop="case_count"
        label="用例数量"
        align="right"
        >
      </el-table-column>
      <el-table-column
        prop="Cove_Count"
        label="覆盖接口数量"
      align="right"
        >
      </el-table-column>
      <el-table-column        
        label="用例覆盖率"
        align="right"
        
        >
        <template slot-scope="scope">
         <div>{{scope.row.Case_Coveage}}%</div>
        </template>
      </el-table-column>
      <el-table-column
        prop="task_count"
        label="任务数"
        align="right"
        >
      </el-table-column>
      <el-table-column
        prop="PlanCase_Count"
        label="执行用例数"
        align="right"
        >
      </el-table-column>
      <el-table-column      
        label="执行覆盖率"
        align="right"
        >
        <template slot-scope="scope">
         <div>{{scope.row.Plan_Coveage}}%</div>
        </template>
      </el-table-column>
      <el-table-column
        prop="report_count"
        label="测试报告数"
        align="right"
        >
      </el-table-column>
    </el-table>
  </div>
</el-card>
 

</template>

<script>
 import {getallprojectmessage } from "../../restful/project";
  
    export default {
        name: "DataStatistics",
        data() {
            return {
                projectMessage: [],
  

            }

        },
        methods: {    

            success(resp) {
                this.$notify({
                    message: resp["msg"],
                    type: 'success',
                    duration: 1000
                });
            },
            failure(resp) {
                this.$notify.error({
                    message: resp.msg,
                    duration: 1000
                });
            },

            getProjectDetail() {
              
                // const pk = this.$route.params.id;
                getallprojectmessage().then(res => {
                    this.projectMessage = res.data
                })
            }
        },
        mounted() {
          
            this.getProjectDetail();          
         
        }
    }

</script>




