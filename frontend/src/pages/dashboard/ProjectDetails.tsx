import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowLeft,
  FileText,
  MessageSquare,
  Bot,
} from "lucide-react";

import { getProject } from "../../api/projects";
import type { ReactElement, JSXElementConstructor, ReactNode, ReactPortal } from "react";

export default function ProjectDetails() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();

  const {
    data: project,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => getProject(projectId!),
    enabled: !!projectId,
  });

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <p className="text-gray-500">
          Loading project...
        </p>
      </div>
    );
  }

  if (isError || !project) {
    return (
      <div className="flex h-96 items-center justify-center">
        <p className="text-red-500">
          Project not found.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Back */}
      <button
        onClick={() => navigate("/dashboard/projects")}
        className="flex items-center gap-2 text-gray-600 hover:text-blue-600"
      >
        <ArrowLeft size={18} />
        Back to Projects
      </button>

      {/* Project Header */}
      <div>
        <h1 className="text-4xl font-bold">
          {project.name}
        </h1>

        <p className="mt-2 text-gray-500">
          {project.description || "No description"}
        </p>

        <div className="mt-4">
          <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
            {project.status}
          </span>
        </div>
      </div>

      {/* Project Features */}
      <div className="grid gap-6 md:grid-cols-3">
        {/* Documents */}
        <button
          onClick={() =>
            navigate(
              `/dashboard/projects/${project.id}/documents`
            )
          }
          className="rounded-xl border bg-white p-6 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
        >
          <div className="mb-4 inline-flex rounded-lg bg-blue-100 p-3">
            <FileText
              size={28}
              className="text-blue-600"
            />
          </div>

          <h2 className="text-xl font-semibold">
            Documents
          </h2>

          <p className="mt-2 text-sm text-gray-500">
            Upload and manage project documents.
          </p>
        </button>

        {/* Chats */}
        <button
          onClick={() =>
            navigate(
              `/dashboard/projects/${project.id}/chats`
            )
          }
          className="rounded-xl border bg-white p-6 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
        >
          <div className="mb-4 inline-flex rounded-lg bg-purple-100 p-3">
            <MessageSquare
              size={28}
              className="text-purple-600"
            />
          </div>

          <h2 className="text-xl font-semibold">
            Chats
          </h2>

          <p className="mt-2 text-sm text-gray-500">
            View your project conversations.
          </p>
        </button>

        {/* Assistant */}
        <button
          onClick={() =>
            navigate(
              `/dashboard/projects/${project.id}/assistant`
            )
          }
          className="rounded-xl border bg-white p-6 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
        >
          <div className="mb-4 inline-flex rounded-lg bg-green-100 p-3">
            <Bot
              size={28}
              className="text-green-600"
            />
          </div>

          <h2 className="text-xl font-semibold">
            AI Assistant
          </h2>

          <p className="mt-2 text-sm text-gray-500">
            Ask questions about your documents.
          </p>
        </button>
      </div>

      {/* Tech Stack */}
      {project.tech_stack && (
        <div className="rounded-xl border bg-white p-6">
          <h2 className="text-xl font-semibold">
            Technology Stack
          </h2>

          <div className="mt-4 flex flex-wrap gap-2">
            {Object.entries(project.tech_stack).map(
              ([category, technologies]) =>
                technologies?.map((technology: string | number | bigint | boolean | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<string | number | bigint | boolean | ReactPortal | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | null | undefined> | null | undefined) => (
                  <span
                    key={`${category}-${technology}`}
                    className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700"
                  >
                    {technology}
                  </span>
                ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}