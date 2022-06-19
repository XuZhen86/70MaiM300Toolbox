#!/bin/bash

# This is an example on how to use the Docker image.
# Please make a copy and modify as needed.

OPTIONS=(
  --init
  --mount type=bind,src=/etc/localtime,dst=/etc/localtime,ro
  --mount type=bind,src=/media/vault/videos/dashcam,dst=/mnt
  --name 70mai-m300-toolbox
  --rm
  --workdir /mnt
)

IMAGE=70mai-m300-toolbox

ARGS=(
  --alsologtostderr
  --connect_key=0123456789abcdef0123456789abcdef
  --log_dir=logs
  --verbosity=1

  --operations=stop-recording
  --operations=get-sd-card-status
  --operations=get-files
  --operations=purge-files
  --operations=get-sd-card-status
  --operations=sync-time
  --operations=start-recording
)

docker run "${OPTIONS[@]}" ${IMAGE} "${ARGS[@]}"
