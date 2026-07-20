import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function login(e) {
  e.preventDefault();

  try {
    const formData = new URLSearchParams();
    formData.append("username", form.email);
    formData.append("password", form.password);

    const res = await axios.post(
      "http://localhost:8000/auth/login",
      formData,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    console.log("LOGIN RESPONSE:", res.data);

    localStorage.setItem("token", res.data.access_token);

    console.log("TOKEN SAVED:", localStorage.getItem("token"));

    alert("Login Successful!");

    navigate("/");
  } catch (err) {
    console.error(err);

    if (err.response) {
      console.log("LOGIN ERROR:", err.response.data);
      alert(err.response.data.detail);
    } else {
      alert("Login Failed");
    }
  }
}

  return (
    <div className="container mt-5" style={{ maxWidth: "500px" }}>
      <h2 className="mb-4">Login</h2>

      <form onSubmit={login}>

        <input
          type="email"
          name="email"
          className="form-control mb-3"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />

        <input
          type="password"
          name="password"
          className="form-control mb-3"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
        />

        <button className="btn btn-primary w-100">
          Login
        </button>

      </form>
    </div>
  );
}