# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao


import os
import sys
import platform
import time
import multiprocessing
from multiprocessing import Process, Queue

#Initialize Phase
p_start_int = 2
max_p_value = 10**99
start_state = False
core_count = os.cpu_count()
arguments = sys.argv
release_ver = platform.release()
try:
    release_ver = int(release_ver)
    version_get = True
except:
    release_ver = 10
    version_get = False
#open files + Initial
if __name__ == "__main__":
    file_path = str(__file__)
    Mersenne_primes_queue = Queue()
    Mersenne_confirm_status = Queue()
    finished = Queue()
    Mersenne_confirm_error = []
    Mersenne_primes = []
    slash1 = "\ "
    slash2 = "/"
    reserved = ["reserved", "/", "?", "%", "*", ":", "|", "<", ">", '"', "-"]
    reserved[0] = slash1[0]
    fstart = file_path.rfind(slash1[0])
    if fstart == -1:
        fstart = file_path.rfind(slash2)
    file_name = file_path[fstart+1:len(file_path)]
    file_path = file_path.replace(file_name, "", 1)
    file_name = file_name[0:file_name.rfind(".")]
    custom_file = "output.txt"
    #Display primes as exponents
    #Defualt False
    ex = False

    #LehmerPy V1.4 Stable
    version = 14
    beta = False

    #Animation Speed - Smaller value = faster, -1 = off
    #Defualt 0.1
    loadani_speed = 0.1


    odd = True

    out_file = False

    maxspeed = False

    # CMD arguments get dealt with here
    map(str(), arguments)
    if "-all" in arguments:
        odd = False
    if "-e" in arguments:
        ex = True
    if "-j" in arguments:
        try:
            core_count = int(arguments[arguments.index("-j") + 1])
        except: 
            pass
    else:       
        for x in arguments:
            x = str(x)
            if "-j" in x and len(x) > 2:
                try:
                    core_count = int(x[2:len(x)])
                except:
                    pass
                break   
    if "-l" in arguments:
        try:
            loadani_speed = float(arguments[arguments.index("-l") + 1])
        except:
            pass
    else:
        for x in arguments:
            x = str(x)
            if "-l" in x and len(x) > 2:
                try:
                    loadani_speed = float(x[2:len(x)])
                    break  
                except:
                    pass
    if "-o" in arguments:
        out_file = True
        try:
            custom_file_str = str(arguments[arguments.index("-o") + 1])
            if not(any(check in custom_file_str for check in reserved)):
                        if not(".txt" in custom_file_str[len(custom_file_str)-4:len(custom_file_str)]):
                            custom_file = custom_file_str + ".txt"
                        else:
                            custom_file = custom_file_str
        except:
            pass
    else:
        for x in arguments:
            x = str(x)
            if "-o" in x and len(x) > 2:
                custom_file_str = str(x[2:len(x)])
                out_file = True    
                if not(any(check in custom_file_str for check in reserved)):
                    if not(".txt" in custom_file_str[len(custom_file_str)-4:len(custom_file_str)]):
                        custom_file = custom_file_str + ".txt"
                    else:
                        custom_file = custom_file_str
                break
    if "-ms" in arguments:
        maxspeed = True
        loadani_speed = -1
        odd = True
    dc = "" if release_ver < 10 else "[-dc]"
    if "/?" in arguments or "?" in arguments:
        print("\n")
        print(f"Usage: {file_name} [-all] {dc} [-e] [-j int] [-l float] [-ms]")
        print(f"{' '*len(file_name)}        [-o name]")
        print("\n")
        print("Options:")
        print("    -all           Tests all numbers")
        if dc == "[-dc]":
            print("    -dc            Disables ANSI colors")
        print("    -e             Displays Mersenne primes as a power")
        print("    -j int         Threads to use")
        print("    -l float       Speed of progress wheel")
        print("    -ms            Use for maximum speed and efficiency")
        print("    -o name        Save output to txt. name is optional")   
        print("\n")

        sys.exit(0)

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]
#not my code
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
#still not mine
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

#Everything past here is mine
class colors():
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
if "-dc" in arguments or (version_get and release_ver < 10):
    colors.PURPLE = ''
    colors.CYAN = ''
    colors.DARKCYAN = ''
    colors.BLUE = ''
    colors.GREEN = ''
    colors.YELLOW = ''
    colors.RED = ''
    colors.BOLD = ''
    colors.UNDERLINE = ''
    colors.END = ''
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
        sys.exit(0)

