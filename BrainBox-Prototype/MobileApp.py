#Importing libraries
import time
import socket
from array import *
import pickle,sys
import threading,time
from piboard import *

# Bluetooth connection with mobile
class bluetoothclient:
    def __init__(self):
        # Nedded dictionary for corresponding values from text to keymap
        TextToKeyMap ={'w': 'KEY_UP','s': 'KEY_DOWN','a': 'KEY_LEFT','d': 'KEY_RIGHT','x': 'KEY_ESC','e': 'KEY_ENTER',}
        # Nedded dictionary for corresponding keymap sent to android mobile
        KeytoBlueMap = {'KEY_UP' : 82,'KEY_PAGEUP' : 75,'KEY_LEFT' : 80,'KEY_RIGHT' : 79,'KEY_DOWN' : 81,'KEY_ENTER' : 40,'KEY_ESC' : 41}            
        hid = Hid()
        hid.addService()
        hid.connect()
        time.sleep(5)
        # Initializing server-client connection
        host,port = "127.0.0.1" , 10146
        clientSocket = socket.socket()
        clientSocket.connect((host,port))
        
        try:
            # Keep listening to send value to bluetooth device (mobile)
            clientSocket.send('bluetooth '+'#')
            textlist = []
            Chartext = clientSocket.recv(1024)
            print Chartext
            while Chartext != "end":
                Chartext = clientSocket.recv(1024)
                hid.sendKey(chr(KeytoBlueMap[TextToKeyMap[Chartext]]))

        # Exception handling        
        except:
            
            print "Server close"
            print "Unexpected Error: ", sys.exc_info()
        finally:
            
            print 'It is down' 
            clientSocket.send("Exit")
            clientSocket.close()
            time.sleep(10)        
    
#Main function
def main():
    bluetoothrun = bluetoothclient()
    
# Starting the file and mobile application       
main()
