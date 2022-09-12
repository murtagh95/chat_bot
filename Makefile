all: up

TEST_PATH=./app/tests
CONTAINER := docker compose -f docker-compose.yml
CONTAINER_SERVER := server

init:
	pip install poetry
	poetry install

pre-commit:
	pre-commit install

black:
	black app/

test:
	export API_TEST=1
	python -m pytest --cov=app --verbose --color=yes $(TEST_PATH)


build:
	$(CONTAINER) build

up:
	$(CONTAINER) up -d

logs:
	$(CONTAINER) logs --tail=$(or $(tail), "50") -f $(or $(container), $(CONTAINER_SERVER))

add-depen:
	$(CONTAINER) exec server poetry add $(filter-out $@,$(MAKECMDGOALS))

down:
	$(CONTAINER) stop
	$(CONTAINER) down

down-delete:
	$(CONTAINER) stop
	$(CONTAINER) down -v --remove-orphans

ps:
	$(CONTAINER) ps
