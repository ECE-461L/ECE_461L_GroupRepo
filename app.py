from flask import Flask, send_from_directory, request, json, jsonify
from flask_cors import cross_origin, CORS
import cipher
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# This may run twice since it is not in main

context = None
flaskApp = None

def main():
    global context
    global flaskApp
    context = AppContext()
    flaskApp = context.app

    # Define routes
    context.app.route("/", methods=["GET"])(index)
    context.app.route("/authenticate", methods=["POST"])(authenticate)
    context.app.route("/register", methods=["POST"])(register)
    context.app.route("/create-project", methods=["POST"])(createProject)
    context.app.route("/use-project", methods=["POST"])(useProject)
    context.app.route("/check-in", methods=["POST"])(checkIn)
    context.app.route("/check-out", methods=["POST"])(checkOut)
    context.app.errorhandler(404)(not_found)

    context.app.run(host=os.environ['HOST'], debug=False, port=int(os.environ['PORT']))
    # local run
    # app.run(host="localhost", debug=True, port=5000) 


class AppContext():
    def __init__(self):
        # Load environment variables
        load_dotenv()

        print("Loaded environment variables:")
        for key, value in os.environ.items():
            print(f"{key}={value}")

        # Create Flask app
        self.app = Flask(__name__, static_folder="./build", static_url_path="/")
        self.cors = CORS(self.app)

        # Set cipher variables
        self.cipherN = int(os.environ['CIPHER_N'])
        self.cipherD = int(os.environ['CIPHER_D'])

        # Connect to MongoDB
        client = MongoClient(os.environ['MONGO_URI'], server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Successfully connected to MongoDB")
        db = os.environ['DB_NAME']

        self.loginDb = client[db][os.environ['LOGIN_COLLECTION']]
        self.projectDb = client[db][os.environ['PROJECT_COLLECTION']]
        self.checkoutDb = client[db][os.environ['CHECKOUT_COLLECTION']]

        # Reset global capacities
        self.checkoutDb.delete_many({})
        globalData = {
            'hwSet1Capacity': f"{os.environ['SET_1_CAPACITY']}",
            'hwSet1Availability': f"{os.environ['SET_1_CAPACITY']}",
            'hwSet2Capacity': f"{os.environ['SET_2_CAPACITY']}",
            'hwSet2Availability': f"{os.environ['SET_2_CAPACITY']}"
        }
        self.checkoutDb.insert_one(globalData)
        print("Initialized global capacities")



# Default behavior to pull from the index.html frontend file
def index():
    return send_from_directory(context.app.static_folder, "index.html")

def authenticate():
    user_data = request.get_json()
    username = user_data.get("username")
    password = user_data.get("password")

    checkUsername = {"username": cipher.encrypt(username, context.cipherN, context.cipherD)}
    searchCreds = {
        "username": cipher.encrypt(username, context.cipherN, context.cipherD),
        "password": cipher.encrypt(password, context.cipherN, context.cipherD)
    }

    if context.loginDb.find_one(checkUsername):
        if context.loginDb.find_one(searchCreds):
            return jsonify({"message": "Authentication successful", "user": username})
        else:
            return jsonify({"message": "Incorrect password"}), 401
    else:
        return jsonify({"message": "User doesn't exist"}), 401


def register():
    user_data = request.get_json()
    username = user_data.get("username")
    password = user_data.get("password")

    checkUsername = {"username": cipher.encrypt(username, context.cipherN, context.cipherD)}
    createUser = {"username": cipher.encrypt(username, context.cipherN, context.cipherD),
                  "password": cipher.encrypt(password, context.cipherN, context.cipherD)}

    if not context.loginDb.find_one(checkUsername):
        context.loginDb.insert_one(createUser)
        return jsonify({"message": "Creating credentials", "user": username})
    else:
        return jsonify({"message": "Username taken"}), 401


def createProject():
    projectData = request.get_json()
    id = projectData.get("projectId")
    name = projectData.get("name")
    description = projectData.get("description")

    checkProjectId = {"projectId": id}
    quantities = context.checkoutDb.find_one({}, {'_id': 0})

    createProjectData = {"projectId": id,
                         "name": name,
                         "description": description,
                         "hwSet1CheckedOut": "0",
                         "hwSet2CheckedOut": "0"}

    returnDocument = {**createProjectData, **quantities}

    if context.projectDb.find_one(checkProjectId):
        return jsonify({"message": "The project Id already exists."}), 401
    else:
        context.projectDb.insert_one(createProjectData)
        return jsonify({"message": "Creating project.", **returnDocument})

def useProject():
    projectData = request.get_json()
    id = projectData.get("projectId")

    checkProjectId = {"projectId": id}
    quantities = context.checkoutDb.find_one({}, {'_id': 0})

    retrievedProjectData = context.projectDb.find_one(checkProjectId, {'_id': 0})
    returnDocument = {**retrievedProjectData, **quantities}

    if retrievedProjectData:
        return jsonify({"message": "Project exists.", **returnDocument})
    else:
        return jsonify({"message": "Project does not exist."}), 401

    
def checkIn():
    projectData = request.get_json()
    id = projectData.get("projectId")
    request1 = int(projectData.get("request1", 0))  # Ensuring default to 0 if not found
    request2 = int(projectData.get("request2", 0))

    checkProjectId = {"projectId": id}
    retrievedProjectData = context.projectDb.find_one(checkProjectId)

    quantities = context.checkoutDb.find_one()

    if retrievedProjectData:
        if quantities['hwSet1Availability'] + request1 > quantities['hwSet1Capacity']:
            return jsonify({"message": "HW set 1 check in quantity exceeds capacity."}), 401
        if quantities['hwSet2Availability'] + request2 > quantities['hwSet2Capacity']:
            return jsonify({"message": "HW set 2 check in quantity exceeds capacity."}), 401

        if retrievedProjectData['hwSet1CheckedOut'] < request1:
            return jsonify({"message": "HW set 1 check in quantity exceeds checked out quantity."}), 401
        if retrievedProjectData['hwSet2CheckedOut'] < request2:
            return jsonify({"message": "HW set 2 check in quantity exceeds checked out quantity."}), 401

        newAvailability1 = quantities['hwSet1Availability'] + request1
        newAvailability2 = quantities['hwSet2Availability'] + request2
        context.checkoutDb.update_one({'_id': quantities['_id']}, {'$set': {'hwSet1Availability': newAvailability1, 'hwSet2Availability': newAvailability2}})

        newHWSet1CheckedOut = retrievedProjectData['hwSet1CheckedOut'] - request1
        newHWSet2CheckedOut = retrievedProjectData['hwSet2CheckedOut'] - request2
        context.projectDb.update_one(checkProjectId, {'$set': {'hwSet1CheckedOut': newHWSet1CheckedOut, 'hwSet2CheckedOut': newHWSet2CheckedOut}})

        updatedProjectData = context.projectDb.find_one(checkProjectId)
        return jsonify({"message": "Checked in requested quantities.", **updatedProjectData})

    else:
        return jsonify({"message": "Project does not exist."}), 401


def checkOut():
    projectData = request.get_json()
    id = projectData.get("projectId")
    request1 = int(projectData.get("request1", 0))
    request2 = int(projectData.get("request2", 0))

    checkProjectId = {"projectId": id}
    retrievedProjectData = context.projectDb.find_one(checkProjectId)

    quantities = context.checkoutDb.find_one()

    if retrievedProjectData:
        if quantities['hwSet1Availability'] - request1 < 0:
            return jsonify({"message": "HW set 1 check out quantity exceeds availability."}), 401
        if quantities['hwSet2Availability'] - request2 < 0:
            return jsonify({"message": "HW set 2 check out quantity exceeds availability."}), 401

        newAvailability1 = quantities['hwSet1Availability'] - request1
        newAvailability2 = quantities['hwSet2Availability'] - request2
        context.checkoutDb.update_one({'_id': quantities['_id']}, {'$set': {'hwSet1Availability': newAvailability1, 'hwSet2Availability': newAvailability2}})

        newHWSet1CheckedOut = retrievedProjectData['hwSet1CheckedOut'] + request1
        newHWSet2CheckedOut = retrievedProjectData['hwSet2CheckedOut'] + request2
        context.projectDb.update_one(checkProjectId, {'$set': {'hwSet1CheckedOut': newHWSet1CheckedOut, 'hwSet2CheckedOut': newHWSet2CheckedOut}})

        updatedProjectData = context.projectDb.find_one(checkProjectId)
        return jsonify({"message": "Checked out requested quantities.", **updatedProjectData})

    else:
        return jsonify({"message": "Project does not exist."}), 401


def not_found(e):
    return send_from_directory(context.app.static_folder, "index.html")


if __name__ == "__main__":
    main()




# @context.app.route("/login-db", methods=["GET"])
# def viewLoginDb():
#     users = loginDb.find({}, {"_id": 0})
#     html_output = "<html><body><table><tr><th>Username</th><th>&nbsp;</th><th>Encrypted Password</th></tr>"
#     for user in users:
#         decrypted_username = cipher.decrypt(user["username"], cipherN, cipherD)
#         encrypted_password = user["password"]
#         html_output += f"<tr><td>{decrypted_username}</td><td>&nbsp;</td><td>{encrypted_password}</td></tr>"

#     html_output += "</table></body></html>"
#     return html_output

# shows project ID, HWset1 capacity, HWset1 availability, HWset2 capacity, HWset2 availability in that order
# @app.route("/project-db", methods=["GET"])
# def viewProjectDb():
#     projects = projectDb.find({}, {"_id": 0})
#     html_output = "<html><body><table><tr><th>Project ID</th><th>&nbsp;</th><th>Project Name</th><th>&nbsp;</th><th>Description</th><th>&nbsp;</th><th>HW Set 1 Capacity</th><th>&nbsp;</th><th>HW Set 1 Availability</th><th>&nbsp;</th><th>HW Set 2 Capacity</th><th>&nbsp;</th><th>HW Set 2 Availability</th></tr>"
#     for project in projects:
#         html_output += f"<tr><td>{project['projectId']}</td><td>&nbsp;</td><td>{project['name']}</td><td>&nbsp;</td><td>{project['description']}</td><td>&nbsp;</td><td>{project['hwSet1Capacity']}</td><td>&nbsp;</td><td>{project['hwSet1Availability']}</td><td>&nbsp;</td><td>{project['hwSet2Capacity']}</td><td>&nbsp;</td><td>{project['hwSet2Availability']}</td></tr>"

#     html_output += "</table></body></html>"
#     return html_output