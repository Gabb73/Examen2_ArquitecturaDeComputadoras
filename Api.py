from flask import Flask, abort, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass


app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///username.db"
ma = Marshmallow(app)
db = SQLAlchemy(app)

@dataclass
class Username(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    username = db.Column(db.String(255))
    mail = db.Column(db.String(255))
  
    def __init__(
        self,
        name,
        lastname,
        username,
        mail,
       
    ):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.mail = mail


    def __repr__(self):
        return "User %i: %s %s %s" % (
            self.id,
            self.name,
            self.lastname,
        )


usuarios = [
    {
        "id": 1,
        "name": "Gabriela",
        "lastname": "Solorzano",
        "username": "gbsn77",
        "mail": "gbsolorzano73@gmail.com",

    }
]

class UserS(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "lastname",
            "username",
            "mail",
        )


user_schema = UserS()
user_schema = UserS(many=True)


usernames = Username.query.all()
print(usernames)


@app.route("/api/usernames/", methods=["GET"])
def get_users():
    return jsonify({"usernames": usernames})

@app.route("/api/usernames/", methods=["POST"])
def new_user():
    if not request.json:
        abort(404)
    new = Username(
        name=request.json["name"],
        lastname=request.json["lastname"],
        username=request.json["usuario"],
        mail=request.json["mail"],
    )

    db.session.commit()
    db.session.add(new)
    return jsonify({"username": Username.as_dict(new)}), 201

@app.route("/api/usernames/" + "<int:id>", methods=["GET"])
def get_usernames(id):
    username = Username.query.get_or_404(id)
    return jsonify({"username": Username.as_dict(usernames)})
