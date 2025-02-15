import os
from flask import Flask, render_template
from sqlalchemy import func
from dollar_data.database import db_session, init_db
from dollar_data.models import Dollar


class Config:
    SCHEDULER_API_ENABLED = True


cwd = os.getcwd()
init_db()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    return app


app = create_app()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def hello_world():
    data = Dollar.query.filter(func.strftime("%d", Dollar.date) == "10").all()
    serialized = list()
    for _ in data:
        serialized.append(_.as_dict())
    return render_template(template_name_or_list="index.html", data=serialized)


@app.route("/test")
def hello():
    return "test"
