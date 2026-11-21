from domain.exceptions import (
    DuplicateRequestIdError,
    RequestNotFoundError,
)
from domain.service_request import ServiceRequest


class RequestService:
    def __init__(self, repository):
        self.repository = repository
        self.requests = repository.load()

    def create_request(self, request_id, employee_name, issue, priority):
        if self.search_request(request_id, suppress_error=True):
            raise DuplicateRequestIdError(
                f"A request with ID {request_id} already exists."
            )

        request = ServiceRequest(request_id, employee_name, issue, priority)
        self.requests.append(request)
        self.repository.save(self.requests)
        return request

    def view_requests(self):
        return list(self.requests)

    def search_request(self, request_id, suppress_error=False):
        for request in self.requests:
            if request.request_id.lower() == str(request_id).strip().lower():
                return request

        if not suppress_error:
            raise RequestNotFoundError("Request not found")
        return None

    def resolve_request(self, request_id, employee_name):
        request = self.search_request(request_id)
        resolved = request.resolve(employee_name)
        if resolved:
            self.repository.save(self.requests)
        return resolved
