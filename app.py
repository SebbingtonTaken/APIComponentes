import boto3
from flask import Flask, Response, jsonify
from decimal import Decimal
from flask_restful import Api, Resource, reqparse, abort
import google.generativeai as genai
import json

API_KEY = open("C:\\Users\\basti\\Desktop\\Cenfotec\\Disenho de Componentes\\Proyecto\\APIComponentes\\API-key.txt", "r").read()


genai.configure(api_key=API_KEY)

app = Flask(__name__)
api = Api(app)
dynamodb = boto3.resource('dynamodb')


pokedex_table = dynamodb.Table('Pokedex')

pokemon_put_args = reqparse.RequestParser()
pokemon_put_args.add_argument("userId", type=str, help="Please include the User ID", required=True)
pokemon_put_args.add_argument("pokemonId", type=str, help="Please include the Pokemon ID", required=True)
pokemon_put_args.add_argument("pokedexEntry", type=str, help="Pokedex entry description")
pokemon_put_args.add_argument("baseHp", type=int, help="Base HP of the Pokemon", required=True)
pokemon_put_args.add_argument("baseAtk", type=int, help="Base Attack of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpAtk", type=int, help="Base Special Attack of the Pokemon", required=True)
pokemon_put_args.add_argument("baseDef", type=int, help="Base Defense of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpDef", type=int, help="Base Special Defense of the Pokemon", required=True)
pokemon_put_args.add_argument("baseSpeed", type=int, help="Base Speed of the Pokemon", required=True)
pokemon_put_args.add_argument("type", type=str, help="Type of the Pokemon", required=True)


pokemon_get_args = reqparse.RequestParser()
pokemon_get_args.add_argument("userId", type=str, help="Please include the User ID", required=True)
pokemon_get_args.add_argument("pokemonId", type=str, help="Please include the Pokemon ID")


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
        if args["pokemonId"]:
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
                return {'data': item}, 200
            except Exception as e:
                print("A server error occurred:", e)
                return {"error": str(e)}, 500
        else:
            try:
                response = pokedex_table.query(
                    KeyConditionExpression=boto3.dynamodb.conditions.Key('UserId').eq(args["userId"])
                )
                items = response.get('Items', [])
                items = [decimal_to_float(item) for item in items]
                return {'data': items}, 200
            except Exception as e:
                return {'error': str(e)}, 500

    def put(self):
        try:
            args = pokemon_put_args.parse_args()
            print("Parsed Arguments:", args)  # Debug print
            pokedex_table.put_item(
                Item={
                    'UserId': args["userId"],
                    'PokemonId': args["pokemonId"],
                    'PokedexEntry': args["pokedexEntry"],
                    'Type': args["type"],
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
            pokemon_json = {
                    'UserId': args["userId"],
                    'PokemonId': args["pokemonId"],
                    'PokedexEntry': "",
                    'Type': args["type"],
                    'BaseHP': args["baseHp"],
                    'BaseAtk': args["baseAtk"],
                    'BaseSpAtk': args["baseSpAtk"],
                    'BaseDef': args["baseDef"],
                    'BaseSpDef': args["baseSpDef"],
                    'BaseSpeed': args["baseSpeed"],
                }
            json_string = json.dumps(pokemon_json)
            model = genai.GenerativeModel("gemini-1.5-flash")
            genai_response = model.generate_content("Interpret the following json as information about a pokemon where pokemonId is the name of the pokemon the name and the rest are its stats and type. Please give me a short pokedex entry for it, while being creative, witty, and funny. The answer must be shorter than 3 sentences. " + json_string)
            pokemon_json["PokedexEntry"]=genai_response.text
            print(genai_response.text)
            print("Parsed Arguments:", args)  # Debug print
            pokedex_table.put_item(
                Item =pokemon_json,
                ConditionExpression="attribute_not_exists(UserId) AND attribute_not_exists(PokemonId)" #checks if pokemon already exists for that user
            )
            return {"message": "Pokemon added successfully"}, 201
        except Exception as e:
            print("A server error occurred:", e)
            return {"error": str(e)}, 500
       
    # def delete(self, pokemon_id):
    #     del pokemons[pokemon_id]
    #     return '', 204

api.add_resource(Pokemon, "/pokedex")




if __name__ =="__main__":
    app.run(debug=True)

