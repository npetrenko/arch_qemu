#!/bin/bash

dir=$(dirname $0)

SOURCE_PATH=/root/protected_archive.tar.gz.enc
UNPACK_PATH=/tmp/protected_archive

openssl enc -aes-256-cbc -d -iter 10 -in $SOURCE_PATH -out $UNPACK_PATH.tar.gz
mkdir $UNPACK_PATH
tar -C $UNPACK_PATH -xf $UNPACK_PATH.tar.gz

$dir/private/copy_files.sh $UNPACK_PATH /
