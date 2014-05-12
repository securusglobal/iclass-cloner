import os
import time
import sys
import handler_ss
import handler_hs
import write_ss
import write_hs
import write_prox
import prox

while True:
    os.system("clear")
    print "Menu"

    print "Please choose an option:"

    print "1. Log iClass Standard Security & Prox"
    print "2. Log iClass High Security & Prox"
    print "3. Write iClass Standard Security from log"
    print "4. Write iClass High Security from log"
    print "5. Write Prox from log"
    print "0. Quit"

    user_option = raw_input('> ')

    if user_option == "1":
        prox.start_prox()
        handler_ss.status_update()

    elif user_option == "2":
        prox.start_prox()
        handler_hs.status_update()

    elif user_option == "3":
        write_ss.pick_card()

    elif user_option == "4":
        write_hs.pick_card()

    elif user_option == "5":
        write_prox.pick_card()

    elif user_option == "0": 
        os.system("scripts/clean.sh")
        sys.exit()    
    else:
        os.system("clear")
        print "Well that obviously doesn't work "
        time.sleep(1) 
        os.system("clear")
