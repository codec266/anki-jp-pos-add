import os
from PyQt6.QtWidgets import QMenu
from aqt import mw, gui_hooks
from aqt.utils import showText, tooltip
from .service import process_note
from .bulk import bulk_add, bulk_remove, find_empty_pos, reset_mappings
from .mapping import resolve_mappings

def editor_button(buttons, editor):
    """ add japanese part of speech button to editor (品詞追加)"""
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    pos_btn = editor.addButton(
        icon_path,
        "jp pos",
        lambda ed: ed.saveNow(lambda: add_pos(ed)),
        tip="add japanese part of speech"
    )
    buttons.append(pos_btn)


def add_pos(editor):
    note = editor.note
    if not note:
        return

    mappings = resolve_mappings(note.model(), editor.widget)
    if not mappings:
        return

    success, msg = process_note(note, mappings["expr"], mappings["read"], mappings["pos"])

    if success:
        if note.id != 0:
            note.flush()

        editor.loadNote()

    if msg:
        tooltip(msg)


def about_dialog():
    showText(
        "Japanese Part of Speech",
        title='About',
    )

# add menu items
pos_menu = QMenu('Part of Speech', mw)
pos_menu_add = pos_menu.addAction('bulk add')
pos_menu_remove = pos_menu.addAction('bulk remove')
pos_menu_find = pos_menu.addAction('find empty')
pos_menu_reset = pos_menu.addAction('reset mappings')
pos_menu_about = pos_menu.addAction('about')

# triggers
pos_menu_add.triggered.connect(bulk_add)
pos_menu_remove.triggered.connect(bulk_remove)
pos_menu_find.triggered.connect(find_empty_pos)
pos_menu_reset.triggered.connect(reset_mappings)
pos_menu_about.triggered.connect(about_dialog)

# add to tools menu
mw.form.menuTools.addMenu(pos_menu)

# add editor button
gui_hooks.editor_did_init_buttons.append(editor_button)