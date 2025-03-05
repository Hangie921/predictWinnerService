.PHONY: venv check_venv_is_activated

venv:
	python3 -m venv venv
	source "./venv/bin/activate"
	pip3 install -r requirements.txt

start_db:
	postgres -D /opt/homebrew/var/postgresql@14
	
check_venv_is_activated:
	which python3

activate_env:
	source venv/bin/activate

start_backend: check_venv_is_activated
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py runserver