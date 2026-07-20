import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { ResumeContext } from "../context/ResumeContext";

export default function ResumeUpload() {
  const navigate = useNavigate();

  const {
  setMatches,
  analysis,
  setAnalysis,
  setRecommendedJobs,
} = useContext(ResumeContext);

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF resume.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await api.post(
        "/resume/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setMatches(res.data.matches || []);
      setRecommendedJobs(res.data.recommended_jobs || []);
      setRecommendedJobs(res.data.recommended_jobs || []);
      setAnalysis(res.data.analysis || null);

      alert("Resume uploaded successfully!");
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-8">

      <div className="bg-white rounded-xl shadow-xl p-8">

        <h1 className="text-4xl font-bold text-blue-700">
          AI Resume Analyzer
        </h1>

        <p className="text-gray-600 mt-3">
          Upload your resume to receive:
        </p>

        <ul className="list-disc ml-6 mt-3 text-gray-700">
          <li>AI Resume Match</li>
          <li>Resume Score</li>
          <li>Strength Analysis</li>
          <li>Weakness Detection</li>
          <li>AI Suggestions</li>
        </ul>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="mt-8 block"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>

      </div>

      {analysis && (

        <div className="bg-white rounded-xl shadow-xl mt-10 p-8">

          <h2 className="text-3xl font-bold text-green-700 mb-6">
            📄 Resume Analysis
          </h2>

          <div className="bg-green-100 rounded-lg p-6 mb-8">

            <h3 className="text-2xl font-bold">
              Resume Score
            </h3>

            <div className="text-5xl text-green-700 font-bold mt-3">
              {analysis.resume_score}/100
            </div>

          </div>

          <div className="grid md:grid-cols-3 gap-8">

            <div>

              <h3 className="text-xl font-bold text-green-700 mb-3">
                ✅ Strengths
              </h3>

              <ul className="list-disc ml-6 space-y-2">

                {analysis.strengths.length > 0 ? (
                  analysis.strengths.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))
                ) : (
                  <li>No strengths detected.</li>
                )}

              </ul>

            </div>

            <div>

              <h3 className="text-xl font-bold text-red-700 mb-3">
                ⚠ Weaknesses
              </h3>

              <ul className="list-disc ml-6 space-y-2">

                {analysis.weaknesses.length > 0 ? (
                  analysis.weaknesses.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))
                ) : (
                  <li>No weaknesses detected.</li>
                )}

              </ul>

            </div>

            <div>

              <h3 className="text-xl font-bold text-blue-700 mb-3">
                💡 AI Suggestions
              </h3>

              <ul className="list-disc ml-6 space-y-2">

                {analysis.suggestions.length > 0 ? (
                  analysis.suggestions.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))
                ) : (
                  <li>No suggestions.</li>
                )}

              </ul>

            </div>

          </div>

          <button
            onClick={() => navigate("/")}
            className="mt-10 bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg"
          >
            View Matching Jobs
          </button>

        </div>

      )}

    </div>
  );
}