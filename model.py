import json
from typing import List, Dict, Any

class FormFillerModel:
    def __init__(self):
        self.fields: List[Dict[str, Any]] = []
        self.runtime_prompt_queue: List[Dict[str, Any]] = []
        self.profiles: Dict[str, Dict[str, str]] = {
            "default": {
                "fullName": "John Doe",
                "email": "john@example.com"
            }
        }
        self.autofill_mode = "Interactive"  # "Passive", "Interactive", "Full Manual"

    def scan_page(self) -> List[Dict[str, Any]]:
        """
        Scans the current web page to identify form fields.
        This is a placeholder and would need to be implemented with a browser
        automation tool like Selenium or Playwright.
        """
        # Placeholder implementation
        self.fields = [
            {"id": "input_1", "type": "text", "label": "What is your opinion on X?", "autofill_mode": "interrupt", "value": None},
            {"id": "input_2", "type": "text", "label": "Full Name", "autofill_mode": "passive", "value": None},
            {"id": "input_3", "type": "email", "label": "Email Address", "autofill_mode": "passive", "value": None},
        ]
        self._prepare_runtime_prompts()
        return self.fields

    def _prepare_runtime_prompts(self):
        """Prepares the queue of fields that require user input."""
        self.runtime_prompt_queue = [
            {"fieldId": field["id"], "labelText": field["label"]}
            for field in self.fields if field["autofill_mode"] == "interrupt"
        ]

    def get_next_prompt(self) -> Dict[str, Any] | None:
        """Gets the next field that requires a runtime prompt."""
        if self.runtime_prompt_queue:
            return self.runtime_prompt_queue.pop(0)
        return None

    def set_field_value(self, field_id: str, value: str):
        """Sets the value for a specific field."""
        for field in self.fields:
            if field["id"] == field_id:
                field["value"] = value
                break

    def autofill_passive_fields(self):
        """Fills in the passive fields based on the current profile."""
        profile = self.profiles.get("default", {})
        for field in self.fields:
            if field["autofill_mode"] == "passive":
                label_lower = field["label"].lower()
                if "full name" in label_lower:
                    self.set_field_value(field["id"], profile.get("fullName", ""))
                elif "email" in label_lower:
                    self.set_field_value(field["id"], profile.get("email", ""))

    def set_autofill_mode(self, mode: str):
        """Sets the autofill mode."""
        if mode in ["Passive", "Interactive", "Full Manual"]:
            self.autofill_mode = mode

    def get_field_preview(self) -> List[Dict[str, Any]]:
        """Returns the current state of all detected fields."""
        return self.fields

    def save_responses(self, filepath: str):
        """Saves responses to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.fields, f, indent=2)

    def load_responses(self, filepath: str):
        """Loads responses from a file."""
        with open(filepath, 'r') as f:
            self.fields = json.load(f)
