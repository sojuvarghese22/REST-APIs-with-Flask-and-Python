from hmac import compare_digest
from models.user import UserModel

#method for authentication
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user
#method for extracting userid

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
 

