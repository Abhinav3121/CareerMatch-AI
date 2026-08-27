import { useEffect, useMemo, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";


function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [resumeId, setResumeId] = useState(null);

  const [results, setResults] = useState({});
  const [applications, setApplications] = useState({});

  const [loading, setLoading] = useState(true);
  const [matching, setMatching] = useState(null);
  const [autoMatching, setAutoMatching] = useState(false);
  const [applying, setApplying] = useState(null);

  const [sortOrder, setSortOrder] = useState("none");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  // ============================================================
  // LOAD JOBS, RESUME AND APPLICATIONS
  // ============================================================

  useEffect(() => {
    const load = async () => {
      try {
        const [
          jobsResponse,
          dashboardResponse,
          applicationsResponse,
        ] = await Promise.all([
          api.get("/jobs"),
          api.get("/dashboard"),
          api.get("/applications/me"),
        ]);

        const loadedJobs = jobsResponse.data;

        setJobs(loadedJobs);

        const latestResume =
          dashboardResponse.data.latest_resume;

        const currentResumeId =
          latestResume?.id || null;

        setResumeId(currentResumeId);


        const applicationMap = {};

        applicationsResponse.data.forEach(
          (application) => {
            applicationMap[application.job_id] =
              application;
          }
        );

        setApplications(applicationMap);

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


  // ============================================================
  // AUTOMATIC MATCHING
  // ============================================================

  useEffect(() => {
    if (!resumeId || jobs.length === 0) {
      return;
    }

    const matchAllJobs = async () => {
      setAutoMatching(true);
      setError("");

      try {
        const responses = await Promise.all(
          jobs.map(async (job) => {
            try {
              const response = await api.post(
                `/jobs/${job.id}/match/${resumeId}`
              );

              return {
                jobId: job.id,
                result: response.data,
              };
            } catch {
              return null;
            }
          })
        );

        const newResults = {};

        responses.forEach((item) => {
          if (item) {
            newResults[item.jobId] =
              item.result;
          }
        });

        setResults(newResults);

      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to calculate job matches."
        );
      } finally {
        setAutoMatching(false);
      }
    };

    matchAllJobs();
  }, [resumeId, jobs]);


  // ============================================================
  // MATCH SINGLE JOB
  // ============================================================

  const matchJob = async (jobId) => {
    if (!resumeId) {
      setError(
        "Please upload a resume before matching jobs."
      );
      return;
    }

    setMatching(jobId);
    setError("");
    setSuccess("");

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


  // ============================================================
  // APPLY FOR JOB
  // ============================================================

  const applyForJob = async (jobId) => {
    if (!resumeId) {
      setError(
        "Please upload a resume before applying for a job."
      );
      return;
    }

    setApplying(jobId);
    setError("");
    setSuccess("");

    try {
      const response = await api.post(
        `/applications/${jobId}`,
        {
          resume_id: resumeId,
        }
      );

      setApplications((previous) => ({
        ...previous,
        [jobId]: response.data,
      }));

      setSuccess(
        "Application submitted successfully."
      );

    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to submit application."
      );
    } finally {
      setApplying(null);
    }
  };


  // ============================================================
  // SORT JOBS
  // ============================================================

  const sortedJobs = useMemo(() => {
    const copy = [...jobs];

    if (sortOrder === "high") {
      copy.sort((a, b) => {
        const scoreA =
          results[a.id]?.match_percentage ?? -1;

        const scoreB =
          results[b.id]?.match_percentage ?? -1;

        return scoreB - scoreA;
      });
    }

    if (sortOrder === "low") {
      copy.sort((a, b) => {
        const scoreA =
          results[a.id]?.match_percentage ?? 101;

        const scoreB =
          results[b.id]?.match_percentage ?? 101;

        return scoreA - scoreB;
      });
    }

    return copy;
  }, [jobs, results, sortOrder]);


  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">

        <div className="page-header">
          <h1>Jobs</h1>

          <p>
            Compare your resume against available
            positions and apply to jobs.
          </p>
        </div>


        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}


        {success && (
          <div className="alert alert-success">
            {success}
          </div>
        )}


        {!loading && jobs.length > 0 && (
          <div
            className="card"
            style={{
              marginBottom: 24,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: 16,
              flexWrap: "wrap",
            }}
          >
            <div>
              <strong>
                Sort jobs by match
              </strong>

              {autoMatching && (
                <div
                  style={{
                    marginTop: 6,
                    fontSize: 14,
                    opacity: 0.7,
                  }}
                >
                  Calculating your match scores...
                </div>
              )}
            </div>

            <select
              value={sortOrder}
              onChange={(event) =>
                setSortOrder(event.target.value)
              }
              style={{
                padding: "10px 14px",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                background: "white",
                minWidth: 220,
                fontSize: 14,
              }}
            >
              <option value="none">
                Default order
              </option>

              <option value="high">
                Match: Highest to Lowest
              </option>

              <option value="low">
                Match: Lowest to Highest
              </option>
            </select>
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

            {sortedJobs.map((job) => {
              const result = results[job.id];
              const application =
                applications[job.id];


              return (
                <div
                  className="card job-card"
                  key={job.id}
                >

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
                    <strong>
                      Required Skills
                    </strong>

                    <div
                      className="skill-list"
                      style={{ marginTop: 8 }}
                    >
                      {job.skills?.map(
                        (skill) => (
                          <span
                            className="skill"
                            key={skill}
                          >
                            {skill}
                          </span>
                        )
                      )}
                    </div>
                  </div>


                  <div>
                    Experience:{" "}
                    <strong>
                      {job.experience_min ?? 0}-
                      {job.experience_max ?? "∞"} years
                    </strong>
                  </div>


                  {result && (
                    <div
                      style={{
                        marginTop: 12,
                        marginBottom: 12,
                        padding: 12,
                        borderRadius: 8,
                        background: "#f5f3ff",
                      }}
                    >
                      <strong>
                        Match:{" "}
                        {result.match_percentage}%
                      </strong>

                      <div
                        style={{
                          marginTop: 4,
                          fontSize: 14,
                        }}
                      >
                        {result.recommendation}
                      </div>
                    </div>
                  )}


                  <div
                    style={{
                      display: "flex",
                      gap: 10,
                      flexWrap: "wrap",
                      marginTop: 12,
                    }}
                  >

                    <button
                      className="btn btn-primary"
                      onClick={() =>
                        matchJob(job.id)
                      }
                      disabled={
                        matching === job.id
                      }
                    >
                      {matching === job.id
                        ? "Matching..."
                        : result
                          ? "Recalculate Match"
                          : "Match My Resume"}
                    </button>


                    {!application ? (

                      <button
                        className="btn btn-primary"
                        onClick={() =>
                          applyForJob(job.id)
                        }
                        disabled={
                          applying === job.id ||
                          !resumeId
                        }
                      >
                        {applying === job.id
                          ? "Applying..."
                          : "Apply"}
                      </button>

                    ) : (

                      <button
                        className="btn"
                        disabled
                        style={{
                          cursor: "default",
                          opacity: 0.9,
                        }}
                      >
                        ✓ Applied —{" "}
                        {application.status
                          .charAt(0)
                          .toUpperCase() +
                          application.status.slice(1)}
                      </button>

                    )}

                  </div>


                  {result && (
                    <div
                      className="card"
                      style={{
                        marginTop: 16,
                      }}
                    >

                      <div className="match-score">
                        {result.match_percentage}%
                      </div>


                      <div className="recommendation">
                        {result.recommendation}
                      </div>


                      <h4>
                        Matched Skills
                      </h4>


                      <div className="skill-list">
                        {result.matched_skills
                          .length ? (

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


                      <h4>
                        Missing Skills
                      </h4>


                      <div className="skill-list">
                        {result.missing_skills
                          .length ? (

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
