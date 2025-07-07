from pydantic import BaseModel

class FriendSchema(BaseModel):
    friend_name: str

class AddFriend(FriendSchema):
    pass

class DeleteFriend(FriendSchema):
    pass

class FriendMain(FriendSchema):
    id: int

    class Config:
        from_attributes = True