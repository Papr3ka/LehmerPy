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
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    file_path = str(__file__)
    Mersenne_primes_queue = Queue()
    Mersenne_confirm_status = Queue()
    finished = Queue()
    manager = multiprocessing.Manager()
    residue = manager.Queue()
    residue_list = []
    Mersenne_confirm_error = []
    Mersenne_primes = []
    perm_stat = True
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

    #LehmerPy V1.5 Stable
    version = 15
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
        if core_count <= 0:
            core_count = 1
    else:       
        for x in arguments:
            x = str(x)
            if "-j" in x and len(x) > 2:
                try:
                    core_count = int(x[2:len(x)])
                except:
                    pass
                break  
        if core_count <= 0:
            core_count = 1
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
    try:
        dc = " " if release_ver < 10 and version_get else " [-dc]"
    except:
        pass
    if "/?" in arguments or "?" in arguments:
        print("\n")
        print(f"Usage: {file_name} [-all]{dc} [-e] [-j int] [-l float] [-ms]")
        print(f"{' '*len(file_name)}        [-o name]")
        print("\n")
        print("Options:")
        print("    -all           Tests all numbers")
        if dc == " [-dc]":
            print("    -dc            Disables ANSI colors")
        print("    -e             Displays Mersenne primes as a power")
        print("    -j int         Threads to use")
        print("    -l float       Speed of progress wheel")
        print("    -ms            Use for maximum speed and efficiency")
        print("    -o name        Save output to txt. name is optional")   
        print("\n")

        sys.exit(0)
#Everything past here is mine
class colors:
    def __init__(self, PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDERLINE, END):
        self.PURPLE = PURPLE
        self.CYAN = CYAN
        self.DARKCYAN = DARKCYAN
        self.BLUE = BLUE
        self.GREEN = GREEN
        self.YELLOW = YELLOW
        self.RED = RED
        self.BOLD = BOLD
        self.UNDERLINE = UNDERLINE 
        self.END = END
    def rmcolor():
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
    def encolor():
        colors.PURPLE = '\033[95m'
        colors.CYAN = '\033[96m'
        colors.DARKCYAN = '\033[36m'
        colors.BLUE = '\033[94m'
        colors.GREEN = '\033[92m'
        colors.YELLOW = '\033[93m'
        colors.RED = '\033[91m'
        colors.BOLD = '\033[1m'
        colors.UNDERLINE = '\033[4m'
        colors.END = '\033[0m'


if "-dc" in arguments or (version_get and release_ver < 10):
    colors.rmcolor()
else:
    colors.encolor()        

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def wait(waitsetc):
    if waitsetc == 2:
        print("Retry? (Y/N)...\n", end="\r")
        rpl = str(input())
        if rpl == "y" or rpl == "Y" or rpl == "Yes" or rpl == "yes" or rpl == "ys":
            return False
        else:
            return True
    if waitsetc == 1:
        print("Press enter to continue...", end="\r")
        wait = str(input())
    if waitsetc == 0:
        wait = str(input("\nPress enter to exit..."))
        sys.exit(0)

def Lucas_lehmer_confirm(p, passes, start_var, var, Mersenne_confirm_status, finished, ex, residue, arguments):
    if "-dc" in arguments or (version_get and release_ver < 10):
        colors.rmcolor()
    else:
        colors.encolor()
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
            print(time.ctime(), colors.GREEN+f"  Pass {counter} completed, {expand_1}{mstr}{p}{expand_2} is a Mersenne Prime"+colors.END)
            Mersenne_confirm_status.put(0)
        else:
            print(time.ctime(), colors.YELLOW+f"  Pass {counter} completed, {expand_1}{mstr}{p}{expand_2} is not a Mersenne Prime"+colors.END)
            Mersenne_confirm_status.put(1)
        residue.put([counter, s])
    finished.put(1)
      
        

def Lucas_lehmer_prog_main_range(p_start_int, start_var, var, max, Mersenne_primes_queue, finished, ex, odd, arguments, maxspeed, progress="progress"):
    if "-dc" in arguments or (version_get and release_ver < 10):
        colors.rmcolor()
    else:
        colors.encolor()
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
            
    print("                                                                                                                                                                                            ", end="\r")


