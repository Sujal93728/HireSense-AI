import API from "./api";

// Authentication
export const register = (data) => API.post("/auth/register", data);

export const login = (data) => API.post("/auth/login", data);

// Jobs
export const getJobs = () => API.get("/jobs");

export const getJob = (id) => API.get(`/jobs/${id}`);

// Chat
export const sendMessage = (data) => API.post("/chat", data);

// Resume
export const uploadResume = (formData) =>
  API.post("/resume/upload", formData);

// Interview
export const startInterview = (data) =>
  API.post("/interview/start", data);

export const submitAnswer = (data) =>
  API.post("/interview/answer", data);

// Dashboard
export const getDashboard = () =>
  API.get("/dashboard");

// Analytics
export const getAnalytics = () =>
  API.get("/analytics/dashboard");