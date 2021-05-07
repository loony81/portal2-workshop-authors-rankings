from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from .authorsUpdateApi import update_authors_steamid_table, update_authors_authortemp_table


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_authors_steamid_table, 'date', run_date=datetime(2021, 5, 7, 17, 17, 5), id='update_steamids_001', replace_existing=True)
    # scheduler.add_job(update_authors_authortemp_table, 'date', run_date=datetime(2021, 5, 7, 16, 25, 5), replace_existing=True)
    scheduler.start()