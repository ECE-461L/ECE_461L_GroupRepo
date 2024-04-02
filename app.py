from flask import Flask, send_from_directory, request, json, jsonify
from flask_cors import cross_origin, CORS
import cipher
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Loaded environment variables:")
for key, value in os.environ.items():
    print(f"{key}={value}")

# Create Flask app
app = Flask(__name__, static_folder="./build", static_url_path="/")
cors = CORS(app)

# Set cipher variables
cipherN = int(os.environ['CIPHER_N'])
cipherD = int(os.environ['CIPHER_D'])

# Connect to MongoDB
client = MongoClient(os.environ['MONGO_URI'], server_api=ServerApi('1'))
client.admin.command('ping')
print("Successfully connected to MongoDB")
db = os.environ['DB_NAME']
loginDb = client[os.environ['DB_NAME']][os.environ['LOGIN_COLLECTION']]
projectDb = client[os.environ['DB_NAME']][os.environ['PROJECT_COLLECTION']]

# updated global quantity correctly
checkoutDb = client[os.environ['DB_NAME']][os.environ['CHECKOUT_COLLECTION']]
# remove old data
checkoutDb.delete_many({})
globalData = {
    'hwSet1Capacity': f"{os.environ['SET_1_CAPACITY']}",
    'hwSet1Availability': f"{os.environ['SET_1_CAPACITY']}",
    'hwSet2Capacity': f"{os.environ['SET_2_CAPACITY']}",
    'hwSet2Availability': f"{os.environ['SET_2_CAPACITY']}"
}
checkoutDb.insert_one(globalData)
print("Initialized global capacities")


# Default behavior to pull from the index.html frontend file
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/login-db", methods=["GET"])
def viewLoginDb():
    users = loginDb.find({}, {"_id": 0})
    html_output = "<html><body><table><tr><th>Username</th><th>&nbsp;</th><th>Encrypted Password</th></tr>"
    for user in users:
        decrypted_username = cipher.decrypt(user["username"], cipherN, cipherD)
        encrypted_password = user["password"]
        html_output += f"<tr><td>{decrypted_username}</td><td>&nbsp;</td><td>{encrypted_password}</td></tr>"

    html_output += "</table></body></html>"
    return html_output

# shows project ID, HWset1 capacity, HWset1 availability, HWset2 capacity, HWset2 availability in that order
# @app.route("/project-db", methods=["GET"])
# def viewProjectDb():
#     projects = projectDb.find({}, {"_id": 0})
#     html_output = "<html><body><table><tr><th>Project ID</th><th>&nbsp;</th><th>Project Name</th><th>&nbsp;</th><th>Description</th><th>&nbsp;</th><th>HW Set 1 Capacity</th><th>&nbsp;</th><th>HW Set 1 Availability</th><th>&nbsp;</th><th>HW Set 2 Capacity</th><th>&nbsp;</th><th>HW Set 2 Availability</th></tr>"
#     for project in projects:
#         html_output += f"<tr><td>{project['projectId']}</td><td>&nbsp;</td><td>{project['name']}</td><td>&nbsp;</td><td>{project['description']}</td><td>&nbsp;</td><td>{project['hwSet1Capacity']}</td><td>&nbsp;</td><td>{project['hwSet1Availability']}</td><td>&nbsp;</td><td>{project['hwSet2Capacity']}</td><td>&nbsp;</td><td>{project['hwSet2Availability']}</td></tr>"

#     html_output += "</table></body></html>"
#     return html_output


@app.route("/authenticate", methods=["POST"])
def authenticate():
    user_data = request.get_json()
    print(user_data)
    username = user_data.get("username")
    password = user_data.get("password")

    checkUsername = {"username": cipher.encrypt(username, cipherN, cipherD)}
    searchCreds = {
        "username": cipher.encrypt(username, cipherN, cipherD),
        "password" : cipher.encrypt(password, cipherN, cipherD)
    }
        
    if loginDb.find_one(checkUsername):
        if loginDb.find_one(searchCreds):
            return jsonify({"message": "Authentication successful", "user": username})
        else:
            return jsonify({"message": "Incorrect password"}), 401
    else:
        return jsonify({"message": "User doesn't exist"}), 401


@app.route("/register", methods=["POST"])
def register():
    user_data = request.get_json()
    print(user_data)
    username = user_data.get("username")
    password = user_data.get("password")

    checkUsername = {"username": cipher.encrypt(username, cipherN, cipherD) }
    createUser = {"username": cipher.encrypt(username, cipherN, cipherD),
                   "password" : cipher.encrypt(password, cipherN, cipherD) }

    if not loginDb.find_one(checkUsername):
        loginDb.insert_one(createUser)
        return jsonify({"message": "Creating credentials", "user": username})
    else:
        return jsonify({"message": "Username taken"}), 401

