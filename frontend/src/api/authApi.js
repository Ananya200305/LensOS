import api from './axios'

export const loginUser = (data) => {
    api.post('/auth/login', data)
}

export const signupUser = (data) => {
    api.post('/auth/signup', data)
}