import os
import getpass

from crontab import CronTab

USER = getpass.getuser()


cron = CronTab(user=USER)
cron.env['HOME'] = os.getcwd()
cron.env['PATH'] = os.getcwd()

job = cron.new(command=f'.venv/bin/python notifier.py')
job.minute.every(1)

cron.write()
