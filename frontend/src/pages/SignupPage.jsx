import React, { useState } from "react";
import { Mail, Lock, Eye, EyeOff, User } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { signupUser } from "../api/authApi";
import ValidationItem from "../components/ValidationItem";

const validate = (form) => {
  const errors = {};


  if (!form.firstName) errors.firstName = "First name required";
  else if (!/^[A-Za-z]+$/.test(form.firstName))
    errors.firstName = "Only letters allowed";


  if (!form.lastName) errors.lastName = "Last name required";
  else if (!/^[A-Za-z]+$/.test(form.lastName))
    errors.lastName = "Only letters allowed";


  if (!form.email) errors.email = "Email required";
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
    errors.email = "Invalid email";


  if (!form.password) errors.password = "Password required";
  else {
    if (form.password.length < 8) errors.password = "Min 8 chars";
    else if (!/[A-Z]/.test(form.password)) errors.password = "1 uppercase";
    else if (!/[a-z]/.test(form.password)) errors.password = "1 lowercase";
    else if (!/\d/.test(form.password)) errors.password = "1 number";
    else if (!/[@$!%*?&]/.test(form.password)) errors.password = "1 special";
  }


  if (!form.confirmPassword)
    errors.confirmPassword = "Confirm password";
  else if (form.password !== form.confirmPassword)
    errors.confirmPassword = "Passwords do not match";


  if (!form.agree) errors.agree = "Accept terms";


  return errors;
};

function SignupPage() {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    agree: false,
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    const updatedForm = {
      ...form,
      [name]: type === "checkbox" ? checked : value,
    };

    setForm(updatedForm);

    // live validation
    setErrors((prev) => ({
      ...prev,
      [name]: validate(updatedForm)[name],
    }));
  };

  const passwordRules = {
  length: form.password.length >= 8,
  uppercase: /[A-Z]/.test(form.password),
  lowercase: /[a-z]/.test(form.password),
  number: /\d/.test(form.password),
  special: /[@$!%*?&]/.test(form.password),
};

  const isFormValid = Object.keys(validate(form)).length === 0;

  const navigate = useNavigate();

  const handleSignup = async () => {
    const validationErrors = validate(form);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      setLoading(true);

      await signupUser({
        first_name: form.firstName.trim(),
        last_name: form.lastName.trim(),
        email: form.email.trim(),
        password: form.password,
      });

      navigate("/login");
    } catch (err) {
      setErrors({
        api:
          err?.response?.data?.message ||
          err?.message ||
          "Signup failed",
      });
    } finally {
      setLoading(false);
    }
  };

  const navToHome = () => {
    navigate("/");
  };

  return (
    <div className="bg-[#000000] min-h-screen flex flex-col items-center py-20 overflow-y-auto text-white">
      {/* LOGO */}
      <div className="absolute top-8 left-10 flex items-center gap-3">
        <div className="w-8 h-8 rounded-md border border-gray-500 flex items-center justify-center">
          ⌘
        </div>
        <button className="text-lg font-semibold" onClick={navToHome}>
          LensOS
        </button>
      </div>

      {/* CARD */}
      <div className="bg-[#ffffff06] backdrop-blur-xl border border-[#1E293B] rounded-2xl w-[420px] p-10 shadow-xl">
        <h1 className="text-3xl font-semibold mb-2">Create your account</h1>

        <p className="text-gray-400 text-sm mb-8">
          Join the next generation of visual computing.
        </p>

        {/* FIRST + LAST NAME */}
        <div className="grid grid-cols-2 gap-4 mb-5">
          <div>
            <label className="text-sm text-gray-400">First name</label>

            <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
              <User size={18} className="text-gray-400" />
              <input
                name="firstName"
                type="text"
                value={form.firstName}
                placeholder="John"
                className="bg-transparent outline-none px-3 py-3 w-full text-sm"
                onChange={handleChange}
              />
              
            </div>
            {errors.firstName && <p className="text-red-400 text-xs mt-1">{errors.firstName}</p>}
          </div>

          <div>
            <label className="text-sm text-gray-400">Last name</label>

            <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
              <User size={18} className="text-gray-400" />
              <input
                name="lastName"
                type="text"
                value={form.lastName}
                placeholder="Doe"
                className="bg-transparent outline-none px-3 py-3 w-full text-sm"
                onChange={handleChange}
              />
            </div>
            {errors.lastName && <p className="text-red-400 text-xs mt-1">{errors.lastName}</p>}
          </div>
        </div>

        {/* EMAIL */}
        <div className="mb-5">
          <label className="text-sm text-gray-400">Email address</label>

          <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
            <Mail size={18} className="text-gray-400" />

            <input
              name="email"
              type="email"
              value={form.email}
              placeholder="name@company.com"
              className="bg-transparent outline-none px-3 py-3 w-full text-sm"
              onChange={handleChange}
            />
          </div>
          {errors.email && <p className="text-red-400 text-xs mt-1">{errors.email}</p>}
        </div>

        {/* PASSWORD */}
        <div className="mb-5">
          <label className="text-sm text-gray-400">Password</label>

          <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
            <Lock size={18} className="text-gray-400" />

            <input
              name="password"
              type={showPassword ? "text" : "password"}
              value={form.password}
              placeholder="••••••••"
              className="bg-transparent outline-none px-3 py-3 w-full text-sm"
              onChange={handleChange}
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
        <div className="text-xs space-y-1 mb-3 mt-2">
          <ValidationItem
            valid={passwordRules.length}
            text="At least 8 characters"
          />
          <ValidationItem
            valid={passwordRules.uppercase}
            text="One uppercase letter"
          />
          <ValidationItem
            valid={passwordRules.lowercase}
            text="One lowercase letter"
          />
          <ValidationItem valid={passwordRules.number} text="One number" />
          <ValidationItem
            valid={passwordRules.special}
            text="One special character"
          />
        </div>
        <div className="mb-5">
          <label className="text-sm text-gray-400">Confirm Password</label>

          <div className="flex items-center bg-[#020617] border border-[#1E293B] rounded-xl mt-2 px-3">
            <Lock size={18} className="text-gray-400" />

            <input
              name="confirmPassword"
              type="password"
              value={form.confirmPassword}
              placeholder="••••••••"
              className="bg-transparent outline-none px-3 py-3 w-full text-sm"
              onChange={handleChange}
            />
          </div>
        </div>
        {form.confirmPassword && (
          <p
            className={`text-xs mb-3 ${
              form.password === form.confirmPassword ? "text-green-400" : "text-red-400"
            }`}
          >
            {form.password === form.confirmPassword
              ? "Passwords match"
              : "Passwords do not match"}
          </p>
        )}

        {/* TERMS */}
        <div className="flex items-center gap-2 text-sm text-gray-400 mb-6">
          <input
            type="checkbox"
            name="agree"
            checked={form.agree}
            onChange={handleChange}
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
          disabled={!isFormValid || loading}
          className={`w-full py-3 rounded-xl font-medium transition ${
            !isFormValid || loading
              ? "bg-gray-500 cursor-not-allowed"
              : "bg-[#1B4273] hover:bg-[#24599c]"
          }`}
        >
          {loading ? "Creating Account..." : "Get Started →"}
        </button>
        {errors.api && (
          <p className="text-red-400 text-sm mt-3 text-center">{errors.api}</p>
        )}

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
