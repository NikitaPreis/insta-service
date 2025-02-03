from pydantic import BaseModel


class InstagramUserProfileSchema(BaseModel):
    id: int
    username: str | None = None
    name: str | None = None
    username: str | None = None
    profile_pic: str | None = None
    follower_count: int | None = None
    is_user_follow_business: bool | None = None
    is_business_follow_user: bool | None = None
