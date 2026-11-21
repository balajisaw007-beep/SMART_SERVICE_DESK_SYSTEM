from domain.exceptions import InvalidPriorityError, InvalidRequestDataError


class ServiceRequest:
    ALLOWED_PRIORITIES = ("LOW", "MEDIUM", "HIGH")

    def __init__(self, request_id, employee_name, issue, priority, status="OPEN"):
        if not request_id or not str(request_id).strip():
            raise InvalidRequestDataError("Request ID cannot be blank.")
        if not employee_name or not str(employee_name).strip():
            raise InvalidRequestDataError("Employee Name cannot be blank.")
        if not issue or not str(issue).strip():
            raise InvalidRequestDataError("Issue description cannot be blank.")

        normalized_priority = str(priority).strip().upper()
        if normalized_priority not in self.ALLOWED_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH")

        normalized_status = str(status).strip().upper()
        if normalized_status not in ("OPEN", "RESOLVED"):
            raise InvalidRequestDataError("Status must be OPEN or RESOLVED.")

        self.request_id = str(request_id).strip()
        self.employee_name = str(employee_name).strip()
        self.issue = str(issue).strip()
        self.priority = normalized_priority
        self.status = normalized_status

    def resolve(self):
        if self.status == "RESOLVED":
            return False
        self.status = "RESOLVED"
        return True

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "OPEN"),
        )

    def __str__(self):
        return (
            f"{self.request_id} | {self.employee_name} | {self.issue} | "
            f"{self.priority} | {self.status}"
        )
