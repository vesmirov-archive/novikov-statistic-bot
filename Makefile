make lint:
	poetry run flake8

make start:
	poetry run python bot.py

make schedule:
	poetry run python scheduler.py

prepare:
	poetry run python prepare.py

make update:
	poetry run python updater.py

make notify:
	poetry run python notifier.py
