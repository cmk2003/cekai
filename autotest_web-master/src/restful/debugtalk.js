import axios from "axios";

export const getDebugtalk = url => {
    return axios.get('/api/testrunner/debugtalk/' + url + '/').then(res => res.data)
};

export const updateDebugtalk = params => {
    return axios.patch('/api/testrunner/debugtalk/', params).then(res => res.data)
};

export const runDebugtalk = params => {
    return axios.post('/api/testrunner/debugtalk/', params).then(res => res.data)
};

export const addPycode = (data, params) => {
    return axios({ url: '/api/testrunner/pycode/', method: 'POST', data: data, params: params })
};

export const deletePycode = (url, params) => {
    return axios.delete('/api/testrunner/pycode/' + url + '/', params)
};

export const delAllPycode = (data, params) => {
    return axios.delete('/api/testrunner/pycode/', { data, params })
};

export const getPycodeList = params => {
    return axios.get('/api/testrunner/pycode/', params)
};

export const getPycodeListPaginationBypage = params => {
    return axios.get('/api/testrunner/pycode/', params)
};

export const getPycode = (url, params) => {
    return axios.get('/api/testrunner/pycode/' + url + '/', params)
};

export const runPycode = (url, params) => {
    return axios.get('/api/testrunner/runpycode/' + url + '/', params)
};

export const updatePycode = (url, params, data) => {
    return axios({ url: '/api/testrunner/pycode/' + url + '/', method: 'PATCH', params: params, data: data })
};