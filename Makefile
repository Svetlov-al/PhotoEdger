build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

test:
	docker compose exec -it backend pytest -v

unit-tests: up
	docker compose run --rm --no-deps --entrypoint=pytest backend /tests/unit

integration-tests: up
	docker compose run --rm --no-deps --entrypoint=pytest backend /tests/integration

e2e-tests: up
	@docker exec -d backend uvicorn src.image.core.main:app --host 0.0.0.0 --port 8000
	docker compose run --rm --no-deps --entrypoint=pytest backend /tests/e2e

logs:
	docker compose logs --tail=25 redis_pubsub

black:
	black -l 86 $$(find * -name '*.py')

run:
	@docker exec -d backend uvicorn src.image.core.main:app --host 0.0.0.0 --port 8000
	@echo "Сервер запущен!"
upgrade:
	docker exec -d backend alembic upgrade head
	@echo "Таблицы созданы!"

downgrade:
	docker exec -d backend alembic downgrade -1