import unittest

from app import app


class TestFineEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_fee_is_returned_as_json(self):
        response = self.client.get("/fine?days=5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"fee": 1.5})

    def test_deluxe_flag_doubles_the_fee(self):
        response = self.client.get("/fine?days=3&deluxe=1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"fee": 1.0})

    def test_non_numeric_days_return_400(self):
        response = self.client.get("/fine?days=abc")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_negative_days_return_400(self):
        response = self.client.get("/fine?days=-1")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()