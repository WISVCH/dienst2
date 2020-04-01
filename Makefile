help: # Shows all commands
	@echo 'All Makefile commands'
	@cat Makefile | grep -v '^\W'

bootstrap: # Copies the default
	cp .env.example .env
	cp sqreen.yaml.example sqreen.yaml

dev: # Runs the Gin server
	go run . server --verbose

migrateup: # Runs the database migrations up
	go run . migrate --direction up --verbose

migratedown: # Runs the database migrations down
	go run . migrate --direction down --verbose

newdb: # Migrates db down and up - WARNING: ALL DB DATA IS DELETED
	make migratedown
	make migrateup

build: # Runs the Golang build
	go build

test: # Runs the unit tests
	go test ./...
