import json
import os

def get_config_path():
    addon_dir = os.path.dirname(__file__)
    user_files = os.path.join(addon_dir, "user_files")
    os.makedirs(user_files, exist_ok=True)
    return os.path.join(user_files, "settings.json")

def get_all_settings():
    """returns the entire settings dictionary, or an empty dict if none exist."""
    config_file = get_config_path()
    if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
        return {}

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def load_settings(model_id: int):
    config_file = get_config_path()

    if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    return data.get(str(model_id))

def save_settings(model_id: int, mappings: dict):
    config_file = get_config_path()
    data = {}

    if os.path.exists(config_file) and os.path.getsize(config_file) > 0:
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass

    data[str(model_id)] = mappings

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def delete_settings(model_id: int):
    config_file = get_config_path()
    if not os.path.exists(config_file):
        return

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return

    if str(model_id) in data:
        del data[str(model_id)]

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)