# How to use

## Preparations
- READ the code -- it can potentially wipe your root fs :) It is non-interactive and asks no confirmations. Safest way to run this code is inside an arch VM
- pay special interest to `lib/constants.py`
- You may want to replace `npetric` and `nikita` with your username. And replace root password (grep for `chpasswd`)
- see `stages` and `resources` -- you might want to change, e.g., the list of installed packages

## How to build
- Build the base image: `./build.py`
- Optionally: patch image with copy-files.yaml: `./copy-files.py`
- Maybe do a test run: `./run.sh`

## On the final host
- Edit `resources/private/resize_to_disk.sh` and replace `disk_path` with the correct path (done manually for safety)
- On the first boot run `resources/after_boot.sh`
- Reboot
- Optionally: run other scipts from `resources`
