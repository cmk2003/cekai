//资料库相关接口
import axios from 'axios'

export const downloadTestdata = params => {
    return axios.post('/api/testrunner/download/', params, { responseType: 'blob' })
};


export const exportvariable = params => {
    return axios.post('/api/testrunner/exportVariables/', params, { responseType: "blob" })
};
export const importvariable = params => {
    return config.baseurl + '/api/testrunner/importvariables/'
};
