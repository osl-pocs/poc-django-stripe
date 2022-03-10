DOCKER=docker-compose --env-file .env --file docker/docker-compose.yaml

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py makemigrations payments
	python manage.py migrate
	python manage.py djstripe_init_customers
	python manage.py djstripe_sync_models
	python manage.py djstripe_sync_plans_from_stripe


.PHONY: dev-createsuperuser
dev-createsuperuser:
	DJANGO_SUPERUSER_PASSWORD=admin \
		python manage.py createsuperuser \
		--username admin \
		--email admin@localhost \
		--noinput

.PHONY: run-tests
run-tests:
	pytest


.PHONY: run-server
run-server:
	python manage.py runserver


# DOCKER

.PHONY:docker-build
docker-build:
	$(DOCKER) build
	$(DOCKER) pull


.PHONY:docker-start
docker-start:
	$(DOCKER) up -d ${SERVICES}


.PHONY:docker-stop
docker-stop:
	$(DOCKER) stop ${SERVICES}


.PHONY:docker-restart
docker-restart: docker-stop docker-start
	echo "[II] Docker services restarted!"


.PHONY:docker-logs
docker-logs:
	$(DOCKER) logs --follow --tail 100 ${SERVICES}

.PHONY: docker-wait
docker-wait:
	echo ${SERVICES} | xargs -t -n1 ./docker/healthcheck.sh

.PHONY:docker-dev-prepare-db
docker-dev-prepare-db:
	# used for development
	$(DOCKER) exec -T epigraphhub bash /opt/EpiGraphHub/docker/prepare-db.sh


.PHONY:docker-run-cron
docker-run-cron:
	$(DOCKER) exec -T ${SERVICE} bash /opt/EpiGraphHub/Data_Collection/CRON_scripts/owid.sh
	$(DOCKER) exec -T ${SERVICE} bash /opt/EpiGraphHub/Data_Collection/CRON_scripts/foph.sh
	# $(DOCKER) exec -T ${SERVICE} bash /opt/EpiGraphHub/Data_Collection/CRON_scripts/forecast.sh


.PHONY:docker-bash
docker-bash:
	$(DOCKER) exec ${SERVICE} bash

.PHONY:docker-run-bash
docker-run-bash:
	$(DOCKER) run --rm ${SERVICE} bash
