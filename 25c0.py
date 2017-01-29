#!/usr/bin/python3

import sys
import ctypes
from sdl2 import *
from array import array
from queue import Queue, Empty
from threading import Thread

W = 96
H = 64
XPAD = 7
YPAD = 2
SCALE = 6

def file_enqueue(file, queue):
    for line in iter(file.readline, b''):
        queue.put([ord(c) for c in line.rstrip()])
    out.close()

def parse(q, px):
    while True:
        try:
            data = q.get_nowait()
            if len(data) >= 5 and data[0] == 0x25 and data[1] == 0xc0:
                x = data[2]
                y = data[3]
                px[y * W + x] = data[4]
        except Empty:
            break

def render(rdr, px):
    # outer screen
    SDL_SetRenderDrawColor(rdr, 0x7a, 0x86, 0x70, 0xff)
    SDL_RenderClear(rdr)

    # screen background
    SDL_SetRenderDrawColor(rdr, 0x75, 0x81, 0x6d, 0xff)
    backRect = SDL_Rect(XPAD * SCALE, YPAD * SCALE, W * SCALE, H * SCALE)
    SDL_RenderFillRect(rdr, backRect)

    # screen pixels
    SDL_SetRenderDrawColor(rdr, 0x34, 0x3d, 0x26, 0xff)
    for y in range(0, H):
        for x in range(0, W):
            if px[y * W + x]:
                pxRect = SDL_Rect((XPAD + x) * SCALE, (YPAD + y) * SCALE, SCALE, SCALE)
                SDL_RenderFillRect(rdr, pxRect)

    SDL_RenderPresent(rdr)

def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"25c0",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              (2 * XPAD + W) * SCALE, (2 * YPAD + H) * SCALE,
                              SDL_WINDOW_SHOWN)
    rdr = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
    px = [0 for x in range(W * H)]

    q = Queue()
    t = Thread(target = file_enqueue, args=(sys.stdin, q))
    t.deamon = True
    t.start()

    running = True
    event = SDL_Event()
    while running:
        parse(q, px)
        render(rdr, px)

        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break

    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
