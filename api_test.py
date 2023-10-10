from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Hello_World(Resource):
    def get(self):
        return {"data" : "Get"}, 201
    
    def post(self):
        return ""
        
    def delete(self):
        return ""

api.add_resource(Hello_World, "/")

if __name__ == "__main__":
    app.run(debug=True)