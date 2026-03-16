import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/authApi";
import { Mail, Lock, Eye, EyeOff } from "lucide-react";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await loginUser({ email, password });
      localStorage.setItem("token", res.data.token);
      navigate("/dashboard");
    } catch (error) {
      console.log(error);
      alert("Login Failed");
    }
  };

  // Enter key login
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleLogin();
    }
  };

  const handleSignup = () => {
    navigate("/signup")
  }

  const navToHome = () => {
    navigate("/")
  }

  return (
    <div className="min-h-screen bg-[#000000] text-white flex flex-col">

      {/* NAVBAR */}
      <nav className="flex justify-between items-center px-10 py-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-md border border-gray-500 flex items-center justify-center">
            ⌘
          </div>
          <button className="text-lg font-semibold" onClick={navToHome}>LensOS</button>
        </div>

        <div className="flex items-center gap-6 text-sm">
          <span className="text-gray-400 cursor-pointer">Documentation</span>
          <button className="bg-[#0F172A] px-4 py-2 rounded-lg">
            Support
          </button>
        </div>
      </nav>

      {/* LOGIN CONTAINER */}
      <div className="flex flex-1 items-center justify-center">

        <div className="flex bg-[#ffffff06] rounded-2xl overflow-hidden shadow-2xl">

          {/* LOGIN CARD */}
          <div className="p-10 w-[420px] backdrop-blur-xl bg-[#ffffff06] border-s-white">

            <h1 className="text-3xl font-semibold mb-2">
              Welcome back
            </h1>

            <p className="text-gray-400 mb-8">
              Enter your credentials to access your workspace
            </p>

            {/* EMAIL */}
            <div className="mb-5">
              <label className="text-sm text-gray-400">
                Email Address
              </label>

              <div className="flex items-center bg-[#020617] border border-gray-800 rounded-lg mt-2 px-3">
                <Mail size={18} className="text-gray-400 mr-2" />

                <input
                  className="w-full bg-transparent p-3 outline-none"
                  placeholder="name@company.com"
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={handleKeyDown}
                />
              </div>
            </div>

            {/* PASSWORD */}
            <div className="mb-6">
              <div className="flex justify-between text-sm text-gray-400">
                <label>Password</label>
                <span className="text-blue-500 cursor-pointer">
                  Forgot?
                </span>
              </div>

              <div className="flex items-center bg-[#020617] border border-gray-800 rounded-lg mt-2 px-3">

                <Lock size={18} className="text-gray-400 mr-2" />

                <input
                  type={showPassword ? "text" : "password"}
                  className="w-full bg-transparent p-3 outline-none"
                  placeholder="••••••••"
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={handleKeyDown}
                />

                {/* EYE BUTTON */}
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="text-gray-400"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>

              </div>
            </div>

            {/* LOGIN BUTTON */}
            <button
              onClick={handleLogin}
              className="w-full bg-[#1B4273] hover:bg-[#24599c] transition p-3 rounded-lg font-medium"
            >
              Sign In →
            </button>

            {/* DIVIDER */}
            <div className="text-center text-gray-500 text-sm my-6">
              OR CONTINUE WITH
            </div>

            {/* OAUTH */}
            <div className="flex gap-4">
              <button className="flex-1 bg-[#020617] border border-gray-800 p-3 rounded-lg">
                Google
              </button>

              <button className="flex-1 bg-[#020617] border border-gray-800 p-3 rounded-lg">
                GitHub
              </button>
            </div>

            {/* SIGNUP */}
            <p className="text-center text-gray-400 text-sm mt-6">
              Don't have an account?{" "}
              <button className="text-blue-500 cursor-pointer" onClick={handleSignup}>
                Sign up
              </button>
            </p>

          </div>

          {/* RIGHT SIDE IMAGE */}
          <div className="hidden md:block w-[420px] relative">

            <img
              src="https://images.unsplash.com/photo-1773408151464-03819f8132c4?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              className="w-full h-full object-cover"
              alt=""
            />

            <div className="absolute bottom-10 left-10 right-10 text-gray-200">
              <p className="italic text-lg">
                "In photography there is a reality so subtle that it becomes more real than reality."
              </p>

              <p className="text-sm text-gray-400 mt-3">
                — Alfred Stieglitz
              </p>
            </div>

          </div>

        </div>

      </div>

      {/* FOOTER */}
      <footer className="text-center text-gray-500 text-sm pb-6">
        Privacy Policy &nbsp;&nbsp; Terms of Service &nbsp;&nbsp; Contact Us
      </footer>

    </div>
  );
}

export default LoginPage;