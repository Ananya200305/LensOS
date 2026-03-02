import api from './axios';

export const uploadAsset = (file) => {
    const formdata = new FormData()
    formdata.append('file', file)

    return api.post('/asset/upload', formdata)
}

export const getAssets = () => {
    api.get('/asset/images')
}