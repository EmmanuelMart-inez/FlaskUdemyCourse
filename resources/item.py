from flask_restful import Resource, reqparse
from flask_jwt import jwt_required 
from models.item import ItemModel

##NOTE: Class should be separate by 2 lines and methods by 1 line in python "CONVENTION"

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
 
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exists".format(name)}, 400 # Bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        #item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except: 
            return {'message': 'An error occurred inserting item.'}, 500 #Internal Server Error

        return item.json(), 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item == None:
            #item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()
    

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': [list(map(lambda x: x.json(), ItemModel.query.all()))]}
        #LIST COMPREHESION