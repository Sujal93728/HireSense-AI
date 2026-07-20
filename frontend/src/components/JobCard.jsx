import { Link } from "react-router-dom";

export default function JobCard({ job }) {
  return (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 p-6 border border-gray-200">

      {/* Job Title */}
      <h2 className="text-2xl font-bold text-blue-700 mb-4">
        {job.title}
      </h2>

      {/* Location */}
      <p className="text-gray-700 mb-2">
        📍 <span className="font-semibold">Location:</span>{" "}
        {job.location || "Not Available"}
      </p>

      {/* Work Type */}
      <p className="text-gray-700 mb-2">
        💼 <span className="font-semibold">Work Type:</span>{" "}
        {job.work_type || "Not Available"}
      </p>

      {/* Company */}
      <p className="text-gray-700 mb-5">
        🏢 <span className="font-semibold">Company ID:</span>{" "}
        {job.company_id ?? "Not Available"}
      </p>

      {/* View Details Button */}
      <Link
        to={`/jobs/${job.job_id}`}
        className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition"
      >
        View Details
      </Link>

    </div>
  );
}