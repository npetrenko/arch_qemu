#!/usr/bin/python
import os
import subprocess
import shutil

from lib.mount import mount_root_partition
from lib.run import run, sudo_run, print_log
import lib.constants as constants

def bootstrap_base(root_fs_path):
    # sudo_run(['pacstrap', root_fs_path, 'base', 'base-devel', 'linux', 'linux-firmware'])
    sudo_run(['pacstrap', root_fs_path, 'base', 'linux', 'linux-firmware'])

def install_bootloader(root_fs_path):
    sudo_run(['extlinux', '--install', os.path.join(root_fs_path, 'boot')])

def run_stages(stages_path, root_fs_path):
    remote_stages = os.path.join(root_fs_path, 'stages')
    sudo_run(['cp', '-R', stages_path, remote_stages])
    stages = os.listdir(remote_stages)
    stages.sort()
    print_log(stages)

    for stage in stages:
        stage_path = os.path.join('stages', stage)
        sudo_run(['arch-chroot', root_fs_path, 'bash', '-ex', stage_path])

def build_partitions(image_path):
    # drop partition table, create gpt
    run(['sgdisk', '-og', image_path])

    # create partition #1 occupying the whole disk
    # leave space for boot sector, which occupies first 440 bytes
    run(['sgdisk', '-n', '1:2048:0', image_path])

    # set "legacy BIOS bootable" attribute for the new partition
    run(['sgdisk', '-A', '1:set:2', image_path])

def build_raw_disk(image_path):
    run(['qemu-img', 'create', image_path, '4G'])

    # install boot sector
    run(['dd', 'bs=440', 'conv=notrunc', 'count=1', 'if=/usr/lib/syslinux/bios/gptmbr.bin', 'of=' + image_path])

    build_partitions(image_path)
    loop_device = constants.LOOP_DEVICE_PATH

    sudo_run(['losetup', '-P', loop_device, image_path])
    try:
        loop_partition = loop_device + 'p1'
        sudo_run(['mkfs.ext4', loop_partition])
        sudo_run(['tune2fs', '-L', 'rootfs', loop_partition])

    finally:
        sudo_run(['losetup', '-d', loop_device])

def submit_resources(root_fs_path):
    sudo_run(["cp", "-R", "./resources/", os.path.join(root_fs_path, "root/resources")])

def build():
    image_path = constants.IMAGE_PATH
    root_fs_path = constants.ROOT_FS_PATH

    build_raw_disk(image_path)
    umounter = mount_root_partition(image_path, root_fs_path)

    try:
        bootstrap_base(root_fs_path)
        install_bootloader(root_fs_path)
        run_stages('./stages', root_fs_path)
        submit_resources(root_fs_path)

    finally:
        umounter()

if __name__ == '__main__':
    build()
