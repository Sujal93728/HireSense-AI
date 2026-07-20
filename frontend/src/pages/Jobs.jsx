import { useEffect, useState, useContext } from "react";
import api from "../services/api";

import Dashboard from "../components/Dashboard";
import SearchBar from "../components/SearchBar";
import JobCard from "../components/JobCard";
import StatCard from "../components/StatCard";
import RecommendedJobs from "../components/RecommendedJobs";

import { ResumeContext } from "../context/ResumeContext";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [workType, setWorkType] = useState("");

  const { matches, recommendedJobs } = useContext(ResumeContext);

  useEffect(() => {
    api
      .get("/jobs")
      .then((res) => {
        console.log("Jobs received:", res.data);
        setJobs(res.data);
      })
      .catch((err) => {
        console.error("API Error:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const filteredJobs = jobs
    .filter((job) => {
      const matchesTitle = (job.title || "")
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesLocation = (job.location || "")
        .toLowerCase()
        .includes(location.toLowerCase());

      const matchesWorkType =
        workType === "" ||
        (job.work_type || "")
          .toLowerCase()
          .includes(workType.toLowerCase());

      return (
        matchesTitle &&
        matchesLocation &&
        matchesWorkType
      );
    })
    .sort((a, b) => {
      const scoreA =
        matches.find((m) => m.job_id === a.job_id)?.match_score || 0;

      const scoreB =
        matches.find((m) => m.job_id === b.job_id)?.match_score || 0;

      return scoreB - scoreA;
    });

  const remoteJobs = jobs.filter((job) =>
    (job.work_type || "").toLowerCase().includes("remote")
  ).length;

  const internships = jobs.filter((job) =>
    (job.work_type || "").toLowerCase().includes("intern")
  ).length;

  return (
    <Dashboard>
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Jobs"
          value={jobs.length}
          color="bg-blue-600"
        />

        <StatCard
          title="Remote Jobs"
          value={remoteJobs}
          color="bg-green-600"
        />

        <StatCard
          title="Internships"
          value={internships}
          color="bg-purple-600"
        />

        <StatCard
          title="Filtered Jobs"
          value={filteredJobs.length}
          color="bg-orange-500"
        />
      </div>

      <SearchBar
        search={search}
        setSearch={setSearch}
        location={location}
        setLocation={setLocation}
        workType={workType}
        setWorkType={setWorkType}
      />

      {loading ? (
        <h2 className="text-center text-2xl mt-10">
          Loading jobs...
        </h2>
      ) : filteredJobs.length === 0 ? (
        <h2 className="text-center text-gray-500 mt-10 text-xl">
          No jobs found.
        </h2>
      ) : (
        <div className="grid gap-6">
          {filteredJobs.map((job) => {
            const resumeMatch = matches.find(
              (m) => m.job_id === job.job_id
            );

            return (
              <div key={job.job_id} className="relative">
                <JobCard job={job} />

                {resumeMatch && (
                  <div
                    className={`absolute top-5 right-5 px-4 py-2 rounded-full text-white font-bold shadow-lg ${
                      resumeMatch.match_score >= 75
                        ? "bg-green-600"
                        : resumeMatch.match_score >= 50
                        ? "bg-yellow-500"
                        : "bg-red-500"
                    }`}
                  >
                    AI Match {resumeMatch.match_score.toFixed(1)}%
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </Dashboard>
  );
}