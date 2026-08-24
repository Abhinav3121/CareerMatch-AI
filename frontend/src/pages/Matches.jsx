import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import api from "../services/api";

function Matches() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadMatches = async () => {
      try {
        const response = await api.get("/matches");

        setMatches(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load match history."
        );
      } finally {
        setLoading(false);
      }
    };

    loadMatches();
  }, []);

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <div className="page-header">
          <h1>Match History</h1>

          <p>
            Review your previous job matching results.
          </p>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Loading matches...
          </div>
        ) : matches.length === 0 ? (
          <div className="card empty">
            No matches yet.
          </div>
        ) : (
          <div className="table-wrapper card">
            <table>
              <thead>
                <tr>
                  <th>Job</th>
                  <th>Company</th>
                  <th>Resume</th>
                  <th>Match</th>
                  <th>Recommendation</th>
                  <th>Matched Skills</th>
                  <th>Missing Skills</th>
                </tr>
              </thead>

              <tbody>
                {matches.map((match) => (
                  <tr key={match.id}>
                    <td>
                      <strong>
                        {match.job_title}
                      </strong>
                    </td>

                    <td>{match.company}</td>

                    <td>
                      {match.resume_filename}
                    </td>

                    <td>
                      <strong>
                        {match.match_percentage}%
                      </strong>
                    </td>

                    <td>
                      <span className="recommendation">
                        {match.recommendation}
                      </span>
                    </td>

                    <td>
                      <div className="skill-list">
                        {match.matched_skills?.map(
                          (skill) => (
                            <span
                              className="skill matched"
                              key={skill}
                            >
                              {skill}
                            </span>
                          )
                        )}
                      </div>
                    </td>

                    <td>
                      <div className="skill-list">
                        {match.missing_skills?.map(
                          (skill) => (
                            <span
                              className="skill missing"
                              key={skill}
                            >
                              {skill}
                            </span>
                          )
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

export default Matches;
