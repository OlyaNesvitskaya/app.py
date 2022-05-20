from flask import Flask, render_template, request, flash
from re import match
import os
from dotenv import load_dotenv

from pymongo import MongoClient
load_dotenv()


client = MongoClient(host=os.environ.get('host'),
                     port=int(os.environ.get('port')))


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
db = client["users_database"]
users = db["users"]


@app.route("/", methods=["GET"])
def home_page():
    if request.method == "GET" and request.args.get('list_of_users'):
        if users.count_documents({}) == 0:
            flash(f"Список поки що порожній")
        return render_template('index.html', items=users.find({}, {'_id': 0}))

    return render_template("index.html")


@app.route("/", methods=["POST"])
def post_email():
    email = request.form['email']
    is_valid_email = match('^\w+@\w+\.\w+$', email)
    if not is_valid_email:
        flash(f'Некоректно введений email!', 'error')
        return render_template("index.html")
    search = users.find_one({'email': email})
    if search:
        flash(f"Вже бачилися, {email}")
    else:
        users.insert_one({"email": email})
        flash(f"Привіт, {email}")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
#