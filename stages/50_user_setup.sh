useradd -m -G wheel npetric

tee /etc/sudoers <<EOF
root ALL=(ALL) ALL
%wheel ALL=(ALL) NOPASSWD: ALL
EOF