def Lucas_lehmer_confirm(p, passes, start_var, var, Mersenne_confirm_status, finished, ex, arguments):
    if "-dc" in arguments or (version_get and release_ver < 10):
        colors.PURPLE = ''
        colors.CYAN = ''
        colors.DARKCYAN = ''
        colors.BLUE = ''
        colors.GREEN = ''
        colors.YELLOW = ''
        colors.RED = ''
        colors.BOLD = ''
        colors.UNDERLINE = ''
        colors.END = ''
    try:
        expand_1 = "2^" if ex else ""
        expand_2 = "-1" if ex else ""
        mstr = "" if ex else "M"
    except BaseException:
        expand_1 = ""
        expand_2 = ""
        mstr = "M"
    for counter in range(start_var+1, passes + 1, var):
        s = 4
        m = (1 << p) - 1
        for _ in range(0, p-2):
            sqr = s*s
            s = (sqr & m) + (sqr >> p)
            if s >= m:
                s -= m
            s -= 2
        if s == 0:
            print(time.ctime(), colors.GREEN+f"  Pass {counter} completed"+colors.END)
            Mersenne_confirm_status.put(0)
        else:
            print(time.ctime(), colors.YELLOW+f"  {expand_1}{mstr}{p}{expand_2} is not a Mersenne Prime"+colors.END)
            Mersenne_confirm_status.put(1)
    finished.put(1)
      
        

def Lucas_lehmer_prog_main_range(p_start_int, start_var, var, max, Mersenne_primes_queue, finished, ex, odd, arguments, maxspeed, progress="progress"):
    if "-dc" in arguments or (version_get and release_ver < 10):
        colors.PURPLE = ''
        colors.CYAN = ''
        colors.DARKCYAN = ''
        colors.BLUE = ''
        colors.GREEN = ''
        colors.YELLOW = ''
        colors.RED = ''
        colors.BOLD = ''
        colors.UNDERLINE = ''
        colors.END = ''
    try:
        expand_1 = "2^" if ex else ""
        expand_2 = "-1" if ex else ""
        mstr = "" if ex else "M"
    except BaseException:
        expand_1 = ""
        expand_2 = ""
        mstr = "M"
    if odd or maxspeed:
        for p in range(p_start_int + start_var*2-1, max + 1, var*2):
            if progress != "progress":
                if progress.empty():
                    progress.put(p)
            s = 4
            m = (1 << p) - 1
            for _ in range(0, p-2):
                sqr = s*s
                s = (sqr & m) + (sqr >> p)
                if s >= m:
                    s -= m
                s -= 2
            if s == 0:
                Mersenne_primes_queue.put(p)
                print(str(time.ctime()), colors.GREEN+f"  Mersenne Prime Found:  {expand_1}{mstr}{p}{expand_2}"+ colors.END)
            p += core_count
    else:
        for p in range(p_start_int + start_var, max + 1, var):
            if progress.empty():
                progress.put(p)
            s = 4
            m = (1 << p) - 1
            for _ in range(0, p-2):
                sqr = s*s
                s = (sqr & m) + (sqr >> p)
                if s >= m:
                    s -= m
                s -= 2
            if s == 0:
                Mersenne_primes_queue.put(p)
                print(str(time.ctime()), colors.GREEN+f"  Mersenne Prime Found:  {expand_1}{mstr}{p}{expand_2}"+ colors.END)
            p += core_count
    finished.put(1)

# This is the Wheel animation
def loading_animation(wait_between, finished, core_count, progress="progress"):
    if not(progress == "progress"):
        avg_prog = []
        progress_stat = 3
        while finished.qsize() != core_count:
            try:
                avg_prog[:] = []
                for x in range(core_count):
                    avg_prog.append(progress.get())
                progress_stat = int(sum(avg_prog)/core_count)
            except:
                pass
            print("| ", progress_stat, end="\r")
            time.sleep(wait_between)
            print("/ ", progress_stat, end="\r")
            time.sleep(wait_between)
            print("- ", progress_stat, end="\r")
            time.sleep(wait_between)
            print("\ ", progress_stat, end="\r")
            time.sleep(wait_between)
            hide_cursor()
    else:
        while finished.qsize() != core_count:
            print("| ", end="\r")
            time.sleep(wait_between)
            print("/ ", end="\r")
            time.sleep(wait_between)
            print("- ", end="\r")
            time.sleep(wait_between)
            print("\ ", end="\r")
            time.sleep(wait_between)
            hide_cursor()
    print("                                                                                                                                                                                            ", end="\r")


