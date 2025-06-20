install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput

build:
	./build.sh

render-start:
	gunicorn --chdir task_manager task_manager.wsgi:application --bind 0.0.0.0:$(PORT)