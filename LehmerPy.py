# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao

import os
import sys
import platform
import time

#Global initialize
p_start_int = 2
max_p_value = 10**31
core_count = os.cpu_count()
arguments = sys.argv
release_ver = platform.release()
try:
    release_ver = int(release_ver)
    version_get = True
except:
    release_ver = 10
    version_get = False

os.system('') # Make sure all threads do this

class colors:
    def __init__(self, sysType=None):
        os.system('') # Somehow this lets ANSI escape codes work
        self.sysType = sysType
        self.purple = '\033[95m'
        self.cyan = '\033[96m'
        self.darkcyan = '\033[36m'
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.bold = '\033[1m'
        self.underline = '\033[4m'
        self.end = '\033[0m'
    def rmcolor(self):
        self.purple = ''
        self.cyan = ''
        self.darkcyan = ''
        self.blue = ''
        self.green = ''
        self.yellow = ''
        self.red = ''
        self.bold = ''
        self.underline = ''
        self.end = ''
    def encolor(self):
        self.purple = '\033[95m'
        self.cyan = '\033[96m'
        self.darkcyan = '\033[36m'
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.bold = '\033[1m'
        self.underline = '\033[4m'
        self.end = '\033[0m'

    def clear(self):
        if self.sysType == None:
            print('\x1b[2J\x1b[H')
        try:
            if self.sysType == "nt":
                os.system('cls')
            elif self.sysType == "posix" or self.sysType == "java":
                os.system('clear')
            else:
                print('\x1b[2J\x1b[H')
        except Exception:
            pass

colors = colors(os.name) # os.name is optional but when used it reduces random times when ANSI codes dont work

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
        try:
            wait = str(input("\nPress enter to exit..."))
            sys.exit(0)
        except:
            sys.exit(0)

def ll(p):
    s = 4
    m = (1 << p) - 1
    for _ in range(0, p-2):
        sqr = s*s
        s = (sqr & m) + (sqr >> p)
        if s >= m:
            s -= m
        s -= 2
    return s

def ll_hm(p):
    s = 4
    m = 2**p - 1
    for _ in range(0, p-2):
        sqr = s*s
        s = (sqr & m) + (sqr >> p)
        if s >= m:
            s -= m
        s -= 2
    return s

def Lucas_lehmer_confirm(p, passes, start_var, var, Mersenne_confirm_status, finished, ex, residue, arguments, memstat):
    try:
        if "-dc" in arguments or (version_get and release_ver < 10):
            colors.rmcolor()
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
            if memstat:
                m = 2**p - 1
            else:
                m = (1 << p) - 1
            for _ in range(0, p-2):
                sqr = s*s
                s = (sqr & m) + (sqr >> p)
                if s >= m:
                    s -= m
                s -= 2
            if s == 0:
                print(time.ctime(), colors.green+f"  Pass {counter} completed, {expand_1}{mstr}{p}{expand_2} is a Mersenne Prime"+colors.end, end="\n")
                Mersenne_confirm_status.put_nowait(0)
            else:
                print(time.ctime(), colors.yellow+f"  Pass {counter} completed, {expand_1}{mstr}{p}{expand_2} is not a Mersenne Prime"+colors.end, end="\n")
                Mersenne_confirm_status.put_nowait(1)
            residue.put_nowait([counter, s])       
    except MemoryError:
        print(f"{time.ctime()}   Worker {start_var+1}: {colors.red}ERROR FATAL:   MemoryError{colors.end}                                       ", end="\n")
    except KeyboardInterrupt:
        pass
    finally:
        finished.put_nowait(1)

