from flask import Flask, render_template
from sqlalchemy import func
from dollar_data.database import db_session, init_db
from dollar_data.models import Dollar
import os

cwd = os.getcwd()
app = Flask(__name__)
init_db()
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def hello_world():
    data = Dollar.query. \
        filter(func.strftime('%d', Dollar.date) == '10'). \
        all()
    serialized = list()
    for _ in data:
        serialized.append(_.as_dict())
    return render_template(template_name_or_list="index.html", data=serialized)
