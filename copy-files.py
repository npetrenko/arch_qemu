#!/usr/bin/python

import os
import subprocess
import shutil
import yaml

from lib.mount import mount_root_partition
import lib.constants as constants

def join_no_leading(first, second):
    return os.path.join(first, second.strip('/'))

def print_log(*args):
    print(*args)

def run(args, **kwargs):
    print_log("+ '" + ' '.join(args) + "'")
    return subprocess.run(' '.join(args), check=True, shell=True, **kwargs)

def sudo_run(args, **kwargs):
    return run(['sudo', '-E'] + args, **kwargs)

def fix_perms(entry, final_path, root_fs_path):
    with_chroot = 'chown {} {} && '.format(entry['owner'], final_path) + \
        'chmod {} {}'.format(entry['permissions'], final_path)

    sudo_run(['arch-chroot', root_fs_path, 'bash', '-c', '"{}"'.format(with_chroot)])

def copy_single_unprotected(entry, root_fs_path):
    to_path = join_no_leading(root_fs_path, entry['to'])
    sudo_run(['cp', entry['from'], to_path])
    fix_perms(entry, entry['to'], root_fs_path)

def copy_single_protected(entry, archive_path, root_fs_path):
    entries_path = join_no_leading(archive_path, "entries")
    entries_abs_path = join_no_leading(root_fs_path, entries_path)
    sudo_run(['mkdir', '-p', entries_abs_path, "|| true"])

    to_abs_path = join_no_leading(entries_abs_path, entry['to'])
    to_path = join_no_leading(entries_path, entry['to'])

    sudo_run(['mkdir', '-p', "$(dirname {})".format(to_abs_path), '|| true'])
    sudo_run(['cp', entry['from'], to_abs_path])
    fix_perms(entry, to_path, root_fs_path)

def seal_archive(archive_path, root_fs_path, result_path_abs):
    print("Enter archive password:")
    passwd = input()

    archive_abs_path = join_no_leading(root_fs_path, archive_path)
    entries_abs_path = join_no_leading(archive_abs_path, "entries")
    sudo_run(['tar', '-C', entries_abs_path, '-czvf', '{}.tar.gz'.format(archive_abs_path), '.'])
    sudo_run(['openssl enc -aes-256-cbc -e -iter 10 -pass pass:{} -in {}.tar.gz -out {}.tar.gz.enc'.format(passwd, archive_abs_path, archive_abs_path)])
    sudo_run(['mv', archive_abs_path + '.tar.gz.enc', result_path_abs])

def prepare_single(entry, root_fs_path):
    cmd = 'mkdir {dir} || true && chmod {permissions} {dir} && chown {owner} {dir}'.format(**entry)
    sudo_run(['arch-chroot', root_fs_path, 'bash', '-c', '"{}"'.format(cmd)])

def copy_files():
    work_dir = '/root/tmp/arch_quemu_builder'
    archive_path = join_no_leading(work_dir, "protected_archive")
    image_path = constants.IMAGE_PATH
    root_fs_path = constants.ROOT_FS_PATH
    protected_archive_result_abs = join_no_leading(root_fs_path, '/root/protected_archive.tar.gz.enc')

    work_dir_abs = join_no_leading(root_fs_path, work_dir)
    archive_path_abs = join_no_leading(root_fs_path, archive_path)

    umounter = mount_root_partition(image_path, root_fs_path)
    try:
        sudo_run(['rm', '-rf', work_dir_abs])
        sudo_run(['mkdir', '-p', work_dir_abs])
        sudo_run(['mkdir', archive_path_abs])

        with open('copy-files.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            for entry in data['prepare']:
                prepare_single(entry, root_fs_path)

            for entry in data['copy-files']:
                if ("protected" in entry) and (entry["protected"] == 1):
                    copy_single_protected(entry, archive_path, root_fs_path)
                else:
                    copy_single_unprotected(entry, root_fs_path)

        seal_archive(archive_path, root_fs_path, protected_archive_result_abs)
        sudo_run(['rm', '-rf', work_dir_abs])

    finally:
        umounter()

if __name__ == '__main__':
    copy_files()
