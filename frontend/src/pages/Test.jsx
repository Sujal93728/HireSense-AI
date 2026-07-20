import { useEffect, useState } from "react";
import { getJobs } from "../services/apiService";

function Test() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    getJobs()
      .then((response) => {
        console.log("Jobs:", response.data);
        setJobs(response.data);
      })
      .catch((error) => {
        console.error("API Error:", error);
      });
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>API Connection Test</h1>

      <p>Total Jobs: {jobs.length}</p>

      {jobs.slice(0, 5).map((job) => (
        <div
          key={job.job_id}
          style={{
            border: "1px solid #ddd",
            marginBottom: "15px",
            padding: "15px",
            borderRadius: "8px",
          }}
        >
          <h3>{job.title}</h3>

          <p>{job.company_name}</p>

          <p>{job.location}</p>
        </div>
      ))}
    </div>
  );
}

export default Test;