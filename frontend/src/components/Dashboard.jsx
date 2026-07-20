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

export default function Dashboard() {
    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboard();
    }, []);

    async function loadDashboard() {
        try {
            const token = localStorage.getItem("token");

            if (!token) {
                alert("Please login first.");
                navigate("/login");
                return;
            }

            console.log("Stored Token:", token);

            const response = await api.get("/dashboard/");

            console.log("Dashboard Response:", response.data);

            setDashboard(response.data);
        } catch (error) {
            console.error("Dashboard Error:", error);

            if (error.response) {
                console.log("Status:", error.response.status);
                console.log("Response:", error.response.data);

                if (error.response.status === 401) {
                    alert("Session expired. Please login again.");

                    localStorage.removeItem("token");

                    navigate("/login");
                    return;
                }
            }

            alert("Unable to load dashboard.");
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return (
            <div className="container mt-5 text-center">
                <h3>Loading Dashboard...</h3>
            </div>
        );
    }

    if (!dashboard) {
        return (
            <div className="container mt-5 text-center">
                <h3>No Dashboard Data Found</h3>
            </div>
        );
    }

    return (
        <div className="container-fluid p-4">

            <h2 className="mb-4">
                Welcome to HireSense AI 🚀
            </h2>

            {/* Statistics */}

            <div className="row g-4">

                <div className="col-md-3">
                    <StatCard
                        title="Average Score"
                        value={dashboard.average_score ?? 0}
                        icon="📈"
                        color="#2563eb"
                    />
                </div>

                <div className="col-md-3">
                    <StatCard
                        title="Best Score"
                        value={dashboard.best_score ?? 0}
                        icon="🏆"
                        color="#16a34a"
                    />
                </div>

                <div className="col-md-3">
                    <StatCard
                        title="Total Interviews"
                        value={dashboard.total_interviews ?? 0}
                        icon="🎤"
                        color="#ea580c"
                    />
                </div>

                <div className="col-md-3">
                    <StatCard
                        title="Recommended Jobs"
                        value={dashboard.recommended_jobs?.length ?? 0}
                        icon="💼"
                        color="#9333ea"
                    />
                </div>

            </div>

            {/* Resume */}

            <div className="row mt-4">

                <div className="col-lg-4">
                    <ResumeScore
                        score={dashboard.resume_score ?? 0}
                    />
                </div>

                <div className="col-lg-4">
                    <SkillGapCard
                        skills={dashboard.missing_skills ?? []}
                    />
                </div>

                <div className="col-lg-4">
                    <AIRecommendations
                        recommendations={dashboard.recommendations ?? []}
                    />
                </div>

            </div>

            {/* Charts */}

            <div className="row mt-4">

                <div className="col-lg-8">
                    <InterviewTrend
                        data={dashboard.interview_trend ?? []}
                    />
                </div>

                <div className="col-lg-4">
                    <SkillDistribution
                        data={dashboard.skill_distribution ?? []}
                    />
                </div>

            </div>

            <div className="row mt-4">

                <div className="col-lg-12">
                    <JobStatusChart
                        data={dashboard.job_status ?? []}
                    />
                </div>

            </div>

            {/* Bottom Widgets */}

            <div className="row mt-4">

                <div className="col-lg-6">
                    <RecentJobs
                        jobs={dashboard.recommended_jobs ?? []}
                    />
                </div>

                <div className="col-lg-6">
                    <RecentInterviews
                        interviews={dashboard.recent_interviews ?? []}
                    />
                </div>

            </div>

        </div>
    );
}