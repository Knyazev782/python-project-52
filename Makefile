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

test:
	uv sync
	uv run manage.py migrate
	RUNNING_TESTS=1 docker compose -f docker-compose.yml up --abort-on-container-exit