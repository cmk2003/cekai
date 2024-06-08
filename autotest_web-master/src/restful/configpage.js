import axios from 'axios'
//配置页面 域名页面，参数页面接口
export const addConfig = params => {
    return axios.post('/api/testrunner/config/', params).then(res => res.data)
};

export const updateConfig = (url, params) => {
    return axios.patch('/api/testrunner/config/' + url + '/', params).then(res => res.data)
};


export const configList = params => {
    return axios.get('/api/testrunner/config/', params).then(res => res.data)
};

export const copyConfig = (url, params) => {
    return axios.post('/api/testrunner/config/' + url + '/', params).then(res => res.data)
};
export const deleteConfig = url => {
    return axios.delete('/api/testrunner/config/' + url + '/').then(res => res.data)
};
export const delAllConfig = params => {
    return axios.delete('/api/testrunner/config/', params).then(res => res.data)
};

export const getConfigPaginationBypage = params => {
    return axios.get('/api/testrunner/config/', params).then(res => res.data)
};
export const getAllHost = url => {
    return axios.get('/api/testrunner/host_ip/' + url + '/').then(res => res.data)
};

export const getAllConfig = url => {
    return axios.get('/api/testrunner/config/' + url + '/').then(res => res.data)
};
export const addHostIP = params => {
    return axios.post('/api/testrunner/host_ip/', params).then(res => res.data)
};

export const hostList = params => {
    return axios.get('/api/testrunner/host_ip/', params).then(res => res.data)
};

export const updateHost = (url, params) => {
    return axios.patch('/api/testrunner/host_ip/' + url + '/', params).then(res => res.data)
};

export const deleteHost = url => {
    return axios.delete('/api/testrunner/host_ip/' + url + '/').then(res => res.data)
};

export const getHostPaginationBypage = params => {
    return axios.get('/api/testrunner/host_ip/', params).then(res => res.data)
};

//UI配置相关接口
export const addUiConfig = params => {
    return axios.post('/api/testrunner/uiconfig/', params).then(res => res.data)
};

export const updateUiConfig = (url, params) => {
    return axios.patch('/api/testrunner/uiconfig/' + url + '/', params).then(res => res.data)
};


export const UiconfigList = params => {
    return axios.get('/api/testrunner/uiconfig/', params).then(res => res.data)
};

export const copyUiConfig = (url, params) => {
    return axios.post('/api/testrunner/uiconfig/' + url + '/', params).then(res => res.data)
};
export const deleteUiConfig = url => {
    return axios.delete('/api/testrunner/uiconfig/' + url + '/').then(res => res.data)
};
export const delAllUiConfig = params => {
    return axios.delete('/api/testrunner/uiconfig/', params).then(res => res.data)
};

export const getUiConfigPaginationBypage = params => {
    return axios.get('/api/testrunner/uiconfig/', params).then(res => res.data)
};
export const getAllUiConfig = url => {
    return axios.get('/api/testrunner/uiconfig/' + url + '/').then(res => res.data)
};