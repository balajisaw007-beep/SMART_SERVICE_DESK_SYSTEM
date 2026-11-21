import json
from pathlib import Path

from domain.service_request import ServiceRequest


class FileRepository:
    def __init__(self, file_path="data/requests.json"):
        self.file_path = Path(file_path)

    def load(self):
        if not self.file_path.exists():
            return []

        try:
            content = self.file_path.read_text(encoding="utf-8")
            if not content.strip():
                return []
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("The requests JSON file is invalid.") from exc

        if not isinstance(data, list):
            raise ValueError("The requests JSON file must contain a list.")

        return [ServiceRequest.from_dict(item) for item in data]

    def save(self, requests):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.file_path.with_suffix(".tmp")
        payload = [request.to_dict() for request in requests]
        temporary_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary_path.replace(self.file_path)
