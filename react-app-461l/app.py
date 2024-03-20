from flask import Flask, send_from_directory, request, json, jsonify
from flask_cors import cross_origin, CORS
import cipher
app = Flask(__name__, static_folder="./build", static_url_path="/")
cors = CORS(app)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://somwakdikar:SZOa1VIGJGsPcI78@cluster.ti6nxe6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["ECE-461L"]
loginDb = db.login
projectDb = db.project


# Send a ping to confirm a successful connection
client.admin.command('ping')
print("Successfully connected to MongoDB")

cipherN = 11
cipherD = -1


# Default behavior to pull from the index.html frontend file
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/db-login", methods=["GET"])
def viewLoginDb():
    users = loginDb.find({}, {"_id": 0})

    html_output = "<html><body><table><tr><th>Username</th><th>&nbsp;</th><th>Encrypted Password</th></tr>"

    for user in users:
        decrypted_username = cipher.decrypt(user["username"], cipherN, cipherD)
        encrypted_password = user["password"]
        html_output += f"<tr><td>{decrypted_username}</td><td>&nbsp;</td><td>{encrypted_password}</td></tr>"

    html_output += "</table></body></html>"

    return html_output


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
        return jsonify({"message": "No user with the submitted username exists"}), 401



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
    set1Capacity = projectData.get("hwSet1Capacity")
    set2Capacity = projectData.get("hwSet2Capacity")

    checkProjectId = {"projectId": id}

    createProject = {"projectId": id,
                    "name": name,
                    "description": description,
                    "hwSet1Capacity": set1Capacity,
                    "hwSet2Capacity": set2Capacity,
                    "hwSet1Availability": set1Capacity,
                    "hwSet2Availability": set2Capacity
                    }

    if projectDb.find_one(checkProjectId.copy()):
        return jsonify({"message": "The project Id already exists."}), 401
    else:
        projectDb.insert_one(createProject.copy())
        return jsonify({"message": "Creating project.", **createProject})


@app.route("/use-project", methods=["POST"])
def useProject():
    projectData = request.get_json()
    print(projectData)
    id = projectData.get("projectId")

    checkProjectId = {"projectId": id}

    retrievedProjectData = projectDb.find_one(checkProjectId, {'_id': 0})

    if retrievedProjectData:
        return jsonify({"message": "Project exists.", **retrievedProjectData})
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

    if retrievedProjectData:
        if int(retrievedProjectData['hwSet1Availability']) + int(request1) > int(retrievedProjectData['hwSet1Capacity']):
            return jsonify({"message": "HW set 1 check in quantity exceeds capacity."}), 401
        if int(retrievedProjectData['hwSet2Availability']) + int(request2) > int(retrievedProjectData['hwSet2Capacity']):
            return jsonify({"message": "HW set 2 check in quantity exceeds capacity."}), 401
        
        newAvailability1 = str(int(retrievedProjectData['hwSet1Availability']) + int(request1))
        newAvailability2 = str(int(retrievedProjectData['hwSet2Availability']) + int(request2))
        projectDb.update_one(checkProjectId, {'$set': {'hwSet1Availability': newAvailability1, 'hwSet2Availability': newAvailability2}})

        updatedProjectData = projectDb.find_one(checkProjectId, {'_id': 0})
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

    if retrievedProjectData:
        if int(retrievedProjectData['hwSet1Availability']) - int(request1) < 0:
            return jsonify({"message": "HW set 1 check out quantity exceeds availability."}), 401
        if int(retrievedProjectData['hwSet2Availability']) - int(request2) < 0:
            return jsonify({"message": "HW set 2 check out quantity exceeds availability."}), 401
        
        newAvailability1 = str(int(retrievedProjectData['hwSet1Availability']) - int(request1))
        newAvailability2 = str(int(retrievedProjectData['hwSet2Availability']) - int(request2))
        projectDb.update_one(checkProjectId, {'$set': {'hwSet1Availability': newAvailability1, 'hwSet2Availability': newAvailability2}})

        updatedProjectData = projectDb.find_one(checkProjectId, {'_id': 0})
        return jsonify({"message": "Checked out requested quantities.", **updatedProjectData})
    
    else:
        return jsonify({"message": "Project does not exist."}), 401


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)

    # From class
    # app.run(host='0.0.0.0', debug=False, port=5000)

