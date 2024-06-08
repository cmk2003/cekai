import axios from 'axios'


//uicase
export const adduicase = params => {
    return axios.post('/api/testrunner/uicase/', params).then(res => res.data)
};
export const getuicase = params => {
    return axios.get('/api/testrunner/uicase/', params).then(res => res.data)
};
export const getuicaseSingle = url => {
    return axios.get('/api/testrunner/uicase/' + url + '/').then(res => res.data)
};
export const deluicase = url => {
    return axios.delete('/api/testrunner/uicase/' + url + '/').then(res => res.data)
};
export const delAlluicase = params => {
    return axios.delete('/api/testrunner/uicase/', params).then(res => res.data)
};
export const updateuicase = (url, params) => {
    return axios.patch('/api/testrunner/uicase/' + url + '/', params).then(res => res.data)
};
export const copyuicase = (url, params) => {
    return axios.post('/api/testrunner/uicase/' + url + '/', params).then(res => res.data)
};
export const runuicase = (params) => {
    return axios.post('/api/testrunner/run_uicase/', params).then(res => res.data)
};
export const runUIcaseByPk = (url, params) => {
    return axios.get('/api/testrunner/run_uicase_pk/' + url + '/', params).then(res => res.data)
};
export const geuicasePaginationBypage = params => {
    return axios.get('/api/testrunner/uicase/', params).then(res => res.data)
};

export const runUIcaseTree = params => {
    return axios.post('/api/testrunner/run_uicase_tree/', params).then(res => res.data)
};
//获取ui测试计划列表
export const UItestPlanList = params => {
    return axios.get('/api/testrunner/uitest/', params).then(res => res.data)
};
export const getUITestPaginationBypage = params => {
    return axios.get('/api/testrunner/uitest/', params).then(res => res.data)
};
export const addUITestPlan = params => {
    return axios.post('/api/testrunner/uitest/', params).then(res => res.data)
};

export const updateUITestPlan = (url, params) => {
    return axios.patch('/api/testrunner/uitest/' + url + '/', params).then(res => res.data)
};
export const editUITest = url => {
    return axios.get('/api/testrunner/uitestplanstep/' + url + '/').then(res => res.data)
};
export const copyUITest = (url, params) => {
    return axios.post('/api/testrunner/uitest/' + url + '/', params).then(res => res.data)
};

export const deleteUITest = url => {
    return axios.delete('/api/testrunner/uitest/' + url + '/').then(res => res.data)
};

export const delAllUITest = params => {
    return axios.delete('/api/testrunner/uitest/', params).then(res => res.data)
};
export const runSingleTestPlanSuite = params => {
    return axios.post('/api/testrunner/run_testplansuite/', params).then(res => res.data)
};
export const runTestPlanByPk = (url, params) => {
    return axios.get('/api/testrunner/run_testplansuite_pk/' + url + '/', params).then(res => res.data)
};
export const runUIPlanSuiteTree = params => {
    return axios.post('/api/testrunner/run_testplansuite_tree/', params).then(res => res.data)
};