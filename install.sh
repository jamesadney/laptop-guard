#!/bin/bash

mkdir -v /usr/share/laptop-guard
cp -v alarm* /usr/share/laptop-guard
cp -rv media /usr/share/laptop-guard
cp -rv modules /usr/share/laptop-guard
cp -rv ui /usr/share/laptop-guard

cp -v laptop-guard /usr/bin

chmod -R -v 755 /usr/share/laptop-guard
chmod -v +x /usr/bin/laptop-guard /usr/share/laptop-guard/alarm-service.py /usr/share/laptop-guard/alarm-gtk.py

mkdir -v /usr/share/doc/laptop-guard
cp -v COPYING /usr/share/doc/laptop-guard
cp -v TODO /usr/share/doc/laptop-guard
cp -v README.rst /usr/share/doc/laptop-guard
