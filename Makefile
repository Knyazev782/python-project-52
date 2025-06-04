install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py

build:
	./build.sh

render-start:
	gunicorn --chdir task_manager.wsgi