import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jmdict.db"


def get_pos(word, reading=None):
    """returns (pos_string, match_type) or (None, error_msg)"""
    if not DB_PATH.exists():
        return None, f"Database not found at: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    result = None
    match_type = ""

    # attempt exact match with both word and reading
    if reading:
        cursor.execute("SELECT formatted_pos FROM entries WHERE word = ? AND reading = ?", (word, reading))
        result = cursor.fetchone()
        if result:
            match_type = "Exact Match"

    # fallback to word-only query if no reading match or reading is empty
    if not result:
        cursor.execute("SELECT formatted_pos FROM entries WHERE word = ?", (word,))
        result = cursor.fetchone()
        if result:
            match_type = "Fallback Match"

    conn.close()

    if result:
        return result[0], match_type

    return None, f"No Part of Speech found for '{word}'."