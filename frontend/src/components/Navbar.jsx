import React from 'react'

function Navbar() {
  return (
    <div>
      <nav className="flex justify-between items-center px-10 py-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-md border border-gray-500 flex items-center justify-center">
            ⌘
          </div>
          <span className="text-lg font-semibold">LensOS</span>
        </div>

        <div className="flex items-center gap-6">
          <button className="text-gray-300 hover:text-white" onClick={handleLoginClick}>
            Login
          </button>

          <button className="bg-blue-600 px-5 py-2 rounded-full hover:bg-blue-500 transition" onClick={handleSignupClick}>
            Sign Up
          </button>
        </div>
      </nav>
    </div>
  )
}

export default Navbar
