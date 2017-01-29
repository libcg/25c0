#!/usr/bin/python3

import time
import math
import sys

def pixel(x, y):
    x = int(math.floor(x))
    y = int(math.floor(y))
    if 0 <= x and x < 96 and 0 <= y and y < 64:
        print("\x25\xc0" + chr(int(x)) + chr(int(y)) + chr(1))
        sys.stdout.flush()

r = 1
a = 0
while True:
    x = 96 / 2 + r * math.sin(a)
    y = 64 / 2 + r * math.cos(a)
    a = a + 0.1
    r = r * 1.01
    pixel(x, y)
    time.sleep(0.01)
