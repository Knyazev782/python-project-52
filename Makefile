install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

test:
	python manage.py migrate
	pytest