import os
import getpass

from crontab import CronTab

USER = getpass.getuser()


cron = CronTab(user=USER)
PATH = os.getcwd()

notify = cron.new(command=f'{PATH}/.venv/bin/python notifier.py')
notify.setall('0 22 * * *')

update = cron.new(command=f'{PATH}/.venv/bin/python updater.py')
update.setall('0 20 * * *')

cron.write()
