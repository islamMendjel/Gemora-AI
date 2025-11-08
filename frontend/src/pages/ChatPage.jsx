import { useState } from "react";
import API from "../utils/axiosInstance";
import toast from "react-hot-toast";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    const newMsg = { sender: "user", text: message };
    setChat((prev) => [...prev, newMsg]);
    setMessage("");
    try {
      const res = await API.post("/chat/chat", { message });
      setChat((prev) => [...prev, { sender: "ai", text: res.data.response }]);
    } catch {
      toast.error("Error communicating with AI");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white p-4">
      <div className="flex-1 overflow-y-auto space-y-2">
        {chat.map((msg, i) => (
          <div key={i} className={`p-2 rounded-xl ${msg.sender === "user" ? "bg-blue-600 self-end" : "bg-gray-700 self-start"} max-w-[70%]`}>
            {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage} className="flex mt-4">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 p-2 rounded-l-xl text-black"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button className="bg-blue-600 hover:bg-blue-700 px-4 rounded-r-xl">Send</button>
      </form>
    </div>
  );
}
