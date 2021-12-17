from datetime import datetime
import os
from sys import version

from flask import render_template, request, current_app as app

from app import App


@app.route('/')
def index():
    return render_template("main.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route("/about")
def about():
    return render_template("about.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/achievements")
def score():
    return render_template("achievements.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S"))
