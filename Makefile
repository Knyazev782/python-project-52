install:
	uv sync

collectstatic:
	python hexlet_code/manage.py collectstatic --noinput

migrate:
	python hexlet_code/manage.py migrate admin zero --fake && python hexlet_code/manage.py migrate task_manager zero --fake && python hexlet_code/manage.py migrate --noinput

build:
	./build.sh

render-start:
	gunicorn --chdir hexlet_code hexlet_code.wsgi