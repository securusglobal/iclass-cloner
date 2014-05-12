import os
import time
import sys
import pickle
import datetime
from subprocess import *

def card_pop(pop_value, list_number):
    return_value = pop_value.pop()
    card_value = return_value[0]
    card_value_split = card_value.split(',')
    csn_value = card_value_split[0]
    time_stamp = return_value[1]
    final_value =  str(list_number) + ' - ' + time_stamp + " - " + csn_value
    return final_value

def write_card(card_data):
    raw_input("[Card is about to be written, make sure card is in reader field and hit ENTER to continue.]")
    card_data = 'lf hid clone ' + card_data
    os.system("echo %s > logs/prox_write" % card_data)
    os.system("/root/pm3/client/proxmark3 < logs/prox_write")
    time.sleep(4)

def pick_card():
    if os.path.exists("logs/cards_prox.p.lck"):
        print "Card file locked"
        time.sleep(1)
        sys.exit()
    elif os.path.exists("logs/cards_prox.p"):
        cards = pickle.load(open("logs/cards_prox.p", "rb"))
    else:
        print "No log file to write from."
        time.sleep(1)
        sys.exit()
    list_prox_cards = pickle.load(open("logs/cards_prox.p", "rb"))
    x = len(list_prox_cards)
    if x > 0:
        list_number = 0
        list_prox_card = []
        for i in range(x):
            list_number += 1
            list_prox_card.append(card_pop(list_prox_cards, list_number))
            sorted_prox_cards = sorted(list_prox_card, key=str.lower)
        os.system("clear")
        print "-------------------------------------------------"
        print '\n'.join(sorted_prox_cards)
        print "-------------------------------------------------"
        print "[Choose number to write or select '0' to quit to menu]"
        choice = raw_input('> ')
        choice = int(choice)
        if choice > x or choice < 0:
            print '[Selection incorrect or is not recognised]'
            time.sleep(2)
            os.system("clear")
            pick_card()
        elif choice == 0:
            pass 
        else:
            for a in range(0, choice):
               return_choice = ""
               return_choice = sorted_prox_cards.pop(0)
            card_value = return_choice.split(' ')
            card_value = card_value[5]
            write_card(card_value)
