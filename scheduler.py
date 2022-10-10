from apscheduler.schedulers.blocking import BlockingScheduler
# from yinglong_backend.collection_data import (collectionPhishData,
#                                              collectionBotnetData,
#                                              collectionC2IntelFeedsData)
from yinglong_backend.update_daliy import (updateRedisToken,
                                           updateRedisSecretCache,
                                           updateRedisDaliyData,
                                           saveWeekDataRecord,
                                           updateTestData)

schedule = BlockingScheduler(timezone='Asia/Shanghai')

# schedule.add_job(collectionPhishData, 'cron', args=(), hour='*/2')
# schedule.add_job(collectionBotnetData, 'cron', args=(), day='*/1')
# schedule.add_job(collectionC2IntelFeedsData, 'cron', args=(), day='*/1')
schedule.add_job(updateRedisToken, 'cron', args=(), minute='*/3')
schedule.add_job(updateRedisSecretCache, 'cron', args=(), minute='*/30')
schedule.add_job(updateRedisDaliyData, 'cron', args=(), minute='*/30')
schedule.add_job(saveWeekDataRecord, 'cron', args=(), day_of_week='6')
schedule.add_job(updateTestData, 'cron', args=(), day='*/1')

if __name__ == '__main__':
    schedule.start()
