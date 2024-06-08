import axios from 'axios'


export const getPaginationBypage = params => {
    return axios.get('/api/testrunner/api/', params).then(res => res.data)
};
export const addAPI = params => {
    return axios.post('/api/testrunner/api/', params).then(res => res.data)
};

export const updateAPI = (url, params) => {
    return axios.patch('/api/testrunner/api/' + url + '/', params).then(res => res.data)
};

export const apiList = params => {
    return axios.get('/api/testrunner/api/', params).then(res => res.data)
};

export const delAPI = url => {
    return axios.delete('/api/testrunner/api/' + url + '/').then(res => res.data)
};

export const delAllAPI = params => {
    return axios.delete('/api/testrunner/api/', params).then(res => res.data)
};

export const getAPISingle = url => {
    return axios.get('/api/testrunner/api/' + url + '/').then(res => res.data)
};

export const synchronizationapi = params => {
    return axios.post('/api/testrunner/synchronization_api/', params)
};

export const copyAPI = (url, params) => {
    return axios.post('/api/testrunner/api/' + url + '/', params).then(res => res.data)
};
export const exportapi = (params,data)=>{
    return axios({url:'/api/testrunner/exportApi/',method: 'POST',params:params,data:data,responseType: "blob"})
};