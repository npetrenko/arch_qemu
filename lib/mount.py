import subprocess
from .run import run, sudo_run
from .constants import LOOP_DEVICE_PATH


def mount_root_partition(image_path, root_fs_path):
    loop_device = LOOP_DEVICE_PATH
    root_partition = 'p1'

    sudo_run(['losetup', '-P', loop_device, image_path])
    sudo_run(['mount', loop_device + root_partition, root_fs_path]);

    def umount():
        sudo_run(['umount', root_fs_path])
        sudo_run(['losetup', '-d', loop_device])

    return umount
