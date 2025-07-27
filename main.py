import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem, QComboBox, QDialog,
    QLabel, QLineEdit, QDialogButtonBox, QFormLayout
)
from model import FormFillerModel

class RuntimeInputDialog(QDialog):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manual Input Required")
        self.dialog_layout = QVBoxLayout(self)

        self.label = QLabel(f"Please provide input for:\n{label_text}")
        self.input_field = QLineEdit()
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.dialog_layout.addWidget(self.label)
        self.dialog_layout.addWidget(self.input_field)
        self.dialog_layout.addWidget(self.buttons)

    def get_input(self):
        return self.input_field.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Autofill Manager")
        self.model = FormFillerModel()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Top controls
        self.controls_layout = QHBoxLayout()
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Passive", "Interactive", "Manual"])
        self.mode_selector.currentTextChanged.connect(self.model.set_autofill_mode)
        self.controls_layout.addWidget(QLabel("Autofill Mode:"))
        self.controls_layout.addWidget(self.mode_selector)
        self.main_layout.addLayout(self.controls_layout)

        # Field preview
        self.field_preview = QTreeWidget()
        self.field_preview.setColumnCount(3)
        self.field_preview.setHeaderLabels(["ID", "Label", "Value"])
        self.main_layout.addWidget(self.field_preview)

        # Trigger buttons
        self.buttons_layout = QHBoxLayout()
        self.scan_button = QPushButton("Scan Current Page")
        self.scan_button.clicked.connect(self.scan_page)
        self.autofill_button = QPushButton("Begin Autofill")
        self.autofill_button.clicked.connect(self.begin_autofill)
        self.buttons_layout.addWidget(self.scan_button)
        self.buttons_layout.addWidget(self.autofill_button)
        self.main_layout.addLayout(self.buttons_layout)

    def scan_page(self):
        fields = self.model.scan_page()
        self.update_field_preview(fields)

    def begin_autofill(self):
        if self.model.autofill_mode == "Passive":
            self.model.autofill_passive_fields()
        elif self.model.autofill_mode == "Interactive":
            self.model.autofill_passive_fields()
            self.process_interactive_queue()

        self.update_field_preview(self.model.get_field_preview())


    def process_interactive_queue(self):
        prompt_data = self.model.get_next_prompt()
        if prompt_data:
            dialog = RuntimeInputDialog(prompt_data["labelText"], self)
            if dialog.exec():
                response = dialog.get_input()
                self.model.set_field_value(prompt_data["fieldId"], response)
                self.process_interactive_queue()  # Process next item

    def update_field_preview(self, fields):
        self.field_preview.clear()
        for field in fields:
            item = QTreeWidgetItem([
                field.get("id", ""),
                field.get("label", ""),
                str(field.get("value", ""))
            ])
            self.field_preview.addTopLevelItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