def Lucas_lehmer_prog_main_range(p_start_int, start_var, var, maximum, Mersenne_primes_queue, finished, ex, odd, arguments, maxspeed, progress, memstat):
    try:
        if "-dc" in arguments or (version_get and release_ver < 10):
            colors.rmcolor()
        try:
            expand_1 = "2^" if ex else ""
            expand_2 = "-1" if ex else ""
            mstr = "" if ex else "M"
        except BaseException:
            expand_1 = ""
            expand_2 = ""
            mstr = "M"
        if odd or maxspeed:
            var_sub = 1 if p_start_int % 2 == 0 else 0 
            for p in range(p_start_int + start_var*2-var_sub, maximum + 1, var*2):
                if progress != "progress":
                    progress.put_nowait("")
                s = 4
                if memstat:
                    m = 2**p - 1
                else:
                    m = (1 << p) - 1
                for _ in range(0, p-2):
                    sqr = s*s
                    s = (sqr & m) + (sqr >> p)
                    if s >= m:
                        s -= m
                    s -= 2
                if s == 0:
                    Mersenne_primes_queue.put_nowait(p)
                    print(str(time.ctime()), colors.green+f"  Mersenne Prime Found:  {expand_1}{mstr}{p}{expand_2}"+ colors.end, end="\n")
                p += core_count
        else:
            for p in range(p_start_int + start_var, maximum + 1, var):
                if progress != "progress":
                    progress.put_nowait("")
                s = 4
                if memstat:
                    m = 2**p - 1
                else:
                    m = (1 << p) - 1
                for _ in range(0, p-2):
                    sqr = s*s
                    s = (sqr & m) + (sqr >> p)
                    if s >= m:
                        s -= m
                    s -= 2
                if s == 0:
                    Mersenne_primes_queue.put_nowait(p)
                    print(str(time.ctime()), colors.green+f"  Mersenne Prime Found:  {expand_1}{mstr}{p}{expand_2}"+ colors.end, end="\n")
                p += core_count
    except MemoryError:
        print(f"{time.ctime()}   Worker {start_var+1}: {colors.red}ERROR FATAL:   MemoryError{colors.end}                     ", end="\n")
    except KeyboardInterrupt:
        pass
    finally:
        finished.put_nowait(1)

# This is the Wheel animation
def loading_animation(wait_between, finished, core_count, progress, start, finish, multiplier):
    if not(progress == "progress"):
        while finished.qsize() != core_count:
            try:
                progress_stat = progress.qsize()*multiplier + start - 1
                print("| ", progress_stat, end="\r")
                time.sleep(wait_between)
                print("/ ", progress_stat, end="\r")
                time.sleep(wait_between)
                print("- ", progress_stat, end="\r")
                time.sleep(wait_between)
                print("\ ", progress_stat, end="\r")
                time.sleep(wait_between)
            except :
                continue
    else:
        try:
            while finished.qsize() != core_count:
                print("| ", end="\r")
                time.sleep(wait_between)
                print("/ ", end="\r")
                time.sleep(wait_between)
                print("- ", end="\r")
                time.sleep(wait_between)
                print("\ ", end="\r")
                time.sleep(wait_between)
        except KeyboardInterrupt:
            pass
    try:
        print(f"  {len(str(progress_stat))*' '}", end="\r")
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print(f"        ", end="\r")

