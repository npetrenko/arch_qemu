#!/bin/bash

KERNEL_VMLINUX="/boot/vmlinuz-linux"
KERNEL_INITRD="/boot/initramfs-linux.img"

# label is hardcoded in other places
KERNEL_ROOT="LABEL=rootfs"
KERNEL_ROOT_FSTYPE="ext4"
KERNEL_ROOT_FLAGS="errors=panic"

KERNEL_CMDLINE="ro console=ttyS0 biosdevname=0 net.ifnames=0"

tee /boot/extlinux.conf <<EOF
DEFAULT linux
LABEL linux
KERNEL $KERNEL_VMLINUX
APPEND initrd=$KERNEL_INITRD root=$KERNEL_ROOT rootfstype=$KERNEL_ROOT_FSTYPE rootflags=$KERNEL_ROOT_FLAGS $KERNEL_CMDLINE
EOF

tee /etc/fstab <<EOF
$KERNEL_ROOT   /   $KERNEL_ROOT_FSTYPE   defaults,$KERNEL_ROOT_FLAGS   0 1
EOF
