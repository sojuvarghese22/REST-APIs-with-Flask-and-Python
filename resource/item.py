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
        
    
    #@jwt_required()  #for not accessing directly if user is authenticated then only he will be authorize for this service
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE from items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

  
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_item(name)
        updated_item = {'name':name,'price': data['price']}

        if item is None:
            obj = ItemModel(name,data['price'])
            try:
                obj.insert()
            except:
                return {"message":"an error occured inserting an item"}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message":"an error occured updating the item"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price':row[1]})
        connection.close()

        return {'items':items}
