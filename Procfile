web: python -m flask run --host=0.0.0.0
shell: python -m flask shell
build: docker build -t api .
docker: bin/docker
install: pip install -r requirements.txt
env: . bin/env
test: export APP_SETTINGS=trace.config.Test; python test.py
lint: pylint ./trace

