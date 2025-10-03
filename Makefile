hello:
	echo "Hello, World!"

install:
	poetry install

migrations:
	python3 mainsignal/manage.py makemigrations

migrate:
	python3 mainsignal/manage.py migrate

runserver:
	python3 mainsignal/manage.py runserver

env:
	source ./env/bin/activate
