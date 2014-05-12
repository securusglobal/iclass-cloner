import os
import sys
import pickle
import datetime
from subprocess import *

def start_prox():
    global p
    p = Popen(['/root/pm3/client/proxmark3'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.stdin.write('lf hid fskdemod\n')

def get_prox_card():
    cards = set()
    if os.path.exists("logs/cards_prox.p"):
        cards = pickle.load(open("logs/cards_prox.p", "rb")) 
    if os.path.exists("/root/script/proxmark3.log"):
        log_file = open("/root/script/proxmark3.log") 
        log_content = log_file.readlines()
        tag_dump = [i for i in log_content if "TAG ID:" in i]
        tag_list = []
        for i in tag_dump:
            stripped = i.replace('#db# TAG ID: ', '')
            stripped = stripped.replace('       \n', '')
            tag_list.append(stripped)
        tag_list = sorted(set(tag_list))
        worker_list = []
        for z in tag_list:
            worker_value = z.split(' ')
            if len(worker_value[0]) == 10:
                worker_value = ','.join(worker_value)
                worker_list.append(worker_value)
            else:
                pass
        for x in worker_list:
            if x not in [ c[0] for c in cards]:
                time_stamp = str(datetime.datetime.now())
                cards.add((x,time_stamp))
                #print "-------"
                #print cards
                lock_file = open('logs/cards_prox.p.lck', 'w')
                pickle.dump(cards, open('logs/cards_prox.p', 'wb'))
                lock_file.close()
                os.remove('logs/cards_prox.p.lck')
    else:
        pass

def clone(shutdown):
    while True:
        if shutdown.is_set():
            p.kill()
            sys.exit()
        get_prox_card()
