import './App.css'
import {Routes, Route, BrowserRouter} from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import ProtectedRoute from './routes/ProtectedRoute'
import DashboardPage from './pages/DashboardPage'

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<LandingPage/>}/>
          <Route path='/login' element={<LoginPage/>}/>
          <Route path='/signup' element={<SignupPage/>}/>
          <Route path='/dashboard'
           element={
            <ProtectedRoute>
              <DashboardPage/>
            </ProtectedRoute>
           }/>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
