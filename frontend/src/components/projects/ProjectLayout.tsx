import { NavLink, Outlet, useParams } from "react-router-dom";

export default function ProjectLayout() {
  const { projectId } = useParams();

  const tabs = [
    {
      name: "Documents",
      path: `/dashboard/projects/${projectId}/documents`,
    },
    {
      name: "Chats",
      path: `/dashboard/projects/${projectId}/chats`,
    },
    {
      name: "AI Assistant",
      path: `/dashboard/projects/${projectId}/assistant`,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="border-b">
        <div className="flex gap-6">
          {tabs.map((tab) => (
            <NavLink
              key={tab.path}
              to={tab.path}
              className={({ isActive }) =>
                `pb-3 ${
                  isActive
                    ? "border-b-2 border-blue-600 font-semibold text-blue-600"
                    : "text-gray-500"
                }`
              }
            >
              {tab.name}
            </NavLink>
          ))}
        </div>
      </div>

      <Outlet />
    </div>
  );
}