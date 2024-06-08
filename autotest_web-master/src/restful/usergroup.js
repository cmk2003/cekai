import axios from 'axios'

// 用户组相关接口
export const AddUserGroup = params => {
    return axios.post('/api/user/group/', params).then(res => res.data)
};
export const GetUserGrouplist = params => {
    return axios.get('/api/user/group/', params).then(res => res.data)
};
export const UpdateUserGroup = params => {
    return axios.patch('/api/user/group/', params).then(res => res.data)
};
export const DeleteUserGroup = url => {
    return axios.delete('/api/user/group/'+url+'/').then(res => res.data)
};
export const DeleteAllUserGroup = params => {
    return axios.delete('/api/user/group/', params).then(res => res.data)
};
export const GetusergroupBypage = params => {
	var url_str = '/api/user/group/?page='+params.page+'&search='
    return axios.get(url_str).then(res => res.data)
};
export const GetPermission = params =>{
    return axios.get('/api/user/permission/', params).then(res => res.data)
};