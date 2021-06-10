"""
    Schedules notifications and sheetsupdates
"""

import os
import getpass

from crontab import CronTab

USER = getpass.getuser()


def main():
    """Schedule notifications and updates via Crontab"""

    cron = CronTab(user=USER)
    cron.env['HOME'] = f'/home/{USER}'
    cwd = os.getcwd()

    notify = cron.new(command=f'{cwd}/.venv/bin/python {cwd}/notifier.py')
    notify.setall('0 22 * * *')

    update = cron.new(command=f'{cwd}/.venv/bin/python {cwd}/updater.py')
    update.setall('0 20 * * *')

    cron.write()


if __name__ == '__main__':
    main()
