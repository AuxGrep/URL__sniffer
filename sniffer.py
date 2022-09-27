#!/usr/bin/python3
#Written_By_Auxgrep

import time
import os

def cmd():

        target_list = input("Enter the target Domain(eg. facebook.com): ")
        time.sleep(2)
        print("")
        data_con = target_list
        limit = "/url_list?limit=200&page=1"
        char2 = limit[0]
        cmdx = os.system('curl -s "https://otx.alienvault.com/api/v1/indicators/domain{}{}{}"| jq -r .url_list[].url'\
        .format(char2, data_con, limit))
cmd();

