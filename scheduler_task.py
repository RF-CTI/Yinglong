from apscheduler.schedulers.background import BackgroundScheduler
from collection_data import collectionBotnetData, collectionPhishData


def collectionData():
    collectionPhishData()
    collectionBotnetData()


def publishData():
    pass


schel = BackgroundScheduler()
schel.add_job(collectionData, 'cron', day='*/1', hour='1')
schel.add_job(publishData, 'cron', day='*/1', hour='2')
