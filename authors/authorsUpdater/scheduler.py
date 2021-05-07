from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from .authorsUpdateApi import update_authors_steamid_table, update_authors_authortemp_table


def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(update_authors_steamid_table, 'cron', day_of_week='5', hour=3, minute=3, id='update_steamids_001', replace_existing=True)
    scheduler.add_job(update_authors_authortemp_table, 'cron', day_of_week='5', hour=3, minute=7, replace_existing=True)
    scheduler.start()