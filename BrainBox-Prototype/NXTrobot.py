# Importing libraries
import socket
import nxt.locator
from nxt.motor import *
from nxt.bluesock import BlueSock

ID = '00:16:53:11:CF:21'

# Function for moving the robot forward
def on(b):
    #forward
    m_left = Motor(b, PORT_B)
    m_right = Motor(b, PORT_C)
    m_both=nxt.SynchronizedMotors(m_left,m_right,0)
    m_both.turn(100, 2000,brake=False)
    flag=1

# Function for braking the robot
def off(b):
    m_left = Motor(b, PORT_B)
    m_right = Motor(b, PORT_C)
    m_both=nxt.SynchronizedMotors(m_left,m_right,0)
    m_both.turn(-100, 2000,brake=False)
    flag=1

  Function for Turning the robot left
def left(b):
    m_right = Motor(b, PORT_C)
    m_right.turn(100, 330)
    flag=1

# Function for Turning the robot left
def right(b):
    m_left = Motor(b, PORT_B)
    m_left.turn(100, 330)
    flag=1

# The main Function
def main():
    # Coonecting with server
    host,port = "127.0.0.1" , 10160
    # Connecting with Robot via Bluetooth
    sock =  BlueSock(ID)
    b = sock.connect()
    clientSocket = socket.socket()
    clientSocket.connect((host,port))
    clientSocket.send('bluetooth '+'#')
    flag=0

    Chartext = clientSocket.recv(1024)
    print Chartext
    # Always listening for command
    while Chartext != "Exit":
        try:
            Chartext = clientSocket.recv(1024)
            if Chartext=='a':
                left(b)
            elif Chartext=='d':
                right(b)
            elif Chartext=='e':
                off(b)
            elif Chartext=='x':
                on(b)
            if flag==1:
                b = sock.connect()
                flag=0
        # Exception Handling
        except:
            sock.close()
            clientSocket.send('Exit')
            clientSocket.close()
            break

# Running the program
#main()
