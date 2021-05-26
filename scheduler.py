from crontab import CronTab

from dotenv import dotenv_values

env = dotenv_values('.env')

USER=env.get('CHRON_USER')

cron = CronTab(user=USER)
job = cron.new(command='.venv/bin/python notifier.py')
job.minute.every(1)

cron.write()
