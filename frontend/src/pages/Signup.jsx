import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import API from "../utils/axiosInstance";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/auth/signup", { username, email, password });
      toast.success("Signup successful!");
      navigate("/");
    } catch {
      toast.error("Signup failed!");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-900 text-white">
      <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded-xl w-80 shadow-lg">
        <h1 className="text-2xl font-bold mb-4 text-center">Signup</h1>
        <input
          type="text"
          placeholder="Username"
          className="w-full mb-3 p-2 rounded text-black"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full mb-3 p-2 rounded text-black"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full mb-3 p-2 rounded text-black"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="w-full bg-green-600 hover:bg-green-700 py-2 rounded">
          Signup
        </button>
        <p className="mt-3 text-center text-sm">
          Already have an account?{" "}
          <a href="/" className="text-blue-400 hover:underline">Login</a>
        </p>
      </form>
    </div>
  );
}
