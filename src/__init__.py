import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu, QMessageBox
from aqt import mw, gui_hooks
from aqt.utils import showText, tooltip, showInfo
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
    addon_dir = os.path.dirname(__file__)
    img_path = os.path.join(addon_dir, "icon.png").replace("\\", "/")

    about_text = f"""
    <div style="font-family: sans-serif;">
        <table style="border-spacing: 0;">
            <tr>
                <td style="padding-right: 15px;" valign="top">
                    <img src="file:///{img_path}" width="80" height="80">
                </td>
                <td valign="top">
                    <h3 style="margin-top: 0;">Japanese Part of Speech</h3>
                    <p style="margin-bottom: 0;">An offline Anki add-on that fetches and assigns Japanese parts of speech to your vocabulary notes.</p>
                </td>
            </tr>
        </table>

        <p>
            <b>Add-on by:</b> codec266<br>
            <b>Version:</b> 1.0.0<br>
            <b>License:</b> MIT
        </p>

        <p>
            <b>Links:</b><br>
            <a href="https://github.com/codec266/anki-jp-pos-add">GitHub</a> | 
            <a href="https://ko-fi.com/codec266">Support on Ko-fi</a>
        </p>

        <hr>

        <p style="font-size: 11px;">
            Dictionary data is based on <a href="https://www.edrdg.org/jmdict/j_jmdict.html">JMdict</a>, property of the 
            Electronic Dictionary Research and Development Group, and is used in 
            conformance with the Group's license.
        </p>
    </div>
    """

    msg_box = QMessageBox(mw)
    msg_box.setWindowTitle("About")
    msg_box.setTextFormat(Qt.TextFormat.RichText)
    msg_box.setText(about_text)
    msg_box.setIcon(QMessageBox.Icon.NoIcon)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()

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