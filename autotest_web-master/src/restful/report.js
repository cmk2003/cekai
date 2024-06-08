import axios from 'axios'

//报告页面接口
export const reportList = params => {
    return axios.get('/api/testrunner/reports/', params).then(res => res.data)
};
export const uireportList = params => {
    return axios.get('/api/testrunner/uireports/', params).then(res => res.data)
};
export const deleteReports = (url, params) => {
    return axios.delete('/api/testrunner/reports/' + url + '/', params)
};

export const getReportsPaginationBypage = params => {
    return axios.get('/api/testrunner/reports/', params).then(res => res.data)
};
export const getUIReportsPaginationBypage = params => {
    return axios.get('/api/testrunner/uireports/', params).then(res => res.data)
};
export const getUIReportsdetail = (url, params) => {
    return axios.get('/api/testrunner/uireports/' + url + '/', params).then(res => res.data)
};
export const deleteUIReports = (url, params) => {
    return axios.delete('/api/testrunner/uireports/' + url + '/', params)
};
export const deleteAllUIReports = (data, params) => {
    return axios({ url: '/api/testrunner/uireports/', method: 'delete', params: params, data: data })
};
export const delAllReports = (data, params) => {
    return axios({ url: '/api/testrunner/reports/', method: 'delete', params: params, data: data })
};

export const watchSingleReports = (url, params) => {
    return axios.get('/api/testrunner/reports/' + url + '/', params)
};
export const getTaskMetaDataList = params => {
    return axios.get('/api/testrunner/taskmeta/', params)
};