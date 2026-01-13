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
uv run main.py | tee ${DIR_DOCKER_BUILD}/output.md

EOM

docker run --rm \
    -u `id -u`:`id -g` \
    -v "${DIR_SOURCE}:${DIR_DOCKER_SOURCE}:rw" \
    -v "${PWD}:${DIR_DOCKER_BUILD}:rw" \
    "$DOCKER_IMAGE" \
    sh -c "$BUILD_COMMANDS"
