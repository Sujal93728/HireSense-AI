import { Link } from "react-router-dom";

export default function RecommendedJobs({ jobs }) {
  if (!jobs || jobs.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
      <h2 className="text-3xl font-bold text-blue-700 mb-6">
        ⭐ AI Recommended Jobs
      </h2>

      <div className="space-y-4">
        {jobs.map((job, index) => (
          <div
            key={job.job_id}
            className="border rounded-lg p-5 hover:shadow-lg transition"
          >
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold">
                  {index + 1}. {job.title}
                </h3>

                <p className="text-gray-600">
                  Match Score: {job.match_score.toFixed(1)}%
                </p>
              </div>

              <Link
                to={`/jobs/${job.job_id}`}
                className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700"
              >
                View
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}