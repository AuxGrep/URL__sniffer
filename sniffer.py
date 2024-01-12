import time
import os
import platform
from datetime import datetime
import urllib.request as connection
import sys
from colorama import Fore, Style

# CODED By AuxGrep

# RANGI
red = Fore.RED
mangeta = Fore.MAGENTA
cyan = Fore.CYAN
reset = Style.RESET_ALL

if len(sys.argv) < 2:
        sys.exit(f'{red}USAGE: sudo python3 sniffer.py <target_domain>{reset}')

date_time = datetime.now()
formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

def net(site='https://google.com'):
    try:
        connection.urlopen(site)
        return True
    except:
        return False
    
def os_check(supported_os):
    if platform.system() in supported_os:
        return True
    else:
        return 'Unsupported os'
    
def Main():
    try:
        if net():
            print(f'{cyan}[Target: {sys.argv[1]}] Starting Program at  {formatted_date_time}{reset}')
            time.sleep(3)
            limit = "/url_list?limit=200&page=1"
            return os.system('curl -s "https://otx.alienvault.com/api/v1/indicators/domain{}{}{}"| \
                             jq -r .url_list[].url'\
                        .format(limit[0], str(sys.argv[1]), limit))
        else:
            sys.exit(f'\n{red}Connect your Pc with internet{reset}')
    except ConnectionError:
        sys.exit(f'{red}The API is Down!! COntact AuxGrep{reset}')

if __name__ == "__main__":
    os_check(supported_os=['Linux', 'Windows'])
    Main()
    



