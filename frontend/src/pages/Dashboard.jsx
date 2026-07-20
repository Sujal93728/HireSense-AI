import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

import StatCard from "../components/StatCard";
import ResumeScore from "../components/ResumeScore";
import SkillGapCard from "../components/SkillGapCard";
import AIRecommendations from "../components/AIRecommendations";
import RecentJobs from "../components/RecentJobs";
import RecentInterviews from "../components/RecentInterviews";

import InterviewTrend from "../components/charts/InterviewTrend";
import SkillDistribution from "../components/charts/SkillDistribution";
import JobStatusChart from "../components/charts/JobStatusChart";

function Dashboard() {
    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);

    useEffect(() => {

        const loadDashboard = async () => {

            const token = localStorage.getItem("token");

            console.log("TOKEN:", token);

            if (!token) {
                alert("Please login first.");
                navigate("/login");
                return;
            }

            try {

                const response = await api.get("/dashboard/");

                console.log("Dashboard Response:", response.data);

                setDashboard(response.data);

            } catch (error) {

                console.error("Dashboard Error:", error);

                if (error.response?.status === 401) {

                    localStorage.removeItem("token");

                    alert("Session expired. Please login again.");

                    navigate("/login");
                }
            }
        };

        loadDashboard();

    }, [navigate]);

    if (!dashboard) {
        return (
            <div className="container mt-5 text-center">
                <h3>Loading Dashboard...</h3>
            </div>
        );
    }

    return (
        <div className="container-fluid p-4">

            <div className="d-flex justify-content-between align-items-center mb-4">
    <h2>Welcome to HireSense AI 🚀</h2>

    <button
        className="btn btn-primary"
        onClick={() => navigate("/interview")}
    >
        🎤 Start AI Interview
    </button>
</div>

            <div className="row g-4">

                <div className="col-md-3">
                    <StatCard
                        title="Average Score"
                        value={dashboard.average_score || 0}
                        icon="📈"
                    />
                </div>

                <div className="col-md-3">
                    <StatCard
                        title="Best Score"
                        value={dashboard.best_score || 0}
                        icon="🏆"
                    />
                </div>

                <div className="col-md-3">
                    <StatCard
                        title="Total Interviews"
                        value={dashboard.total_interviews || 0}
                        icon="🎤"
                    />
                </div>

                <div className="col-md-3">
                    <StatCard
                        title="Recommended Jobs"
                        value={dashboard.recommended_jobs?.length || 0}
                        icon="💼"
                    />
                </div>

            </div>

            <div className="row mt-4">

                <div className="col-lg-4">
                    <ResumeScore
                        score={dashboard.resume_score || 0}
                    />
                </div>

                <div className="col-lg-4">
                    <SkillGapCard
                        skills={dashboard.missing_skills || []}
                    />
                </div>

                <div className="col-lg-4">
                    <AIRecommendations
                        recommendations={dashboard.recommendations || []}
                    />
                </div>

            </div>

            <div className="row mt-4">

                <div className="col-lg-8">
                    <InterviewTrend
                        data={dashboard.interview_trend || []}
                    />
                </div>

                <div className="col-lg-4">
                    <SkillDistribution
                        data={dashboard.skill_distribution || []}
                    />
                </div>

            </div>

            <div className="row mt-4">

                <div className="col-lg-12">
                    <JobStatusChart
                        data={dashboard.job_status || []}
                    />
                </div>

            </div>

            <div className="row mt-4">

                <div className="col-lg-6">
                    <RecentJobs
                        jobs={dashboard.recommended_jobs || []}
                    />
                </div>

                <div className="col-lg-6">
                    <RecentInterviews
                        interviews={dashboard.recent_interviews || []}
                    />
                </div>

            </div>

        </div>
    );
}

export default Dashboard;