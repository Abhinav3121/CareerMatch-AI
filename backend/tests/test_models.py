import unittest

from app.database import Base
from app.models import User, Resume, Job, JobMatch


class ModelTests(unittest.TestCase):

    def test_expected_tables_are_registered(self):
        expected_tables = {
            "users",
            "resumes",
            "jobs",
            "job_matches",
        }

        self.assertEqual(
            set(Base.metadata.tables.keys()),
            expected_tables,
        )

    def test_user_relationships(self):
        relationships = set(
            User.__mapper__.relationships.keys()
        )

        self.assertEqual(
            relationships,
            {"resumes", "job_matches"},
        )

    def test_resume_relationships(self):
        relationships = set(
            Resume.__mapper__.relationships.keys()
        )

        self.assertEqual(
            relationships,
            {"user", "job_matches"},
        )

    def test_job_relationships(self):
        relationships = set(
            Job.__mapper__.relationships.keys()
        )

        self.assertEqual(
            relationships,
            {"job_matches"},
        )

    def test_job_match_relationships(self):
        relationships = set(
            JobMatch.__mapper__.relationships.keys()
        )

        self.assertEqual(
            relationships,
            {"user", "resume", "job"},
        )


if __name__ == "__main__":
    unittest.main()
