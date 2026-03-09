import React from 'react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {loginUser} from '../api/authApi'

function LoginPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    const handleLogin = async() => {
        try {
            const res = await loginUser({email, password})
            localStorage.setItem('token', res.data.token)
            navigate("/dashboard")
        } catch (error) {
            console.log(error)
            alert("Login Failed")
        }
    }

  return (
    <>
      <div className='h-screen flex items-center justify-center bg-[#0f172a]'>
        <div className='bg-[#111827] p-8 rounded-xl w-96'>
            <h1 className="text-white text-2xl mb-4">Login</h1>
            <input
                className="w-full mb-3 p-2 rounded bg-gray-800 text-white"
                placeholder="Email"
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                className="w-full mb-3 p-2 rounded bg-gray-800 text-white"
                placeholder="Password"
                onChange={(e) => setPassword(e.target.value)}
            />
            <button
                onClick={handleLogin}
                className="w-full bg-[#1B4273] text-white p-2 rounded"
            >Login
            </button>
        </div>
      </div>
    </>
  )
}

export default LoginPage
