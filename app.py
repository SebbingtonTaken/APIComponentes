import boto3
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort
import json


app = Flask(__name__)
api = Api(app)
dynamodb = boto3.resource('dynamodb')

# on the table resource are accessed or its load() method is called.
pokedex_table = dynamodb.Table('Pokedex')
creation_date = pokedex_table.creation_date_time


pokemons = {}
pokemon_put_args = reqparse.RequestParser()
pokemon_put_args.add_argument("pokemonId", type=str, help="Please include the Pokemon ID", required=True)
pokemon_put_args.add_argument("pokedexEntry", type=str, help="Pokedex entry description", required=True)
pokemon_put_args.add_argument("baseHp", type=int, help="Base HP of the Pokemon", required=True)
pokemon_put_args.add_argument("baseAtk", type=int, help="Base Attack of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpAtk", type=int, help="Base Special Attack of the Pokemon", required=True)
pokemon_put_args.add_argument("baseDef", type=int, help="Base Defense of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpDef", type=int, help="Base Special Defense of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpeed", type=int, help="Base Speed of the Pokemon", required=True)


def abort_if_pokemon_doesnt_exist(pokemon_id):
    if pokemon_id not in pokemons:
        abort(Response("The Pokemon ID entered is invalid",404))
class Pokemon(Resource):
    def get(self):
        #abort_if_pokemon_doesnt_exist(pokemon_id)
        try:
            response = pokedex_table.get_item(
            Key={
                'UserId': 'schinchillaa@ucenfotec.ac.cr',
                'PokemonId': 'Bulbasaur'
            }
            )
            item = response['Item']
            return {item}, 200
            print(item)
        except Exception as e:
            print("An error occurred:", e)
            return {"error": str(e)}, 500
        
        dt_str = creation_date.strftime("%Y-%m-%d %H:%M:%S")
        json_data = json.dumps(dt_str)  
        return json_data
    #pokemons[pokemon_id]
    def put(self, pokemon_id):
        abort_if_pokemon_doesnt_exist(pokemon_id)
        args = pokemon_put_args.parse_args()
        pokemons[pokemon_id] = {"name": args["name"]}
        return pokemons[pokemon_id], 201
    def post(self):
        try:
            args = pokemon_put_args.parse_args()
            print("Parsed Arguments:", args)  # Debug print
            pokedex_table.put_item(
                Item={
                    'UserId': 'schinchillaa@ucenfotec.ac.cr',
                    'PokemonId': args["pokemonId"],
                    'PokedexEntry': args["pokedexEntry"],
                    'BaseHP': args["baseHp"],
                    'BaseAtk': args["baseAtk"],
                    'BaseSpAtk': args["baseSpAtk"],
                    'BaseDef': args["baseDef"],
                    'BaseSpDef': args["baseSpDef"],
                    'BaseSpeed': args["baseSpeed"],
                }
            )
            return {"message": "Pokemon added successfully"}, 201
        except Exception as e:
            print("An error occurred:", e)
            return {"error": str(e)}, 500
       
    def delete(self, pokemon_id):
        abort_if_pokemon_doesnt_exist(pokemon_id)
        del pokemons[pokemon_id]
        return '', 204
api.add_resource(Pokemon, "/Pokedex/")

# Get the service resource.


# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes



if __name__ =="__main__":
    app.run(debug=True)

#Changed file name to be lowercase