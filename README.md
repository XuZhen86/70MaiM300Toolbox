# 70Mai M300 Toolbox

A Python CLI script that allows interfacing with the [70Mai M300 dashcam](https://www.70mai.com/m300/). This script covers most features that the phone app offers.

Last tested with `'softversion': '1.0.2ww', 'softversion_date': '2021.8.03'`.

## Initial Pairing

A 32-char hex string is required for all interactions with the dashcam.
The string is generated when pairing the dashcam with the 70Mai phone app.
Wi-Fi package sniffing is required for intercept the token.
The token is also stored in the app's local storage, and would require infiltrating the phone's secure storage.
I've reverse engineered the pairing process and the token can now be generated without the phone app.
Note that because the phone app doesn't know the token, you have to re-pair the dashcam with the phone app before you can use it with the phone app again. Follow the steps for the initial pairing:

1. Connect to the dashcam Wi-Fi. The default password is `12345678`.
2. Choose a random 32-char hex string as the seed token. You can search Google for "random hex string generator".
3. Run the following command and follow dashcam prompt to click the side button for confirmation.

```
70mai-m300-toolbox --token=<seed_token> --generate_token
```

4. The new 32-char hex token should be printed. Save this token and use it for all subsequent interactions.

## Downloading Files

The script downloads video files from the dashcam and saves the video files to local disk.
The files are organized into the folder structure `file_type_dir/YYYYMMDD/file.mp4` and the file type directory names must be supplied with flag `--file_type_dirs`.
The script deletes the downloaded file from the dashcam if flag `--purge_after_download` is supplied. The file is purged if there's a local file that has the same size.

```
70mai-m300-toolbox \
  --token=<token> \
  --get_files \
  --file_type_dirs=Normal \
  --file_type_dirs=Unknown1 \
  --file_type_dirs=Parking \
  --file_type_dirs=Unknown3 \
  --file_type_dirs=Unknown4 \
  --file_type_dirs=TimeLapse \
  --purge_after_download
```

If needed, use the following flags to print the number of files or the list of files instead of downloading them.
* `--get_file_count`: Prints the number of files under each category.
* `--get_file_entries=0`: Prints the file list for a specific category. The example is for category 0. Change the number to print for other categories.

## SD Card

* `--format_sd_card`: Wipes the SD card. Note that the formatting could fail for unknown reasons, and manual unplug and re-plug is needed.
* `--get_sd_card_status`: Prints the SD card status. The status includes the state, total capacity in MB, and used capacity in MB. Note that the used capacity does not include the file that is being actively written to.

## Wi-Fi

* `--set_wifi_password=<new_password>`: Sets a new Wi-Fi password. The password must be between 8 and 63 characters in length. The Wi-Fi disconnects after setting the new password and you need to re-connect to the dashcam Wi-Fi with the new password. Note that the phone app restricts the password length to 8 and the password cannot be changed from the app if the new password is longer than 8.
* `--set_wifi_on_boot=<true|false>`: Sets if Wi-Fi is enabled when the dashcam is turned on.

## Reading Status

* `--[no]get_parking_wire` Query if a parking wire is detected. A parking wire is required for the time lapse mode.
* `--[no]get_settings` Reads all settings.

## Other Settings

* `--[no]reset`: Resets the dashcam to factory default settings. Wi-Fi password would resets to "12345678" and it would require generating a new token.
* `--[no]set_audio_recording`: Sets if audio is recorded with the video.
* `--set_auto_off_time`: Sets the time in minutes before turning off if the vehicle stays stationary. It is helpful when the dashcam is wired to a power supply that does not turn off when the car is off. Once automatically turned off, the dashcam must be manually turned on by clicking the power button. Setting the value to 0 causes the dashcam to turn off immediately after booting up. If this happens, click the reset button to turn it on, then click the reset button immediately when the blue light turns off. It may take a few tries to get it to work.
  (an integer in the range [1, 2147483647])
* `--[no]set_chime_on_boot`: Sets if a chime is played when the dashcam is turned on.
* `--set_date_format=<yyyymmdd|ddmmyyyy|mmddyyyy>`: Sets the format of the date in the video watermark.
* `--set_event_sensitivity=<off|low|mid|high>`: Sets the acceleration sensitivity for an event recording to start. This feature is usually advertized as "Collision Recording", based on the assumption that significant acceleration can be measured during a collision. High sensitivity means a mild acceleration would trigger the event. The videos are saved to the Event folder and will not be overwritten.
* `--set_flicker_frequency: <freq_60hz|freq_55hz|freq_50hz>`: Sets the local power line frequency for flicker resistance.
* `--set_language=<english|russian|japanese|korean|spanish|portuguese|traditional_chinese|polish|thai>`: Sets the language of the voice announcements.
* `--[no]set_recording`: Continue or pause the recording. The dashcam keeps recording while the data is being transferred, and the files may not stay static. It can be helpful to stop the recording during a data transfer to mitigate this issue. It also saves car battery when not recording and is helpful when the car is parked in a garage.
* `--[no]set_time_lapse_recording`: Turn the time lapse recording on or off. The dashcam can continue to record time lapse videos when the vehicle is parked. 1 frame is captured each second and the outputted video is in 30fps.The parking wire needs to be detected before entering time lapse recording.
* `--set_timestamp`: Sets the current timestamp. The timestamp shown in the video will always equal to the timestamp set here. The dashcam does not have a concept of timezone, and the timestamp has to be updated when the timezone or Daylight Saving Time changes. Supply a timestamp in the format of "%Y%m%d%H%M%S". Use $(date +'%Y%m%d%H%M%S') to generate the timestamp. Supply "-" to automatically generate the timestamp. Please double check the timezone of the operating system or container, so the correct timestamp is generated.
* `--set_video_codec=<h264|hevc>`: Sets the video codec.
* `--set_video_resolution=<res_1920x1080p30|res_2304x1296p30>`: Sets the video resolution.
* `--set_video_split_time`: Sets the max length in seconds of the video files. The max video length is bounded by the max file size of the FAT32 file system. At 35:35, H264 1080p recording reaches the maximum 4GB file size. The API does not return accurate file sizes for >2GB files. Setting the value to less than 1020 (that is 17 minutes) is recommended.
  (an integer in the range [60, 2135])
* `--[no]set_voice_control`: Enable or disable voice control.
* `--set_volume=<high|mid|low|mute>`: Sets the speaker volume. Mute disables all sound output and the only indicator of dashcam operation is the light ring.

## Sending Commands Manually

The following flags are available for manually sending a command with optional params. The `--token` flag is still required, and the script automatically appends the `-timestamp` and the `-signkey` params before sending. Assuming the signkey algorithm is the same, this can be used for interfacing with other 70Mai dashcam models.

* `--send_command`: Manually send a command, useful for debugging. -timestamp and -signkey will be added automatically. The text payload will be printed.
* `--with_params`: The optional params to be sent with the command. Must be a JSON-formatted object that can be decoded into type "dict[str, str | int]". This flag is ignored unless --send_command is set.
  (default: '{}')
* `--[no]pretty_print_result`: Print the result with pprint() instead of print().
  (default: 'true')

For example:

```
70mai-m300-toolbox \
  --token=<token> \
  --send_command=CommandWithoutParams.cgi

70mai-m300-toolbox \
  --token=<token> \
  --send_command=CommandWithParams.cgi \
  --with_params='{"str_key_1": "str_value_1", "str_key_2": 2, "str_key_3": "str_value_3"}'
```

## Docker

I highly recommend running the script in Docker, just to keep the installed Python packages tidy.
The Docker image should be built locally.
See `Makefile` for building an image.
See `docker-example.sh` for running the container.

## Reverse Engineering :)

Take a look at the `reverse_engineering` folder.
The commands can be de-compiled from the Android APK.
The pairing process was implemented in C++ and required some hack to figuring it out.

Please file an issue for adding a new command or tweaking an existing command.

## Disclaimer

This project is for educational purpose only. The author of this project assumes no responsibility or liability for any errors or omissions in the content of this project. The information contained in this project is provided on an "as is" basis with no guarantees of completeness, accuracy, usefulness or timeliness.
