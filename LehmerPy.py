#/usr/bin/env pypy3
# Put "!" infront of line 1 to make compatible with linux

# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao

import os
import sys
import platform
import time
import multiprocessing
from multiprocessing import Process, Queue

#Initialize Phase
p_start_int = 3
max_p_value = 10**64
start_state = False
core_count = os.cpu_count()

#open files + Initial
if __name__ == "__main__":
    file_path = os.path.realpath(__file__)
    file_path = file_path.replace("LehmerPy.py", "")
    log = open(file_path + "Log.txt", "a")
    save = open(file_path + "Save.txt","w")
    Mersenne_primes_queue = Queue()
    Mersenne_confirm_status = Queue()
    finished = Queue()
    Mersenne_confirm_error = []
    Mersenne_primes = []

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def wait(waitsetc):
    if waitsetc == 1:
        clear()
        wait = str(input("Press enter to continue..."))
    if waitsetc == 0:
        wait = str(input("\nPress enter to exit..."))
    clear()

def Lucas_lehmer_confirm(p, var, pass_num, start_num, core_count, Mersenne_confirm_status, finished):
    for counter in range(start_num, start_num + pass_num):
        s = 4
        m = 2**p - 1
        for x in range(0, p-2):
            s = ((s*s)-2) % m
        if s == 0:
            print(time.ctime(), "Pass", counter, "completed")
            Mersenne_confirm_status.put(0)
        else:
            print(time.ctime(), p, "    is not a Mersenne Prime")
            Mersenne_confirm_status.put(1)
    finished.put(1)
      
        

def Lucas_lehmer_prog_main_range(p_startint, var, max, Mersenne_primes_queue, finished):
    global log
    p = p_start_int + var - 1
    while p + var - 1 <= max:
        s = 4
        m = 2**p - 1
        for x in range(0, p-2):
            s = ((s*s)-2) % m
        if s == 0:
            Mersenne_primes_queue.put(p)
            msg = str(time.ctime()) + "  Mersenne Prime Found:  " + str(p)
            print(msg)
        p += core_count
    finished.put(1)




if __name__ == "__main__":
    clear()
    print(r" _/\\\_____________________________/\\\___________________________________________________________/\\\\\\\\\\\\\_________________        ")        
    print(r" _\/\\\____________________________\/\\\__________________________________________________________\/\\\/////////\\\_______________       ")
    print(r"  _\/\\\____________________________\/\\\__________________________________________________________\/\\\_______\/\\\____/\\\__/\\\_      ")
    print(r"   _\/\\\_________________/\\\\\\\\__\/\\\____________/\\\\\__/\\\\\_______/\\\\\\\\___/\\/\\\\\\\__\/\\\\\\\\\\\\\/____\//\\\/\\\__     ")
    print(r"    _\/\\\_______________/\\\/////\\\_\/\\\\\\\\\\___/\\\///\\\\\///\\\___/\\\/////\\\_\/\\\/////\\\_\/\\\/////////_______\//\\\\\___    ")
    print(r"     _\/\\\______________/\\\\\\\\\\\__\/\\\/////\\\_\/\\\_\//\\\__\/\\\__/\\\\\\\\\\\__\/\\\___\///__\/\\\_________________\//\\\____   ")
    print(r"      _\/\\\_____________\//\\///////___\/\\\___\/\\\_\/\\\__\/\\\__\/\\\_\//\\///////___\/\\\_________\/\\\______________/\\_/\\\_____  ")
    print(r"       _\/\\\\\\\\\\\\\\\__\//\\\\\\\\\\_\/\\\___\/\\\_\/\\\__\/\\\__\/\\\__\//\\\\\\\\\\_\/\\\_________\/\\\_____________\//\\\\/______ ")
    print(r"        _\///////////////____\//////////__\///____\///__\///___\///___\///____\//////////__\///__________\///_______________\////________")
    print("\n\n")
    print("1:Range - Will Calculate Mersenne Primes in a specific range\n2:Confirm - Will Confirm if a number is a Mersenne Prime or not")
    mode = input("MODE:")
    try:
        mode = int(mode)
    except BaseException:
        pass
    if mode == 1 or mode == "range":
        print("\nRange")
        try:
            p_start_int = int(input("MIN:"))
            if p_start_int < 2:
                pstart_int = 2
        except:
            pass
        try:
            max_p_value = int(input("MAX:"))
        except:
            pass
        print("\n")
        fallback_core_count = 2
        if core_count == 0:
            msg = str(time.ctime()) + "  ERROR: Unable to retreive core count"
            print(msg)
            print(str(time.ctime()),"  Setting core count to", fallback_core_count)
            core_count = fallback_core_count
        for num in range(core_count):
            print(str(time.ctime()),"  Starting Workers")
            multi = Process(target=Lucas_lehmer_prog_main_range, args=(p_start_int, num, max_p_value, Mersenne_primes_queue, finished))
            multi.start()
        while finished.qsize() != core_count:
            time.sleep(0.1)
        for num in range(core_count):
            msg = str(time.ctime()) +"  Stopping Workers"
            print(msg)
            multi.join()
        Mersenne_primes.sort()
        while not Mersenne_primes_queue.empty():
            Mersenne_primes.append(Mersenne_primes_queue.get())
        Mersenne_primes.sort()
        print("\n")
        for x in Mersenne_primes:
            print("2^"+str(x)+"-1 =", 2**x - 1)
        wait(0)
    if mode == 2 or mode == "confirm":
        print("\nConfirmation")
        try:
            p = int(input("Confirm:"))
        except:
            pass
        try:
            passes = int(input("Passes:"))
        except:
            pass
        fallback_core_count = 2
        if core_count == 0:
            print(str(time.ctime()),"  ERROR: Unable to retreive core count")
            print(str(time.ctime()),"  Setting core count to", fallback_core_count)
            core_count = fallback_core_count
        if p <= core_count:
            core_count = int(core_count / 2)
        used_pass = 1
        for num in range(core_count):
            print(time.ctime(),"  Starting Workers")
            individual_pass = int(passes / core_count)
            if num + 1 == core_count:
                individual_pass = passes % core_count
                if individual_pass == 0:
                    individual_pass == core_count
                individual_pass += 1
            var = core_count
            multi = Process(target=Lucas_lehmer_confirm, args=(p, var, individual_pass, used_pass, core_count, Mersenne_confirm_status, finished))
            multi.start()
            used_pass += individual_pass
        while finished.qsize() != core_count:
            time.sleep(0.1)
        for num in range(core_count):
            multi.join()
        while not Mersenne_confirm_status.empty():
            Mersenne_confirm_error.append(Mersenne_confirm_status.get())
        if max(Mersenne_confirm_error) == min(Mersenne_confirm_error):
            print("\nNo Errors Detected")
            if max(Mersenne_confirm_error) == 0:
                print("2^"+str(p)+"-1 =", 2**p - 1, "\n  Is a Mersenne Prime")
            else:
                print("2^"+str(p)+"-1 =", 2**p - 1, "\n  Is not a Mersenne Prime")
        else:
            print(len(Mersenne_confirm_error) - max(set(Mersenne_confirm_error), key=Mersenne_confirm_error.count), " Errors Detected")
        wait(0)
