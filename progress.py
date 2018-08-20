#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


def show_progress(current, total):
    sys.stdout.write("%.f" % float(current * 1.0 / total * 100.0))
    sys.stdout.write("%\r")
    sys.stdout.flush()

