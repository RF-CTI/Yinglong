from apscheduler.schedulers.blocking import BlockingScheduler
from yinglong_backend.collection_data import (collectionPhishData,
                                              collectionBotnetData)

schedule = BlockingScheduler(timezone='Asia/Shanghai')

schedule.add_job(collectionPhishData, 'cron', args=(), hour='*/2')
schedule.add_job(collectionBotnetData, 'cron', args=(), day='*/1')


if __name__ == '__main__':
    schedule.start()
