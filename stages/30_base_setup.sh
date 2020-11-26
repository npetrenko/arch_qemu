#!/bin/bash

# setup timezone
ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime

hwclock --systohc

echo en_US.UTF-8 UTF-8 > /etc/locale.gen

locale-gen

echo LANG=en_US.UTF-8 > /etc/locale.conf

echo arch-dev-qemu > /etc/hostname

tee /etc/hosts <<EOF
127.0.0.1   localhost
::1         localhost
127.0.1.1   arch-dev-qemu.localdomain    arch-dev-qemu
EOF

echo "root:password" | chpasswd
