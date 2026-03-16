import React, { useState } from "react";
import { Mail, Lock, Eye, EyeOff, User } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { signupUser } from "../api/authApi";

function SignupPage() {

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [agree, setAgree] = useState(false);

  const navigate = useNavigate();

  const handleSignup = async () => {
    if (!agree) {
      alert("Please accept Terms of Service");
      return;
    }

    try {
      await signupUser({
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password
      });

      navigate("/login");

    } catch (err) {
      console.log(err);
      alert("Signup failed");
    }
  };

  const navToHome = () => {
    navigate("/")
  }

  return (
    <div className="bg-[#000000] min-h-screen flex flex-col items-center py-20 overflow-y-auto text-white">

      {/* LOGO */}
      <div className="absolute top-8 left-10 flex items-center gap-3">
        <div className="w-8 h-8 rounded-md border border-gray-500 flex items-center justify-center">
          ⌘
        </div>
        <button className="text-lg font-semibold" onClick={navToHome}>LensOS</button>
      </div>

      {/* CARD */}
      <div className="bg-[#ffffff06] backdrop-blur-xl border border-[#1E293B] rounded-2xl w-[420px] p-10 shadow-xl">

        <h1 className="text-3xl font-semibold mb-2">
          Create your account
        </h1>

        <p className="text-gray-400 text-sm mb-8">
          Join the next generation of visual computing.
        </p>

        {/* FIRST + LAST NAME */}
        <div className="grid grid-cols-2 gap-4 mb-5">

          <div>
            <label className="text-sm text-gray-400">
              First name
            </label>

            <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
              <User size={18} className="text-gray-400" />
              <input
                type="text"
                placeholder="John"
                className="bg-transparent outline-none px-3 py-3 w-full text-sm"
                onChange={(e) => setFirstName(e.target.value)}
              />
            </div>
          </div>

          <div>
            <label className="text-sm text-gray-400">
              Last name
            </label>

            <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
              <User size={18} className="text-gray-400" />
              <input
                type="text"
                placeholder="Doe"
                className="bg-transparent outline-none px-3 py-3 w-full text-sm"
                onChange={(e) => setLastName(e.target.value)}
              />
            </div>
          </div>

        </div>

        {/* EMAIL */}
        <div className="mb-5">
          <label className="text-sm text-gray-400">
            Email address
          </label>

          <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
            <Mail size={18} className="text-gray-400" />

            <input
              type="email"
              placeholder="name@company.com"
              className="bg-transparent outline-none px-3 py-3 w-full text-sm"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
        </div>

        {/* PASSWORD */}
        <div className="mb-5">
          <label className="text-sm text-gray-400">
            Password
          </label>

          <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
            <Lock size={18} className="text-gray-400" />

            <input
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              className="bg-transparent outline-none px-3 py-3 w-full text-sm"
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="text-gray-400"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>

          </div>
        </div>

        {/* TERMS */}
        <div className="flex items-center gap-2 text-sm text-gray-400 mb-6">

          <input
            type="checkbox"
            checked={agree}
            onChange={() => setAgree(!agree)}
          />

          <span>
            I agree to the
            <span className="text-blue-500"> Terms of Service </span>
            and
            <span className="text-blue-500"> Privacy Policy</span>
          </span>

        </div>

        {/* BUTTON */}
        <button
          onClick={handleSignup}
          className="w-full bg-[#1B4273] hover:bg-[#24599c] transition py-3 rounded-xl font-medium"
        >
          Get Started →
        </button>

        {/* DIVIDER */}
        <div className="text-center text-xs text-gray-500 my-6">
          OR CONTINUE WITH
        </div>

        {/* OAUTH */}
        <div className="flex gap-4">

          <button className="flex-1 border border-[#1E293B] py-3 rounded-xl text-sm hover:bg-[#020617]">
            Google
          </button>

          <button className="flex-1 border border-[#1E293B] py-3 rounded-xl text-sm hover:bg-[#020617]">
            GitHub
          </button>

        </div>

        {/* LOGIN LINK */}
        <p className="text-center text-sm text-gray-400 mt-6">
          Already have an account?
          <span
            onClick={() => navigate("/login")}
            className="text-blue-500 cursor-pointer ml-1"
          >
            Log in
          </span>
        </p>

      </div>

      {/* FOOTER */}
      <p className="text-xs text-gray-500 mt-10">
        © 2024 LensOS Technologies Inc. All rights reserved.
      </p>

    </div>
  );
}

export default SignupPage;