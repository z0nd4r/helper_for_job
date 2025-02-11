from users.schemas import ClientCreate, ClientUpdate, ClientMain

def create_user(user_in: ClientCreate):
    user = user_in.model_dump()
    return {
        
    }

def read_user(user_in: str):
    pass