import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


#class for Item Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        result = ItemModel.find_item(name)
        if result:
            return result.json()
        return {'message': 'item not found'}, 404
     
           
        
    def post(self, name):
        result = ItemModel.find_item(name)
        if result is None:
            data = Item.parser.parse_args()
            item = ItemModel(name,data['price'])
            item.insert()
            

            return item.json(), 200
            
        return {'message': 'item already exists'}
        
    
    @jwt_required()  #for not accessing directly if user is authenticated then only he will be authorize for this service
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

  
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}
