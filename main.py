from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from wtforms.validators  import InputRequired, Length, ValidationError
import getpass


db = SQLAlchemy() 
main = Flask(__name__)
main.secret_key = "secretkey"
main.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db.init_app(main)



login_manager = LoginManager()
login_manager.init_app(main)
login_manager.login_view ="login" 

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


class Account(db.Model,UserMixin):
    __tablename__='Account'
    id= db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    userrole = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<Account %r' %self.id
    
   

@main.route('/',methods=['POST','GET'])
def index():
    return render_template('main.html')


if __name__ == "__main__":
    main.run(debug = True) 