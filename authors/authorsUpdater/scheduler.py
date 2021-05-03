from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from .authorsUpdateApi import update_authors_steamid_table, update_authors_authortemp_table


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_authors_steamid_table, 'cron', day_of_week='0', hour=21, minute=1, id='update_steamids_001', replace_existing=True)
    scheduler.add_job(update_authors_authortemp_table, 'cron', day_of_week='0', hour=21, minute=5, replace_existing=True)
    scheduler.start()