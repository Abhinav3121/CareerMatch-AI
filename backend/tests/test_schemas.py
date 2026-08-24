import unittest

from pydantic import ValidationError

from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate
from app.schemas.job import JobCreate


class SchemaTests(unittest.TestCase):

    def test_valid_login_request(self):
        data = LoginRequest(
            email="test@example.com",
            password="test-password-value",
        )

        self.assertEqual(
            str(data.email),
            "test@example.com",
        )

    def test_invalid_email_is_rejected(self):
        with self.assertRaises(ValidationError):
            LoginRequest(
                email="not-an-email",
                password="test-password-value",
            )

    def test_short_password_is_rejected(self):
        with self.assertRaises(ValidationError):
            UserCreate(
                name="Test User",
                email="test@example.com",
                password="short",
            )

    def test_valid_job_schema(self):
        job = JobCreate(
            title="Python Developer",
            company="Example Corp",
            description="Backend Python development",
            skills=["Python", "FastAPI", "PostgreSQL"],
        )

        self.assertEqual(
            job.title,
            "Python Developer",
        )

        self.assertEqual(
            job.skills,
            ["Python", "FastAPI", "PostgreSQL"],
        )


if __name__ == "__main__":
    unittest.main()
