install:
	uv sync

collectstatic:
	python python-project-52/hexlet_code/manage.py collectstatic --noinput

migrate:
	python python-project-52/hexlet_code/manage.py migrate

build:
	./build.sh

render-start:
	gunicorn --chdir python-project-52/hexlet_code hexlet_code.wsgi