@app.route("/create-project", methods=["POST"])
def createProject():
    projectData = request.get_json()
    print(projectData)
    id = projectData.get("projectId")
    name = projectData.get("name")
    description = projectData.get("description")

    checkProjectId = {"projectId": id}
    quantities = checkoutDb.find_one({}, {'_id': 0})

    createProject = {"projectId": id,
                    "name": name,
                    "description": description
                    }
    
    returnDocument = {**createProject, **quantities}

    print(returnDocument)

    if projectDb.find_one(checkProjectId.copy()):
        return jsonify({"message": "The project Id already exists."}), 401
    else:
        projectDb.insert_one(createProject.copy())
        return jsonify({"message": "Creating project.", **returnDocument})


@app.route("/use-project", methods=["POST"])
def useProject():
    projectData = request.get_json()
    print(projectData)
    id = projectData.get("projectId")

    checkProjectId = {"projectId": id}
    quantities = checkoutDb.find_one({}, {'_id': 0})


    retrievedProjectData = projectDb.find_one(checkProjectId, {'_id': 0})
    returnDocument = {**retrievedProjectData, **quantities}

    if retrievedProjectData:
        return jsonify({"message": "Project exists.", **returnDocument})
    else:
        return jsonify({"message": "Project does not exist."}), 401
    

@app.route("/check-in", methods=["POST"])
def checkIn():
    projectData = request.get_json()
    id = projectData.get("projectId")
    request1 = projectData.get("request1")
    request2 = projectData.get("request2")

    checkProjectId = {"projectId": id}
    retrievedProjectData = projectDb.find_one(checkProjectId, {'_id': 0})

    quantities = checkoutDb.find_one()
    # returnDocument = {**retrievedProjectData, **quantities}

    if retrievedProjectData:
        if int(quantities['hwSet1Availability']) + int(request1) > int(quantities['hwSet1Capacity']):
            return jsonify({"message": "HW set 1 check in quantity exceeds capacity."}), 401
        if int(quantities['hwSet2Availability']) + int(request2) > int(quantities['hwSet2Capacity']):
            return jsonify({"message": "HW set 2 check in quantity exceeds capacity."}), 401
        
        newAvailability1 = str(int(quantities['hwSet1Availability']) + int(request1))
        newAvailability2 = str(int(quantities['hwSet2Availability']) + int(request2))
        checkoutDb.update_one({'_id': quantities['_id']}, {'$set': {'hwSet1Availability': newAvailability1, 'hwSet2Availability': newAvailability2}})

        updatedQuantities = checkoutDb.find_one({}, {'_id': 0})

        updatedProjectData = {**retrievedProjectData, **updatedQuantities}
        return jsonify({"message": "Checked in requested quantities.", **updatedProjectData})
    
    else:
        return jsonify({"message": "Project does not exist."}), 401


@app.route("/check-out", methods=["POST"])
def checkOut():
    projectData = request.get_json()
    id = projectData.get("projectId")
    request1 = projectData.get("request1")
    request2 = projectData.get("request2")

    checkProjectId = {"projectId": id}
    retrievedProjectData = projectDb.find_one(checkProjectId, {'_id': 0})

    quantities = checkoutDb.find_one()

    if retrievedProjectData:
        if int(quantities['hwSet1Availability']) - int(request1) < 0:
            return jsonify({"message": "HW set 1 check out quantity exceeds availability."}), 401
        if int(quantities['hwSet2Availability']) - int(request2) < 0:
            return jsonify({"message": "HW set 2 check out quantity exceeds availability."}), 401
        
        newAvailability1 = str(int(quantities['hwSet1Availability']) - int(request1))
        newAvailability2 = str(int(quantities['hwSet2Availability']) - int(request2))
        checkoutDb.update_one({'_id': quantities['_id']}, {'$set': {'hwSet1Availability': newAvailability1, 'hwSet2Availability': newAvailability2}})

        updatedQuantities = checkoutDb.find_one({}, {'_id': 0})

        updatedProjectData = {**retrievedProjectData, **updatedQuantities}
        return jsonify({"message": "Checked out requested quantities.", **updatedProjectData})
    
    else:
        return jsonify({"message": "Project does not exist."}), 401

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host=os.environ['HOST'], debug=False, port=int(os.environ['PORT']))
    # local run
    # app.run(host="localhost", debug=True, port=5000) 