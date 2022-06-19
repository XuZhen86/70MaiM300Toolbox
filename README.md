# 70Mai M300 Toolbox
A Python CLI application that allows interfacing with the [70Mai M300 dashcam](https://www.70mai.com/m300/).

## Supported Operations
The following operations were reverse engineered from the 70Mai Android APK.

* `format-sd-card`: The same as pressing the button 3 times. The formatting could fail and the LED ring turns red.
* `get-files`: Incrementally download all dashcam footage and organize them locally. Files that are already downloaded and matching file sizes are skipped.
* `get-sd-card-status`: Read SD card status, capacity, and used space.
* `purge-files`: Incrementally delete footage on dashcam. Only the footage that are present locally and matching file sizes are deleted.
* `start-recording`: Start recording. The LED ring turns green.
* `stop-recording`: Stop recording. The LED ring turns blue. Useful when parked in the garage and is downloading footage.
* `sync-time`: Sync to current system time. Double check the container timezone when using this tool in Docker.
* `update-wifi-password`: Create a new 63-char-long Wi-Fi password with mixed uppercase, lowercase, and numbers. The 70Mai app only allows 8-char password and you won't be able to change the password via the app.

## Get the Connect Key
The dashcam requires a `signkey` param on all API calls. The `signkey` is an md5 hash of the command, params, timestamp, and the Connect Key. The different timestamp and the different Connect Key are the reasons why links on [this post](https://dashcamtalk.com/forum/threads/70mai-pro-rtsp-stream-photo-capture.37637/) aren't working.

### Via App Data of the 70Map app
70Map app sores a copy of Connect Key locally.

* Search for ways to get the app data for a particular app.
* Find the file called `LKDB.db`. It's an unencrypted SQLite file.
* Navigate to `CardvrEquipmentDB` table and find the `connectKey` column.

Because the Connect Key is randomly(?) generated everytime when pairing the dashcam with the app, I recommend the next method as it doesn't require infiltrating protected storage areas of the phone.

### Via Wi-Fi package capturing
All data exchange between the app and the dashcam are in plain text HTTP.

* Search for ways to capture Wi-Fi packages.
* Start capturing packages on channel 6.
* Do the normal pairing process.
* Stop capturing.
* Import the .pcap file into Wireshark.
* Configure the Wi-Fi password and Wireshark automatically analyzes the HTTP packages. This step may fail due to incomplete capturing. Try capturing and pairing again.
* Find the request package `GET /cgi-bin/BindByBanya.cgi`.
* Find the response package and its JSON payload. The `Token` field is the Connect Key.

## How to install/use the tool
The tool can be installed locally or built into a Docker image. **The Connect Key is required when using the tool.**

* To install locally
  * Make sure you have Python 3.10 and up.
  * Do `make install`.
  * Do `70mai-m300-toolbox` to verify installation.
* To build the Docker image
  * Do `make docker-image`.
  * See `example.sh` on how to use the Docker image.

## Discussions
### Why doing this?
The 70Mai app requires my precise location to connect to dashcam wifi and I'm not happy with it. Also I want to save all footages without unplugging the SD card.

### Reverse engineering the Android APK?
Yes. I had to read and trace JVM assembly code (.smali), but it's a lot more forgiving than x86 assembly.

### Is there a way to bypass the 70Mai app completely?
Looks like the app is still needed during the initial pairing. It's using a native function when generating the Connect Key.

```
.class public Lcom/banyac/key/BanyacKeyUtils;
.source "BanyacKeyUtils.java"
.method private native sign(JLjava/lang/String;)Ljava/lang/String;
```

### What are the other commands?
Many commands are listed in this class. Although not all commands would work for the model M300.
```
.class public Lcom/banyac/dashcam/b/c;
.source "HisiCommand.java"
```

### Turn on SSH or Telnet?
It would be fantastic if someone could figure this out!
