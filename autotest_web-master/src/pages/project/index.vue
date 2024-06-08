<template>
    <el-tabs style="padding-top: 10px; margin-left: 10px;" v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="项目列表" name="first">
        <ProjectList v-if="tabs.first">

        </ProjectList>
    </el-tab-pane>
    <el-tab-pane label="统计数据" name="second">
        <DataStatistics v-if="tabs.second">

        </DataStatistics>
    </el-tab-pane>
    <el-tab-pane label="用户管理" name="three" v-if="this.$store.state.Is_superuser==true || this.$store.state.Is_superuser=='true'" >
        <UserList v-if="tabs.three ">

        </UserList>
    </el-tab-pane>
    <el-tab-pane label="权限管理" name="four" v-if="this.$store.state.Is_superuser==true || this.$store.state.Is_superuser=='true'" >
        <UserGroup v-if="tabs.four ">

        </UserGroup>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
import ProjectList from '@/pages/project/ProjectList'
import DataStatistics from '@/pages/project/DataStatistics'
import UserList  from '@/pages/userpage/users'
import UserGroup from '@/pages/userpage/usergroup'
  export default {
    components: {
           ProjectList,
           DataStatistics ,          
           UserList,
           UserGroup

        },
    data() {
      return {
       activeName: "first",
      tabs: {
        first: true,
        second: false,
        three: false,
        four: false,
      },

      };
    },
    methods: {
      handleClick(tab) {
      this.activeName = tab.name;
      switch (this.activeName) {
        case "first":
          this.switchTab("first");
          break;
        case "second":
          this.switchTab("second");
          break;
        case "three":
          this.switchTab("three");
          break;
        case "four":
          this.switchTab("four");
          break;
      }
 
    },
switchTab(tab) {
      for (let key in this.tabs) {
        if (key === tab) {
         this.tabs[key] = true;
        } else {
          this.tabs[key] = false;
        }
      }
    },

    }
  };
</script>