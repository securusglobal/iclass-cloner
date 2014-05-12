import os
import time
import threading
import iclass_ss
import prox
import pickle

def card_pop(pop_value):
    return_value = pop_value.pop()
    card_value = return_value[0]
    card_value_split = card_value.split(',')
    csn_value = card_value_split[0]
    time_stamp = return_value[1]
    final_value =  time_stamp + " - " + csn_value
    return final_value

def status_update():
    try:
        shutdown = threading.Event()
        iclass_thread = threading.Thread(target=iclass_ss.clone, args=[shutdown])
        iclass_thread.start()
        prox_thread = threading.Thread(target=prox.clone, args=[shutdown])
        prox_thread.start()
        while True:
            os.system("clear")
            if os.path.exists("logs/cards_ss.p.lck"):
                print "iClass Standard Security credential being dumped"
            elif os.path.exists("logs/cards_ss.p"):
                iclass_cards = pickle.load(open("logs/cards_ss.p", "rb"))
                iclass_number = len(iclass_cards)
                print "You have logged %r iClass Standard Security card(s)" % (iclass_number)
            else:
                print "You have not logged any iClass Standard Security cards yet."
            print ""
            print "[Last 3 iClass cards]"
            if os.path.exists("logs/cards_ss.p.lck"):
                print "iClass Standard Security credential being dumped"
            elif os.path.exists("logs/cards_ss.p"):
                last_iclass_cards = pickle.load(open("logs/cards_ss.p", "rb"))
                x = len(last_iclass_cards)
                if x > 0:
                    last_iclass_card = []
                    for i in range(x):
                        last_iclass_card.append(card_pop(last_iclass_cards))
                    sorted_iclass_cards = sorted(last_iclass_card, key=str.lower)
                    sorted_iclass_cards = sorted_iclass_cards[-3:]
                    print "----------------------------------------------"
                    print '\n'.join(sorted_iclass_cards)
                    print "----------------------------------------------"
                    
                else:
                    print "You have not logged any cards yet"
            else:
                print "You have not logged any iClass Standard Security cards yet."
            print ""
            print ""
            if os.path.exists("logs/cards_prox.p.lck"):
                print "Prox credential being dumped"
            elif os.path.exists("logs/cards_prox.p"):
                prox_cards = pickle.load(open("logs/cards_prox.p", "rb"))
                prox_number = len(prox_cards)
                print "You have logged %r Prox card(s)" % (prox_number)
            else:
                print "You have not logged any Prox cards yet."
            print ""
            print "[Last 3 Prox cards]"
            if os.path.exists("logs/cards_prox.p.lck"):
                print "Prox credential being dumped"
            elif os.path.exists("logs/cards_prox.p"):
                last_prox_cards = pickle.load(open("logs/cards_prox.p", "rb"))
                x = len(last_prox_cards)
                if x > 0:
                    last_prox_card = []
                    for i in range(x):
                        last_prox_card.append(card_pop(last_prox_cards))
                    sorted_prox_cards = sorted(last_prox_card, key=str.lower)
                    sorted_prox_cards = sorted_prox_cards[-3:]
                    print "----------------------------------------------"
                    print '\n'.join(sorted_prox_cards)
                    print "----------------------------------------------"
                    print"Press CTRL-C to exit to menu"

                else:
                    print "You have not logged any cards yet"
            else:
                print "You have not logged any Prox cards yet."
            time.sleep(1)

    except KeyboardInterrupt:
        shutdown.set()
        os.system("clear")
