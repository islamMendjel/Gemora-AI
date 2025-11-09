import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Chat from "./pages/Chat";
import { useAuthStore } from "./store/useAuthStore";
import toast, { Toaster } from "react-hot-toast";

export default function App() {
  const { token } = useAuthStore();

  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={token ? <Chat /> : <Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/chat" element={token ? <Chat /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}
