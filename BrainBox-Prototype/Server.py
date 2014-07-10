#Importing libraries needed for implementation
import SocketServer
import threading
import time
from random import randint
from array import*
import pickle



# Flag to determine if it is working
end = 0
# List of clients to the server
clientslist = []
# Array that acts like a buffer to the clients
chatoutputlist = []

# A class that performs threading
class threadHandler(SocketServer.BaseRequestHandler):
    
    # A method for sending messages from the server
    def SendMessage(self):

        # Same global variables outside class
        global clientslist , end  ,chatoutputlist
        try :
            while True:
                # Seding all the data to the proper client
                if self.client_address == clientslist[0]:
                    while len(chatoutputlist[0]) != 0:
                        inf = chatoutputlist[0].pop(0)
                        print inf ,chatoutputlist
                        self.request.sendall(inf)
                else:
                   while len(chatoutputlist[1]) != 0:
                        inf = chatoutputlist[1].pop(0)
                        print inf,chatoutputlist
                        self.request.sendall(inf)
        # Exception handling
        except:print 'Exception occured... Exiting threading'
        
    # A method that keeps listening after connection has been estabilished with clients
    def ChatWithClient(self,username):
        
        # Same global variables outside class
        global clientslist , end  ,chatoutputlist
        # Flag for turning on/off connection with clients
        # Default flag for connection is ON since connection is already estabilished
        play='ON'
        
        while play=='ON':
            try:
                time.sleep(1)
                self.request.sendall('You are connected to the server. ')
                appinfo = username.split()

                if appinfo[0] == 'bluetooth':
                    print "You are connected to moblie through Bluetooth. ",appinfo 

                if appinfo[0] == 'clientoutput':                        
                    print "Info :",appinfo 
                # Only one client connected handling
                while len(clientslist) == 1:
                        print "Waiting ......."
                        inf = self.request.recv(1024)
                        if inf == 'Exit':
                            play = 'off'
                            print clientslist
                            clientslist.remove(self.client_address)
                            break                  
                # Two clients connected handling
                while len(clientslist) == 2:
                    inf = "On"
                    while inf != "Exit":
                        inf = self.request.recv(1024)
                        if self.client_address == clientslist[0]:
                            chatoutputlist[1].append(inf)
                        else:
                            chatoutputlist[0].append(inf)
                    if inf == 'Exit':
                            play = 'off'
                            print clientslist
                            clientslist.remove(self.client_address)
                            break
                        
                if play == 'off':
                    print "Off, Client out"
                    
           # Exception handling
            except:
                    play = 'Off'

    # Handles incoming message
    def handle(self):
        global clientslist ,chatoutputlist 
        data = ""

        clientinfo= self.request.recv(1024)          
        clientslist.append(self.client_address)
        chatoutputlist.append([])
        send_thread = threading.Thread(target=self.SendMessage, args=())
        send_thread.start()     
        self.ChatWithClient(clientinfo)

class ThreadServer (SocketServer.ThreadingMixIn , SocketServer.ForkingTCPServer):
    pass



#Main function
def main():
    global end
    #intializing the server connection 
    host = ''
    port = 10160
    
    server = ThreadServer((host,port),threadHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    try:
        while end == 0 :
            print "Working",clientslist
            time.sleep(10)
    # Exception handling        
    except:
        print 'Server is exiting'
        server.shutdown()
        time.sleep(5)
        print 'exit'
        
    finally:
        if  len(clientslist) != 0:
            for address in clientslist:
                socket.sendto('Exit',address)
            
        print 'Server is exiting'
        server.shutdown()
        time.sleep(6)

# Starting up the file and server
#main()
