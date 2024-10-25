from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

pokemon_put_args = reqparse.RequestParser()
pokemon_put_args.add_argument("name", type=str, help="Enter name",required=True)
pokemon_put_args.add_argument("desc", type=str, help="Enter desc",required=True)

pokemons = {}

class Pokemon(Resource):
    def get(self, pokemon_id):
        return {}
    def put(self, pokemon_id):
        args = pokemon_put_args.parse_args()
        return{pokemon_id: args}

api.add_resource(Pokemon, "/helloworld/<int:pokemon_id>")



if __name__ =="__main__":
    app.run(debug=True)

#Changed file name to be lowercase