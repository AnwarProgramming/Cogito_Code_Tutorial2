from flask import Flask, make_response, jsonify, request

#  Flask RESTful is an extension for Flask that adds support for quickly building REST APIs.
# It provides tools for creating resources, handling requests and formatting responses.

from flask_restful import Api, Resource


user_details = []

app = Flask(__name__)

api = Api(app) # Api is a wrapper around your Flask application that adds REST API features.


# Generally, we call flask api as 'resources'.
# Api = traffic controller/router
# Resource = endpoint class
# get/post/put/delete = actions performed when a request arrives
class HelloWorld(Resource):
    
    # def get(self):
    #     data = {
    #         'message': 'Hello, World!'
    #     }
    #     return make_response(jsonify(data), 200)

    
    def get(self, username):
        print(user_details)
        for user in user_details:
            if user['user_name'] == username:
                return make_response(jsonify(user), 200)
            
    
    def post(self):
        credentials = request.get_json()

        # data validation
        if 'user_name' not in credentials or 'address' not in credentials:
            return make_response(jsonify({'message':'Invalid data'}), 400)
        
        user_details.append(credentials)
        result = {
            'message' : 'User added successfully',
            'user': {
                'user_name' : credentials['user_name'],
                'address': credentials['address']
            }
        }

        return make_response(jsonify(result), 201)


    def delete(self):
        pass

api.add_resource(HelloWorld, '/api','/api/<string:username>')
# we are using flask_restful instead of @app.route because it can handle multiple endpoints for same class

if __name__=='__main__':
    app.run(debug=True)