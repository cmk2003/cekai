
import axios from 'axios'
//获取组织树
export const getTree =(url, params)  =>{
    return axios.get('/api/testrunner/tree/' + url + '/', params).then(res => res.data)
};
//获取一级组织
export const getOneLevelTree = params  =>{
    return axios.get('/api/testrunner/getoneleveltree/', params).then(res => res.data)
};
//修改组织树
export const updateTree =(url, params)  =>{
    return axios.patch('/api/testrunner/tree/' + url + '/', params).then(res => res.data)
};
