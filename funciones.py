import csv
import urllib.request
import requests

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    
    return render_template("apology.html",code=code,message=message),code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(isbn):
    """Buscando libros"""
    
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn).json()

    try:
        info = response["items"][0]["volumeInfo"]
    except:
        info = None

    return info


  


