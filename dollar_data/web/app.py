import os
from flask_apscheduler import APScheduler
from flask import Flask, render_template
from sqlalchemy import func
from dollar_data.database import db_session, init_db
from dollar_data.jobs import update_database, check_missing_entries
from dollar_data.models import Dollar


class Config:
    SCHEDULER_API_ENABLED = True


cwd = os.getcwd()
app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
init_db()


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


if __name__ == "__main__":
    scheduler.add_job(
        func=update_database, trigger="interval", id="update_database", hours=24
    )
    scheduler.add_job(
        func=check_missing_entries,
        trigger="interval",
        id="check_missing_entries",
        hours=24,
    )
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True, use_reloader=False)
