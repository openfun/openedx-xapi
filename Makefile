# Get local user ids
UID              = $(shell id -u)
GID              = $(shell id -g)

# Docker
COMPOSE          = UID=$(UID) GID=$(GID) docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm -e HOME="/tmp"
COMPOSE_EXEC     = $(COMPOSE) exec

# Django
MANAGE           = $(COMPOSE_EXEC) lms python manage.py lms

default: help

bootstrap: build dev migrate superusers ## bootstrap the project

build:  ## build the xapi image
	$(COMPOSE) build lms
.PHONY: build

dev:  ## start the lms service (and its dependencies)
	$(COMPOSE) up -d lms nginx
.PHONY: dev

down:  ## stop & remove all services
	$(COMPOSE) down
.PHONY: stop

logs:  ## get lms service logs
	$(COMPOSE) logs -f lms
.PHONY: logs

migrate:  ## perform database migrations
	$(MANAGE) migrate
.PHONY: migrate

status:  ## an alias for docker-compose ps
	$(COMPOSE) ps
.PHONY: status

stop:  ## stop running services
	$(COMPOSE) stop
.PHONY: stop

superusers:  ## create superusers (Open edX portal & learning locker)
	$(MANAGE) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@foex.edu', 'openedx-rox')";
	$(COMPOSE_EXEC) api node cli/dist/server createSiteAdmin admin@foex.edu foex openedx-rox
.PHONY: superusers

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
