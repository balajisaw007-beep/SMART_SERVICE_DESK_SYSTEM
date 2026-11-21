# Smart Service Desk Management System

A Python CLI application for creating, viewing, searching, and resolving employee IT support requests. The application demonstrates object-oriented design, domain-driven structure, exception handling, JSON persistence, and a branch-based Git workflow.

## Implemented Features

- Create a service request with an automatically assigned `OPEN` status
- Prevent duplicate Request IDs
- View all saved requests
- Search by Request ID
- Resolve an open request
- Prevent a second resolution of an already resolved request
- Allow resolution only by the employee who created the request; a mismatched Employee Name raises `RequestResolutionUnauthorizedError`
- Validate priorities as `LOW`, `MEDIUM`, or `HIGH`
- Persist requests in `data/requests.json`
- Safely handle missing or empty JSON data
- Show friendly messages for invalid menu choices and domain errors

## Concepts Used

- **OOP:** `ServiceRequest` encapsulates request data and the resolve behavior.
- **Exception handling:** custom domain exceptions represent duplicate IDs, missing requests, invalid priorities, and invalid request data.
- **File handling:** `FileRepository` uses JSON and atomic temporary-file replacement.
- **SOLID:** request use cases are separate from JSON storage; `RequestService` depends on repository behavior, not a particular UI or domain implementation.
- **DDD:** domain, application, infrastructure, presentation, and data responsibilities are separated.
- **Git:** development work occurs on `development`, and the tested result is merged into `main`.

## Project Structure

```text
smart-service-desk/
|-- domain/
|   |-- service_request.py
|   |-- exceptions.py
|   `-- __init__.py
|-- application/
|   |-- request_service.py
|   `-- __init__.py
|-- infrastructure/
|   |-- file_repository.py
|   `-- __init__.py
|-- data/
|   `-- requests.json
|-- main.py
|-- test_smart_service_desk.py
|-- README.md
`-- .gitignore
```

## Run the Application

From the project directory:

```bash
python main.py
```

Run the automated tests:

```bash
python -m unittest -v
```

## Mandatory Demonstration

1. Choose `1` and create `SR101` with priority `HIGH`.
2. Choose `1` again and attempt to create `SR101` to demonstrate duplicate handling.
3. Choose `2` to view all requests.
4. Choose `3` and search for `SR101`.
5. Choose `4`, enter `Rahul` as the creator/owner name, and resolve `SR101`.
6. Choose `4` with the wrong Employee Name to demonstrate creator-only resolution.
7. Choose `4` again with `Rahul` and confirm the request is already resolved.
8. Choose `5` to exit.
9. Restart with `python main.py` and search for `SR101` to show that `RESOLVED` was persisted.

Resolution rule: the Employee Name used during resolution must match the Employee Name used when the request was created. This models real-life ownership and prevents an unauthorized employee from resolving another employee's request.

## Git Workflow

The repository should contain only `main` and `development` working branches. Development is performed on `development` through meaningful commits. After testing, it is merged into `main`:

```bash
git switch development
# make and test changes
git add .
git commit -m "Complete CLI application"
git switch main
git merge development
git push -u origin main
```

View the resulting history:

```bash
git log --oneline --graph --all
```
