import axios from 'axios'
import store from '../store/state'
import router from '../router'
import {Message } from 'element-ui';



axios.defaults.withCredentials = true;
axios.defaults.baseURL = config.baseurl;

axios.interceptors.request.use(function (config) {
    
    if (store.token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
        
        config.headers.Authorization = `${store.token}`;
    }
    return config;
    },function (error) {
        return Promise.reject(error);
    });
axios.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    try {
        if (error.response.status === 401) {
            Message.error({
                message: '请先登录'
            });
            router.replace({
                name: 'Login'
            })
        }else if (error.response.status === 500 || error.response.status === 404) {
            
            Message.error({
                message: '服务器内部异常, 请检查',
                duration: 1000
            })
      
        }else if (error.response.status === 504) {
            Message.error({
                message: '请求超时,请联系系统管理员',
                duration: 1000
            })
        }else if (error.response.status === 405) {
            Message.error({
            message: 'Not Allowed'
          })
        }else{
            if (error.response.data.constructor === String){
                NotificaNotificationstion.error({
                    title: 'error',
                    message: error.response.data
                })
            } else {
                for (let key in error.response.data){
                    if (error.response.data[key].constructor === Array){
                        Message.error({
                            title: key,
                            message: error.response.data[key][0]
                            })
                    }else if (error.response.data[key].constructor === String){
                        Message.error({
                            title: key,
                            message: error.response.data[key]
                        })
                    }
                }
            }
        }
        return Promise.reject(error.response.data)
    }
    catch (e) {
        
        Message.error({
            message: '服务器连接超时，请重试'
        })
    }
});


//自己封装的接口请求的方法，只适用简单的传参
export const getRequest = function(path, data={}) {
    return axios.get( path, {
        params: data,
        withCredentials: true
    }).then(res => res.data)
};
export const postRequest = function(path, data={}) {
    return axios.post(path, data).then(res => res.data)
};

export const putRequest = function(path, data={}) {
    data["withCredentials"] = true
    return axios.put(path, data).then(res => res.data)
};

export const deleteRequest = function(path,data={}) {
    
    data["withCredentials"] = true
    return axios.delete(path, data).then(res => res.data)
};

export const patch_request = function(path, data={}) {
    data["withCredentials"] = true
    return axios.patch(path, data).then(res => res.data)
};