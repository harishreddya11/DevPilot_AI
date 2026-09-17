import api from "./client";

export interface TechStack {
  backend?: string[];
  frontend?: string[];
  database?: string[];
  language?: string[];
  cache?: string[];
  queue?: string[];
  deployment?: string[];
  cloud?: string[];
}

export interface Project {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  tech_stack?: TechStack;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  tech_stack?: TechStack;
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string;
  tech_stack?: TechStack;
  status?: string;
}

export const getProjects = async (): Promise<Project[]> => {
  const { data } = await api.get("/projects");
  return data;
};

export const createProject = async (
  payload: CreateProjectRequest
): Promise<Project> => {
  const { data } = await api.post("/projects", payload);
  return data;
};

export const updateProject = async (
  id: string,
  payload: UpdateProjectRequest
): Promise<Project> => {
  const { data } = await api.patch(`/projects/${id}`, payload);
  return data;
};

export const deleteProject = async (id: string): Promise<void> => {
  await api.delete(`/projects/${id}`);
};

export const getProject = async (id: string): Promise<Project> => {
  const { data } = await api.get(`/projects/${id}`);
  return data;
};