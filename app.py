import boto3
from flask import Flask, Response
from decimal import Decimal
from flask_restful import Api, Resource, reqparse, abort
import json


app = Flask(__name__)
api = Api(app)
dynamodb = boto3.resource('dynamodb')


pokedex_table = dynamodb.Table('Pokedex')

pokemon_put_args = reqparse.RequestParser()
pokemon_put_args.add_argument("userId", type=str, help="Please include the User ID", required=True)
pokemon_put_args.add_argument("pokemonId", type=str, help="Please include the Pokemon ID", required=True)
pokemon_put_args.add_argument("pokedexEntry", type=str, help="Pokedex entry description", required=True)
pokemon_put_args.add_argument("baseHp", type=int, help="Base HP of the Pokemon", required=True)
pokemon_put_args.add_argument("baseAtk", type=int, help="Base Attack of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpAtk", type=int, help="Base Special Attack of the Pokemon", required=True)
pokemon_put_args.add_argument("baseDef", type=int, help="Base Defense of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpDef", type=int, help="Base Special Defense of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpeed", type=int, help="Base Speed of the Pokemon", required=True)


pokemon_get_args = reqparse.RequestParser()
pokemon_get_args.add_argument("userId", type=str, help="Please include the User ID", required=True)
pokemon_get_args.add_argument("pokemonId", type=str, help="Please include the Pokemon ID", required=True)


#function to make Dynamo db datatype compatible with Python        
def decimal_to_float(obj):
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

class Pokemon(Resource):
    def get(self):
        args = pokemon_get_args.parse_args()
        try:
            response = pokedex_table.get_item(
                Key={
                    'UserId': args["userId"],
                    'PokemonId': args["pokemonId"],
                }
            )
            item = response.get('Item')
            
            if not item:
                return {"message": "Pokemon not found for this User ID"}, 404

            # Convert Decimals to float for JSON serialization
            item = decimal_to_float(item)
            return item, 200
        except Exception as e:
            print("A server error occurred:", e)
            return {"error": str(e)}, 500
    def put(self):
        try:
            args = pokemon_put_args.parse_args()
            print("Parsed Arguments:", args)  # Debug print
            pokedex_table.put_item(
                Item={
                    'UserId': args["userId"],
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
            return {"message": "Pokemon updated successfully"}, 201
        except Exception as e:
            print("A server error occurred:", e)
            return {"error": str(e)}, 500
    def post(self):
        try:
            args = pokemon_put_args.parse_args()
            print("Parsed Arguments:", args)  # Debug print
            pokedex_table.put_item(
                Item={
                    'UserId': args["userId"],
                    'PokemonId': args["pokemonId"],
                    'PokedexEntry': args["pokedexEntry"],
                    'BaseHP': args["baseHp"],
                    'BaseAtk': args["baseAtk"],
                    'BaseSpAtk': args["baseSpAtk"],
                    'BaseDef': args["baseDef"],
                    'BaseSpDef': args["baseSpDef"],
                    'BaseSpeed': args["baseSpeed"],
                },
                ConditionExpression="attribute_not_exists(UserId) AND attribute_not_exists(PokemonId)" #checks if pokemon already exists for that user
            )
            return {"message": "Pokemon added successfully"}, 201
        except Exception as e:
            print("A server error occurred:", e)
            return {"error": str(e)}, 500
       
    def delete(self, pokemon_id):
        abort_if_pokemon_doesnt_exist(pokemon_id)
        del pokemons[pokemon_id]
        return '', 204

api.add_resource(Pokemon, "/pokedex")




if __name__ =="__main__":
    app.run(debug=True)

