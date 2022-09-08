from apscheduler.schedulers.background import BackgroundScheduler


def mergeData():
    return


schel = BackgroundScheduler()
schel.add_job(mergeData, 'cron', day='*/1', hour='1')
