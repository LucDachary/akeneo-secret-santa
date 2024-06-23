build:
	docker-compose build

up:
	docker-compose up -d --force-recreate
	sleep 1
	docker-compose exec webapp python manage.py migrate
	docker-compose exec webapp python manage.py loaddata draw
	docker-compose exec webapp python manage.py loaddata pair

clean:
	docker-compose down -v --remove-orphans
