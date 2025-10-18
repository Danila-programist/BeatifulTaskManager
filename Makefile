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

backend_env:  ##@Environment Activate Poetry shell for backend
	cd backend && poetry shell

env_file: ##@Environment Create or update .env file
	$(eval SHELL:=/bin/bash)
	if [ ! -f .env ]; then \
		cp .env.example .env; \
	elif ! cmp -s .env .env.example; then \
		cp .env.example .env; \
	fi

up:  ##@Docker Start docker-compose services
	docker-compose up -d  

down:  ##@Docker Stop docker-compose services
	docker-compose down

logs:   ##@Docker Show logs from docker-compose
	docker-compose logs -f

rebuild:  ##@Docker Rebuild and restart services
	docker-compose down && docker-compose up -d --build

test_backend: ##@Testing Run tests for backend
	cd backend && poetry run pytest -v

test-cov_backend: ##@Testing Run tests with coverage for backend
	cd backend && poetry run pytest --cov=. --cov-report=term:skip-covered

format:   ##@Code Format code with black
	cd backend && poetry run black .

lint: ##@Code Lint code with pylint
	cd backend && poetry run pylint app main.py tests

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

%::
	@echo $(MESSAGE)

PHONY: up down backend_env help rebuild logs format test-cov_backend test_backend lint