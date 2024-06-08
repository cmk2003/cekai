<template>
    <el-container>
        <el-header style="padding-top: 10px; height: 50px;padding: 0;">
            <div>
                <el-row :gutter="50">
                    <el-col :span="6" >
                        <el-input placeholder="请输入配置名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search" @click="getConfigList"></el-button>
                        </el-input>
                    </el-col>

                </el-row>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                <div style="position: fixed; bottom: 0; right:0; left: 220px; top: 150px">
                    <el-table
                    :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                        highlight-current-row
                        :data="configData.results"
                        :show-header="configData.results.length !== 0 "
                        stripe
                        height="75%"
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
                            label="配置名称"

                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.name}}</div>
                            </template>
                        </el-table-column>

                        <el-table-column

                            label="所属页面"
                        >
                            <template slot-scope="scope">
                                <div v-text="scope.row.base_page === '' ? '无' : scope.row.base_page"></div>

                            </template>
                        </el-table-column>
                            <el-table-column
                                label="描述"
                                width="500"
                            >
                                <template slot-scope="scope">
                                    <div style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis;" :title="scope.row.configdesc">{{scope.row.configdesc}}</div>

                                </template>
                            </el-table-column>
                        <el-table-column
                            width="100"
                            label="创建人"
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.create_user}}</div>

                            </template>
                        </el-table-column>
                        <el-table-column

                            label="更新时间"
                        >
                            <template slot-scope="scope">
                                <div>{{scope.row.update_time|datetimeFormat}}</div>

                            </template>
                        </el-table-column>

                        <el-table-column
                            label="操作"
                        >
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        v-if="permissions.includes('change')"
                                        size="mini"
                                        @click="handleEditConfig(scope.row)"
                                    >编辑</el-button>

                                    <el-button
                                        type="success"
                                       v-if="permissions.includes('add')"
                                        size="mini"
                                        @click="handleCopyConfig(scope.row.id)"
                                    >复制
                                    </el-button>

                                    <el-button
                                        type="danger"
                                       v-if="permissions.includes('delete')"
                                        size="mini"
                                        @click="handleDelConfig(scope.row.id)"
                                    >删除
                                    </el-button>
                                </el-row>
                            </template>

                        </el-table-column>

                    </el-table>
                 <el-col :span="7">
                        <el-pagination
                        style="padding-top:10px;"
                            :page-size="11"
                            v-show="configData.count !== 0 "                       
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="configData.count"
                        >
                        </el-pagination>
                    </el-col>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import * as configpage from "../../../../restful/configpage";
    export default {
        name: "ConfigList",
        props: {
            back: Boolean,
            project: {
                require: true
            },
            del: Boolean,
            permissions:{
                require:true
            }
        },
        data() {
            return {
                search: '',
                selectConfig: [],
                currentRow: '',
                currentPage: 1,
                configdes:"",
                configData: {
                    count: 0,
                    results: []
                },
               
            }
        },
        watch: {
            back() {
                this.getConfigList();
            },

            del() {
                if (this.selectConfig.length !== 0) {
                    this.$confirm('此操作将永久删除配置，是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }).then(() => {
                        configpage.delAllUiConfig({data: this.selectConfig}).then(resp => {
                            this.getConfigList();
                        })
                    })
                } else {
                    this.$notify.warning({
                        title: '提示',
                        message: '请至少勾选一个配置',
                        duration: 1000
                    })
                }
            }
        },

        methods: {
            handleSelectionChange(val) {
                this.selectConfig = val;
            },

            handleCurrentChange(val) {
                configpage.getUiConfigPaginationBypage({
                    params: {
                        page: this.currentPage,
                        project: this.project,
                        search: this.search
                    }
                }).then(resp => {
                    this.configData = resp;
                })
            },

            //删除api
            handleDelConfig(index) {
                this.$confirm('此操作将永久删除该配置，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    configpage.deleteUiConfig(index).then(resp => {
                        if (resp.success) {
                            this.getConfigList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            },

            handleEditConfig(row) {
                this.$emit('respConfig', row);
            },

            handleCopyConfig(id) {
                this.$prompt('请输入配置名称', '提示', {
                    confirmButtonText: '确定',
                    inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                    inputErrorMessage: '配置名称不能为空'
                }).then(({value}) => {
                    configpage.copyUiConfig(id, {
                        'name': value
                    }).then(resp => {
                        if (resp.success) {
                            this.getConfigList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            },

            cellMouseEnter(row) {
                this.currentRow = row;
            },

            cellMouseLeave(row) {
                this.currentRow = '';
            },

            getConfigList() {
                configpage.UiconfigList({
                    params: {
                        project: this.project,
                        search: this.search
                    }
                }).then(resp => {
                    this.configData = resp;
                })
            },
        },
        mounted() {
            this.getConfigList();
        }
    }
</script>

<style scoped>


</style>
