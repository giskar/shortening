init:
	docker image build -t short-url  .

.PHONY: init

start:
	docker run --name some-short-url -p 8000:8000 -d short-url

.PHONY: start
