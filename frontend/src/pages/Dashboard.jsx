import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Navbar from "../components/Navbar";
import api from "../services/api";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const response = await api.get("/dashboard");
        setDashboard(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load dashboard."
        );
      }
    };

    loadDashboard();
  }, []);

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <div className="page-header">
          <h1>Dashboard</h1>

          <p>
            Track your resume, jobs and career matches.
          </p>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {!dashboard && !error ? (
          <div className="loading">
            Loading dashboard...
          </div>
        ) : dashboard ? (
          <>
            <div className="grid grid-4">
              <div className="card stat-card">
                <div className="stat-label">
                  Resume Count
                </div>

                <div className="stat-value">
                  {dashboard.resume_count}
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-label">
                  Available Jobs
                </div>

                <div className="stat-value">
                  {dashboard.job_count}
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-label">
                  Latest Resume Score
                </div>

                <div className="stat-value">
                  {dashboard.latest_resume?.score ?? 0}
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-label">
                  User
                </div>

                <div className="stat-value">
                  {dashboard.user?.name || "User"}
                </div>
              </div>
            </div>

            <h2 className="section-title">
              Quick Actions
            </h2>

            <div className="grid grid-3">
              <Link to="/resume" className="card">
                <h3>Upload Resume</h3>

                <p>
                  Upload a PDF or DOCX resume and let
                  CareerMatch AI analyze your skills.
                </p>

                <button className="btn btn-primary">
                  Manage Resume
                </button>
              </Link>

              <Link to="/jobs" className="card">
                <h3>Explore Jobs</h3>

                <p>
                  Browse available jobs and compare
                  your skills against their requirements.
                </p>

                <button className="btn btn-primary">
                  View Jobs
                </button>
              </Link>

              <Link
                to="/recommendations"
                className="card"
              >
                <h3>Recommendations</h3>

                <p>
                  See jobs ranked according to your
                  resume skills.
                </p>

                <button className="btn btn-primary">
                  View Recommendations
                </button>
              </Link>
            </div>

            <h2 className="section-title">
              Latest Resume
            </h2>

            <div className="card">
              {dashboard.latest_resume ? (
                <div>
                  <h3>
                    {dashboard.latest_resume.filename}
                  </h3>

                  <p>
                    Resume ID:{" "}
                    {dashboard.latest_resume.id}
                  </p>

                  <p>
                    Score:{" "}
                    <strong>
                      {dashboard.latest_resume.score}
                    </strong>
                  </p>
                </div>
              ) : (
                <div className="empty">
                  No resume uploaded yet.
                </div>
              )}
            </div>
          </>
        ) : null}
      </main>
    </div>
  );
}

export default Dashboard;
