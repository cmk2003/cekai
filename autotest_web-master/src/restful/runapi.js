import axios from 'axios'


export const runSingleAPI = params => {
    return axios.post('/api/testrunner/run_api/', params).then(res => res.data)
};

export const runAPIByPk = (url, params) => {
    return axios.get('/api/testrunner/run_api_pk/' + url + '/', params).then(res => res.data)
};

export const runAPITree = params => {
    return axios.post('/api/testrunner/run_api_tree/', params).then(res => res.data)
};

export const runSingleTestSuite = params => {
    return axios.post('/api/testrunner/run_testsuite/', params).then(res => res.data)
};

export const runSingleTest = params => {
    return axios.post('/api/testrunner/run_test/', params).then(res => res.data)
};

export const runTestByPk = (url, params) => {
    return axios.get('/api/testrunner/run_testsuite_pk/' + url + '/', params).then(res => res.data)
};

export const runSuiteTree = params => {
    return axios.post('/api/testrunner/run_suite_tree/', params).then(res => res.data)
};