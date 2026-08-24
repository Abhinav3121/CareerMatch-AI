import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";

function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [resumeId, setResumeId] = useState(null);

  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);
  const [matching, setMatching] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [jobsResponse, dashboardResponse] =
          await Promise.all([
            api.get("/jobs"),
            api.get("/dashboard"),
          ]);

        setJobs(jobsResponse.data);

        setResumeId(
          dashboardResponse.data.latest_resume?.id ||
            null
        );
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load jobs."
        );
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const matchJob = async (jobId) => {
    if (!resumeId) {
      setError(
        "Please upload a resume before matching jobs."
      );
      return;
    }

    setMatching(jobId);
    setError("");

    try {
      const response = await api.post(
        `/jobs/${jobId}/match/${resumeId}`
      );

      setResults((previous) => ({
        ...previous,
        [jobId]: response.data,
      }));
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to match this job."
      );
    } finally {
      setMatching(null);
    }
  };

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <div className="page-header">
          <h1>Jobs</h1>

          <p>
            Compare your resume against available
            positions.
          </p>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Loading jobs...
          </div>
        ) : jobs.length === 0 ? (
          <div className="card empty">
            No jobs available.
          </div>
        ) : (
          <div className="grid grid-2">
            {jobs.map((job) => {
              const result = results[job.id];

              return (
                <div className="card job-card" key={job.id}>
                  <div className="job-title">
                    {job.title}
                  </div>

                  <div className="company">
                    {job.company}
                  </div>

                  <div className="location">
                    📍 {job.location}
                  </div>

                  <div className="description">
                    {job.description}
                  </div>

                  <div>
                    <strong>Required Skills</strong>

                    <div
                      className="skill-list"
                      style={{ marginTop: 8 }}
                    >
                      {job.skills?.map((skill) => (
                        <span
                          className="skill"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    Experience:{" "}
                    <strong>
                      {job.experience_min}-
                      {job.experience_max} years
                    </strong>
                  </div>

                  <button
                    className="btn btn-primary"
                    onClick={() => matchJob(job.id)}
                    disabled={matching === job.id}
                  >
                    {matching === job.id
                      ? "Matching..."
                      : "Match My Resume"}
                  </button>

                  {result && (
                    <div className="card">
                      <div className="match-score">
                        {result.match_percentage}%
                      </div>

                      <div className="recommendation">
                        {result.recommendation}
                      </div>

                      <h4>Matched Skills</h4>

                      <div className="skill-list">
                        {result.matched_skills.length ? (
                          result.matched_skills.map(
                            (skill) => (
                              <span
                                className="skill matched"
                                key={skill}
                              >
                                {skill}
                              </span>
                            )
                          )
                        ) : (
                          <span>None</span>
                        )}
                      </div>

                      <h4>Missing Skills</h4>

                      <div className="skill-list">
                        {result.missing_skills.length ? (
                          result.missing_skills.map(
                            (skill) => (
                              <span
                                className="skill missing"
                                key={skill}
                              >
                                {skill}
                              </span>
                            )
                          )
                        ) : (
                          <span>None</span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}

export default Jobs;
