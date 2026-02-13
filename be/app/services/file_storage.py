from pathlib import Path

from app.config import DATA_DIR, STATIC_DIR


def get_user_data_dir(user_id: int) -> Path:
    return Path(DATA_DIR) / str(user_id)


def get_raw_dir(user_id: int, lang: str) -> Path:
    return get_user_data_dir(user_id) / "raw" / lang


def get_splitted_dir(user_id: int, lang: str) -> Path:
    return get_user_data_dir(user_id) / "splitted" / lang


def get_proxy_dir(user_id: int, lang: str) -> Path:
    return get_user_data_dir(user_id) / "proxy" / lang


def get_db_dir(user_id: int, lang_from: str, lang_to: str) -> Path:
    return get_user_data_dir(user_id) / "db" / lang_from / lang_to


def get_alignment_db_path(
    user_id: int, lang_from: str, lang_to: str, guid: str
) -> Path:
    return get_db_dir(user_id, lang_from, lang_to) / f"{guid}.db"


def get_vis_img_path(user_id: int, guid: str) -> Path:
    return Path(STATIC_DIR) / "img" / str(user_id) / f"{guid}.best.png"


def get_download_dir(user_id: int) -> Path:
    return get_user_data_dir(user_id) / "download"


def ensure_user_dirs(user_id: int, lang: str) -> None:
    get_raw_dir(user_id, lang).mkdir(parents=True, exist_ok=True)
    get_splitted_dir(user_id, lang).mkdir(parents=True, exist_ok=True)
    get_proxy_dir(user_id, lang).mkdir(parents=True, exist_ok=True)
    img_dir = Path(STATIC_DIR) / "img" / str(user_id)
    img_dir.mkdir(parents=True, exist_ok=True)
