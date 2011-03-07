#!/bin/bash

mkdir /usr/share/laptop-guard
cp alarm* /usr/share/laptop-guard
cp -r media /usr/share/laptop-guard
cp -r modules /usr/share/laptop-guard
cp -r ui /usr/share/laptop-guard

cp laptop-guard /usr/bin

chmod -R 755 /usr/share/laptop-guard
chmod +x /usr/bin/laptop-guard /usr/share/laptop-guard/alarm-service.py /usr/share/laptop-guard/alarm-gtk.py

mkdir /usr/share/doc/laptop-guard
cp COPYING /usr/share/doc/laptop-guard
cp TODO /usr/share/doc/laptop-guard
cp README /usr/share/doc/laptop-guard