# 🖥️ Smart Service Desk Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Data](https://img.shields.io/badge/Storage-JSON-green)
![Testing](https://img.shields.io/badge/Tests-unittest-orange)
![Git](https://img.shields.io/badge/Git-main%20%7C%20development-red?logo=git&logoColor=white)

> A structured Python command-line application for creating, viewing, searching, resolving, and persistently storing IT support requests.

## 🚀 Implemented Features

### ✅ Required Features

- Create a service request with a unique Request ID
- Automatically assign the `OPEN` status to a new request
- Validate priority as `LOW`, `MEDIUM`, or `HIGH`
- View all saved requests
- Search for a request using only its Request ID
- Resolve an open request and change its status to `RESOLVED`
- Prevent resolving the same request again
- Persist every create and resolve operation in `data/requests.json`
- Safely load missing or empty JSON data
- Handle duplicate IDs, missing requests, invalid priorities, invalid fields, and invalid menu choices with friendly messages

> [!IMPORTANT]
> ### ⭐ Extra Feature: Creator-Only Resolution
>
> **Real-life authorization is built into the resolution workflow:** only the employee who created a request can resolve it.
>
> - Resolution requires the Request ID and creator's Employee Name.
> - Names are checked case-insensitively and surrounding spaces are ignored.
> - A mismatched name raises `RequestResolutionUnauthorizedError`.
> - An unauthorized attempt leaves the request `OPEN`.
> - Request IDs are also searched case-insensitively.

## 🧰 Technology and Concepts

- Python 3
- Object-oriented programming
- Custom exceptions and specific exception handling
- JSON file handling
- Atomic JSON writes through a temporary `.tmp` file
- Single Responsibility and Dependency Inversion
- Basic Domain-Driven Design
- Unit testing with `unittest`
- Git branch-and-merge workflow

## 📁 Project Structure

```text
project/
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

## 🏗️ Responsibility of Each Layer

- `domain/` contains the `ServiceRequest` model, priority validation, resolve behavior, and domain exceptions.
- `application/` contains the create, view, search, and resolve use cases in `RequestService`.
- `infrastructure/` contains JSON loading and saving in `FileRepository`.
- `main.py` contains the menu, prompts, application flow, and user-friendly output.
- `data/requests.json` stores the persistent application records.

The domain model does not open or update JSON files. JSON and file-system responsibilities belong to the infrastructure layer.

## 📋 Prerequisites

- Python 3.10 or newer
- Git
- Windows PowerShell, Command Prompt, or another terminal

Check both tools:

```powershell
python --version
git --version
```

## ⚙️ Setup

Open the project directory:

```powershell
cd C:\Users\balaj\OneDrive\Desktop\project
```

Optional virtual-environment setup on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

No third-party Python package is required to run the application.

If PowerShell prevents virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## ▶️ Run the Application

Without a virtual environment:

```powershell
python main.py
```

With a virtual environment activated:

```powershell
python main.py
```

The expected menu is:

```text
SMART SERVICE DESK SYSTEM
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit
Enter your choice:
```

## ✍️ Input Formats

### Create Service Request

```text
Request ID: SR101
Employee Name: Rahul
Issue Description: Laptop is not starting
Priority: HIGH
```

The complete format is:

```text
Request ID | Employee Name | Issue Description | Priority
```

Only these priorities are accepted:

```text
LOW
MEDIUM
HIGH
```

Priority names are case-insensitive. For example, `high` is normalized to `HIGH`. Numeric values such as `1` or `2` are rejected with:

```text
Error: Priority must be LOW, MEDIUM or HIGH
```

Blank values are rejected, and a duplicate Request ID displays:

```text
Error: A request with ID SR101 already exists.
```

### View All Requests

The output format is:

```text
Request ID | Employee Name | Issue | Priority | Status
```

Example:

```text
SR101 | Rahul | Laptop is not starting | HIGH | OPEN
SR102 | Priya | Wi-Fi issue | MEDIUM | RESOLVED
```

### Search Request

Enter only the Request ID. An existing request shows all of its details. An unknown Request ID displays:

```text
Error: Request not found
```

### 🔒 Resolve Request

Enter the Request ID and the same Employee Name used when creating it:

```text
Enter Request ID: SR101
Enter your Employee Name to confirm ownership: Rahul
```

Successful resolution changes `OPEN` to `RESOLVED` and saves the change. Resolving it again shows:

```text
Service Request is already RESOLVED.
```

Using another Employee Name shows:

```text
Error: Only the employee who created this request can resolve it.
```

## 🎯 Mandatory Evaluation Demonstration

1. Run `python main.py`.
2. Choose `1` and create `SR101`:

   ```text
   Request ID: SR101
   Employee Name: Rahul
   Issue: Laptop is not starting
   Priority: HIGH
   ```

3. Choose `1` again and repeat `SR101` to demonstrate duplicate handling.
4. Choose `2` to view all requests.
5. Choose `3` and search for `SR101`.
6. Choose `4`, enter `SR101`, and enter `Rahul` to resolve the request.
7. Choose `4` again and enter `Priya` to demonstrate creator-only resolution.
8. Choose `4` with `Rahul` again to confirm it is already resolved.
9. Choose `5` to exit.
10. Restart with `python main.py`.
11. Choose `3` and search for `SR101`.
12. Confirm that the saved status is `RESOLVED`.

## 💾 Persistence Check

The service requests are stored in `data/requests.json`. To manually inspect the saved data:

```powershell
Get-Content data\requests.json
```

The application also automatically creates `data/` if it is missing and handles an empty JSON file as an empty request list.

## 🧪 Run Tests

Run all automated tests:

```powershell
python -m unittest -v
```

Run test discovery:

```powershell
python -m unittest discover -v
```

Run a syntax compilation check:

```powershell
python -m compileall -q domain application infrastructure main.py test_smart_service_desk.py
```

The tests cover duplicate IDs, invalid priorities, not-found searches, creator-only resolution, repeated resolution, and persistence after repository reload.

## 🌿 Git Workflow

The repository uses two branches:

- `main`: final tested working version
- `development`: implementation and feature development

View branches:

```powershell
git branch
git branch --show-current
```

View commit history:

```powershell
git log --oneline --graph --decorate --all
```

Typical development workflow:

```powershell
git switch development
git add .
git commit -m "Implement requested feature"
python -m unittest -v
git switch main
git merge --no-ff development -m "Merge development into main"
git log --oneline --graph --all
```

Push the final result when a remote is configured:

```powershell
git remote add origin <repository-url>
git push -u origin main
git push origin development
```

To update an existing remote:

```powershell
git remote set-url origin <repository-url>
git push -u origin main
git push origin development
```

## 🎓 Viva and Evaluation Notes

- `ServiceRequest` belongs in the domain layer because it represents the core support-request data and owns priority validation and resolution behavior.
- `OPEN` changes to `RESOLVED` inside `ServiceRequest.resolve()`.
- JSON handling is outside `ServiceRequest`; `FileRepository` reads and writes data, keeping file technology out of the domain model.
- `RequestService` implements application use cases and coordinates domain objects with persistence.
- `DuplicateRequestIdError`, `RequestNotFoundError`, `InvalidPriorityError`, `InvalidRequestDataError`, and `RequestResolutionUnauthorizedError` are custom exceptions.
- The creator-only rule is an extra feature based on real-life ownership and is not a replacement for the assignment's base requirements.

## 📤 Submission Details

```text
Name:
Participant ID:
Git Repository URL:
Final Commit ID:
```

Useful commands for filling the submission details:

```powershell
git remote -v
git rev-parse HEAD
git status
```
