install:
	uv sync

collectstatic:
	python python-project-52/hexlet_code/manage.py collectstatic --noinput

migrate:
	python python-project-52/hexlet_code/manage.py migrate admin zero --fake && python python-project-52/hexlet_code/manage.py migrate task_manager zero --fake && python python-project-52/hexlet_code/manage.py migrate --noinput

build:
	./build.sh

render-start:
	gunicorn --chdir python-project-52/hexlet_code hexlet_code.wsgi

