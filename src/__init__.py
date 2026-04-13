import os
from PyQt6.QtWidgets import QMenu
from aqt import mw, gui_hooks
from aqt.utils import showText


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
    pass

def about_dialog():
    showText(
        "Japanese Part of Speech",
        title='About',
    )

def bulk_add():
    pass

# add menu items
pos_menu = QMenu('Part of Speech', mw)
pos_menu_add = pos_menu.addAction('bulk add')
pos_menu_about = pos_menu.addAction('about')

# triggers
pos_menu_add.triggered.connect(bulk_add)
pos_menu_about.triggered.connect(about_dialog)

# add to tools menu
mw.form.menuTools.addMenu(pos_menu)

# add editor button
gui_hooks.editor_did_init_buttons.append(editor_button)
