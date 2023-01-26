from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Message(BaseModel):
    """
    Attributes:
        uid (UUID):
        created_by (str):
        created_at (str):
        msg:
    """
    uid: UUID
    created_by: str  # class名
    created_at: datetime
    # = datetime.now() これは使えません．BaseModelは毎度生成されるわけではありません．
    msg: str  # 変更予定
