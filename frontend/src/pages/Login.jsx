import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import API from "../api/axios";
import toast from "react-hot-toast";
import { useAuthStore } from "../store/useAuthStore";
import { Link, useNavigate } from "react-router-dom";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm({ resolver: zodResolver(schema) });
  const { setToken, setUser } = useAuthStore();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const res = await API.post("/auth/login", data);
      setToken(res.data.access_token);
      setUser({ username: res.data.username });
      toast.success("Welcome back!");
      navigate("/chat");
    } catch (err) {
      toast.error(err.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-[#0d1117]">
      <div className="bg-[#161b22] border border-gray-800 rounded-2xl p-8 w-96 shadow-lg">
        <h2 className="text-2xl font-bold text-center text-gray-100 mb-6">Login</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <input {...register("email")} placeholder="Email" className="w-full p-3 rounded bg-[#1f2937] border border-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600" />
          {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}

          <input type="password" {...register("password")} placeholder="Password" className="w-full p-3 rounded bg-[#1f2937] border border-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600" />
          {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}

          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded transition">Login</button>
        </form>
        <p className="text-sm text-gray-400 mt-4 text-center">
          Don’t have an account? <Link to="/signup" className="text-blue-500">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
