# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao
import os
import platform
import time
import multiprocessing
from multiprocessing import Process, Lock

max_p_value = 100000
p_start_int = 3
start_state = False
Mersenne_primes = []
fallback_core_count = 2

core_count = os.cpu_count()
if core_count == 0:
    print(time.ctime(),"  ERROR: Unable to retreive core count")
    print("Setting core count to", fallback_core_count)
    core_count = fallback_core_count

def Lucas_lehmer(p):
    s = 4
    m = 2**p - 1
    for x in range(0, p-2):
        s = ((s*s)-2) % m
    if s == 0:
        return True
    else:
        return False

def Lucas_lehmer_prog_main(l, var):
    global start_state
    while True:
        if start_state == False:
            p_prog = p_start_int + var - 1
            start_state = True
        if Lucas_lehmer(p_prog):
            print(time.ctime(),"  Mersenne Prime Found:  ", p_prog)
            Mersenne_primes.append(p_prog)
        p_prog += core_count
  
if __name__ == "__main__":
    lock = Lock()
    for num in range(core_count):
        print(time.ctime(),"  Starting Workers")
        p = Process(target=Lucas_lehmer_prog_main, args=(lock, num))
        p.start()

