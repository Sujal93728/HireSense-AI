import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";

export default function JobDetails() {
  const { jobId } = useParams();

  const [job, setJob] = useState(null);
  const [salary, setSalary] = useState(null);
  const [skillGap, setSkillGap] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [interview, setInterview] = useState(null);

  const [loading, setLoading] = useState(true);
  const [loadingInterview, setLoadingInterview] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const jobRes = await api.get(`/jobs/${jobId}`);
        setJob(jobRes.data);

        try {
          const salaryRes = await api.get(`/jobs/${jobId}/salary`);
          setSalary(salaryRes.data);
        } catch {}

        try {
          const gapRes = await api.get(`/resume/skill-gap/${jobId}`);
          setSkillGap(gapRes.data);
        } catch {}

        try {
          const roadmapRes = await api.get(
            `/resume/career-roadmap/${jobId}`
          );
          setRoadmap(roadmapRes.data);
        } catch {}

      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [jobId]);

  async function generateInterviewQuestions() {
    try {
      setLoadingInterview(true);

      const res = await api.get(`/resume/interview/${jobId}`);

      setInterview(res.data);

    } catch (err) {
      console.log(err);
    } finally {
      setLoadingInterview(false);
    }
  }

  if (loading) {
    return (
      <div className="text-center mt-20 text-3xl">
        Loading...
      </div>
    );
  }

  if (!job) {
    return (
      <div className="text-center mt-20">
        <h1 className="text-4xl font-bold text-red-600">
          Job Not Found
        </h1>

        <Link
          to="/"
          className="inline-block mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg"
        >
          Back
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-8">

      <Link
        to="/"
        className="text-blue-600 hover:underline"
      >
        ← Back to Jobs
      </Link>

      <div className="bg-white rounded-xl shadow-xl p-8 mt-5">

        <h1 className="text-4xl font-bold text-blue-700">
          {job.title}
        </h1>

        <div className="mt-6 space-y-3 text-lg">

          <p>
            📍 <strong>Location:</strong> {job.location || "N/A"}
          </p>

          <p>
            💼 <strong>Work Type:</strong> {job.work_type || "N/A"}
          </p>

          <p>
            🏢 <strong>Company:</strong> {job.company_name || "N/A"}
          </p>

          <p>
            💰 <strong>Salary:</strong> {job.max_salary || "Not Available"}
          </p>

        </div>

        <hr className="my-8"/>

        <h2 className="text-2xl font-bold mb-4">
          Job Description
        </h2>

        <p className="leading-8 whitespace-pre-line">
          {job.description || "No description available"}
        </p>

      </div>

      {salary && (

        <div className="bg-green-100 rounded-xl shadow-lg p-6 mt-8">

          <h2 className="text-2xl font-bold text-green-700 mb-4">
            💰 AI Salary Prediction
          </h2>

          <p className="text-xl">
            Predicted Salary:
            <strong>
              {" "}
              ${salary.predicted_salary}
            </strong>
          </p>

          <p className="mt-2">
            Confidence:
            <strong>
              {" "}
              {salary.confidence}%
            </strong>
          </p>

        </div>

      )}
           {/* Skill Gap Analysis */}

      {skillGap && (
        <div className="bg-orange-100 rounded-xl shadow-lg p-6 mt-8">

          <h2 className="text-2xl font-bold text-orange-700 mb-5">
            🎯 Skill Gap Analysis
          </h2>

          <p className="text-lg mb-6">
            Match Score:
            <strong> {skillGap.score}%</strong>
          </p>

          <div className="grid md:grid-cols-2 gap-8">

            <div>

              <h3 className="text-xl font-bold text-green-700 mb-3">
                ✅ Matched Skills
              </h3>

              <ul className="list-disc ml-6 space-y-2">

                {skillGap.matched_skills.length === 0 ? (
                  <li>No matched skills found.</li>
                ) : (
                  skillGap.matched_skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))
                )}

              </ul>

            </div>

            <div>

              <h3 className="text-xl font-bold text-red-700 mb-3">
                ❌ Missing Skills
              </h3>

              <ul className="list-disc ml-6 space-y-2">

                {skillGap.missing_skills.length === 0 ? (
                  <li>No missing skills 🎉</li>
                ) : (
                  skillGap.missing_skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))
                )}

              </ul>

            </div>

          </div>

        </div>
      )}

      {/* Career Roadmap */}

      {roadmap && (
        <div className="bg-blue-100 rounded-xl shadow-lg p-6 mt-8">

          <h2 className="text-3xl font-bold text-blue-700 mb-6">
            🛣 AI Career Roadmap
          </h2>

          <p className="text-lg">
            Career Readiness:
            <strong> {roadmap.career_readiness}%</strong>
          </p>

          <p className="text-lg mb-6">
            Estimated Learning Time:
            <strong> {roadmap.estimated_days} Days</strong>
          </p>

          <div className="space-y-4">

            {roadmap.roadmap.map((item, index) => (
              <div
                key={index}
                className="bg-white rounded-lg shadow p-5 flex justify-between items-center"
              >

                <div>

                  <h3 className="font-bold text-xl">
                    {item.skill}
                  </h3>

                  <p className="text-gray-600">
                    Level: {item.level}
                  </p>

                </div>

                <div className="text-blue-700 font-bold text-lg">
                  {item.days} Days
                </div>

              </div>
            ))}

          </div>

        </div>
      )}

      {/* Interview Questions */}

      <div className="mt-10">

        <button
          onClick={generateInterviewQuestions}
          className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold shadow"
        >
          {loadingInterview
            ? "Generating..."
            : "🎤 Generate Interview Questions"}
        </button>

      </div>

      {interview && (

        <div className="bg-white rounded-xl shadow-xl p-8 mt-8">

          <h2 className="text-3xl font-bold text-purple-700 mb-5">
            🎤 AI Interview Questions
          </h2>

          <p className="mb-3">
            <strong>Difficulty:</strong> {interview.difficulty}
          </p>

          <p className="mb-6">
            <strong>Estimated Time:</strong> {interview.estimated_time}
          </p>

          <ol className="list-decimal ml-6 space-y-4">

            {interview.questions.length === 0 ? (
              <li>No interview questions available.</li>
            ) : (
              interview.questions.map((question, index) => (
                <li key={index} className="text-lg">
                  {question}
                </li>
              ))
            )}

          </ol>

        </div>

      )}

    </div>
  );
}