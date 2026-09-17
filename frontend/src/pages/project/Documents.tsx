import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import {
  FileText,
  Trash2,
  RefreshCw,
} from "lucide-react";

import DocumentUpload from "../../components/projects/DocumentUpload";
import {
  getProjectDocuments,
  deleteDocument,
} from "../../api/documents";

export default function Documents() {
  const { projectId } = useParams<{
    projectId: string;
  }>();

  const queryClient = useQueryClient();

  const {
    data: documents = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["documents", projectId],
    queryFn: () =>
      getProjectDocuments(projectId!),
    enabled: !!projectId,
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDocument,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["documents", projectId],
      });
    },
  });

  if (!projectId) {
    return (
      <div className="rounded-xl border bg-white p-8 text-center">
        <p className="text-red-500">
          Project ID is missing.
        </p>
      </div>
    );
  }

  const handleDelete = (documentId: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmed) {
      return;
    }

    deleteMutation.mutate(documentId);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-blue-100 p-3">
            <FileText
              size={28}
              className="text-blue-600"
            />
          </div>

          <div>
            <h1 className="text-3xl font-bold">
              Documents
            </h1>

            <p className="mt-1 text-gray-500">
              Upload documents and use them with your AI assistant.
            </p>
          </div>
        </div>
      </div>

      {/* Upload */}
      <DocumentUpload
        projectId={projectId}
        onUploadSuccess={() => {
          queryClient.invalidateQueries({
            queryKey: ["documents", projectId],
          });
        }}
      />

      {/* Documents */}
      <div className="rounded-xl border bg-white shadow-sm">
        <div className="flex items-center justify-between border-b p-5">
          <div>
            <h2 className="text-xl font-semibold">
              Uploaded Documents
            </h2>

            <p className="text-sm text-gray-500">
              {documents.length} document
              {documents.length !== 1 ? "s" : ""}
            </p>
          </div>

          <button
            onClick={() =>
              queryClient.invalidateQueries({
                queryKey: ["documents", projectId],
              })
            }
            className="rounded-lg border p-2 text-gray-600 hover:bg-gray-100"
            title="Refresh"
          >
            <RefreshCw size={18} />
          </button>
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="p-10 text-center">
            <p className="text-gray-500">
              Loading documents...
            </p>
          </div>
        )}

        {/* Error */}
        {isError && (
          <div className="p-10 text-center">
            <p className="text-red-500">
              Failed to load documents.
            </p>
          </div>
        )}

        {/* Empty */}
        {!isLoading &&
          !isError &&
          documents.length === 0 && (
            <div className="p-10 text-center">
              <FileText
                size={48}
                className="mx-auto mb-4 text-gray-300"
              />

              <h3 className="text-lg font-semibold">
                No documents yet
              </h3>

              <p className="mt-1 text-gray-500">
                Upload your first document above.
              </p>
            </div>
          )}

        {/* List */}
        {!isLoading &&
          !isError &&
          documents.length > 0 && (
            <div className="divide-y">
              {documents.map((document) => (
                <div
                  key={document.id}
                  className="flex items-center justify-between p-5 hover:bg-gray-50"
                >
                  <div className="flex items-center gap-4">
                    <div className="rounded-lg bg-blue-100 p-3">
                      <FileText
                        size={24}
                        className="text-blue-600"
                      />
                    </div>

                    <div>
                      <h3 className="font-medium">
                        {document.filename}
                      </h3>

                      <p className="mt-1 text-sm text-gray-500">
                        {document.file_type.toUpperCase()}
                        {" · "}
                        {formatFileSize(document.file_size)}
                        {" · "}
                        {new Date(
                          document.uploaded_at
                        ).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() =>
                      handleDelete(document.id)
                    }
                    disabled={deleteMutation.isPending}
                    className="rounded-lg p-2 text-red-500 hover:bg-red-50 disabled:opacity-50"
                    title="Delete document"
                  >
                    <Trash2 size={20} />
                  </button>
                </div>
              ))}
            </div>
          )}
      </div>
    </div>
  );
}