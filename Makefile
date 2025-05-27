install:
	uv sync

collectstatic:
	python hexlet_code/manage.py collectstatic --noinput

migrate:
	python hexlet_code/manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi