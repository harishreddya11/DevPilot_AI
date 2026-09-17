import api from "./client";

export interface Document {
  id: string;
  user_id: string;
  project_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  storage_path: string;
  uploaded_at: string;
}

export const uploadDocument = async (
  projectId: string,
  file: File
): Promise<Document> => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    `/documents/${projectId}/documents`,
    formData
  );

  return response.data;
};

export const getProjectDocuments = async (
  projectId: string
): Promise<Document[]> => {
  const response = await api.get(
    `/documents/${projectId}/documents`
  );

  return response.data;
};

export const deleteDocument = async (
  documentId: string
): Promise<void> => {
  await api.delete(`/documents/${documentId}`);
};