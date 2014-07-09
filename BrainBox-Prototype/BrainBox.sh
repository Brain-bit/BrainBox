#!/bin/sh
renice -20 -p $$

(sleep 10;python Server.py)&
