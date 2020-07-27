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
max_p_value = 10**99
start_state = False
core_count = os.cpu_count()

#open files + Initial
if __name__ == "__main__":
#    file_path = os.path.realpath(__file__)
#    file_path = file_path.replace("LehmerPy.py", "")
#    log = open(file_path + "Log.txt", "a")
#    save = open(file_path + "Save.txt","w")
    Mersenne_primes_queue = Queue()
    Mersenne_confirm_status = Queue()
    finished = Queue()
    Mersenne_confirm_error = []
    Mersenne_primes = []
    ex = False

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

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

def Lucas_lehmer_confirm(p, passes, start_var, var, Mersenne_confirm_status, finished, ex):
    try:
        if ex:
            expand_1 = "2^"
            expand_2 = "-1"
        else:
            expand_1 = ""
            expand_2 = ""
    except BaseException:
        expand_1 = ""
        expand_2 = ""
    for counter in range(start_var+1, passes + 1, var):
        s = 4
        m = 2**p - 1
        for x in range(0, p-2):
            s = ((s*s)-2) % m
        if s == 0:
            print(time.ctime(), colors.GREEN+f"  Pass {counter} completed"+colors.END)
            Mersenne_confirm_status.put(0)
        else:
            print(time.ctime(),f"  {expand_1}{p}{expand_2} is not a Mersenne Prime")
            Mersenne_confirm_status.put(1)
    finished.put(1)
      
        

def Lucas_lehmer_prog_main_range(p_start_int, start_var, var, max, Mersenne_primes_queue, finished, ex):
    try:
        if ex:
            expand_1 = "2^"
            expand_2 = "-1"
        else:
            expand_1 = ""
            expand_2 = ""
    except BaseException:
        expand_1 = ""
        expand_2 = ""
    for p in range(p_start_int + start_var, max + 1, var):
        s = 4
        m = 2**p - 1
        for x in range(0, p-2):
            s = ((s*s)-2) % m
        if s == 0:
            Mersenne_primes_queue.put(p)
            print(str(time.ctime()) + colors.GREEN+f"  Mersenne Prime Found:  {expand_1}{p}{expand_2}"+ colors.END)
        p += core_count
    finished.put(1)

def loading_animation(wait_between, finished, core_count):
    while finished.qsize() != core_count:
        print("|", end="\r")
        time.sleep(wait_between)
        print("/", end="\r")
        time.sleep(wait_between)
        print("-", end="\r")
        time.sleep(wait_between)
        print("\ ", end="\r")
        time.sleep(wait_between)
        hide_cursor()
    print(" ", end="\r")


