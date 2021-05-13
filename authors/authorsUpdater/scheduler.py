from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from .authorsUpdateApi import update_authors_steamid_table, update_authors_authortemp_table


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_authors_steamid_table, 'cron', day_of_week='4', hour=3, minute=5, id='update_steamids_001', replace_existing=True)
    scheduler.add_job(update_authors_authortemp_table, 'cron', day_of_week='4', hour=3, minute=10, replace_existing=True)
    scheduler.start()