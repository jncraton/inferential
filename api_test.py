from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Hello_World(Resource):
    def get(self):
        return {"data": "hello from api_test"}, 201

    def post(self):
        return {"data": "hello from api_test post"}, 201

    def delete(self):
        return ""


api.add_resource(Hello_World, "/")

if __name__ == "__main__":
    app.run(debug=True)
