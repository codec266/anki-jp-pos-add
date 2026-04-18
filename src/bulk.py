from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QListWidget, QDialogButtonBox, QVBoxLayout
from aqt import mw, dialogs
from aqt.utils import tooltip
from .config import delete_settings, get_all_settings
from .service import process_note
from .mapping import resolve_mappings


def choose_item_dialog(msg, choices, startrow=0):
    """dialog to select an item from a list."""
    dialog = QDialog(mw.app.activeWindow())
    dialog.setWindowTitle("Selection")
    dialog.setWindowModality(Qt.WindowModality.WindowModal)
    layout = QVBoxLayout(dialog)

    label = QLabel(msg)
    layout.addWidget(label)

    list_widget = QListWidget()
    list_widget.addItems(choices)
    list_widget.setCurrentRow(startrow)
    layout.addWidget(list_widget)

    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)

    if dialog.exec() == 0:
        return None
    return list_widget.currentRow()


def get_deck_and_model():
    """Prompts user to pick a deck, then a note type used in that deck."""
    decks = mw.col.decks.all_names()
    if not decks:
        return None, None

    d_idx = choose_item_dialog("Select a Deck", decks)
    if d_idx is None:
        return None, None
    deck_name = decks[d_idx]
    deck_id = mw.col.decks.id(deck_name)

    note_type_ids = mw.col.db.list(
        "SELECT DISTINCT mid FROM notes JOIN cards ON cards.nid = notes.id WHERE cards.did = ?", deck_id
    )

    if not note_type_ids:
        tooltip("No notes found in this deck.")
        return None, None

    models = [mw.col.models.get(mid) for mid in note_type_ids]
    model_names = [m['name'] for m in models]

    if len(model_names) == 1:
        m_idx = 0
    else:
        m_idx = choose_item_dialog("Select a Note Type", model_names)
        if m_idx is None:
            return None, None

    model_name = model_names[m_idx]
    return deck_name, model_name


def bulk_add():
    deck_name, model_name = get_deck_and_model()
    if not deck_name or not model_name:
        return

    model = mw.col.models.by_name(model_name)

    mappings = resolve_mappings(model, mw.app.activeWindow(), is_remove=False)
    if not mappings:
        return

    note_ids = mw.col.find_notes(f'"deck:{deck_name}" "note:{model_name}"')
    if not note_ids:
        tooltip("No matching notes found.")
        return

    mw.checkpoint("Bulk Add Part of Speech")
    mw.progress.start(label="Adding Part of Speech...", max=len(note_ids))
    success_count = 0

    for i, nid in enumerate(note_ids):
        note = mw.col.get_note(nid)
        success, _ = process_note(note, mappings["expr"], mappings["read"], mappings["pos"])

        if success:
            note.flush()
            success_count += 1

        if i % 50 == 0:
            mw.progress.update(value=i)

    mw.progress.finish()
    mw.reset()
    tooltip(f"Successfully added Part of Speech to {success_count} notes.")


def bulk_remove():
    deck_name, model_name = get_deck_and_model()
    if not deck_name or not model_name:
        return

    model = mw.col.models.by_name(model_name)

    mappings = resolve_mappings(model, mw.app.activeWindow(), is_remove=True)
    if not mappings:
        return

    pos_field = mappings["pos"]

    note_ids = mw.col.find_notes(f'"deck:{deck_name}" "note:{model_name}"')
    if not note_ids:
        tooltip("No matching notes found.")
        return

    mw.checkpoint("Bulk Remove Part of Speech")
    mw.progress.start(label="Removing Part of Speech...", max=len(note_ids))

    count = 0

    for i, nid in enumerate(note_ids):
        note = mw.col.get_note(nid)
        if pos_field in note and note[pos_field]:
            note[pos_field] = ""
            note.flush()
            count += 1

        if i % 50 == 0:
            mw.progress.update(value=i)

    mw.progress.finish()
    mw.reset()
    tooltip(f"Cleared '{pos_field}' from {count} notes.")

def reset_mappings():
    settings = get_all_settings()
    if not settings:
        tooltip("No custom mappings have been saved yet.")
        return

    configured_names = []
    configured_ids = []

    for mid_str in settings.keys():
        try:
            mid = int(mid_str)
            model = mw.col.models.get(mid)
            if model:
                configured_names.append(model['name'])
                configured_ids.append(mid)
        except ValueError:
            continue

    if not configured_names:
        tooltip("No valid mappings found to reset.")
        return

    idx = choose_item_dialog("select note type to reset:", configured_names)
    if idx is None:
        return

    target_mid = configured_ids[idx]
    target_name = configured_names[idx]

    delete_settings(target_mid)
    tooltip(f"Reset mappings for '{target_name}'.")

def find_empty_pos():
    deck_name, model_name = get_deck_and_model()
    if not deck_name or not model_name:
        return

    model = mw.col.models.by_name(model_name)

    mappings = resolve_mappings(model, mw.app.activeWindow(), is_remove=True)
    if not mappings:
        return

    pos_field = mappings["pos"]

    query = f'"deck:{deck_name}" "note:{model_name}" "{pos_field}:"'

    browser = dialogs.open("Browser", mw)

    if hasattr(browser, "search_for"):
        browser.search_for(query)
    else:
        browser.form.searchEdit.lineEdit().setText(query)
        browser.onSearchActivated()

