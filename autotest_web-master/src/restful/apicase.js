import axios from "axios";


export const addTestCase = params => {
    return axios.post('/api/testrunner/test/', params).then(res => res.data)
};

export const updateTestCase = (url, params) => {
    return axios.patch('/api/testrunner/test/' + url + '/', params).then(res => res.data)
};

export const testList = params => {
    return axios.get('/api/testrunner/test/', params).then(res => res.data)
};

export const deleteTest = url => {
    return axios.delete('/api/testrunner/test/' + url + '/').then(res => res.data)
};

export const delAllTest = params => {
    return axios.delete('/api/testrunner/test/', params).then(res => res.data)
};

export const coptTest = (url, params) => {
    return axios.post('/api/testrunner/test/' + url + '/', params).then(res => res.data)
};

export const editTest = url => {
    return axios.get('/api/testrunner/teststep/' + url + '/').then(res => res.data)
};

export const getTestPaginationBypage = params => {
    return axios.get('/api/testrunner/test/', params).then(res => res.data)
};
//同步用例
export const generateCase = data => {
    return axios.post('/api/testrunner/generateCase/', data).then(res => res.data)
};

