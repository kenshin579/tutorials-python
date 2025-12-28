REGISTRY 	:= kenshin579
APP    		:= advenoh
TAG         := python-web-hello
IMAGE       := $(REGISTRY)/$(APP):$(TAG)
PLATFORM	:= linux/x86-64

.PHONY: docker-build
docker-build:
	@docker build --platform $(PLATFORM) -t $(IMAGE) -f Dockerfile .

.PHONY: docker-push
docker-push: docker-build
	@docker push $(IMAGE)

.PHONY: freeze-build
freeze-build:
	@pip3 freeze > requirements.txt
