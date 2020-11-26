#!/bin/bash
set -ex

src_path="$1"
dst_path="$2"

find "$src_path" -type f |
  while read src_file; do
    dst_file="$dst_path${src_file#$src_path}"
    cp -p $src_file $dst_file
  done
