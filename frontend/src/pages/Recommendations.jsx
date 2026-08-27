import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";

function Recommendations() {
  const [recommendations, setRecommendations] =
    useState([]);

  const [sortOrder, setSortOrder] = useState("desc");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadRecommendations = async () => {
      try {
        const dashboardResponse =
          await api.get("/dashboard");

        const resumeId =
          dashboardResponse.data.latest_resume?.id;

        if (!resumeId) {
          setRecommendations([]);
          return;
        }

        const response = await api.get(
          `/recommendations/resume/${resumeId}`
        );

        setRecommendations(response.data.recommendations || []);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load recommendations."
        );
      } finally {
        setLoading(false);
      }
    };

    loadRecommendations();
  }, []);

  const sortedRecommendations = [...recommendations].sort(
    (a, b) =>
      sortOrder === "desc"
        ? b.match_percentage - a.match_percentage
        : a.match_percentage - b.match_percentage
  );

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <div className="page-header">
          <h1>Job Recommendations</h1>

          <p>
            Jobs ranked according to your resume
            skills.
          </p>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Calculating recommendations...
          </div>
        ) : recommendations.length === 0 ? (
          <div className="card empty">
            No recommendations available. Upload a
            resume first.
          </div>
        ) : (
          <>
            <div
              className="card"
              style={{
                marginBottom: 20,
                display: "flex",
                alignItems: "center",
                justifyContent: "flex-end",
                gap: 10,
              }}
            >
              <label htmlFor="match-sort">
                <strong>Sort by Match:</strong>
              </label>

              <select
                id="match-sort"
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
                style={{
                  padding: "8px 12px",
                  borderRadius: 6,
                  border: "1px solid #ccc",
                  fontSize: 14,
                }}
              >
                <option value="desc">Highest Match</option>
                <option value="asc">Lowest Match</option>
              </select>
            </div>

            <div className="grid grid-2">
              {sortedRecommendations.map((item) => (
              <div
                className="card job-card"
                key={item.job.id}
              >
                <div className="job-title">
                  {item.job.title}
                </div>

                <div className="company">
                  {item.job.company}
                </div>

                <div className="location">
                  📍 {item.job.location}
                </div>

                <div className="match-score">
                  {item.match_percentage}%
                </div>

                <div className="recommendation">
                  {item.recommendation}
                </div>

                <div className="progress">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${Math.min(
                        item.match_percentage,
                        100
                      )}%`,
                    }}
                  />
                </div>

                <h4>Matched Skills</h4>

                <div className="skill-list">
                  {item.matched_skills?.length ? (
                    item.matched_skills.map((skill) => (
                      <span
                        className="skill matched"
                        key={skill}
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span>None</span>
                  )}
                </div>

                <h4>Missing Skills</h4>

                <div className="skill-list">
                  {item.missing_skills?.length ? (
                    item.missing_skills.map((skill) => (
                      <span
                        className="skill missing"
                        key={skill}
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span>None</span>
                  )}
                </div>
              </div>
            ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default Recommendations;
