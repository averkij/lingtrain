from datetime import datetime

from pydantic import BaseModel


class AlignmentOut(BaseModel):
    id: int
    guid: str
    name: str
    lang_from: str
    lang_to: str
    state: int
    curr_batches: int
    total_batches: int
    is_deleted: bool
    is_uploaded: bool
    proxy_from_loaded: bool
    proxy_to_loaded: bool
    document_from_id: int
    document_to_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class AlignmentCreate(BaseModel):
    document_from_guid: str
    document_to_guid: str
    name: str


class AlignStart(BaseModel):
    align_all: bool = False
    batch_ids: list[int] = []
    batch_shift: int = 0
    window: int = 50
    use_proxy_from: bool = False
    use_proxy_to: bool = False


class AlignNext(BaseModel):
    amount: int = 1
    batch_shift: int = 0
    window: int = 50
    use_proxy_from: bool = False
    use_proxy_to: bool = False


class ResolveRequest(BaseModel):
    batch_ids: list[int] = []
    use_proxy_from: bool = False
    use_proxy_to: bool = False
    handle_start: bool = False
    handle_finish: bool = False


class EditRequest(BaseModel):
    index_id: int
    text: str = ""
    text_type: str = "to"
    operation: str
    target: str = ""
    candidate_line_id: int = -1
    candidate_text: str = ""
    batch_id: int
    batch_index_id: int
    line_id_from: int = -1
    line_id_to: int = -1


class SplitRequest(BaseModel):
    direction: str
    line_id: int
    part1: str
    part2: str


class MarkAdd(BaseModel):
    type: str
    val_from: str
    val_to: str
    par_id_from: int
    par_id_to: int


class MarkEdit(BaseModel):
    mark_id: int
    operation: str
    direction: str = ""
    type: str = ""
    value: str = ""
    par_id: int = -1


class ExportRequest(BaseModel):
    format: str
    side: str = "from"
    paragraphs: bool = False
    direction: str = "to"
    left_lang: str = "from"


class BookRequest(BaseModel):
    par_direction: str = "to"
    left_lang: str = "from"
    style: str = "none"


class ProcessingPage(BaseModel):
    count: int = 50
    page: int = 1
