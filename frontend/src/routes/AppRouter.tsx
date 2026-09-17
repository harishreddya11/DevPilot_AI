import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";

import ProtectedRoute from "./ProtectedRoute";

import DashboardLayout from "../components/layout/DashboardLayout";

import Home from "../pages/dashboard/Home";
import Projects from "../pages/dashboard/Projects";
import ProjectDetails from "../pages/dashboard/ProjectDetails";

import Documents from "../pages/project/Documents";
import Chats from "../pages/project/Chats";
import Assistant from "../pages/project/Assistant";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          {/* Dashboard Home */}
          <Route index element={<Home />} />

          {/* Projects List */}
          <Route path="projects" element={<Projects />} />

          {/* Project Details */}
          <Route
            path="projects/:projectId"
            element={<ProjectDetails />}
          />

          {/* Project Documents */}
          <Route
            path="projects/:projectId/documents"
            element={<Documents />}
          />

          {/* Project Chats */}
          <Route
            path="projects/:projectId/chats"
            element={<Chats />}
          />

          {/* AI Assistant */}
          <Route
            path="projects/:projectId/assistant"
            element={<Assistant />}
          />
        </Route>

        {/* 404 Page */}
        <Route
          path="*"
          element={
            <div className="flex h-screen items-center justify-center text-2xl font-bold">
              404 | Page Not Found
            </div>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}