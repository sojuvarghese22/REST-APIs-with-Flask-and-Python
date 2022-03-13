from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity
from resource.user import UserRegister
from resource.item import Item,ItemList
app = Flask(__name__) #application
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'jose' #secret key
api = Api(app) #can send request of get, push, put, delete  

jwt = JWT(app, authenticate, identity)  #gives endpoint (/auth)


api.add_resource(Item, '/item/<string:name>')  #endpoint
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True) 

