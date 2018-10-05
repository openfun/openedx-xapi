# Get local user ids
UID              = $(shell id -u)
GID              = $(shell id -g)

# Docker
COMPOSE          = UID=$(UID) GID=$(GID) docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm -e HOME="/tmp"
COMPOSE_EXEC     = $(COMPOSE) exec

# Django
MANAGE           = $(COMPOSE_RUN) lms python manage.py lms

default: help

bootstrap: build migrate ## bootstrap the project

build:  ## build the xapi image
	$(COMPOSE) build lms
.PHONY: build

dev:  ## start the lms service (and its dependencies)
	$(COMPOSE) up -d lms
.PHONY: dev

logs:  ## get lms service logs
	$(COMPOSE) logs -f lms
.PHONY: logs

migrate:  ## perform database migrations
	$(MANAGE) migrate
.PHONY: migrate

stop:  ## stop running services
	$(COMPOSE) stop
.PHONY: stop

superuser:  ## create a super user
	$(MANAGE) createsuperuser
.PHONY: superuser

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
