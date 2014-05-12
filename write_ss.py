import os
import time
import sys
import serial
import pickle

#ser = serial.Serial(0, baudrate=57600, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
ser = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)

def csn_trim(c):
    d = c[2:-2]
    return d

def card_pop(pop_value, list_number):
    return_value = pop_value.pop()
    card_value = return_value[0]
    card_value_split = card_value.split(',')
    csn_value = card_value_split[0]
    time_stamp = return_value[1]
    final_value =  str(list_number) + ' - ' + time_stamp + " - " + csn_value
    return final_value

def get_csn_div():
    ser.write("\x80\xA4\x00\x32\x09") #Select_Card
    csn = ser.read(size=12) #Receive CSN
    ser.write("\x80\x52\x00\x03\x08") # Select_Current_Key
    ser.read(size=1) #ACK
    ser.write(csn_trim(csn)) #Transmit CSN
    ser.read(size=2) #ACK
    ser.write("\x80\xC0\x00\x00\x08") #Retrieve_Data
    div_key = ser.read(size=11) #Receive Reader Diversification Key

def write_data_blocks():
    ser.write("\x80\xA4\x30\x32\x09") #Select_Card
    ser.read(size=12) #Receive CSN
    ser.write("\x80\xC2\x69\x08\x0a") #Transmit(Write)
    ser.read(size=1) #ACK

def write_card(card_data):
    raw_input("[Card is about to be written, make sure card is in reader field and hit ENTER to continue.]")
    card_data = card_data[0]
    card_data = card_data.split(',')
    block9 = "\x87\x09" + card_data[-1].decode('hex')
    block8 = "\x87\x08" + card_data[-2].decode('hex')
    block7 = "\x87\x07" + card_data[-3].decode('hex')
    get_csn_div()
    time.sleep(0.2)

    write_data_blocks()
    ser.write(block7) #Write Block1 , Block Address, Data 
    ser.read(size=2) #ACK
    time.sleep(0.2)

    write_data_blocks()
    ser.write(block8) #Write Block1 , Block Address, Data 
    ser.read(size=2) #ACK
    time.sleep(0.2)

    write_data_blocks()
    ser.write(block9) #Write Block1 , Block Address, Data 
    ser.read(size=2) #ACK
    time.sleep(0.2)

    #Todo confirm write was good?
    ser.write("\x80\x70\x30\x00\x00") #Play Sound
    ser.read(size=2)
    
def pick_card():
    if os.path.exists("logs/cards_ss.p.lck"):
        print "Card file locked"
        time.sleep(1)
        sys.exit()
    elif os.path.exists("logs/cards_ss.p"):
        cards = pickle.load(open("logs/cards_ss.p", "rb"))
    else:
        print "No log file to write from."
        time.sleep(1)
        sys.exit()
    list_iclass_cards = pickle.load(open("logs/cards_ss.p", "rb"))
    x = len(list_iclass_cards)
    if x > 0:
        list_number = 0
        list_iclass_card = []
        for i in range(x):
            list_number += 1
            list_iclass_card.append(card_pop(list_iclass_cards, list_number))
            sorted_iclass_cards = sorted(list_iclass_card, key=str.lower)
        os.system("clear")
        print "-------------------------------------------------"
        print '\n'.join(sorted_iclass_cards)
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
               return_choice = sorted_iclass_cards.pop(0)
            csn_value = return_choice.split(' ')
            csn_value = csn_value[5]
            for item in cards:
                if csn_value in item[(0)]:
                    write_card(item)
