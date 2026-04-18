from .db import get_pos
from anki.utils import strip_html


def process_note(note, expr_field="Expression", read_field="Kana Reading", pos_field="Part of Speech"):
    """Processes a single note using specified field names. Returns (success_bool, status_message)."""

    if pos_field not in note:
        return False, f"No '{pos_field}' field found on this note."

    if expr_field not in note:
        return False, f"No '{expr_field}' field found on this note."

    word = strip_html(note[expr_field]).strip()
    if not word:
        return False, f"The '{expr_field}' field is empty."

    # Reading is optional, only extract if it was mapped/exists
    reading = ""
    if read_field and read_field in note:
        reading = strip_html(note[read_field]).strip()

    # get pos from database
    pos_string, match_type_or_err = get_pos(word, reading)

    if pos_string:
        note[pos_field] = pos_string
        return True, f"[{match_type_or_err}] {pos_string}"

    return False, match_type_or_err