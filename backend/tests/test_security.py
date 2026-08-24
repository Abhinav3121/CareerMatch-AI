import unittest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class SecurityTests(unittest.TestCase):

    def test_password_hash_and_verify(self):
        password = "correct-test-password"

        hashed = hash_password(password)

        self.assertNotEqual(hashed, password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(
            verify_password("wrong-test-password", hashed)
        )

    def test_access_token_round_trip(self):
        user_id = 123

        token = create_access_token(user_id)
        decoded_user_id = decode_access_token(token)

        self.assertIsInstance(token, str)
        self.assertEqual(decoded_user_id, user_id)

    def test_invalid_access_token_is_rejected(self):
        with self.assertRaises(ValueError):
            decode_access_token("this-is-not-a-valid-jwt")


if __name__ == "__main__":
    unittest.main()
