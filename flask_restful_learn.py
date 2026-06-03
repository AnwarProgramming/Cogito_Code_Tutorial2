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

    
    def get( self, username=None ):

        if username is None:
            return make_response(jsonify(user_details), 200)
        
        for user in user_details:
            if user['user_name'] == username:
                return make_response(jsonify(user), 200)
        
        return make_response(jsonify({'message': 'User not found'}, 404))
            
    
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


# Here is the complete workflow of how flask_restful processes requests and manages your application behind the scenes.

# Think of Flask-RESTful as a structured abstraction layer built on top of standard Flask. Instead of using multiple route decorators (@app.route) for different HTTP methods, it routes incoming requests to a specific Resource class based on the URL matching.
# The Workflow Blueprint

# [ Incoming Client Request ] 
#           │
#           ▼
#     [ Flask App ] ──(Passes request)──> [ Flask-RESTful Api Engine ]
#                                                    │
#                                             (Inspects Route & Method)
#                                                    │
#                                                    ▼
#                                       [ Matches URL to Resource ]
#                                       e.g., /api/john -> HelloWorld
#                                                    │
#                                                    ▼
#                                       [ Invokes HTTP Method Function ]
#                                       e.g., GET -> get(self, username)
#                                                    │
#                                                    ▼
# [ Client receives JSON + Status ] <─── [ Returns Response ]

# Step-by-Step Breakdown
# 1. Initialization and Routing Setup

# When you run the script, Flask-RESTful sets up the routing table using your add_resource configuration:
# Python

# api.add_resource(HelloWorld, '/api', '/api/<string:username>')

#     The Api object acts as the central router.

#     It registers both paths (/api and /api/<string:username>) to point directly to your HelloWorld class.

# 2. The Request Arrives

# Let’s look at what happens during different client requests:
# Scenario A: A POST Request to /api

#     Routing: A client sends a POST request to /api with a JSON body (e.g., {"user_name": "Alice", "address": "Wonderland"}).

#     Dispatching: The Api router inspects the HTTP method (POST) and maps it to the post(self) method inside the HelloWorld class.

#     Execution: * request.get_json() extracts the data payload.

#         The code validates if user_name and address exist.

#         If valid, it appends the dictionary to the global user_details list and returns a 201 Created response.

# Scenario B: A GET Request to /api/Alice

#     Routing: A client sends a GET request to /api/Alice.

#     Variable Parsing: Flask-RESTful automatically extracts "Alice" from the URL string because of the converter definition <string:username>.

#     Dispatching: The router maps the GET method to get(self, username). Crucially, it passes "Alice" into the function as the username argument.

#     Execution:

#         The for loop iterates through user_details looking for a dictionary where 'user_name' == 'Alice'.

#         If found, it serializes that specific user's dictionary to JSON and returns a 200 OK response.