from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def root():
    return render_template("index.html")
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/products")
def products():
    return render_template("products.html")


if __name__ == "__main__":
    app.run(debug=True)