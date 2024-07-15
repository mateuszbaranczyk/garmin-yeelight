from flask_apscheduler import APScheduler
from garlight.bulbs import Bulbs

scheduler = APScheduler()


@scheduler.task("cron", minute="*")
def update_bulbs_connection():
    bulbs = Bulbs()
    bulbs.discover_and_assign()
