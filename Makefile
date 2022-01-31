DOCKER:=docker-compose --file docker/docker-compose.yaml

.PHONY: docker-start-db
docker-start-db:
	$(DOCKER) up -d dj-stripe-db


.PHONY: migrate
migrate:
	python manage.py migrate
	python manage.py djstripe_sync_models


.PHONY: dev-createsuperuser
dev-createsuperuser:
	DJANGO_SUPERUSER_PASSWORD=admin \
		python manage.py createsuperuser \
		--username admin \
		--email admin@localhost \
		--noinput
