import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ScrollToBottom from "react-scroll-to-bottom";
import toast from "react-hot-toast";
import API from "../api/axios";
import { useAuthStore } from "../store/useAuthStore";
import { useNavigate } from "react-router-dom";

export default function Chat() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPlaceholder, setShowPlaceholder] = useState(true);

  // --------------------------
  // 🧠 Fetch all chats
  // --------------------------
  const fetchChats = async () => {
    try {
      const res = await API.get("/chat/list");
      setChats(res.data);
    } catch (err) {
      handleAuthError(err);
    }
  };

  // --------------------------
  // 💬 Load chat messages
  // --------------------------
  const loadMessages = async (chatId) => {
    try {
      const res = await API.get(`/chat/${chatId}/history`);
      setActiveChat(chatId);
      setMessages(res.data.messages || []);
      setShowPlaceholder(false);
    } catch (err) {
      handleAuthError(err);
    }
  };

  // --------------------------
  // 🆕 Create new chat
  // --------------------------
  const startNewChat = async () => {
    if (!input.trim()) return toast.error("Enter a message first");

    const userMsg = { role: "user", text: input };
    setInput("");
    setShowPlaceholder(false);
    setMessages([userMsg, { role: "assistant", text: "🤔 AI is thinking..." }]);
    setLoading(true);

    try {
      const res = await API.post("/chat/new", { message: userMsg.text });
      const newChat = res.data;
      setChats((prev) => [newChat, ...prev]);
      setActiveChat(newChat.chat_id);
      const aiMsg = { role: "assistant", text: newChat.response };
      setMessages([userMsg, aiMsg]);
    } catch (err) {
      handleAuthError(err);
      toast.error("Failed to start new chat");
      setMessages([]);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------
  // ✉️ Send message
  // --------------------------
  const sendMessage = async () => {
    if (!input.trim() || !activeChat || loading) return;

    const userMsg = { role: "user", text: input };
    setInput("");
    setShowPlaceholder(false);

    const thinkingMsg = { role: "assistant", text: "🤔 AI is thinking..." };
    setMessages((prev) => [...prev, userMsg, thinkingMsg]);
    setLoading(true);

    try {
      const res = await API.post("/chat/send", {
        chat_id: activeChat,
        message: userMsg.text,
      });

      const aiMsg = { role: "assistant", text: res.data.response };
      setMessages((prev) =>
        prev.map((msg) =>
          msg.text === "🤔 AI is thinking..." ? aiMsg : msg
        )
      );
    } catch (err) {
      handleAuthError(err);
      toast.error("Failed to get AI response");
      setMessages((prev) =>
        prev.map((msg) =>
          msg.text === "🤔 AI is thinking..."
            ? { ...msg, text: "⚠️ Error generating response" }
            : msg
        )
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------
  // ⌨️ Enter key send
  // --------------------------
  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      activeChat ? sendMessage() : startNewChat();
    }
  };

  // --------------------------
  // ❌ Delete chat with confirmation
  // --------------------------
  const deleteChat = async (chatId) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this chat?");
    if (!confirmDelete) return;

    try {
      await API.delete(`/chat/${chatId}/delete`);
      toast.success("Chat deleted successfully");

      setChats((prev) => prev.filter((c) => c.id !== chatId));

      if (activeChat === chatId) {
        setActiveChat(null);
        setMessages([]);
        setInput("");
        setShowPlaceholder(true);
      }
    } catch (err) {
      handleAuthError(err);
      toast.error("Failed to delete chat");
    }
  };

  // --------------------------
  // 🚨 Handle expired tokens
  // --------------------------
  const handleAuthError = (err) => {
    if (err?.response?.status === 401) {
      toast.dismiss();
      toast.error("Session expired. Please log in again.", { duration: 4000 });
      setTimeout(() => {
        logout();
        navigate("/login");
      }, 2500);
    }
  };

  useEffect(() => {
    fetchChats();
  }, []);

  // --------------------------
  // 💬 UI
  // --------------------------
  return (
    <div className="flex h-screen bg-[#0d1117] text-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-[#111827] border-r border-gray-800 p-4 flex flex-col">
        <button
          onClick={() => {
            setActiveChat(null);
            setMessages([]);
            setInput("");
            setShowPlaceholder(true);
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-3 rounded-lg mb-4 transition"
        >
          + New Chat
        </button>

        <div className="flex-1 overflow-y-auto space-y-2 scrollbar-hide">
          <AnimatePresence>
            {chats.map((chat) => (
              <motion.div
                key={chat.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -40 }}
                transition={{ duration: 0.2 }}
                className={`flex justify-between items-center p-3 rounded-lg cursor-pointer transition group ${
                  activeChat === chat.id
                    ? "bg-blue-600 text-white"
                    : "hover:bg-gray-800 text-gray-300"
                }`}
              >
                <span
                  onClick={() => loadMessages(chat.id)}
                  className="flex-1 truncate"
                >
                  {chat.title}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteChat(chat.id);
                  }}
                  className="text-red-500 opacity-0 group-hover:opacity-100 transition text-sm ml-2"
                >
                  ✕
                </button>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        <div className="border-t border-gray-700 mt-4 pt-3 text-sm text-gray-400">
          <div className="flex justify-between items-center">
            <span>{user?.username}</span>
            <button
              onClick={() => {
                logout();
                navigate("/login");
              }}
              className="text-red-400 hover:text-red-500 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </aside>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        <header className="px-6 py-4 border-b border-gray-800 bg-[#111827]/70 backdrop-blur-sm sticky top-0 z-10 flex justify-between items-center">
          <h1 className="text-lg font-semibold">🤖 Senku AI</h1>

          {activeChat && (
            <button
              onClick={() => deleteChat(activeChat)}
              className="text-red-400 hover:text-red-500 transition text-sm border border-red-500 px-3 py-1 rounded-md"
            >
              Delete Chat
            </button>
          )}
        </header>

        <ScrollToBottom className="flex-1 overflow-y-auto px-6 py-6 flex flex-col gap-5 scrollbar-hide">
          {showPlaceholder && (
            <div className="flex justify-center items-center text-gray-500 italic mt-10">
              Select or start a chat
            </div>
          )}

          {activeChat && messages.length === 0 && !showPlaceholder && (
            <div className="flex justify-center items-center text-gray-500 italic mt-10">
              No messages yet. Start chatting!
            </div>
          )}

          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white shadow-lg"
                    : "bg-[#1e293b] text-gray-100 border border-gray-700"
                }`}
              >
                {msg.text}
              </div>
            </motion.div>
          ))}
        </ScrollToBottom>

        {/* Input */}
        <footer className="p-4 border-t border-gray-800 bg-[#111827]/60 backdrop-blur-sm flex">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            rows={1}
            placeholder="Ask anything..."
            className="flex-1 bg-[#1f2937] resize-none text-gray-100 placeholder-gray-500 border border-gray-700 rounded-l-md p-3 outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <button
            onClick={activeChat ? sendMessage : startNewChat}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-r-md transition disabled:opacity-50"
          >
            Send
          </button>
        </footer>
      </div>
    </div>
  );
}
