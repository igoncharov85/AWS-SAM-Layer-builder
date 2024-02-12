#!/bin/bash

set -ex

PYTHON_VERSION=${1:-3.12}
DOCKER_IMAGE="public.ecr.aws/sam/build-python${PYTHON_VERSION}:latest"
DOCKER_ARCHITECTURE="-x86_64"
PYTHON_PACKAGE_FOLDER="python"
PIP="pip"

docker run -v $(pwd):/var/task ${DOCKER_IMAGE}${DOCKER_ARCHITECTURE} sh -c \
"${PIP} install --root-user-action=ignore --upgrade pip && ${PIP} install --root-user-action=ignore -r requirements.txt -t ${PYTHON_PACKAGE_FOLDER}"

zip -9 -r layers/aws-lambda-layer-${PYTHON_VERSION}${DOCKER_ARCHITECTURE}.zip ${PYTHON_PACKAGE_FOLDER}