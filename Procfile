web: APP_SETTINGS=trace.config.PRODUCTION python -m flask run --host=0.0.0.0
dev: python -m flask run --host=0.0.0.0
shell: PROD=1; python -m flask shell
build: docker build -t api .
docker: bin/docker
install: pip install -r requirements.txt
env: . bin/env
test: export APP_SETTINGS=trace.config.Test; python test.py
lint: pylint ./trace
psql: psql -h mytrace-db.c1yc0fhyowtw.us-west-1.rds.amazonaws.com -U azai91 -d mytrace_db
test_services: export APP_SETTINGS=trace.config.Test; ./env/bin/pytest -v tests
update_reqs: pip freeze > requirements.txt