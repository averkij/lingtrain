"""Export service - migrated from a-studio/backend/main.py download/create endpoints"""

import datetime
import logging

from app.models.alignment import Alignment
from app.services.file_storage import (
    get_alignment_db_path,
    get_download_dir,
)

logger = logging.getLogger(__name__)

TYPE_FROM = "from"
TYPE_TO = "to"
FORMAT_PLAIN = "txt"
FORMAT_TMX = "tmx"
FORMAT_XML = "xml"
FORMAT_JSON = "json"
FORMAT_DB = "lt"


def download_processing(
    user_id: int,
    alignment: Alignment,
    file_format: str,
    side: str = "from",
    paragraphs: bool = False,
    direction: str = "to",
    left_lang: str = "from",
) -> str:
    from lingtrain_aligner import saver, reader

    db_path = str(
        get_alignment_db_path(
            user_id, alignment.lang_from, alignment.lang_to, alignment.guid
        )
    )

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    download_dir = get_download_dir(user_id)
    download_dir.mkdir(parents=True, exist_ok=True)
    download_file = str(
        download_dir
        / f"{alignment.guid}_{alignment.lang_from}_{side}_{timestamp}.{file_format}"
    )

    if not side:
        side = "from"

    if paragraphs:
        pars, _, _, _ = reader.get_paragraphs(db_path, direction)
        saver.save_paragraphs(pars, side, download_file)
        return download_file

    if left_lang == "from":
        lang_order = [TYPE_FROM, TYPE_TO]
    else:
        lang_order = [TYPE_TO, TYPE_FROM]

    if file_format == FORMAT_TMX:
        saver.save_tmx(db_path, download_file, alignment.lang_from, alignment.lang_to)
    elif file_format == FORMAT_XML:
        saver.save_xml(db_path, download_file, lang_order, direction)
    elif file_format == FORMAT_JSON:
        saver.save_json(db_path, download_file, lang_order, direction)
    elif file_format == FORMAT_PLAIN:
        saver.save_plain_text(db_path, download_file, side)
    elif file_format == FORMAT_DB:
        download_file = db_path

    return download_file


def get_book_preview(
    user_id: int,
    alignment: Alignment,
    par_direction: str = "to",
    left_lang: str = "from",
    style: str = "none",
) -> str:
    from lingtrain_aligner import reader

    db_path = str(
        get_alignment_db_path(
            user_id, alignment.lang_from, alignment.lang_to, alignment.guid
        )
    )

    if reader.is_empty_cells(db_path):
        return ""

    par_amount = 5
    paragraphs, delimeters, metas, _ = reader.get_paragraphs(
        db_path=db_path, direction=par_direction, par_amount=par_amount
    )

    if left_lang == "from":
        lang_order = [TYPE_FROM, TYPE_TO]
    else:
        lang_order = [TYPE_TO, TYPE_FROM]

    return reader.create_polybook_preview(
        lang_ordered=lang_order,
        paragraphs=paragraphs,
        delimeters=delimeters,
        metas=metas,
        template=style,
        styles=[],
        par_amount=par_amount,
    )


def download_book(
    user_id: int,
    alignment: Alignment,
    par_direction: str = "to",
    left_lang: str = "from",
    style: str = "none",
) -> str:
    from lingtrain_aligner import reader

    db_path = str(
        get_alignment_db_path(
            user_id, alignment.lang_from, alignment.lang_to, alignment.guid
        )
    )

    if reader.is_empty_cells(db_path):
        return ""

    paragraphs, delimeters, metas, sent_counter = reader.get_paragraphs(
        db_path, par_direction
    )

    if left_lang == "from":
        lang_order = [TYPE_FROM, TYPE_TO]
    else:
        lang_order = [TYPE_TO, TYPE_FROM]

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    download_dir = get_download_dir(user_id)
    download_dir.mkdir(parents=True, exist_ok=True)
    download_file = str(
        download_dir
        / f"{alignment.guid}_{alignment.lang_from}_{alignment.lang_to}_{timestamp}.html"
    )

    reader.create_book(
        lang_ordered=lang_order,
        paragraphs=paragraphs,
        delimeters=delimeters,
        metas=metas,
        sent_counter=sent_counter,
        output_path=download_file,
        template=style,
        styles=[],
    )

    return download_file
