all:
	python3 manage.py makemigrations
	python3 manage.py migrate
	clear
	python3 manage.py runserver 192.168.1.29:8000