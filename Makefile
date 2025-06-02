install:
	uv sync

collectstatic:
	python hexlet_code/manage.py collectstatic --noinput

migrate:
	python hexlet_code/manage.py migrate

build:
	./build.sh

render-start:
	gunicorn --chdir hexlet_code hexlet_code.wsgi

