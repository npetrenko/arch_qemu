#!/bin/bash
set -ex

disk_path=PATH_TO_YOUR_ROOT_DEVICE

# copy backup header to the end of the disk
sgdisk -e $disk_path

# expand partition to occupy full space
# steps:
# 1. delete partition
# 2. create a new one in its place. remark: 2048 is also hardcoded in other places
# 3. make it bootable again!
sgdisk -d 1 \
       -n 1:2048:0 \
       -A 1:set:2 \
       $disk_path

# sync kernel
partprobe $disk_path

# resize root filesystem
resize2fs "${disk_path}1"

echo "you should now reboot"
