#!/bin/bash

mkdir /usr/share/laptop-alarm
cp alarm* /usr/share/laptop-alarm
cp -r media /usr/share/laptop-alarm
cp -r modules /usr/share/laptop-alarm
cp -r ui /usr/share/laptop-alarm

cp laptop-alarm /usr/bin

chmod +x /usr/bin/laptop-alarm /usr/share/laptop-alarm/alarm-service.py /usr/share/laptop-alarm/alarm-gtk.py

mkdir /usr/share/doc/laptop-alarm
cp COPYING /usr/share/doc/laptop-alarm
cp TODO /usr/share/doc/laptop-alarm
cp README /usr/share/doc/laptop-alarm