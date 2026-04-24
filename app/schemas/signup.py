from datetime import datetime

from app.schemas.common import APIModel
from app.schemas.user import UserSummary


class SignupData(APIModel):
    id: int
    activity_id: int
    user_id: int
    status: str
    remark: str
    created_at: datetime
    user: UserSummary
