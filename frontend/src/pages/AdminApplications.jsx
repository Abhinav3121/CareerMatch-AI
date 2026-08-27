import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";


function AdminApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [processingId, setProcessingId] = useState(null);


  const loadApplications = async () => {
    try {
      setError("");

      const response = await api.get(
        "/applications/admin/all"
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


  useEffect(() => {
    loadApplications();
  }, []);


  const updateApplication = async (
    applicationId,
    action
  ) => {
    try {
      setError("");
      setProcessingId(applicationId);

      await api.put(
        `/applications/admin/${applicationId}/${action}`
      );

      await loadApplications();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          `Unable to ${action} application.`
      );
    } finally {
      setProcessingId(null);
    }
  };


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
          <h1>Admin Applications</h1>

          <p>
            Review job applications and decide
            whether to accept or reject them.
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
            No applications have been submitted yet.
          </div>

        ) : (

          <div className="grid grid-2">

            {applications.map((application) => {

              const applicant =
                application.candidate;

              const job =
                application.job;

              const isProcessing =
                processingId === application.id;


              return (
                <div
                  className="card"
                  key={application.id}
                >

                  <div className="job-title">
                    {job?.title || "Unknown Job"}
                  </div>

                  <div className="company">
                    {job?.company || "Unknown Company"}
                  </div>

                  {job?.location && (
                    <div className="location">
                      📍 {job.location}
                    </div>
                  )}


                  <div
                    style={{
                      marginTop: 18,
                    }}
                  >
                    <strong>Applicant</strong>
                  </div>


                  <div
                    style={{
                      marginTop: 6,
                    }}
                  >
                    {applicant?.name ||
                      "Unknown applicant"}
                  </div>


                  {applicant?.email && (
                    <div
                      style={{
                        marginTop: 4,
                        fontSize: 14,
                        opacity: 0.7,
                      }}
                    >
                      {applicant.email}
                    </div>
                  )}


                  {application.match_percentage !==
                    null &&
                    application.match_percentage !==
                      undefined && (
                      <div
                        style={{
                          marginTop: 18,
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
                      marginTop: 18,
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


                  {application.applied_at && (
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
                  )}


                  {application.status ===
                    "pending" && (

                    <div
                      style={{
                        display: "flex",
                        gap: 10,
                        marginTop: 20,
                      }}
                    >

                      <button
                        className="btn btn-primary"
                        disabled={isProcessing}
                        onClick={() =>
                          updateApplication(
                            application.id,
                            "accept"
                          )
                        }
                      >
                        {isProcessing
                          ? "Processing..."
                          : "Accept"}
                      </button>


                      <button
                        className="btn"
                        disabled={isProcessing}
                        onClick={() =>
                          updateApplication(
                            application.id,
                            "reject"
                          )
                        }
                      >
                        Reject
                      </button>

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


export default AdminApplications;