def main():
    #Default Values Initialize phase

    #Display primes as exponents
    #Default False
    ex = False # -e

    individual_output = False # -io

    #LehmerPy V1.7 Development Beta
    #Const
    VERSION = 17
    BETA = False

    #Animation Speed - Smaller value = faster, -1 = off
    #Default 0.1
    loadani_speed = 0.1 # -l

    odd = True # -all or -ms
    out_file = False # -o
    maxspeed = False # -ms

    # Global Vars
    global p_start_int
    global max_p_value
    global core_count
    global arguments
    global release_ver
    global version_get
    global ll
    global ll_hm

    #Initialize Phase
    file_path = str(__file__)
    residue_list = []
    Mersenne_confirm_error = []
    Mersenne_primes = []
    perm_stat = True
    slash1 = "\ "
    slash2 = "/"
    doubleslash = slash1[0]*2
    reserved = ["reserved", "/", "?", "%", "*", ":", "|", "<", ">", '"', "-"]
    reserved[0] = slash1[0]
    fstart = file_path.rfind(slash1[0])
    if fstart == -1:
        fstart = file_path.rfind(slash2)
    file_name = file_path[fstart+1:len(file_path)]
    file_path = file_path.replace(file_name, "", 1)
    file_name = file_name[0:file_name.rfind(".")]
    custom_file = "output.txt"
    premquit = False
    multiplier = 1
    high_memory = False
    import hashlib
    hash_md5 = hashlib.md5()

    # CMD arguments get dealt with here
    if "-all" in arguments:
        odd = False
    if "-dc" in arguments or (version_get and release_ver < 10):
        colors.rmcolor()
    else:
        colors.encolor()
    if "-e" in arguments:
        ex = True
    if "-io" in arguments:
        individual_output = True
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
                    core_count = int(x[2:])
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
                    loadani_speed = float(x[2:])
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
                custom_file_str = str(x[2:])
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
    if "-np" in arguments:
        noprocess = True
    else:
        import multiprocessing
        from multiprocessing import Process, Queue
        multiprocessing.freeze_support()
        multiprocessing.set_start_method('spawn')
        Mersenne_primes_queue = Queue()
        Mersenne_confirm_status = Queue()
        finished = Queue()
        manager = multiprocessing.Manager()
        residue = manager.Queue()
        noprocess = False
    if "/?" in arguments or "?" in arguments:
        print("\n")
        print(f"Usage: {file_name} [-all]{dc} [-e] [-io] [-j int] [-l float] [-ms]")
        print(f"{' '*len(file_name)}        [-np] [-o name]")
        print("\n")
        print("Options:")
        print("    -all           Tests all numbers")
        if dc == " [-dc]":
            print("    -dc            Disables ANSI colors")
        print("    -e             Displays Mersenne primes as a power")
        print("    -io            Individualy outputs numbers as separate text files")
        print("    -j int         Threads to use")
        print("    -l float       Speed of progress wheel")
        print("    -ms            Use for maximum speed and efficiency")
        print("    -np            Disables multiprocessing")
        print("    -o name        Save output to txt. name is optional")
        print("\n")

        sys.exit(0)
    colors.clear()

    # ASCII Art
    # 4x
    ascii_art = [r"""_/\\\_____________________________/\\\___________________________________________________________/\\\\\\\\\\\\\_________________                
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

    if version_get and (release_ver < 10): ascii_art.pop(0)                                
    ascii_art_op = int(time.time()*100) % len(ascii_art)
    print(colors.bold+ascii_art[ascii_art_op]+colors.end)
    print("\n\n")
    VERSION /= 10
    if BETA:
        BETA = "b"
    else:
        BETA = ""
    print(f"v{VERSION}{BETA}\n")
    print("1:"+colors.bold+"R"+colors.end+"ange - Will Calculate Mersenne Primes in a specific range")
    print("2:"+colors.bold+"C"+colors.end+"onfirm - Will Confirm if a number is a Mersenne Prime or not")
    
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
        if p_start_int <= 2: p_start_int = 2
        if p_start_int >= ((1 << 32) - 1) or max_p_value >= ((1 <<32) - 1): high_memory = True
        print("\n")
        if not noprocess:
            fallback_core_count = 2
            if "-1" in str(loadani_speed):
                progress = "progress"
                start = p_start_int
                finish = 1
            else:
                progress = multiprocessing.JoinableQueue()
            print(f"{platform.processor()}\n")
            multiplier = 2 if odd or maxspeed else 1
            if core_count <= 0:
                print(str(time.ctime()),"  "+colors.red+"ERROR: Unable to retreive core count"+colors.end)
                print(str(time.ctime()),colors.yellow+f"  Setting core count to {fallback_core_count}"+colors.end)
                core_count = fallback_core_count
            if high_memory:
                print(f"{time.ctime()}{colors.yellow}   WARNING:   Memory usage will be higher than expected{colors.end}")
            start_date = time.ctime()
            start_time = time.time()        
            for num in range(core_count):
                print(str(time.ctime()), "  Starting Workers")
                multi = Process(target=Lucas_lehmer_prog_main_range, name=f"Worker {num + 1}", args=(p_start_int, num, core_count, max_p_value, Mersenne_primes_queue, finished, ex, odd, arguments, maxspeed, progress, high_memory))
                multi.start()
            if not "-1" in str(loadani_speed):
                loadani = Process(target=loading_animation, name="LoadingAnimation", args=(loadani_speed, finished, core_count, progress, p_start_int, max_p_value, multiplier))
                loadani.start()
            while finished.qsize() != core_count:
                try:
                    time.sleep(0.0001)
                except KeyboardInterrupt:
                    break
                except:
                    continue
            if not "-1" in str(loadani_speed):
                loadani.terminate()
                loadani.join()
            for num in range(core_count):
                print(str(time.ctime()), "  Stopping Workers")
                multi.terminate()
                multi.join()
            end_time = time.time()
            end_date = time.ctime()
            print(str(time.ctime()), "  Finishing")
            try:
                while not progress.empty():
                    progress.get_nowait()
            except AttributeError:
                pass
            while not Mersenne_primes_queue.empty():
                Mersenne_primes.append(Mersenne_primes_queue.get_nowait()) 
            Mersenne_primes.sort()
        else:
            print(f"{platform.processor()}\n")
            print(f"{time.ctime()}   Starting")
            if high_memory:
                ll = ll_hm
                print(f"{time.ctime()}{colors.yellow}   WARNING:   Memory usage will be higher than expected{colors.end}")
            try:
                expand_1 = "2^" if ex else ""
                expand_2 = "-1" if ex else ""
                mstr = "" if ex else "M"
            except BaseException:
                expand_1 = ""
                expand_2 = ""
                mstr = "M"
            start_date = time.ctime()
            start_time = time.time()
            try:
                if odd or maxspeed:
                    p_start_int -= 1 if p_start_int % 2 == 0 else 0
                    for p in range(p_start_int, max_p_value + 1, 2):
                        if ll(p) == 0:
                            print(time.ctime()+colors.green+f"   Mersenne Prime Found:  {expand_1}{mstr}{p}{expand_2}"+colors.end)
                            Mersenne_primes.append(p)
                else:
                    for p in range(p_start_int, max_p_value):
                        if ll(p) == 0:
                            print(time.ctime()+colors.green+f"   Mersenne Prime Found:  {expand_1}{mstr}{p}{expand_2}"+colors.end)
                            Mersenne_primes.append(p)
            except MemoryError:
                print(f"{time.ctime()}   {colors.red}ERROR FATAL:   MemoryError{colors.end}")
            except KeyboardInterrupt:
                pass
            print(f"{time.ctime()}   Finishing")
            end_time = time.time()
            end_date = time.ctime()
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
        print(f"{colors.underline}{colors.bold}Mersenne Prime{plural}{colors.end}{colors.end}")
        for x in Mersenne_primes:
            print(f"2^{x}-1 = {2**x-1}\n")
        print(f"\n\n{colors.bold}{colors.underline}Perfect Number{plural}{colors.end}{colors.end}")
        for x in Mersenne_primes:
            print(f"2^{x - 1} · (2^{x}-1) = {(2**(x-1))*(2**x-1)}\n")
        if individual_output == True:
            print("\n")
            primeLength = Mersenne_primes.index(max(Mersenne_primes))
            for prime in Mersenne_primes:
                ioname = f"M{prime}.txt"
                try:
                    with open(file_path+f"M{prime}.txt", "r", encoding='utf-8') as indread:
                        if os.path.exists(file_path+f"M{prime}.txt"):
                            indread.seek(0)
                            contents = indread.read()
                            if str(2**prime-1) != str(contents):
                                print(f"Changing contents of {file_path + ioname} ", end="")
                                while perm_stat:
                                    try:
                                        with open(file_path+f"M{prime}.txt", "w") as indout:
                                            indout.write(str(2**prime-1))
                                        perm_stat = False
                                        with open(file_path + ioname, "rb") as f:
                                            for chunk in iter(lambda: f.read(4096), b""):
                                                hash_md5.update(chunk)
                                            print(f"{' '*(primeLength-len(str(ioname))+12)}{hash_md5.hexdigest()}")
                                    except PermissionError:
                                        print(colors.red+"ERROR:   Permission to write to file denied"+colors.end)
                                        if wait(2):
                                            perm_stat = False
                                    except IOError:
                                        print(colors.red+"ERROR:   I/O Error"+colors.end)
                                        if wait(2):
                                            perm_stat = False
                                perm_stat = True
                            else:
                                print(f"{ioname} already exists ", end="")
                                with open(file_path + ioname, "rb") as f:
                                    for chunk in iter(lambda: f.read(4096), b""):
                                        hash_md5.update(chunk)
                                    print(f"{' '*(primeLength-len(str(ioname))+12)}{hash_md5.hexdigest()}")
                except FileNotFoundError:
                    while perm_stat:
                        try:
                            print(f"Generating {ioname} ", end="")
                            with open(file_path+f"M{prime}.txt", "w") as indout:
                                indout.write(str(2**prime-1))
                            perm_stat = False
                            with open(file_path + ioname, "rb") as f:
                                for chunk in iter(lambda: f.read(4096), b""):
                                    hash_md5.update(chunk)
                                print(f"{' '*(primeLength-len(str(ioname))+12)}{hash_md5.hexdigest()}")
                        except PermissionError:
                            print(colors.red+"ERROR:   Permission to write to file denied"+colors.end)
                            if wait(2):
                                perm_stat = False
                        except IOError:
                            print(colors.red+"ERROR:   I/O Error"+colors.end)
                            if wait(2):
                                perm_stat = False
                    perm_stat = True
            print("\n", end="")
        if out_file:
            print("\n")
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
                    print(colors.red+"ERROR:   Permission to write to file denied"+colors.end)
                    if wait(2):
                        perm_stat = False
                except  IOError:
                    print(colors.red+"ERROR:   I/O Error"+colors.end)
                    if wait(2):
                        perm_stat = False
            with open(file_path + custom_file,"a") as output:
                output.write("\n\n---------------------------------------------------------------------------------------\n")
                output.write(f"{file_name} v{VERSION}{BETA} Args: ")  
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
                print(f"{colors.green}Success{colors.end}\n{custom_file} {sign}{modified_size-original_size} Byte{plural}")            
        print("\n")
        wait(0)


# Confirm Mode


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
        if passes <= 0 or p <= 0: sys.exit(0)
        if p >= ((1 << 32) - 1): high_memory = True
        if not noprocess:
            fallback_core_count = 2
            print(f"\n\n{platform.processor()}\n")
            if core_count <= 0:
                print(str(time.ctime()),"  "+colors.red+"ERROR: Unable to retreive core count"+colors.end)
                print(str(time.ctime()),colors.yellow+f"  Setting core count to {fallback_core_count}"+colors.end)
                core_count = fallback_core_count
            if passes <= core_count:
                core_count = int(passes)
                if core_count <= 0:
                    core_count = 1
            progress = "progress"
            start = 0
            finish = 0
            if high_memory:
                print(f"{time.ctime()}{colors.yellow}   WARNING:   Memory usage will be higher than expected{colors.end}")
            start_date = time.ctime()
            start_time = time.time()
            for num in range(core_count):
                plural = " " if passes == 1 else "s"
                print(time.ctime(),f"  Starting Worker{plural}")
                multi = Process(target=Lucas_lehmer_confirm, name=f"Worker {num + 1}", args=(p, passes, num, core_count, Mersenne_confirm_status, finished, ex, residue, arguments, high_memory))
                multi.start()
            if not "-1" in str(loadani_speed):
                loadani = Process(target=loading_animation, name="LoadingAnimation", args=(loadani_speed, finished, core_count, progress, start, finish, multiplier)) 
                loadani.start()
            while finished.qsize() != core_count:
                try:
                    time.sleep(0.0001)
                except KeyboardInterrupt:
                    premquit = True
                    break
                except:
                    continue
            end_time = time.time()
            end_date = time.ctime()
            for num in range(core_count):
                print(str(time.ctime()) +f"   Stopping Worker{plural}")
                multi.terminate()
                multi.join()
            print(str(time.ctime())+"   Finishing")
            if not "-1" in str(loadani_speed):
                loadani.terminate()
                loadani.join()
            while not Mersenne_confirm_status.empty():
                Mersenne_confirm_error.append(Mersenne_confirm_status.get_nowait())
        else:
            print(f"\n\n{platform.processor()}\n")
            print(f"{time.ctime()}   Starting")
            if high_memory:
                ll = ll_hm
                print(f"{time.ctime()}{colors.yellow}   WARNING:   Memory usage will be higher than expected{colors.end}")
            try:
                expand_1 = "2^" if ex else ""
                expand_2 = "-1" if ex else ""
                mstr = "" if ex else "M"
            except BaseException:
                expand_1 = ""
                expand_2 = ""
                mstr = "M"
            start_date = time.ctime()
            start_time = time.time()
            try:
                for x in range(1, passes + 1):
                    lres = ll(p)
                    if lres == 0:
                        print(time.ctime(), colors.green+f"  Pass {x} completed, {expand_1}{mstr}{p}{expand_2} is a Mersenne Prime"+colors.end)
                        Mersenne_confirm_error.append(0)
                    else:
                        print(time.ctime(), colors.yellow+f"  Pass {x} completed, {expand_1}{mstr}{p}{expand_2} is not a Mersenne Prime"+colors.end)  
                        Mersenne_confirm_error(1)
                    residue_list.append([x, lres])
            except MemoryError:
                print(f"{time.ctime()}   {colors.red}ERROR FATAL:   MemoryError{colors.end}")
            except KeyboardInterrupt:
                pass
            print(f"{time.ctime()}   Finishing")
            end_time = time.time()
            end_date = time.ctime()            
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
        if not noprocess:
            while not residue.empty():
                residue_list.append(residue.get_nowait())
        residue_list.sort(key=lambda x: x[0])
        try:
            # for res in residue_list:
            #     print(f"Pass {res[0]}, Residue {res[1]}")
            padding = len(str(max(residue_list, key=lambda k:k[1]))) + len(str(residue_list.index(max(residue_list, key=lambda k:k[1])))) + 8
            columns = 3 if not(version_get and release_ver < 10) else 1 # + 1
            st_length = 0
            high_sec = 0
            rows = len(residue_list) // columns + len(residue_list) % columns
            for print_var in range(0,len(residue_list)*columns+1, columns):
                try:
                    ind_variation = 0
                    for sp_var in range(0,rows*columns+1,rows):
                        st_length = len(str(residue_list[print_var+print_var + ind_variation][0])) + len(str(residue_list[print_var+print_var + ind_variation][1]))
                        print(f"Pass {residue_list[print_var+print_var + ind_variation][0]}, Residue {residue_list[print_var+print_var + ind_variation][1]} {' '*(padding - st_length)}", end="")
                        high_sec = print_var+print_var + ind_variation
                        ind_variation += 1
                    print("\n",end="")
                except IndexError:
                    break
            for print_var in range(high_sec + 1, len(residue_list)):
                st_length = len(str(residue_list[print_var][0])) + len(str(residue_list[print_var][1]))
                print(f"Pass {residue_list[print_var][0]}, Residue {residue_list[print_var][1]} {' '*(padding - st_length)}", end="")
            print("\n", end="")
            if max(residue_list, key=lambda x: x[1]) == min(residue_list, key=lambda x: x[1]):
                error = False
                if max(Mersenne_confirm_error) == 0:
                    print(f"\n{colors.underline}{colors.bold}Mersenne Prime{colors.end}{colors.end}\n2^{p}-1 = {2**p - 1}")
                    if not error:
                        print("No errors detected")
                    print(f"\n{colors.underline}{colors.bold}Perfect Number{colors.end}{colors.end}\n2^{p - 1} · (2^{p}-1) = {(2**(p-1))*(2**p-1)}")
                else:
                    print(f"\n{colors.underline}{colors.bold}Mersenne Number{colors.end}{colors.end}\n2^{p}-1 = {2**p - 1}")
            else:
                print("Error Detected")
                error = True
        except ValueError:
            print(colors.red+"ERROR:   Premature Quit"+colors.end)
            sys.exit(0)
        print("\n")
        if individual_output and max(Mersenne_confirm_error) == 0:
            print("\n", end="")
            primeLength = len(str(p))
            prime = p
            ioname = f"M{prime}.txt"
            try:
                with open(file_path+f"M{prime}.txt", "r", encoding='utf-8') as indread:
                    if os.path.exists(file_path+f"M{prime}.txt"):
                        indread.seek(0)
                        contents = indread.read()
                        if str(2**prime-1) != str(contents):
                            print(f"Changing contents of {file_path + ioname} ", end="")
                            while perm_stat:
                                try:
                                    with open(file_path+f"M{prime}.txt", "w") as indout:
                                        indout.write(str(2**prime-1))
                                    perm_stat = False
                                    with open(file_path + ioname, "rb") as f:
                                        for chunk in iter(lambda: f.read(4096), b""):
                                            hash_md5.update(chunk)
                                        print(f"{' '*(primeLength-len(str(ioname))+12)}{hash_md5.hexdigest()}")
                                except PermissionError:
                                    print(colors.red+"ERROR:   Permission to write to file denied"+colors.end)
                                    if wait(2):
                                        perm_stat = False
                                except IOError:
                                    print(colors.red+"ERROR:   I/O Error"+colors.end)
                                    if wait(2):
                                        perm_stat = False
                            perm_stat = True
                        else:
                            print(f"{ioname} already exists ", end="")             
                            with open(file_path + ioname, "rb") as f:
                                for chunk in iter(lambda: f.read(4096), b""):
                                    hash_md5.update(chunk)
                                print(f"{' '*(primeLength-len(str(ioname))+12)}{hash_md5.hexdigest()}")                                        
            except FileNotFoundError:
                while perm_stat:
                    try:
                        print(f"Generating {ioname} ", end="")
                        with open(file_path+f"M{prime}.txt", "w") as indout:
                            indout.write(str(2**prime-1))
                        perm_stat = False
                        with open(file_path + ioname, "rb") as f:
                            for chunk in iter(lambda: f.read(4096), b""):
                                hash_md5.update(chunk)
                            print(f"{' '*(primeLength-len(str(ioname))+12)}{hash_md5.hexdigest()}")                      
                    except PermissionError:
                        print(colors.red+"ERROR:   Permission to write to file denied"+colors.end)
                        if wait(2):
                            perm_stat = False
                    except IOError:
                        print(colors.red+"ERROR:   I/O Error"+colors.end)
                        if wait(2):
                            perm_stat = False
                perm_stat = True
            print("\n", end="")            
        if out_file:
            print("\n")
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
                    print(colors.red+"ERROR:   Permission to write to file denied"+colors.end)
                    if wait(2):
                        perm_stat = False
                except IOError:
                    print(colors.red+"ERROR:   I/O Error"+colors.end)
                    if wait(2):
                        perm_stat = False
            with open(file_path + custom_file,"a") as output:
                output.write("\n---------------------------------------------------------------------------------------\n")
                output.write(f"{file_name} v{VERSION}{BETA} Args: ")  
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
                padding = len(str(max(residue_list, key=lambda k:k[1]))) + len(str(residue_list.index(max(residue_list, key=lambda k:k[1])))) + 8
                rows = len(residue_list) // columns + len(residue_list) % columns
                for print_var in range(0,len(residue_list)*columns+1, columns):
                    try:
                        ind_variation = 0
                        for sp_var in range(0,rows*columns+1,rows):
                            st_length = len(str(residue_list[print_var+print_var + ind_variation][0])) + len(str(residue_list[print_var+print_var + ind_variation][1]))
                            output.write(f"Pass {residue_list[print_var+print_var + ind_variation][0]}, Residue {residue_list[print_var+print_var + ind_variation][1]} {' '*(padding - st_length)}")
                            high_sec = print_var+print_var + ind_variation
                            ind_variation += 1
                        output.write("\n")
                    except IndexError:
                        break
                for print_var in range(high_sec + 1, len(residue_list)):
                    st_length = len(str(residue_list[print_var][0])) + len(str(residue_list[print_var][1]))
                    output.write(f"Pass {residue_list[print_var][0]}, Residue {residue_list[print_var][1]} {' '*(padding - st_length)}")
                output.write("\n\n")
                if premquit:
                    output.write("(Premature Quit)\n")
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
                print(f"{colors.green}Success{colors.end}\n{custom_file} {sign}{modified_size-original_size} Bytes")
            print("\n")

        wait(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
# End of Program
