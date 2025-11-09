import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import API from "../api/axios";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";

const schema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export default function Signup() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      await API.post("/auth/signup", data);
      toast.success("Account created successfully!");
      navigate("/login");
    } catch (err) {
      toast.error(err.response?.data?.error || "Signup failed");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-[#0d1117]">
      <div className="bg-[#161b22] border border-gray-800 rounded-2xl p-8 w-96 shadow-lg">
        <h2 className="text-2xl font-bold text-center text-gray-100 mb-6">Sign Up</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Username */}
          <input
            {...register("username")}
            placeholder="Username"
            className="w-full p-3 rounded bg-[#1f2937] border border-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          {errors.username && (
            <p className="text-red-500 text-sm">{errors.username.message}</p>
          )}

          {/* Email */}
          <input
            {...register("email")}
            placeholder="Email"
            className="w-full p-3 rounded bg-[#1f2937] border border-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          {errors.email && (
            <p className="text-red-500 text-sm">{errors.email.message}</p>
          )}

          {/* Password */}
          <input
            type="password"
            {...register("password")}
            placeholder="Password"
            className="w-full p-3 rounded bg-[#1f2937] border border-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          {errors.password && (
            <p className="text-red-500 text-sm">{errors.password.message}</p>
          )}

          {/* Submit */}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded transition"
          >
            Sign Up
          </button>
        </form>

        <p className="text-sm text-gray-400 mt-4 text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-500 hover:underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}