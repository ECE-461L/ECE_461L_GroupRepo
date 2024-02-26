from flask import Flask, send_from_directory, request, json, jsonify
from flask_cors import cross_origin, CORS

app = Flask(__name__, static_folder="./build", static_url_path="/")
cors = CORS(app)


# Default behavior to pull from the index.html frontend file
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/authenticate", methods=["POST"])
def authenticate():
    user_data = request.get_json()
    print(user_data)
    username = user_data.get("username")
    password = user_data.get("password")

    # using admin and password for now
    if username == "admin" and password == "password":
        return jsonify({"message": "Authentication successful (from Server)", "user": username})
    else:
        return jsonify({"message": "Authentication failed (from Server)"}), 401



@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)

    # From class
    # app.run(host='0.0.0.0', debug=False, port=5000)

