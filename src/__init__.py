import os
import sqlite3
from pathlib import Path
from PyQt6.QtWidgets import QMenu
from anki.utils import strip_html
from aqt import mw, gui_hooks
from aqt.utils import showText, tooltip


DB_PATH = Path(__file__).parent / "jmdict.db"

def editor_button(buttons, editor):
    """ add japanese part of speech button to editor (品詞追加)"""
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    pos_btn = editor.addButton(
        icon_path,
        "jp pos",
        add_pos,
        tip="add japanese part of speech"
    )
    buttons.append(pos_btn)

def add_pos(editor):
    note = editor.note
    if not note:
        return

    source_field = None
    if "Expressions" in note:
        source_field = "Expressions"
    elif "Expression" in note:
        source_field = "Expression"

    if "Part of Speech" not in note:
        tooltip("No 'Part of Speech' field found on this note type.")
        return

    if not source_field:
        tooltip("No 'Expression' field found on this note type.")
        return

    raw_word = note[source_field]
    clean_word = strip_html(raw_word).strip()

    if not clean_word:
        tooltip("The Expression field is empty.")
        return

    # Identify the reading field
    reading_field = None
    for rf in ["Kana Reading", "Kana", "Reading"]:
        if rf in note:
            reading_field = rf
            break

    clean_reading = None
    if reading_field:
        clean_reading = strip_html(note[reading_field]).strip()

    if not DB_PATH.exists():
        tooltip(f"Database not found at: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    result = None
    match_type = ""

    # attempt exact match with both word and reading
    if clean_reading:
        cursor.execute("SELECT formatted_pos FROM entries WHERE word = ? AND reading = ?", (clean_word, clean_reading))
        result = cursor.fetchone()
        if result:
            match_type = "Exact Match"

    # fallback to word-only query if no reading match or reading is empty
    if not result:
        cursor.execute("SELECT formatted_pos FROM entries WHERE word = ?", (clean_word,))
        result = cursor.fetchone()
        if result:
            match_type = "Fallback Match"

    conn.close()

    if not result:
        tooltip(f"No Part of Speech found for '{clean_word}'.")
        return

    pos_string = result[0]

    # debug
    tooltip(f"[{match_type}] {pos_string}")

    note["Part of Speech"] = pos_string
    editor.loadNote()

def about_dialog():
    showText(
        "Japanese Part of Speech",
        title='About',
    )

def bulk_add():
    pass

def bulk_remove():
    pass

# add menu items
pos_menu = QMenu('Part of Speech', mw)
pos_menu_add = pos_menu.addAction('bulk add')
pos_menu_remove = pos_menu.addAction('bulk remove')
pos_menu_about = pos_menu.addAction('about')

# triggers
pos_menu_add.triggered.connect(bulk_add)
pos_menu_remove.triggered.connect(bulk_remove)
pos_menu_about.triggered.connect(about_dialog)

# add to tools menu
mw.form.menuTools.addMenu(pos_menu)

# add editor button
gui_hooks.editor_did_init_buttons.append(editor_button)
