import boto3
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
api = Api(app)
dynamodb = boto3.resource('dynamodb')

# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('Users')

table_creation = table.creation_date_time
print(table.creation_date_time)

pokemons = {}
pokemon_put_args = reqparse.RequestParser()
pokemon_put_args.add_argument("name", type=str, help="Please include the name of the pokemon", required=True)

def abort_if_pokemon_doesnt_exist(pokemon_id):
    if pokemon_id not in pokemons:
        abort(Response("The Pokemon ID entered is invalid",404))
class Pokemon(Resource):
    def get(self,pokemon_id):
        #abort_if_pokemon_doesnt_exist(pokemon_id)
        dt_str = table_creation.strftime("%Y-%m-%d %H:%M:%S")
        json_data = json.dumps(dt_str)  
        return json_data
    #pokemons[pokemon_id]
    def put(self, pokemon_id):
        abort_if_pokemon_doesnt_exist(pokemon_id)
        args = pokemon_put_args.parse_args()
        pokemons[pokemon_id] = {"name": args["name"]}
        return pokemons[pokemon_id], 201
    def post(self,pokemon_id):
        args = pokemon_put_args.parse_args()
        pokemons[pokemon_id] = {"name": args["name"]}
        return pokemons[pokemon_id], 201
    def delete(self, pokemon_id):
        abort_if_pokemon_doesnt_exist(pokemon_id)
        del pokemons[pokemon_id]
        return '', 204
api.add_resource(Pokemon, "/helloworld/<int:pokemon_id>")

# Get the service resource.


# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes



if __name__ =="__main__":
    app.run(debug=True)

#Changed file name to be lowercase