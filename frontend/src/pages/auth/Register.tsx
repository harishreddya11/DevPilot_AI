import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { register as registerUser } from "../../api/auth";
import axios from "axios";

type RegisterForm = {
  full_name: string;
  email: string;
  password: string;
};

export default function Register() {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>();

  const onSubmit = async (data: RegisterForm) => {
    try {
      await registerUser(data);

      alert("Registration successful");
      navigate("/login");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        alert(error.response?.data?.detail || "Registration failed");
      } else {
        alert("Registration failed");
      }
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-md rounded-lg bg-white p-8 shadow"
      >
        <h1 className="mb-6 text-center text-4xl font-bold">
          Create Account
        </h1>

        <input
          {...register("full_name", {
            required: "Full name is required",
          })}
          placeholder="Full Name"
          className="mb-2 w-full rounded border p-3"
        />
        {errors.full_name && (
          <p className="mb-3 text-sm text-red-500">
            {errors.full_name.message}
          </p>
        )}

        <input
          {...register("email", {
            required: "Email is required",
          })}
          type="email"
          placeholder="Email"
          className="mb-2 w-full rounded border p-3"
        />
        {errors.email && (
          <p className="mb-3 text-sm text-red-500">
            {errors.email.message}
          </p>
        )}

        <input
          {...register("password", {
            required: "Password is required",
            minLength: {
              value: 8,
              message: "Password must be at least 8 characters",
            },
          })}
          type="password"
          placeholder="Password"
          className="mb-4 w-full rounded border p-3"
        />
        {errors.password && (
          <p className="mb-4 text-sm text-red-500">
            {errors.password.message}
          </p>
        )}

        <button
          type="submit"
          className="w-full rounded bg-green-600 p-3 text-white hover:bg-green-700"
        >
          Register
        </button>
      </form>
    </div>
  );
}