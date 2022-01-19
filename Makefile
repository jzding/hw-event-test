.PHONY: build-docker

# Current  version
VERSION ?=latest

# Default image tag
PROXY_IMG ?= quay.io/redhat_emp1/hw-event-proxy:$(VERSION)
SIDECAR_IMG ?= quay.io/redhat_emp1/cloud-event-proxy:$(VERSION)
CONSUMER_IMG ?= quay.io/redhat_emp1/cloud-native-event-consumer:$(VERSION)

# Export GO111MODULE=on to enable project to be built from within GOPATH/src
export GO111MODULE=on
export CGO_ENABLED=0

ifeq (,$(shell go env GOBIN))
  GOBIN=$(shell go env GOPATH)/bin
else
  GOBIN=$(shell go env GOBIN)
endif

export COMMON_GO_ARGS=-race

build:
	go fmt ./...
	make lint
	go build -o ./build/redfish-event-test cmd/main.go

run:
	go run cmd/main.go

lint:
	golint `go list ./... | grep -v vendor`
	golangci-lint run


kustomize:
ifeq (, $(shell which kustomize))
		@{ \
		set -e ;\
		KUSTOMIZE_GEN_TMP_DIR=$$(mktemp -d) ;\
		cd $$KUSTOMIZE_GEN_TMP_DIR ;\
		go mod init tmp ;\
		go get sigs.k8s.io/kustomize/kustomize/v3@v3.5.4 ;\
		rm -rf $$KUSTOMIZE_GEN_TMP_DIR ;\
		}
KUSTOMIZE=$(GOBIN)/kustomize
else
KUSTOMIZE=$(shell which kustomize)
endif

# Deploy all in the configured Kubernetes cluster in ~/.kube/config
deploy-example:kustomize
	cd ./manifests && $(KUSTOMIZE) edit set image hw-event-proxy=${PROXY_IMG} && $(KUSTOMIZE) edit set image cloud-event-proxy=${SIDECAR_IMG} && $(KUSTOMIZE) edit set image  cloud-native-event-consumer=${CONSUMER_IMG}
	$(KUSTOMIZE) build ./manifests | kubectl apply -f -

# Deploy all in the configured Kubernetes cluster in ~/.kube/config
undeploy-example:kustomize
	cd ./manifests && $(KUSTOMIZE) edit set image hw-event-proxy=${PROXY_IMG} && $(KUSTOMIZE) edit set image cloud-event-proxy=${SIDECAR_IMG} && $(KUSTOMIZE) edit set image cloud-native-event-consumer=${CONSUMER_IMG}
	$(KUSTOMIZE) build ./manifests | kubectl delete -f -
