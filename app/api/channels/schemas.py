from pydantic import BaseModel

class ChannelSchema(BaseModel):
    name: str
    description: str = None

class ChannelCreate(ChannelSchema):
    pass

class ChannelUpdate(ChannelSchema):
    pass


class ChannelMain(ChannelSchema):
    id: int

    class Config:
        from_attributes = True
