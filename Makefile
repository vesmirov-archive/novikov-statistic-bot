lint:
	poetry run flake8

start:
	poetry run python bot.py

schedule:
	poetry run python scheduler.py

prepare:
	poetry run python prepare.py

update:
	poetry run python updater.py

notify:
	poetry run python notifier.py
