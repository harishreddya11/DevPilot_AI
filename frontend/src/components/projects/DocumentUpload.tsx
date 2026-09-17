import { useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  FileText,
  Upload,
  X,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

import { uploadDocument } from "../../api/documents";

interface DocumentUploadProps {
  projectId: string;
  onUploadSuccess?: () => void;
}

export default function DocumentUpload({
  projectId,
  onUploadSuccess,
}: DocumentUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const mutation = useMutation({
    mutationFn: (file: File) => uploadDocument(projectId, file),

    onSuccess: () => {
      setSelectedFile(null);

      if (inputRef.current) {
        inputRef.current.value = "";
      }

      onUploadSuccess?.();
    },
  });

  const validateFile = (file: File): boolean => {
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword",
    ];

    const allowedExtensions = [".pdf", ".doc", ".docx"];

    const extension = file.name
      .toLowerCase()
      .substring(file.name.lastIndexOf("."));

    if (
      !allowedTypes.includes(file.type) &&
      !allowedExtensions.includes(extension)
    ) {
      alert("Only PDF, DOC, and DOCX files are allowed.");
      return false;
    }

    return true;
  };

  const handleFile = (file: File | undefined) => {
    if (!file) return;

    if (!validateFile(file)) {
      return;
    }

    setSelectedFile(file);
    mutation.reset();
  };

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    handleFile(event.target.files?.[0]);
  };

  const handleDragOver = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setDragActive(false);
  };

  const handleDrop = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setDragActive(false);

    const file = event.dataTransfer.files?.[0];

    handleFile(file);
  };

  const handleUpload = () => {
    if (!selectedFile) return;

    mutation.mutate(selectedFile);
  };

  const handleRemove = () => {
    setSelectedFile(null);
    mutation.reset();

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-10 text-center transition ${
          dragActive
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300 bg-white hover:border-blue-400 hover:bg-gray-50"
        }`}
      >
        <Upload
          size={48}
          className="mx-auto mb-4 text-blue-600"
        />

        <h2 className="text-xl font-semibold text-gray-800">
          Upload a document
        </h2>

        <p className="mt-2 text-gray-500">
          Drag and drop your file here, or click to browse
        </p>

        <p className="mt-2 text-sm text-gray-400">
          Supported formats: PDF, DOC, DOCX
        </p>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleInputChange}
          className="hidden"
        />
      </div>

      {/* Selected File */}
      {selectedFile && (
        <div className="rounded-xl border bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-blue-100 p-3">
                <FileText
                  size={24}
                  className="text-blue-600"
                />
              </div>

              <div>
                <p className="font-medium text-gray-800">
                  {selectedFile.name}
                </p>

                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={handleRemove}
              disabled={mutation.isPending}
              className="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-red-500"
            >
              <X size={20} />
            </button>
          </div>

          {/* Upload Button */}
          <button
            type="button"
            onClick={handleUpload}
            disabled={mutation.isPending}
            className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Upload size={18} />

            {mutation.isPending
              ? "Uploading..."
              : "Upload Document"}
          </button>
        </div>
      )}

      {/* Success */}
      {mutation.isSuccess && (
        <div className="flex items-center gap-2 rounded-lg border border-green-200 bg-green-50 p-4 text-green-700">
          <CheckCircle size={20} />

          <span>
            Document uploaded successfully.
          </span>
        </div>
      )}

      {/* Error */}
      {mutation.isError && (
        <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
          <AlertCircle size={20} />

          <span>
            Document upload failed. Please try again.
          </span>
        </div>
      )}
    </div>
  );
}