

import axios from 'axios'
//全局变量页面接口
export const addVariables = params => {
    return axios.post('/api/testrunner/variables/', params).then(res => res.data)
};

export const variablesList = params => {
    return axios.get('/api/testrunner/variables/', params).then(res => res.data)
};

export const getVariablesPaginationBypage = params => {
    return axios.get('/api/testrunner/variables/', params).then(res => res.data)
};


export const updateVariables = (url, params) => {
    return axios.patch('/api/testrunner/variables/' + url + '/', params).then(res => res.data)
};

export const deleteVariables = url => {
    return axios.delete('/api/testrunner/variables/' + url + '/').then(res => res.data)
};

export const delAllVariabels = params => {
    return axios.delete('/api/testrunner/variables/', params).then(res => res.data)
};
export const gettokenmsg = params => {
    return axios.post('/api/testrunner/gettokenmsg/', params)
};

//UI全局变量页面接口
export const addUiVariables = params => {
    return axios.post('/api/testrunner/uivariables/', params).then(res => res.data)
};

export const UivariablesList = params => {
    return axios.get('/api/testrunner/uivariables/', params).then(res => res.data)
};

export const getUiVariablesPaginationBypage = params => {
    return axios.get('/api/testrunner/uivariables/', params).then(res => res.data)
};


export const updateUiVariables = (url, params) => {
    return axios.patch('/api/testrunner/uivariables/' + url + '/', params).then(res => res.data)
};

export const deleteUiVariables = url => {
    return axios.delete('/api/testrunner/uivariables/' + url + '/').then(res => res.data)
};

export const delAllUiVariabels = params => {
    return axios.delete('/api/testrunner/uivariables/', params).then(res => res.data)
};