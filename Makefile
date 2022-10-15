init:
	mkdir -p postgres-data

build:
	docker-compose build

dev:
	docker-compose up -d db web

logs:
	docker-compose logs --follow web

clean:
	docker-compose stop
	docker-compose rm -f

makemigrations:
	docker-compose exec web ./manage.py makemigrations

migrate:
	docker-compose exec web ./manage.py migrate

createsuperuser:
	docker-compose exec web ./manage.py createsuperuser

shell:
	docker-compose exec web ./manage.py shell

shellplus:
	docker-compose exec web ./manage.py shell_plus

dbshell:
	docker-compose exec web ./manage.py dbshell

bash:
	docker-compose exec web bash


