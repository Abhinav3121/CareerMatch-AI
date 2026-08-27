import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";


function Applications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const loadApplications = async () => {
      try {
        const response = await api.get(
          "/applications/me"
        );

        setApplications(response.data);

      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load applications."
        );
      } finally {
        setLoading(false);
      }
    };

    loadApplications();
  }, []);


  const statusClass = (status) => {
    if (status === "accepted") {
      return "skill matched";
    }

    if (status === "rejected") {
      return "skill missing";
    }

    return "skill";
  };


  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">

        <div className="page-header">
          <h1>My Applications</h1>

          <p>
            Track the status of jobs you have applied for.
          </p>
        </div>


        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}


        {loading ? (
          <div className="loading">
            Loading applications...
          </div>

        ) : applications.length === 0 ? (

          <div className="card empty">
            You haven't applied for any jobs yet.
          </div>

        ) : (

          <div className="grid grid-2">

            {applications.map((application) => (

              <div
                className="card"
                key={application.id}
              >

                <div className="job-title">
                  {application.job.title}
                </div>

                <div className="company">
                  {application.job.company}
                </div>

                {application.job.location && (
                  <div className="location">
                    📍 {application.job.location}
                  </div>
                )}


                {application.match_percentage !== null && (
                  <div
                    style={{
                      marginTop: 16,
                      fontSize: 18,
                    }}
                  >
                    Match:{" "}
                    <strong>
                      {application.match_percentage}%
                    </strong>
                  </div>
                )}


                <div
                  style={{
                    marginTop: 16,
                  }}
                >
                  Status:
                </div>


                <div
                  className={statusClass(
                    application.status
                  )}
                  style={{
                    display: "inline-block",
                    marginTop: 8,
                    textTransform: "capitalize",
                  }}
                >
                  {application.status}
                </div>


                <div
                  style={{
                    marginTop: 16,
                    fontSize: 14,
                    opacity: 0.7,
                  }}
                >
                  Applied:{" "}
                  {new Date(
                    application.applied_at
                  ).toLocaleDateString()}
                </div>

              </div>

            ))}

          </div>
        )}

      </main>
    </div>
  );
}


export default Applications;
