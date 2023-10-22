#!/bin/bash

# This is an example on how to use the Docker image.
# Please make a copy and modify as needed.

OPTIONS=(
  --init
  --mount type=bind,src=/etc/localtime,dst=/etc/localtime,ro
  --mount type=bind,src=/media/vault/videos/dashcam,dst=/workdir
  --name 70mai-m300-toolbox
  --rm
  --workdir /workdir
)

IMAGE=70mai-m300-toolbox

ARGS=(
  --alsologtostderr

  --log_dir=logs
  --verbosity=1

  --token=00000000000000000000000000000000

  --set_audio_recording=true
  --chime_on_boot=false
  --set_date_format=YYYYMMDD
  --set_event_sensitivity=off
  --set_language=english
  --set_recording=true
  --set_time_lapse_recording=false
  --set_timestamp=$(date +'%Y%m%d%H%M%S')
  --set_video_codec=H264
  --set_video_resolution=RES_1920X1080P30
  --set_video_split_time=60
  --set_voice_control=false
  --set_volume=mute
  --set_wifi_on_boot=true
)

docker run "${OPTIONS[@]}" ${IMAGE} "${ARGS[@]}"
