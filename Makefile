SHELL := /bin/bash

.PHONY: bootstrap deploy status

bootstrap:
	./scripts/minikube-init.sh
	./scripts/tls-init.sh
	./scripts/db-init.sh

deploy:
	kubectl apply -k k8s/overlays/dev

status:
	kubectl get ns
	kubectl -n ingress-nginx get pods
	kubectl -n client-wp get all
	kubectl -n client-pts get all
