# V4L2 OBSBOT Camera Control Guide for Debian

## Overview

This guide covers controlling OBSBOT cameras on Debian systems using Video4Linux2 (v4l2) utilities. The OBSBOT Tail Air operates as a UVC (USB Video Class) device and can be controlled through v4l2 commands.

## Prerequisites

```bash
# Install required packages
sudo apt-get update
sudo apt-get install v4l-utils vlc

# Optional but recommended tools
sudo apt-get install uvcdynctrl
```

## Device Setup

### Verify Camera Detection

```bash
# List all video devices
v4l2-ctl --list-devices

# Look for OBSBOT Tail Air output similar to:
OBSBOT Tail Air: OBSBOT Tail Ai (usb-0000:00:14.0-3.4):
        /dev/video9
        /dev/video10
```

### Set Permissions

```bash
# Add user to video group
sudo usermod -a -G video $USER

# Set device permissions
sudo chmod 666 /dev/video9
sudo chmod 666 /dev/video10
```

## Camera Controls

### List Available Controls
```bash
v4l2-ctl -d /dev/video9 --list-ctrls

# Key controls available:
# pan_absolute: -468000 to 468000
# tilt_absolute: -324000 to 324000
# zoom_absolute: 0 to 100
```

### Basic Commands

```bash
# Center camera
v4l2-ctl -d /dev/video9 --set-ctrl=pan_absolute=0
v4l2-ctl -d /dev/video9 --set-ctrl=tilt_absolute=0
v4l2-ctl -d /dev/video9 --set-ctrl=zoom_absolute=0

# Pan right/left
v4l2-ctl -d /dev/video9 --set-ctrl=pan_absolute=100000  # right
v4l2-ctl -d /dev/video9 --set-ctrl=pan_absolute=-100000 # left

# Tilt up/down
v4l2-ctl -d /dev/video9 --set-ctrl=tilt_absolute=100000  # up
v4l2-ctl -d /dev/video9 --set-ctrl=tilt_absolute=-100000 # down

# Set zoom level
v4l2-ctl -d /dev/video9 --set-ctrl=zoom_absolute=50  # 50% zoom
```

### Preview Camera

```bash
# Using VLC
vlc v4l2:///dev/video9

# Using FFplay
ffplay /dev/video9

# Using v4l2-ctl
v4l2-ctl -d /dev/video9 --stream-mmap --stream-to=- | ffplay -i -
```

## Camera Modes

### Switch to UVC Mode
The camera must be in UVC mode for these controls to work:
1. Hold mode button (3 dots) on camera
2. Wait for mode switch indication
3. Camera will appear as UVC device

### Video Formats

```bash
# List supported formats
v4l2-ctl -d /dev/video9 --list-formats-ext

# Supported formats include:
# - MJPG (Motion-JPEG)
# - YUYV
# - H264
```

## Troubleshooting

### Common Issues

1. "Bad file descriptor" errors:
```bash
# Reload uvcvideo module
sudo modprobe -r uvcvideo
sudo modprobe uvcvideo nodrop=1
```

2. Permission denied:
```bash
# Check group membership
groups
# Add to video group if needed
sudo usermod -a -G video $USER
# Log out and back in
```

3. Camera not detected:
```bash
# Check USB connection
lsusb | grep OBSBOT
# Check video devices
ls -l /dev/video*
```

### Debug Information

```bash
# Get detailed device info
udevadm info -a -n /dev/video9

# Check kernel messages
dmesg | grep -i uvc

# Monitor device controls
v4l2-ctl -d /dev/video9 --all
```

## Advanced Usage

### Custom Control Scripts

Example bash function for common movements:
```bash
obsbot_center() {
    v4l2-ctl -d /dev/video9 --set-ctrl=pan_absolute=0
    v4l2-ctl -d /dev/video9 --set-ctrl=tilt_absolute=0
    v4l2-ctl -d /dev/video9 --set-ctrl=zoom_absolute=0
}
```

### UVC Extension Units

The OBSBOT uses UVC extension units for advanced controls. Access these with:
```bash
uvcdynctrl -d /dev/video9 -L
```

## References

- [V4L2 Documentation](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/v4l2.html)
- [UVC Protocol](https://www.usb.org/document-library/video-class-v15-document-set)
- [OBSBOT Technical Specs](https://www.obsbot.com/obsbot-tail-air)