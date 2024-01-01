all:
	python3 manage.py makemigrations | lolcat -a -d 1
	python3 manage.py migrate | lolcat -a -d 1
	python3 manage.py collectstatic
	clear
	python3 manage.py runserver $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2 | head -n1):8000 
git:
	git add .
	git commit -m'commit via makefile'
	git push
