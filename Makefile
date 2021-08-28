export FLASK_APP=gurella
export FLASK_ENV=development

all: run

run:
	python3 -m flask run

init-db-migrations:
	flask db init

create-db-migration:
	./create_migrations.sh

run-db-migrations:
	flask db upgrade

