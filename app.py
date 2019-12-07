from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister   
from resources.item import Item, ItemList
from resources.store import Store, StoreList

#We dont need to call JSONIFY in flask restful cause it do by itself
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth endopoint

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

#When we execute an app python named it with the name __main__ so, if we import this file from another, it won't run this main part.
if __name__ == '__main__': 
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)