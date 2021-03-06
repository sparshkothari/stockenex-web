from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from flask import Blueprint, request, render_template, url_for, session, flash
from models import User
from models import Stock
from werkzeug.wrappers.response import Response
from mongoengine import *
import json

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if "logged_in" not in session.keys() or not session["logged_in"]:
        return redirect(url_for('home_bp.login'))
    userData = json.loads(session["userData"])
    return render_template("profile/profile.html", userData=userData)


@profile_bp.route('/subscription', methods=['POST'])
def subscription():
    if not session["logged_in"]:
        abort(401)
    userData = json.loads(session["userData"])
    u = User.objects(Q(username=userData["username"]) & Q(password=userData["password"])).first()
    u.subscriptionType = request.form["subscriptionType"]
    u.save()
    userData = u.to_json()
    session["userData"] = userData
    return Response(userData, 200)

@profile_bp.route('/user', methods=['GET'])
def user():
    if not session["logged_in"]:
        abort(401)
    return Response(session["userData"], 200)


@profile_bp.route('/addSymbols', methods=['POST'])
def addSymbols():
    if not session["logged_in"]:
        abort(401)
    userData = json.loads(session["userData"])
    u = User.objects(Q(username=userData["username"]) & Q(password=userData["password"])).first()
    symbols_ = json.loads(request.form["symbols"])
    u.symbols = u.symbols + symbols_
    u.save()
    userData = u.to_json()
    session["userData"] = userData
    return Response(userData, 200)

@profile_bp.route('/removeSymbols', methods=['POST'])
def removeSymbols():
    if not session["logged_in"]:
        abort(401)
    userData = json.loads(session["userData"])
    u = User.objects(Q(username=userData["username"]) & Q(password=userData["password"])).first()
    symbols_ = json.loads(request.form["symbols"])
    for s in symbols_:
        if s in u.symbols:
            u.symbols.remove(s);
    u.save()
    userData = u.to_json()
    session["userData"] = userData
    return Response(userData, 200)


@profile_bp.route('/stock', methods=['GET'])
def stock():
    return Response(Stock.objects.to_json(), 200)