if __name__ == "__main__":
    clear()
    acsii_title = int(time.time_ns()/1000) % 4
    if acsii_title == 0:
        print(r" _/\\\_____________________________/\\\___________________________________________________________/\\\\\\\\\\\\\_________________        ")        
        print(r" _\/\\\____________________________\/\\\__________________________________________________________\/\\\/////////\\\_______________       ")
        print(r"  _\/\\\____________________________\/\\\__________________________________________________________\/\\\_______\/\\\____/\\\__/\\\_      ")
        print(r"   _\/\\\_________________/\\\\\\\\__\/\\\____________/\\\\\__/\\\\\_______/\\\\\\\\___/\\/\\\\\\\__\/\\\\\\\\\\\\\/____\//\\\/\\\__     ")
        print(r"    _\/\\\_______________/\\\/////\\\_\/\\\\\\\\\\___/\\\///\\\\\///\\\___/\\\/////\\\_\/\\\/////\\\_\/\\\/////////_______\//\\\\\___    ")
        print(r"     _\/\\\______________/\\\\\\\\\\\__\/\\\/////\\\_\/\\\_\//\\\__\/\\\__/\\\\\\\\\\\__\/\\\___\///__\/\\\_________________\//\\\____   ")
        print(r"      _\/\\\_____________\//\\///////___\/\\\___\/\\\_\/\\\__\/\\\__\/\\\_\//\\///////___\/\\\_________\/\\\______________/\\_/\\\_____  ")
        print(r"       _\/\\\\\\\\\\\\\\\__\//\\\\\\\\\\_\/\\\___\/\\\_\/\\\__\/\\\__\/\\\__\//\\\\\\\\\\_\/\\\_________\/\\\_____________\//\\\\/______ ")
        print(r"        _\///////////////____\//////////__\///____\///__\///___\///___\///____\//////////__\///__________\///_______________\////________")
    if acsii_title == 1:
        print(r"  _          _                         _____       ")
        print(r" | |        | |                       |  __ \      ")
        print(r" | |     ___| |__  _ __ ___   ___ _ __| |__) |   _ ")
        print(r" | |    / _ \ '_ \| '_ ` _ \ / _ \ '__|  ___/ | | |")
        print(r" | |___|  __/ | | | | | | | |  __/ |  | |   | |_| |")
        print(r" |______\___|_| |_|_| |_| |_|\___|_|  |_|    \__, |")
        print(r"                                              __/ |")
        print(r"                                             |___/ ")
    if acsii_title == 2:
        print(r" ____          .__                        __________        ")
        print(r"|    |    ____ |  |__   _____   __________\______   \___.__.")
        print(r"|    |  _/ __ \|  |  \ /     \_/ __ \_  __ \     ___<   |  |")
        print(r"|    |__\  ___/|   Y  \  Y Y  \  ___/|  | \/    |    \___  |")
        print(r"|_______ \___  >___|  /__|_|  /\___  >__|  |____|    / ____|")
        print(r"        \/   \/     \/      \/     \/                \/     ")
    if acsii_title == 3:
        print(r"    __         __                        ____       ")
        print(r"   / /   ___  / /_  ____ ___  ___  _____/ __ \__  __")
        print(r"  / /   / _ \/ __ \/ __ `__ \/ _ \/ ___/ /_/ / / / /")
        print(r" / /___/  __/ / / / / / / / /  __/ /  / ____/ /_/ / ")
        print(r"/_____/\___/_/ /_/_/ /_/ /_/\___/_/  /_/    \__, /  ")
        print(r"                                           /____/   ")
    print("\n\n")
    print("1:"+colors.BOLD+"R"+colors.END+"ange - Will Calculate Mersenne Primes in a specific range")
    print("2:"+colors.BOLD+"C"+colors.END+"onfirm - Will Confirm if a number is a Mersenne Prime or not")
    try:
        mode = input("MODE:")
    except:
        pass
    if str(mode) == "1" or mode == "range" or mode == "Range" or mode == "R" or mode == "r":
        print("\nRange")
        try:
            p_start_int = int(input("MIN:"))
            if p_start_int <= 2:
                pstart_int = 2
        except:
            pass
        try:
            max_p_value = int(input("MAX:"))
        except:
            pass
        hide_cursor()
        print("\n")
        fallback_core_count = 2
        if core_count == 0:
            print(str(time.ctime()),"  "+colors.RED+"ERROR: Unable to retreive core count"+colors.END)
            print(str(time.ctime()),colors.YELLOW+f"  Setting core count to {fallback_core_count}"+colors.END)
            core_count = fallback_core_count

        loadani = Process(target=loading_animation, args=(0.1, finished, core_count))        
        for num in range(core_count):
            print(str(time.ctime()) + "  Starting Workers")
            multi = Process(target=Lucas_lehmer_prog_main_range, args=(p_start_int, num, core_count, max_p_value, Mersenne_primes_queue, finished, ex))
            multi.start()
        loadani.start()
        while finished.qsize() != core_count:
            time.sleep(0.1)
        for num in range(core_count):
            print(str(time.ctime()) +"  Stopping Workers")
            multi.join()
            loadani.join()
        Mersenne_primes.sort()
        while not Mersenne_primes_queue.empty():
            Mersenne_primes.append(Mersenne_primes_queue.get())
        Mersenne_primes.sort()
        print("\n")
        for x in Mersenne_primes:
            print("2^"+str(x)+"-1 =", 2**x - 1)
        show_cursor()
        wait(0)
    if str(mode) == "2" or mode == "confirm" or mode == "Confirm" or mode == "C" or mode == "c":
        print("\nConfirmation")
        try:
            p = int(input("Confirm:"))
        except:
            pass
        try:
            passes = int(input("Passes:"))
        except:
            pass
        hide_cursor()
        fallback_core_count = 2
        if core_count == 0:
            print(str(time.ctime()),"  "+colors.RED+"ERROR: Unable to retreive core count"+colors.END)
            print(str(time.ctime()),colors.YELLOW+f"  Setting core count to {fallback_core_count}"+colors.END)
            core_count = fallback_core_count
        if passes <= core_count:
            core_count = int(passes)
            if core_count <= 0:
                core_count = 1
        loadani = Process(target=loading_animation, args=(0.1, finished, core_count)) 
        for num in range(core_count):
            if passes == 1:
                plural = " "
            else:
                plural = "s"
            print(time.ctime(),f"  Starting Worker{plural}")
            multi = Process(target=Lucas_lehmer_confirm, args=(p, passes, num, core_count, Mersenne_confirm_status, finished, ex))
            multi.start()
        loadani.start()
        while finished.qsize() != core_count:
            time.sleep(0.1)
        for num in range(core_count):
            print(str(time.ctime()) +f"   Stopping Worker{plural}")
            multi.join()
            loadani.join()
        while not Mersenne_confirm_status.empty():
            Mersenne_confirm_error.append(Mersenne_confirm_status.get())
        if max(Mersenne_confirm_error) == min(Mersenne_confirm_error):
            print("\nNo Errors Detected")
            if max(Mersenne_confirm_error) == 0:
                print("2^"+str(p)+"-1 =", 2**p - 1, "\nIs a Mersenne Prime")
            else:
                print("2^"+str(p)+"-1 =", 2**p - 1, "\nIs not a Mersenne Prime")
        else:
            print(len(Mersenne_confirm_error) - max(set(Mersenne_confirm_error), key=Mersenne_confirm_error.count), " Errors Detected")
        show_cursor()
        wait(0)
