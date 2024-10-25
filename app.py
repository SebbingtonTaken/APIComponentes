from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Pokemon(Resource):
    def get(self):
        return {"data": "Soy un Entrenador Pokemon que hace deploy desde github!"}

api.add_resource(Pokemon, "/helloworld")



if __name__ =="__main__":
    app.run(debug=True)

#Changed file name to be lowercase