import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";
import JobDetails from "./pages/JobDetails";
import ResumeUpload from "./pages/ResumeUpload";
import Test from "./pages/Test";
import Register from "./pages/Register";
import CareerAssistant from "./pages/CareerAssistant";
import Login from "./pages/Login";
import Interview from "./pages/Interview";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/jobs" element={<Jobs />} />
      <Route path="/jobs/:id" element={<JobDetails />} />
      <Route path="/resume" element={<ResumeUpload />} />
      <Route path="/test" element={<Test />} />
      <Route path="/register" element={<Register />} />
      <Route path="/career" element={<CareerAssistant />} />
      <Route path="/login" element={<Login />} />
      <Route
    path="/interview"
    element={<Interview />}
/>
    </Routes>
  );
}

export default App;