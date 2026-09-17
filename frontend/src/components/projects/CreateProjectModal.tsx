import { useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProject } from "../../api/projects";
import type { CreateProjectRequest } from "../../api/projects";
interface Props {
  open: boolean;
  onClose: () => void;
}

export default function CreateProjectModal({ open, onClose }: Props) {
  const queryClient = useQueryClient();

  const { register, handleSubmit, reset } = useForm<CreateProjectRequest>();

  const mutation = useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["projects"],
      });

      reset();
      onClose();
    },
  });

  const onSubmit = (data: CreateProjectRequest) => {
    mutation.mutate(data);
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-lg rounded-xl bg-white p-6">
        <h2 className="mb-4 text-2xl font-bold">
          Create Project
        </h2>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-4"
        >
          <input
            {...register("name", { required: true })}
            placeholder="Project Name"
            className="w-full rounded border p-3"
          />

          <textarea
            {...register("description")}
            placeholder="Description"
            className="w-full rounded border p-3"
          />

          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="rounded border px-4 py-2"
            >
              Cancel
            </button>

            <button
              type="submit"
              className="rounded bg-blue-600 px-4 py-2 text-white"
            >
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}