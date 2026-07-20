import { useState } from "react";
import axios from "axios";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function register(e) {
    e.preventDefault();

    try {
      await axios.post(
        "http://localhost:8000/auth/register",
        form
      );

      alert("Registration Successful!");
      window.location.href = "/login";

    } catch (err) {
      console.error("Registration Error:", err);

      if (err.response) {
        console.log("Status:", err.response.status);
        console.log("Data:", err.response.data);

        alert(
          `Error ${err.response.status}: ${JSON.stringify(
            err.response.data
          )}`
        );
      } else {
        alert(err.message);
      }
    }
  }   // <-- This closing brace was missing

  return (
    <div className="container mt-5">
      <h2>Create Account</h2>

      <form onSubmit={register}>
        <input
          className="form-control mb-3"
          placeholder="Username"
          name="username"
          value={form.username}
          onChange={handleChange}
        />

        <input
          className="form-control mb-3"
          placeholder="Email"
          name="email"
          value={form.email}
          onChange={handleChange}
        />

        <input
          type="password"
          className="form-control mb-3"
          placeholder="Password"
          name="password"
          value={form.password}
          onChange={handleChange}
        />

        <button className="btn btn-success">
          Register
        </button>
      </form>
    </div>
  );
}