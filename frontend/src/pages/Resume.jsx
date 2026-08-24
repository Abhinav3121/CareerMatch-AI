import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";

function Resume() {
  const [resume, setResume] = useState(null);
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [loadingResume, setLoadingResume] = useState(true);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadLatestResume = async () => {
    try {
      const dashboardResponse =
        await api.get("/dashboard");

      const latest =
        dashboardResponse.data.latest_resume;

      if (latest?.id) {
        const response = await api.get(
          `/resumes/${latest.id}`
        );

        setResume(response.data);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load resume."
      );
    } finally {
      setLoadingResume(false);
    }
  };

  useEffect(() => {
    loadLatestResume();
  }, []);

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Please select a PDF or DOCX file.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const formData = new FormData();

      formData.append("file", file);

      const response = await api.post(
        "/resumes/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResume(response.data);

      setMessage(
        "Resume uploaded and analyzed successfully."
      );

      setFile(null);

      event.target.reset();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Resume upload failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <div className="page-header">
          <h1>Resume Analysis</h1>

          <p>
            Upload your resume to extract skills and
            calculate your resume score.
          </p>
        </div>

        {message && (
          <div className="alert alert-success">
            {message}
          </div>
        )}

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        <div className="card">
          <h2>Upload Resume</h2>

          <form onSubmit={handleUpload}>
            <div className="upload-box">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(event) =>
                  setFile(event.target.files?.[0] || null)
                }
              />

              <p>
                Supported formats: PDF and DOCX.
                Maximum size: 5 MB.
              </p>

              {file && (
                <strong>
                  Selected: {file.name}
                </strong>
              )}
            </div>

            <br />

            <button
              className="btn btn-primary"
              disabled={loading}
            >
              {loading
                ? "Uploading and analyzing..."
                : "Upload Resume"}
            </button>
          </form>
        </div>

        {loadingResume ? (
          <div className="loading">
            Loading resume...
          </div>
        ) : resume ? (
          <>
            <h2 className="section-title">
              Resume Analysis
            </h2>

            <div className="grid grid-2">
              <div className="card">
                <h3>Resume Score</h3>

                <div className="resume-score">
                  {resume.score ?? 0}
                </div>

                <div className="progress">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${Math.min(
                        resume.score ?? 0,
                        100
                      )}%`,
                    }}
                  />
                </div>

                <p>
                  <strong>
                    {resume.original_filename}
                  </strong>
                </p>
              </div>

              <div className="card resume-info">
                <h3>Candidate</h3>

                <p>
                  <strong>Name:</strong>{" "}
                  {resume.analysis?.name || "Not detected"}
                </p>

                <p>
                  <strong>Email:</strong>{" "}
                  {resume.analysis?.email ||
                    "Not detected"}
                </p>

                <p>
                  <strong>Phone:</strong>{" "}
                  {resume.analysis?.phone ||
                    "Not detected"}
                </p>
              </div>
            </div>

            <div className="card" style={{ marginTop: 20 }}>
              <h3>Detected Skills</h3>

              <div className="skill-list">
                {resume.analysis?.skills?.length ? (
                  resume.analysis.skills.map((skill) => (
                    <span
                      className="skill matched"
                      key={skill}
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <span>No skills detected.</span>
                )}
              </div>
            </div>

            <div
              className="grid grid-2"
              style={{ marginTop: 20 }}
            >
              <div className="card">
                <h3>Education</h3>

                <p>
                  {resume.analysis?.education ||
                    "Not detected"}
                </p>
              </div>

              <div className="card">
                <h3>Experience</h3>

                <p>
                  {resume.analysis?.experience ||
                    "Not detected"}
                </p>
              </div>
            </div>
          </>
        ) : (
          <div className="card empty">
            No resume uploaded yet.
          </div>
        )}
      </main>
    </div>
  );
}

export default Resume;
