import bcrypt
from flask import render_template, session, request, flash
from app import *
from models import User, Role


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



