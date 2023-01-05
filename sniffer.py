#!/usr/bin/python3
#Written_By_Auxgrep

import time
import os
import sys
import platform


def cmd():

        try:
                if platform.system() != 'Linux':
                        print('Script works with Linux Only')
                        sys.exit()
                else:
                        target_list = str(sys.argv[1])
                        time.sleep(1)
                        data_con = target_list
                        limit = "/url_list?limit=200&page=1"
                        char2 = limit[0]
                        cmdx = os.system('curl -s "https://otx.alienvault.com/api/v1/indicators/domain{}{}{}"| jq -r .url_list[].url'\
                        .format(char2, data_con, limit))
        except OSError:
                print('Unkown Error occured!! exiting')
                sys.exit()
cmd();