if __name__ == "__main__":
    clear()

    # ACSII Art
    # 4x
    acsii_title = int(time.time()*100) % 4
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
    version /= 10
    if beta:
        beta = "b"
    else:
        beta = ""
    print(f"v{version}{beta}\n")
    print("1:"+colors.BOLD+"R"+colors.END+"ange - Will Calculate Mersenne Primes in a specific range")
    print("2:"+colors.BOLD+"C"+colors.END+"onfirm - Will Confirm if a number is a Mersenne Prime or not")
    try:
        mode = input("MODE:")
    except:
        sys.exit(0)
        # Range
    if str(mode) == "1" or mode == "range" or mode == "Range" or mode == "R" or mode == "r":
        print("\nRange")
        try:
            p_start_int = input("MIN:")
        except:
            pass
        try:
            max_p_value = input("MAX:")
        except:
            sys.exit(0)
        try:
            p_start_int = int(p_start_int)
            max_p_value = int(max_p_value)
        except:
            if "," in str(p_start_int):
                p_start_int = str(p_start_int)
                p_start_int = p_start_int.replace(",","")
            if "," in str(max_p_value):
                max_p_value = str(max_p_value)
                max_p_value = max_p_value.replace(",","")
        try:
            p_start_int = int(p_start_int)
            max_p_value = int(max_p_value)
        except:
            sys.exit(0)
        if p_start_int <= 2:
            p_start_int = 2
        hide_cursor()
        print("\n")
        fallback_core_count = 2
        if loadani_speed == -1:
            progress = "progress"
        else:
            progress = multiprocessing.JoinableQueue(core_count)
        print(f"{platform.processor()}\n")
        if core_count <= 0:
            print(str(time.ctime()),"  "+colors.RED+"ERROR: Unable to retreive core count"+colors.END)
            print(str(time.ctime()),colors.YELLOW+f"  Setting core count to {fallback_core_count}"+colors.END)
            core_count = fallback_core_count
        start_date = time.ctime()
        start_time = time.time()        
        for num in range(core_count):
            print(str(time.ctime()), "  Starting Workers")
            multi = Process(target=Lucas_lehmer_prog_main_range, args=(p_start_int, num, core_count, max_p_value, Mersenne_primes_queue, finished, ex, odd, arguments, maxspeed, progress))
            multi.start()
        if loadani_speed != -1:
            loadani = Process(target=loading_animation, args=(loadani_speed, finished, core_count, progress))
            loadani.start()
        while finished.qsize() != core_count:
            time.sleep(0.01)
        try:
            while not progress.empty():
                try:
                    progress.get(timeout=0.001)
                except:
                    pass
        except:
            pass
        if loadani_speed != -1:
            progress.close()
            loadani.terminate()
        for num in range(core_count):
            print(str(time.ctime()), "  Stopping Workers")
            multi.join()
        end_time = time.time()
        end_date = time.ctime()
        print(str(time.ctime()), "  Finishing")
        while not Mersenne_primes_queue.empty():
            Mersenne_primes.append(Mersenne_primes_queue.get())
        Mersenne_primes.sort()
        time_taken = float('%.4f'%(end_time - start_time))
        unit = "seconds"
        if time_taken >= 600:
            time_taken /= 60
            unit = "minutes"
            if time_taken >= 600:
                time_taken /= 60
                unit = "hours"
                if time_taken >= 240:
                    time_taken /= 24
                    unit = "days"
                    if time_taken >= 70:
                        time_taken /= 7
                        unit = "weeks"
        print(f"\nCompute Time: {time_taken} {unit}\n")
        for x in Mersenne_primes:
            print("2^"+str(x)+"-1 =", 2**x-1)
        if out_file:
            with open(file_path + custom_file,"a") as output:
                output.write("\n\n---------------------------------------------------------------------------------------\n")
                output.write(f"{platform.processor()}\n")
                output.write(f"Mode: Range from {p_start_int} to {max_p_value}\n")
                output.write(f"Start: {start_date}  End: {end_date}\n")
                output.write(f"Compute Time: {time_taken} {unit}\n")
                for x in Mersenne_primes:
                    plural = " " if len(str(2**int(x)-1)) == 1 else "s"
                    output.write(f"\n2^{x}-1   ---   {len(str(2**x-1))} Digit{plural}\n")
                    output.write(f"{2**x-1}\n")
                output.write("---------------------------------------------------------------------------------------")
        show_cursor()
        print("\n")
        wait(0)
    # Confirm
    if str(mode) == "2" or mode == "confirm" or mode == "Confirm" or mode == "C" or mode == "c":
        print("\nConfirmation")
        try:
            p = input("Confirm:")
        except:
            pass
        try:
            passes = input("Passes:")
        except:
            sys.exit(0)
        try:
            p = int(p)
            passes = int(passes)
        except:
            if "," in str(p):
                p = str(p)
                p = p.replace(",","")
            if "," in str(passes):
                passes = str(passes)
                passes = passes.replace(",","")
        try:
            p = int(p)
            passes = int(passes)
        except:
            sys.exit(0)
        if passes <= 0 or p <= 0:
            sys.exit(0)
        hide_cursor()
        fallback_core_count = 2
        print(f"\n\n{platform.processor()}\n")
        if core_count <= 0:
            print(str(time.ctime()),"  "+colors.RED+"ERROR: Unable to retreive core count"+colors.END)
            print(str(time.ctime()),colors.YELLOW+f"  Setting core count to {fallback_core_count}"+colors.END)
            core_count = fallback_core_count
        if passes <= core_count:
            core_count = int(passes)
            if core_count <= 0:
                core_count = 1
        start_date = time.ctime()
        start_time = time.time()
        for num in range(core_count):
            plural = " " if passes == 1 else "s"
            print(time.ctime(),f"  Starting Worker{plural}")
            multi = Process(target=Lucas_lehmer_confirm, args=(p, passes, num, core_count, Mersenne_confirm_status, finished, ex, arguments))
            multi.start()
        if loadani_speed != -1:
            loadani = Process(target=loading_animation, args=(loadani_speed, finished, core_count)) 
            loadani.start()
        while finished.qsize() != core_count:
            time.sleep(0.01)
        end_time = time.time() 
        end_date = time.ctime()
        for num in range(core_count):
            print(str(time.ctime()) +f"   Stopping Worker{plural}")
            multi.join()
        print(str(time.ctime())+"   Finishing")
        if loadani_speed != -1:
            loadani.terminate()
        while not Mersenne_confirm_status.empty():
            Mersenne_confirm_error.append(Mersenne_confirm_status.get())
        time_taken = float('%.4f'%(end_time - start_time))
        unit = "seconds"
        if time_taken >= 600:
            time_taken /= 60
            unit = "minutes"
            if time_taken >= 600:
                time_taken /= 60
                unit = "hours"
                if time_taken >= 240:
                    time_taken /= 24
                    unit = "days"
                    if time_taken >= 70:
                        time_taken /= 7
                        unit = "weeks"
        print(f"\nCompute Time: {time_taken} {unit}\n")
        if max(Mersenne_confirm_error) == min(Mersenne_confirm_error):
            print("\nNo Errors Detected")
            error = False
            if max(Mersenne_confirm_error) == 0:
                print("2^"+str(p)+"-1 =", 2**p - 1, "\nIs a Mersenne Prime")
            else:
                print("2^"+str(p)+"-1 =", 2**p - 1, "\nIs not a Mersenne Prime")
        else:
            print("Error Detected")
            error = True
        if out_file:
            with open(file_path + custom_file,"a") as output:
                output.write("\n\n---------------------------------------------------------------------------------------\n")
                output.write(f"{platform.processor()}\n")
                plural = "es" if passes > 1 else ""
                output.write(f"Mode: Confirm {p} with {passes} pass{plural}\n")
                output.write(f"Start: {start_date}  End: {end_date}\n")
                output.write(f"Compute Time: {time_taken} {unit}\n")
                plural = "s" if error != 2 else ""
                if error:
                    output.write("Error Detected")
                else:
                    output.write("No errors detected")
                plural = "" if len(str(2**p-1)) == 1 else "s"
                output.write(f"\n\n2^{p}-1   ---   {len(str(2**p-1))} Digit{plural}\n")
                output.write(f"{2**p-1}\n")
                output.write("---------------------------------------------------------------------------------------")
        show_cursor()
        wait(0)
    else:
        sys.exit(0)
# End of Program
