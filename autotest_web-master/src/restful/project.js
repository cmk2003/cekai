import {getRequest, postRequest, deleteRequest,patch_request} from "./common";
import axios from 'axios'

const projectpath="/api/testrunner/project/"
//获取项目列表
export const getProjectList = (data) =>{
    return getRequest(projectpath, data)
};

//新增项目接口
export const addProject = (params) =>{
    return postRequest(projectpath, params)
};
//删除项目接口
export const deleteProject = (config) =>{
    return deleteRequest(projectpath, config)
};
//修改项目接口
export const updateProject = (data) =>{
    return patch_request(projectpath,data)
};
//获取项目详情接口
export const getProjectDetail = (pk) =>{
    return getRequest(projectpath+ pk + '/')
};
//项目分页
export const getPagination = (url) =>{
    return getRequest(url)
};
//获取用例图表数据
export const gettagcount = (params) =>{
    return getRequest("/api/testrunner/gettagcount/", params)
};
//获取报告图表数据
export const getreporttail = (params) =>{
    return getRequest("/api/testrunner/getreporttail/", params)
};
export const getallprojectmessage =() =>{
    return axios.get('/api/testrunner/getallprojectmessage/').then(res => res.data)
}