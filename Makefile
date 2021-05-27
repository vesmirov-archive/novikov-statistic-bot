make lint:
	poetry run flake8

make start:
	poetry run python bot.py

make schedule:
	poetry run python scheduler.py
