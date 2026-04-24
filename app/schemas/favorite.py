from app.schemas.common import APIModel


class FavoriteData(APIModel):
    activity_id: int
    is_favorite: bool
