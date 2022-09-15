from yinglong_server import app
from flask_script import Manager, Server
#from apscheduler.schedulers.background import BackgroundScheduler
#from yinglong_backend.collection_data import (collectionPhishData,
#                                              collectionBotnetData)

manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("127.0.0.1", port=8000))

#schedule = BackgroundScheduler(timezone='Asia/Shanghai')

#schedule.add_job(collectionPhishData, 'cron', args=(), hour='*/2')
#schedule.add_job(collectionBotnetData, 'cron', args=(), day='*/1')

if __name__ == '__main__':
    #schedule.start()
    manager.run()
