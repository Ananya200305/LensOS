import api from './axios';

export const uploadAsset = async (file) => {
    const formdata = new FormData();
    formdata.append('file', file);

    const response = await api.post('/asset/upload', formdata);
    return response;
};

export const getAssets = async () => {
    const response = await api.get('/asset');
    return response;
};

export const getAssetStatus = async (id) => {
    const response = await api.get(`/asset/${id}/status`);
    return response;
};

export const getAssetIntelligence = async (id) => {
    const response = await api.get(`/asset/intelligence/${id}`);
    return response;
};

export const getAssetFilters = async () => {
    const response = await api.get('/asset/filters');
    return response;
};

export const deleteAsset = async (id) => {
    const response = await api.delete(`/asset/delete/${id}`);
    return response;
};

export const searchAsset = async (query) => {
    const response = await api.post('/asset/search', null, {
        params: { query },
    });
    return response;
};

export const hybridSearchAssets = async (payload) => {
    const response = await api.post('/asset/search/hybrid', payload);
    return response;
};

export const reprocessAsset = async (id) => {
    const response = await api.patch(`/asset/reprocess/${id}`);
    return response;
};
