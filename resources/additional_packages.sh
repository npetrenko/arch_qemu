pacman --noconfirm -S perf gdb clang rsync

pacman --noconfirm -S base-devel

sudo -u npetric bash <<EOF
mkdir /tmp/yay
(cd /tmp/yay && \
    git clone https://aur.archlinux.org/yay.git && \
    cd yay && \
    makepkg --noconfirm -si)
rm -rf /tmp/yay
EOF
