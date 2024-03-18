from flask import Flask, send_from_directory, request, json, jsonify
from flask_cors import cross_origin, CORS
import cipher
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__, static_folder="./build", static_url_path="/")
cors = CORS(app)

uri = "mongodb+srv://somwakdikar:SZOa1VIGJGsPcI78@cluster.ti6nxe6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client = MongoClient(uri, server_api=ServerApi('1'))

cipherN = 11
cipherD = -1

client.admin.command('ping')
print("Successfully connected to MongoDB")


# Default behavior to pull from the index.html frontend file
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/db-login", methods=["GET"])
def viewLoginDb():
    loginDb = client["ECE-461L"].login
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
    loginDb = client["ECE-461L"].login

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
    loginDb = client["ECE-461L"].login

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
    


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    # app.run(debug=True)

    # From class
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))

