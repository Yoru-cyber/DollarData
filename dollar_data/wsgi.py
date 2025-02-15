import atexit
import os
from apscheduler.schedulers.background import BackgroundScheduler
from dollar_data.jobs import check_missing_entries, update_database
from dollar_data.web.app import app  # noqa

cwd = os.getcwd()
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=update_database, trigger="interval", id="update_database", hours=24
)
scheduler.add_job(
    func=check_missing_entries,
    trigger="interval",
    id="check_missing_entries",
    hours=24,
)


def shutdown_scheduler():
    scheduler.shutdown()


atexit.register(shutdown_scheduler)
scheduler.start()
