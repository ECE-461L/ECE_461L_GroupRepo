from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html")
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
