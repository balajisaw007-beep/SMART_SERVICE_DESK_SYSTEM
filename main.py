from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestIdError,
    InvalidPriorityError,
    InvalidRequestDataError,
    RequestNotFoundError,
    RequestResolutionUnauthorizedError,
)
from infrastructure.file_repository import FileRepository


MENU = """SMART SERVICE DESK SYSTEM
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit
Enter your choice: """


def read_required(prompt):
    value = input(prompt).strip()
    if not value:
        raise InvalidRequestDataError("This field cannot be blank.")
    return value


def create_request(service):
    print("Request format: Request ID, Employee Name, Issue Description, Priority")
    print("Priority format: LOW, MEDIUM, or HIGH")
    request_id = read_required("Enter Request ID (example: SR101): ")
    employee_name = read_required("Enter Employee Name (example: Rahul): ")
    issue = read_required("Enter Issue (example: Laptop is not starting): ")
    priority = read_required("Enter Priority (LOW, MEDIUM, or HIGH): ")
    request = service.create_request(request_id, employee_name, issue, priority)
    print("Service Request created successfully.")
    print(request)


def view_requests(service):
    requests = service.view_requests()
    if not requests:
        print("No service requests found.")
        return
    for request in requests:
        print(request)


def search_request(service):
    request_id = read_required("Enter Request ID: ")
    request = service.search_request(request_id)
    print(request)


def resolve_request(service):
    request_id = read_required("Enter Request ID: ")
    employee_name = read_required("Enter your Employee Name to confirm ownership: ")
    resolved = service.resolve_request(request_id, employee_name)
    if resolved:
        print("Service Request resolved successfully.")
    else:
        print("Service Request is already RESOLVED.")


def main():
    try:
        service = RequestService(FileRepository())
    except ValueError as exc:
        print(f"Error loading requests: {exc}")
        return

    while True:
        try:
            choice = input(MENU).strip()
            if choice == "1":
                create_request(service)
            elif choice == "2":
                view_requests(service)
            elif choice == "3":
                search_request(service)
            elif choice == "4":
                resolve_request(service)
            elif choice == "5":
                print("Goodbye.")
                break
            else:
                print("Invalid menu option. Enter a number from 1 to 5.")
        except (
            DuplicateRequestIdError,
            RequestNotFoundError,
            InvalidPriorityError,
            InvalidRequestDataError,
            RequestResolutionUnauthorizedError,
        ) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
