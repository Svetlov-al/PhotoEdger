# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/unit /tests/integration /tests/e2e

unit-tests:
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/unit

integration-tests: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/integration

e2e-tests: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/e2e

logs:
	docker-compose logs --tail=25 api redis_pubsub

black:
	black -l 86 $$(find * -name '*.py')

run:
	docker exec -d backend uvicorn src.image.core.main:app --host 0.0.0.0 --port 8000 --reload

upgrade:
	docker exec -d backend alembic upgrade head

downgrade:
	docker exec -d backend alembic downgrade -1