if __name__ == "__main__":
    clear()

    # ACSII Art
    # 4x
    acsii_title = [r"""_/\\\_____________________________/\\\___________________________________________________________/\\\\\\\\\\\\\_________________                
_\/\\\____________________________\/\\\__________________________________________________________\/\\\/////////\\\_______________       
 _\/\\\____________________________\/\\\__________________________________________________________\/\\\_______\/\\\____/\\\__/\\\_      
  _\/\\\_________________/\\\\\\\\__\/\\\____________/\\\\\__/\\\\\_______/\\\\\\\\___/\\/\\\\\\\__\/\\\\\\\\\\\\\/____\//\\\/\\\__     
   _\/\\\_______________/\\\/////\\\_\/\\\\\\\\\\___/\\\///\\\\\///\\\___/\\\/////\\\_\/\\\/////\\\_\/\\\/////////_______\//\\\\\___    
    _\/\\\______________/\\\\\\\\\\\__\/\\\/////\\\_\/\\\_\//\\\__\/\\\__/\\\\\\\\\\\__\/\\\___\///__\/\\\_________________\//\\\____   
     _\/\\\_____________\//\\///////___\/\\\___\/\\\_\/\\\__\/\\\__\/\\\_\//\\///////___\/\\\_________\/\\\______________/\\_/\\\_____  
      _\/\\\\\\\\\\\\\\\__\//\\\\\\\\\\_\/\\\___\/\\\_\/\\\__\/\\\__\/\\\__\//\\\\\\\\\\_\/\\\_________\/\\\_____________\//\\\\/______ 
       _\///////////////____\//////////__\///____\///__\///___\///___\///____\//////////__\///__________\///_______________\////________""",
r"""  _          _                         _____       
 | |        | |                       |  __ \      
 | |     ___| |__  _ __ ___   ___ _ __| |__) |   _ 
 | |    / _ \ '_ \| '_ ` _ \ / _ \ '__|  ___/ | | |
 | |___|  __/ | | | | | | | |  __/ |  | |   | |_| |
 |______\___|_| |_|_| |_| |_|\___|_|  |_|    \__, |
                                              __/ |
                                             |___/ """,
r""" ____          .__                        __________        
|    |    ____ |  |__   _____   __________\______   \___.__.
|    |  _/ __ \|  |  \ /     \_/ __ \_  __ \     ___<   |  |
|    |__\  ___/|   Y  \  Y Y  \  ___/|  | \/    |    \___  |
|_______ \___  >___|  /__|_|  /\___  >__|  |____|    / ____|
        \/   \/     \/      \/     \/                \/     """,
r"""    __         __                        ____       
   / /   ___  / /_  ____ ___  ___  _____/ __ \__  __
  / /   / _ \/ __ \/ __ `__ \/ _ \/ ___/ /_/ / / / /
 / /___/  __/ / / / / / / / /  __/ /  / ____/ /_/ / 
/_____/\___/_/ /_/_/ /_/ /_/\___/_/  /_/    \__, /  
                                           /____/   """]
    acsii_title_op = int(time.time()*100) % len(acsii_title)
    print(colors.BOLD+acsii_title[acsii_title_op]+colors.END)
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
            time.sleep(0.0001)
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
            multi.terminate()
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
        plural = "" if len(Mersenne_primes) == 1 else "s"
        print(f"{colors.UNDERLINE}{colors.BOLD}Mersenne Prime{plural}{colors.END}{colors.END}")
        for x in Mersenne_primes:
            print(f"2^{x}-1 = {2**x-1}\n")
        print(f"\n\n{colors.BOLD}{colors.UNDERLINE}Perfect Number{plural}{colors.END}{colors.END}")
        for x in Mersenne_primes:
            print(f"2^{x - 1} · (2^{x}-1) = {(2**(x-1))*(2**x-1)}\n")
        if out_file:
            print("\n\n")
            while perm_stat:
                try:
                    if os.path.exists(file_path + custom_file):
                        print(f"Writing to file at {file_path}{custom_file}")
                        original_size = os.path.getsize(file_path + custom_file)
                    else:
                        print(f"Generating file at {file_path}{custom_file}")
                        original_size = 0
                    with open(file_path + custom_file,"a") as output:
                        output.write("\n")
                        perm_stat = False
                except PermissionError:
                    print(colors.RED+"ERROR:   Permission to write to file denied"+colors.END)
                    if wait(2):
                        perm_stat = False
                except  IOError:
                    print(colors.RED+"ERROR:   I/O Error"+colors.END)
                    if wait(2):
                        perm_stat = False
            with open(file_path + custom_file,"a") as output:
                output.write("\n\n---------------------------------------------------------------------------------------\n")
                output.write(f"{file_name} v{version}{beta} Args: ")  
                for w in range(1, len(arguments)):
                    output.write(f"{arguments[w]} ")
                output.write(f"\n{platform.processor()}\n")
                output.write(f"Mode: Range from {p_start_int} to {max_p_value}\n")
                output.write(f"Start: {start_date}  End: {end_date}\n")
                output.write(f"Compute Time: {time_taken} {unit}\n")
                for x in Mersenne_primes:
                    plural = " " if len(str(2**int(x)-1)) == 1 else "s"
                    output.write(f"\n2^{x}-1   ---   {len(str(2**x-1))} Digit{plural}\n")
                    output.write(f"{2**x-1}\n")
                plural = "" if len(Mersenne_primes) == 1 else "s"
                output.write(f"\nPerfect Number{plural}\n")
                for x in Mersenne_primes:
                    output.write(f"2^{x - 1} · (2^{x}-1)\n{(2**(x-1))*(2**x-1)}\n\n")
                output.write("---------------------------------------------------------------------------------------")
            if not perm_stat:
                modified_size = os.path.getsize(file_path + custom_file)
                sign = "-" if modified_size - original_size < 0 else "+"
                plural = "" if modified_size - original_size == 0 else "s"
                print(f"{colors.GREEN}Success{colors.END}\n{custom_file} {sign}{modified_size-original_size} Byte{plural}")            
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
            multi = Process(target=Lucas_lehmer_confirm, args=(p, passes, num, core_count, Mersenne_confirm_status, finished, ex, residue, arguments))
            multi.start()
        if loadani_speed != -1:
            loadani = Process(target=loading_animation, args=(loadani_speed, finished, core_count)) 
            loadani.start()
        while finished.qsize() != core_count:
            time.sleep(0.0001)
        end_time = time.time() 
        end_date = time.ctime()
        for num in range(core_count):
            print(str(time.ctime()) +f"   Stopping Worker{plural}")
            multi.terminate()
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
        while not residue.empty():
            residue_list.append(residue.get())
        residue_list.sort(key=lambda x: x[0])
        for res in residue_list:
            print(f"Pass {res[0]}, Residue {res[1]}")
        if max(residue_list, key=lambda x: x[1]) == min(residue_list, key=lambda x: x[1]):
            error = False
            if max(Mersenne_confirm_error) == 0:
                print(f"\n{colors.UNDERLINE}{colors.BOLD}Mersenne Prime{colors.END}{colors.END}\n2^{p}-1 = {2**p - 1}")
                if not error:
                    print("No errors detected")
                print(f"\n{colors.UNDERLINE}{colors.BOLD}Perfect Number{colors.END}{colors.END}\n2^{p - 1} · (2^{p}-1) = {(2**(p-1))*(2**p-1)}")
            else:
                print(f"\n{colors.UNDERLINE}{colors.BOLD}Mersenne Number{colors.END}{colors.END}\n2^{p}-1 = {2**p - 1}")
        else:
            print("Error Detected")
            error = True
        if out_file:
            print("\n\n")
            while perm_stat:
                try:
                    if os.path.exists(file_path + custom_file):
                        print(f"Writing to file at {file_path}{custom_file}")
                        original_size = os.path.getsize(file_path + custom_file)
                    else:
                        print(f"Generating file at {file_path}{custom_file}")
                        original_size = 0
                    with open(file_path + custom_file,"a") as output:
                        output.write("\n")
                        perm_stat = False
                except PermissionError:
                    print(colors.RED+"ERROR:   Permission to write to file denied"+colors.END)
                    if wait(2):
                        perm_stat = False
                except IOError:
                    print(colors.RED+"ERROR:   I/O Error"+colors.END)
                    if wait(2):
                        perm_stat = False
            with open(file_path + custom_file,"a") as output:
                output.write("\n---------------------------------------------------------------------------------------\n")
                output.write(f"{file_name} v{version}{beta} Args: ")  
                for w in range(1, len(arguments)):
                    output.write(f"{arguments[w]} ")
                output.write(f"\n{platform.processor()}\n")
                plural = "es" if passes > 1 else ""
                output.write(f"Mode: Confirm {p} with {passes} pass{plural}\n")
                output.write(f"Start: {start_date}  End: {end_date}\n")
                output.write(f"Compute Time: {time_taken} {unit}\n")
                plural = "s" if error != 2 else ""
                if error:
                    output.write("Error Detected\n\n")
                else:
                    output.write("No errors detected\n\n")
                for res in residue_list:
                    output.write(f"Pass {res[0]}, Residue {res[1]}\n")
                plural = "" if len(str(2**p-1)) == 1 else "s"
                output.write(f"\n\n2^{p}-1   ---   {len(str(2**p-1))} Digit{plural}")
                if not error: 
                    if max(Mersenne_confirm_error) == 0:
                        output.write("   ---   is a Mersenne Prime\n")
                    else:
                        output.write("   ---   is not a Mersenne Prime\n")
                else:
                    output.write("\n")
                output.write(f"{2**p-1}\n")
                if max(Mersenne_confirm_error) == 0:
                    output.write(f"\nPerfect Number\n2^{p - 1} · (2^{p}-1)\n{(2**(p-1))*(2**p-1)}\n")
                output.write("---------------------------------------------------------------------------------------")
            if not perm_stat:
                modified_size = os.path.getsize(file_path + custom_file)
                sign = "-" if modified_size - original_size < 0 else "+"
                plural = "" if modified_size - original_size == 0 else "s"
                print(f"{colors.GREEN}Success{colors.END}\n{custom_file} {sign}{modified_size-original_size} Bytes")
        
        wait(0)
    else:
        sys.exit(0)
    
# End of Program
