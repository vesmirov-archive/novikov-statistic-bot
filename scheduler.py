import os
import getpass

from crontab import CronTab

USER = getpass.getuser()


cron = CronTab(user=USER)
cron.env['PATH'] = f'/home/{USER}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'  # noqa

cwd = os.getcwd()

notify = cron.new(command=f'{cwd}/.venv/bin/python {cwd}/notifier.py')
notify.setall('0 22 * * *')

update = cron.new(command=f'{cwd}/.venv/bin/python {cwd}/updater.py')
update.setall('0 20 * * *')

cron.write()
