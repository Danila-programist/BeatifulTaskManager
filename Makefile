HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
	print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
	@{$$help{$$_}},"\n" for keys %help;

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command. Use 'make help' for list of commands."
else
MESSAGE = "Done"
endif

include .env
export


backend_env:  ##@Environment Activate Poetry shell for backend
	cd backend && poetry shell

env_file: ##@Environment Create or update .env file
	$(eval SHELL:=/bin/bash)
	if [ ! -f .env ]; then \
		cp .env.example .env; \
	elif ! cmp -s .env .env.example; then \
		cp .env.example .env; \
	fi

up: build_frontend ##@Docker Start docker-compose services
	docker-compose up -d  

down:  ##@Docker Stop docker-compose services
	docker-compose down

logs:   ##@Docker Show logs from docker-compose
	docker-compose logs -f

rebuild: build_frontend ##@Docker Rebuild and restart services
	docker-compose down && docker-compose up -d --build

psql:  ##@Database Open PostgreSQL inside docker container
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(DB_NAME) -U $(DB_USER)

revision:  ##@Database Create Alembic revision local
	cd backend && poetry run alembic revision --autogenerate

migration:  ##@Database Apply Alembic migrations local
	cd backend && poetry run alembic upgrade head

test_backend: test-db-down test-db ##@Testing Run tests for backend
	cd backend && TESTING=1 poetry run pytest -v && cd .. && make test-db-down

test-cov_backend: test-db-down test-db ##@Testing Run tests with coverage for backend
	cd backend && TESTING=1 poetry run pytest --cov=. --cov-report=term:skip-covered && cd .. && make test-db-down

test-db: ##@Testing Apply test-db for backend
	docker-compose -f docker-compose.test.yml up -d
	@echo "Waiting for test_db to become healthy..."
	@for i in $$(seq 1 60); do \
		status=$$(docker inspect --format='{{.State.Health.Status}}' test_db 2>/dev/null || echo unknown); \
		echo "health: $$status"; \
		if [ "$$status" = "healthy" ]; then echo "test_db healthy"; exit 0; fi; \
		sleep 1; \
	done; echo "test_db failed to become healthy" && docker logs test_db && exit 1

test-db-down: ##@Testing Remove test-db for backend
	docker-compose -f docker-compose.test.yml down -v --remove-orphans

format:   ##@Code Format code with black for backend
	cd backend && poetry run black .

lint: ##@Code Lint code with pylint for backend
	cd backend && poetry run pylint app main.py tests

help: ##@Help Show this help 
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

clean: ##@Code Remove Python cache files and directories
	@echo "Cleaning Python cache files..."
	@echo "Removing __pycache__ directories with sudo..."
	@for dir in $$(find . -type d -name "__pycache__"); do \
		echo "Removing: $$dir"; \
		sudo rm -rf "$$dir"; \
	done
	@rm -rf backend/.coverage 2>/dev/null || true
	@rm -rf backend/.pytest_cache 2>/dev/null || true
	@echo "Python cache cleaned!"
	
build_frontend: ##@Frontend Build frontend (npm install + npm run build)
	cd frontend && npm install && npm run build

%::
	@echo $(MESSAGE)

PHONY: up down backend_env help rebuild logs format test-cov_backend test_backend lint env_file test-db clean build_frontend