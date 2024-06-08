import axios from 'axios'

export const deleteDataBase = pk => {
    return axios.delete('/api/testrunner/databaseconfig/' + pk + '/').then(res => res.data)
}
export const updateDataBase = (pk, params) => {
    return axios.put('/api/testrunner/databaseconfig/' + pk + '/', params).then(res => res.data)
}
export const addDataBase = params => {
    return axios.post('/api/testrunner/databaseconfig/', params).then(res => res.data)
}
export const getDataBaseList = (pk, params) => {
    return axios.get('/api/testrunner/databaseconfig/' + pk + '/', params).then(res => res.data)

}
export const getPagination = url => {
    return axios.get(url).then(res => res.data)
}