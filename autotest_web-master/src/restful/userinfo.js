import {getRequest, postRequest, deleteRequest,patch_request} from "./common";

//注册接口
export const register = params => {
    return postRequest('/api/user/register/', params)
};
//登录接口
export const login = params => {
    return postRequest('/api/user/login/', params)
};
//退出登录
export const logout = params => {
    return postRequest('/api/user/logout/', params)
};
//获取用户权限接口
export const getpermissions = params => {
    return getRequest('/api/testrunner/getpermissionslist/', params)
};
//修改用户信息
export const userinfo = params => {
    return patch_request('/api/user/userinfo/', params)
};
export const getuserlist = params => {
    return getRequest('/api/user/userinfo/', params)
};
//修改用户密码
export const updatapassword = params => {
    return postRequest('/api/user/updateuserpassword/', params)
};
export const adduser = params => {
    return postRequest('/api/user/userinfo/', params)
};
export const deluser = url => {
    return deleteRequest('/api/user/userinfo/' + url + '/')
};

export const delAlluser = params => {
    return deleteRequest('/api/user/userinfo/', params)
};

export const getuserPaginationBypage = params => {
    return getRequest('/api/user/userinfo/', params)
};