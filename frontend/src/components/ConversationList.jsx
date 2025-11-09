import { useEffect, useState } from "react";
import API from "../api/axios";

export default function ConversationList({ activeId, onSelect, onCreate }) {
  const [convs, setConvs] = useState([]);

  const load = async () => {
    try {
      const res = await API.get("/conversations/");
      setConvs(res.data);
    } catch (e) {
      console.error(e);
    }
  };
  useEffect(() => { load(); }, []);

  return (
    <div className="w-72 bg-[#0b1220] border-r border-gray-800 p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-gray-100 font-semibold">Conversations</h3>
        <button className="text-sm text-blue-400" onClick={async ()=>{
          const r = await API.post("/conversations/", { title: "New chat" });
          onCreate && onCreate(r.data.id);
          load();
        }}>New</button>
      </div>
      <div className="space-y-2">
        {convs.map(c => (
          <div key={c.id} onClick={()=>onSelect(c.id)} className={`p-2 rounded cursor-pointer ${c.id === activeId ? 'bg-[#13213a]' : 'hover:bg-[#081223]'}`}>
            <div className="text-sm text-gray-200">{c.title || "New chat"}</div>
            <div className="text-xs text-gray-500">{c.updated_at}</div>
          </div>
        ))}
      </div>
    </div>
  );
}