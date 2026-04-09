from PyQt6.QtWidgets import QMenu
from aqt import mw
from aqt.utils import showText


def about_dialog() -> None:
    showText(
        "Japanese Part of Speech",
        title='About',
    )

# add menu items
pos_menu = QMenu('Part of Speech', mw)
pos_menu_about = pos_menu.addAction('About')

# triggers
pos_menu_about.triggered.connect(about_dialog)

# add to tools menu
mw.form.menuTools.addMenu(pos_menu)

