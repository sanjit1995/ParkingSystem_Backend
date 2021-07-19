def generate_token(user_id: str, password: str):
    return user_id + "_" + password

def verify_id_in_token(token: str, user_id:str):
    if user_id == token.split("_")[0]:
        return True
    else:
        return False

def get_user_id_from_token(token: str):
    return token.split("_")[0]