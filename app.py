from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import qrcode
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cardapio.db'
db = SQLAlchemy(app)