#!/usr/bin/env bash

set -x

DIR_SCRIPT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DIR_SOURCE="${DIR_SCRIPT}/.."
DIR_BUILD=$PWD

DOCKER_IMAGE="ghcr.io/astral-sh/uv:python3.14-alpine"

DIR_DOCKER_SOURCE="/home/source"
DIR_DOCKER_BUILD="/home/build"

read -r -d '' BUILD_COMMANDS << EOM

cd ${DIR_DOCKER_SOURCE}
uv sync --locked

cd ${DIR_DOCKER_BUILD}
uv run --project ${DIR_DOCKER_SOURCE} ${DIR_DOCKER_SOURCE}/main.py | tee -a log.txt

EOM

docker run --rm \
    -e XAI_API_KEY \
    -e MAILGUN_API_KEY \
    -e MAILING_LIST \
    -e DEBUG \
    -e DEBUG_PROMPT \
    -v "${DIR_SOURCE}:${DIR_DOCKER_SOURCE}:rw" \
    -v "${PWD}:${DIR_DOCKER_BUILD}:rw" \
    "$DOCKER_IMAGE" \
    sh -c "$BUILD_COMMANDS"
