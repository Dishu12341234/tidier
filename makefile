all:
	python3 manage.py makemigrations | lolcat -a -d 1
	python3 manage.py migrate | lolcat -a -d 1
	clear
	python3 manage.py collectstatic | lolcat -a -d 1
	python3 manage.py runserver $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2 | head -n1):8000  | lolcat -a -d 1
git:
	git add . | lolcat -a -d 1
	git commit -m'commit via makefile' | lolcat -a -d 1
	git push | lolcat -a -d 1
