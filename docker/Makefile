

VERSION = 0.2.0.4

ORG = yesworkflow
REPO = yw-noworkflow
IMAGE = ${ORG}/${REPO}

build:
	echo Build untagged image so that it is automatically tagged 'latest'
	docker build -t ${IMAGE} .
	echo Tag new image with current version number: ${VERSION}
	docker tag ${IMAGE} ${IMAGE}:${VERSION}

push:
	echo Push to Docker Hub the specified version of the image: ${VERSION}
	docker push ${IMAGE}:${VERSION}

pull:
	echo Pull from Docker Hub the specified version of the image: ${VERSION}
	docker pull ${IMAGE}:${VERSION}

run:
	echo Interactively run the specified version of the image: ${VERSION}
	docker run -it ${IMAGE}:${VERSION}
