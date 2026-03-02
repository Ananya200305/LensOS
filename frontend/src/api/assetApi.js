import api from './axios';

export const uploadAsset = async (file) => {
    const formdata = new FormData()
    formdata.append('file', file)

    const response = await api.post('/asset/upload', formdata)
    return response
}

export const getAssets = async () => {
    const response = await api.get('/asset')
    return response
}