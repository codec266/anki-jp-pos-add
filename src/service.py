from .utils import FieldUtil
from .db import get_pos


def process_note(note):
    """Processes a single note. Returns (success_bool, status_message)."""
    if "Part of Speech" not in note:
        return False, "No 'Part of Speech' field found on this note type."

    # verify an expression field exists on this note
    has_source = any(f in note for f in FieldUtil.EXPRESSION_FIELDS)
    if not has_source:
        return False, "No 'Expression' field found on this note type."

    word = FieldUtil.get_word(note)
    if not word:
        return False, "The Expression field is empty."

    reading = FieldUtil.get_reading(note)

    # get pos from database
    pos_string, match_type_or_err = get_pos(word, reading)

    if pos_string:
        note["Part of Speech"] = pos_string
        return True, f"[{match_type_or_err}] {pos_string}"

    return False, match_type_or_err

