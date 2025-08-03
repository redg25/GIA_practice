# Buildozer Docker Setup

This repository contains a Docker-based setup for building Android APKs using Buildozer and Kivy.

## Prerequisites

- Docker installed on your system
- Android device or emulator for testing (optional)
- ADB (Android Debug Bridge) installed for device connectivity

## Quick Start

### 1. Build the Docker Image

```bash
docker build --tag=kivy/buildozer .
```

### 2. Run the Container

```bash
docker run --interactive --tty --rm \
  --volume "$HOME/.buildozer":/home/user/.buildozer \
  --volume "$PWD":/home/user/hostcwd \
  --entrypoint /bin/bash \
  kivy/buildozer
```

### 3. Check Connected Devices (Optional)

```bash
adb devices
```

Use this command to verify that your Android device is properly connected and recognized.

## Usage

### Building the APK

Once inside the container, you can run standard Buildozer commands:

```bash
buildozer android debug
buildozer android release
```

### Installing and Testing the APK

1. **Navigate to the bin directory:**
   ```bash
   cd bin
   ```

2. **Check connected devices:**
   ```bash
   adb devices
   ```

3. **Install the APK to your device:**
   ```bash
   adb -s <devices> install myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
   ```
   
   Replace `<devices>` with your actual device ID from the `adb devices` output.

4. **Monitor app logs (debugging):**
   ```bash
   adb -s <devices> logcat *:S python:D
   ```
   
   This shows only Python-related debug logs, filtering out system noise.