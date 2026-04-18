from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QDialogButtonBox, QVBoxLayout, QComboBox, QFormLayout
from .config import load_settings, save_settings


class FieldMapDialog(QDialog):
    """Dialog to map missing fields if defaults aren't found."""

    def __init__(self, field_names, parent=None, is_remove=False):
        super().__init__(parent)
        self.setWindowTitle("Map Note Fields")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.is_remove = is_remove

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Default fields not found. Please map them:"))

        form = QFormLayout()

        def set_default(cb, text):
            idx = cb.findText(text)
            if idx >= 0:
                cb.setCurrentIndex(idx)

        self.pos_cb = QComboBox()
        self.pos_cb.addItems(field_names)
        set_default(self.pos_cb, "Part of Speech")

        if not self.is_remove:
            self.expr_cb = QComboBox()
            self.expr_cb.addItems(field_names)
            set_default(self.expr_cb, "Expression")

            self.read_cb = QComboBox()
            self.read_cb.addItem("")  # Allow empty/none for reading
            self.read_cb.addItems(field_names)
            set_default(self.read_cb, "Kana Reading")

            form.addRow("Expression Field:", self.expr_cb)
            form.addRow("Kana Reading Field:", self.read_cb)

        form.addRow("Part of Speech Field:", self.pos_cb)
        layout.addLayout(form)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_mappings(self):
        if self.is_remove:
            return {"pos": self.pos_cb.currentText()}
        return {
            "expr": self.expr_cb.currentText(),
            "read": self.read_cb.currentText(),
            "pos": self.pos_cb.currentText()
        }


def resolve_mappings(model, parent_window, is_remove=False):
    """Returns the field mappings dict, prompting the user if necessary."""
    model_id = model['id']
    field_names = [f['name'] for f in model['flds']]

    saved_mapping = load_settings(model_id)
    if saved_mapping:
        if all(val in field_names or not val for val in saved_mapping.values()):
            if is_remove:
                return {"pos": saved_mapping.get("pos")}
            return saved_mapping

    defaults = {"expr": "Expression", "read": "Kana Reading", "pos": "Part of Speech"}
    if all(v in field_names for v in defaults.values()):
        save_settings(model_id, defaults)
        if is_remove:
            return {"pos": defaults["pos"]}
        return defaults

    dialog = FieldMapDialog(field_names, parent_window, is_remove=is_remove)
    if dialog.exec() == 0:
        return None

    mappings = dialog.get_mappings()

    if not is_remove:
        save_settings(model_id, mappings)

    return mappings