import tempfile
import unittest
from pathlib import Path

from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestIdError,
    InvalidPriorityError,
    RequestNotFoundError,
)
from domain.service_request import ServiceRequest
from infrastructure.file_repository import FileRepository


class ServiceDeskTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "requests.json"
        self.service = RequestService(FileRepository(self.file_path))

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_create_duplicate_and_resolve(self):
        request = self.service.create_request("SR101", "Rahul", "Laptop is not starting", "HIGH")
        self.assertEqual(request.status, "OPEN")

        with self.assertRaises(DuplicateRequestIdError):
            self.service.create_request("SR101", "Rahul", "Duplicate", "LOW")

        self.assertTrue(self.service.resolve_request("SR101"))
        self.assertFalse(self.service.resolve_request("SR101"))

    def test_search_not_found(self):
        with self.assertRaises(RequestNotFoundError):
            self.service.search_request("missing")

    def test_invalid_priority(self):
        with self.assertRaises(InvalidPriorityError):
            ServiceRequest("SR102", "Priya", "Wi-Fi issue", "URGENT")

    def test_data_persists_after_repository_reload(self):
        self.service.create_request("SR101", "Rahul", "Laptop is not starting", "HIGH")
        self.service.resolve_request("SR101")

        reloaded = RequestService(FileRepository(self.file_path))
        request = reloaded.search_request("SR101")
        self.assertEqual(request.status, "RESOLVED")


if __name__ == "__main__":
    unittest.main()
