#Importing libraries
import time
import socket
from array import *
import pickle,sys
import threading,time
from piboard import *
text = " "
lock = threading.Lock()


    
#Main function
def main():
    TextToKeyMap ={    '1': 'KEY_1',    '2': 'KEY_2',    '3': 'KEY_3',    '4': 'KEY_4',    '5': 'KEY_5',    '6': 'KEY_6',    'h': 'KEY_H',    'o': 'KEY_O',    'w': 'KEY_UP',    's': 'KEY_DOWN',    'a': 'KEY_LEFT',    'd': 'KEY_RIGHT',    'x': 'KEY_ESC',    'e': 'KEY_ENTER',    'l': 'KEY_L'}
    KeytoBlueMap = {'KEY_1' : 30,    'KEY_2' : 31,    'KEY_3' : 32,    'KEY_4' : 33,    'KEY_5' : 34,    'KEY_6' : 35,    'KEY_7' : 36,    'KEY_8' : 37,    'KEY_9' : 38,    'KEY_0' : 39,    'KEY_E' : 8,    'KEY_R' : 21,    'KEY_T' : 23,    'KEY_Y' : 28,    'KEY_U' : 24,    'KEY_I' : 12,    'KEY_O' : 18,    'KEY_P' : 19,    'KEY_H' : 11,    'KEY_E' : 8,    'KEY_L' : 15,    'KEY_O ': 18,    'KEY_W' : 26,    'KEY_R' : 21,    'KEY_D' : 7,    'KEY_1' : 30,    'KEY_SPACE' : 44,    'KEY_UP' : 82,    'KEY_PAGEUP' : 75,    'KEY_LEFT' : 80,    'KEY_RIGHT' : 79,    'KEY_DOWN' : 81,    'KEY_ENTER' : 40,    'KEY_ESC' : 41}
                
    MODIFIER_NONE = 0x00
    SHIFT_LEFT = 0x02
    
     
    global text , lock
    hid = Hid()
    hid.addService()
    hid.connect()
    time.sleep(5)
    host,port = "127.0.0.1" , 10141
    clientSocket = socket.socket()
    clientSocket.connect((host,port))
    
    try:
        #username = raw_input("Please Enter Your Username:")
        clientSocket.send('bluetooth '+'#')#username)
        textlist = []
        Chartext = clientSocket.recv(1024)
        print Chartext
        while Chartext != "end":
            Chartext = clientSocket.recv(1024)
            hid.sendKey(chr(KeytoBlueMap[TextToKeyMap[Chartext]]))
            
    except:
        
        print "server close"
        print "Unexpected error:", sys.exc_info()
    finally:
        
        print 'it is down' 
        clientSocket.send("Exit")
        clientSocket.close()
        time.sleep(10)        
        
main()
