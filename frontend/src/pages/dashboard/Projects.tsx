import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { FolderPlus } from "lucide-react";

import { getProjects } from "../../api/projects";
import CreateProjectModal from "../../components/projects/CreateProjectModal";
import { useNavigate } from "react-router-dom";
export default function Projects() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const {
    data: projects = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["projects"],
    queryFn: getProjects,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-gray-500 text-lg">Loading projects...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-red-500 text-lg">
          Failed to load projects.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Projects</h1>
            <p className="text-gray-500">
              Manage all your AI projects.
            </p>
          </div>

          <button
            onClick={() => setOpen(true)}
            className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
          >
            <FolderPlus size={18} />
            New Project
          </button>
        </div>

        {/* Empty State */}
        {projects?.length === 0 ? (
          <div className="rounded-xl border border-dashed bg-white p-12 text-center">
            <h2 className="text-xl font-semibold">
              No Projects Yet
            </h2>

            <p className="mt-2 text-gray-500">
              Create your first AI project to get started.
            </p>

            <button
              onClick={() => setOpen(true)}
              className="mt-6 rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700"
            >
              Create Project
            </button>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {projects.map((project) => (
              <div
                key={project.id}
                className="rounded-xl border bg-white p-5 shadow-sm transition hover:shadow-lg"
              >
                <h2 className="text-xl font-semibold">
                  {project.name}
                </h2>

                <p className="mt-2 text-gray-600">
                  {project.description || "No description"}
                </p>

                <div className="mt-4 space-y-1 text-sm text-gray-500">
                  <p>
                    <span className="font-medium">Status:</span>{" "}
                    {project.status}
                  </p>

                  <p>
                    <span className="font-medium">Created:</span>{" "}
                    {new Date(project.created_at).toLocaleDateString()}
                  </p>
                </div>

                <div className="mt-6 flex gap-2">
                  <button
                      onClick={() => navigate(`/dashboard/projects/${project.id}`)}
                      className="rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700"
                    >
                      Open
                    </button>

                  <button className="rounded border px-3 py-2 hover:bg-gray-100">
                    Edit
                  </button>

                  <button className="rounded border border-red-300 px-3 py-2 text-red-600 hover:bg-red-50">
                    Delete
                  </button>
                  
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Project Modal */}
      <CreateProjectModal
        open={open}
        onClose={() => setOpen(false)}
      />
    </>
  );
}