import { Link } from "react-router-dom";
import { Folder, MessageSquare, FileText, Settings, LogOut } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col p-4">
      <h1 className="text-2xl font-bold mb-8">DevPilot AI</h1>

      <nav className="space-y-2">
        <Link to="/dashboard/projects" className="flex items-center gap-2 rounded p-3 hover:bg-slate-800">
          <Folder size={20} />
          Projects
        </Link>

        <Link to="/dashboard/chats" className="flex items-center gap-2 rounded p-3 hover:bg-slate-800">
          <MessageSquare size={20} />
          Chats
        </Link>

        <Link to="/dashboard/documents" className="flex items-center gap-2 rounded p-3 hover:bg-slate-800">
          <FileText size={20} />
          Documents
        </Link>

        <Link to="/dashboard/settings" className="flex items-center gap-2 rounded p-3 hover:bg-slate-800">
          <Settings size={20} />
          Settings
        </Link>

        

      </nav>

      <div className="mt-auto">
        <button className="flex w-full items-center gap-2 rounded p-3 hover:bg-red-600">
          <LogOut size={20} />
          Logout
        </button>
      </div>
    </aside>
  );
}