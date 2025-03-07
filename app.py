from src import database_operations as db
from src import funcs
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", data=funcs.get_2_random())

if __name__ == '__main__':
    app.run(debug=True)
