all:
	python3 manage.py makemigrations
	python3 manage.py migrate
	clear
	python3 manage.py runserver $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2 | head -n1):8000