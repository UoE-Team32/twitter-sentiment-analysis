.PHONY: default
default: local

build:
	docker-compose build

local: build
	docker-compose up -d

logs:
	docker-compose logs
