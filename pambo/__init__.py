from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,jsonify,flash;
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required,LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,date
import socket
import os
import random
app=Flask(__name__,template_folder='template')
Talisman(app)
key="@piontonsale"
app.config["SECRET_KEY"]=key;
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///pos.db'
posData=SQLAlchemy(app)
logins=LoginManager(app)
from pambo import routes