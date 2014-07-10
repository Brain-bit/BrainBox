
# Importing libraries
import numpy
import socket
import os
import time
import usb.core
import usb.util
import utils
import numpy as np
from math import *
from Crypto.Cipher import AES
from epoc import *

#time
slidersend = []

# A Function that calculates the mean of a list
def mean(lst):
    mean = sum(lst)/len(lst)
    return mean

# A Function that calculats the covarience between 2 variables (signals)
def cov(x,y):
    covariance = 0
    meanx = mean(x)
    meany = mean(y)
    n = len(x)
    for i in range(n):
        itemCovariance = ((x[i]-meanx)*(y[i]-meany))/(n+1)
        covariance = covariance + itemCovariance
    return covariance

# A Function that is responsible for smoothing
def smooth_fun(lst,lstsmoothed):
    smooth = 0
    smooth = sum(lst)/4
    lstsmoothed.append(smooth)
    return lstsmoothed
    
    

# A class that detects facial expressions using brain signals
class Detect:
    
    # Initializing empty lists for every electrode
    af3_s = []
    f7_s = []
    t7_s = []
    f8_s = []
    af4_s = []
    fc6_s = []

    # Initializing average variables for every electrode
    avg_af3 = 0 
    avg_f7 = 0
    avg_t7 = 0
    avg_f8 = 0
    avg_af4 = 0
    avg_fc6 = 0

    
    data = []
    
    # The expressive detection method
    def expressive(self,run,clientSocket):
        global e  # 
        global slidersend
        smoothingcount = 0
        samplecount = 0
        slider = []
        n= 0
        l ,ri ,ral,cl,cl2 = 0,0,0,0,0
        smooth = 0

        # Initializing empty lists for smoothing for each electrode
        af3smooth = []
        f7smooth = []
        f8smooth = []
        af4smooth = []
        t7smooth = []
        fc6smooth = []


        
        # Initializing Slider variables
        raise_p = 0
        left_p = 0
        right_p = 0
        clench_p = 0
         

        # Initializing Covariance variables
        cov_af3_f7 = 0  #for left wink
        cov_f8_af4 = 0  #for right wink
        cov_af3_af4 = 0 #for raise eyebrows
        cov_t7_fc6 = 0  #for clench teeth
        

                
        print " Ready, Set, Do something with your face"
        while run:
            try:
                self.data = e.get_sample()
                if self.data:
                    
                    # Appending signals
                    self.af3_s.append(self.data[2]) 
                    self.f7_s.append(self.data[3])
                    self.t7_s.append(self.data[4])
                    self.f8_s.append(self.data[10])
                    self.af4_s.append(self.data[11])
                    self.fc6_s.append(self.data[12])
                    smoothingcount = smoothingcount+1
                    samplecount = samplecount+1

                     # After collecting 4 samples, smooth them into one
                    if smoothingcount == 4:
                        smoothingcount = 0
                        af3smooth = smooth_fun(self.af3_s,af3smooth)
                        self.af3_s = []

                        f7smooth = smooth_fun(self.f7_s,f7smooth)
                        self.f7_s = []

                        f8smooth = smooth_fun(self.f8_s,f8smooth)
                        self.f8_s = []

                        af4smooth = smooth_fun(self.af4_s,af4smooth)
                        self.af4_s = []

                        fc6smooth = smooth_fun(self.fc6_s,fc6smooth)
                        self.fc6_s = []

                        t7_smooth = smooth_fun(self.t7_s,t7smooth)
                        self.t7_s = []


                        # Quality Checking

                        # Initializing quality checking variables for each electrode
##                      quality_AF3=0
##                      quality_A4=0                        
##                      quality_F7=0
##                      quality_F8=0
##                      quality_FC5=0
##                      quality_FC6=0
##
##                      # Obtaining the quality of the electrode
##                      x=e.quality['AF3']
##                      y=e.quality['AF4']
##                      z=e.quality['F7']
##                      a=e.quality['F8']
##                      b=e.quality['FC5']
##                      c=e.quality['FC6']
##                      
##                      # Checking for the quality of each electrode used to provide a warning to the user
##                      if x<4: 
##                          if quality_Af3==0:
##                              print "******************"
##                              print "CAUTION! AF3 signal is weak"
##                              print "******************"
##                          else:
##                              quality_AF3++;
##                      else:
##                          if quality_Af3!=0:
##                              print "AF3 signal is good again! :)"
##                          
##                      if y<4:
##                          if quality_AF4==0:
##                              print "******************"
##                              print "CAUTION! AF4 signal is weak"
##                              print "******************"
##                          else:
##                              quality_AF4++;
##                      else:
##                          if quality_AF4!=0:
##                              print "AF4 signal is good again! :)"
##                          
##                      if z<4:
##
##                          if quality_F7==0:
##                              print "******************"
##                              print "CAUTION! F7 signal is weak"
##                              print "******************"
##                          else:
##                              quality_F7++;
##                      else:
##                          if quality_F7!=0:
##                              print "F7 signal is good again! :)"
##
##                      
##                      if a<4:
##                          if quality_F8==0:
##                              print "******************"
##                              print "CAUTION! F8 signal is weak"
##                              print "******************"
##                          else:
##                              quality_F8++;
##                      else:
##                          if quality_F8!=0:
##                              print "F8 signal is good again! :)"
##          
##                      if b<4:
##                          if quality_FC5==0:
##                              print "******************"
##                              print "CAUTION! FC5 signal is weak"
##                              print "******************"
##                          else:
##                              quality_FC5++;
##                      else:
##                          if quality_FC5!=0:
##                              print "FC5 signal is good again! :)"
##                      
##                      if c<4:
##                          if quality_FC6==0:
##                              print "******************"
##                              print "CAUTION! FC6 signal is weak"
##                              print "******************"
##                          else:
##                              quality_FC6++;
##                      else:
##                          if quality_FC6!=0:
##                              print "FC6 signal is good again! :)"

                    # After collecting one hundred samples, begin processing
                    if samplecount == 100:
                                                
                        samplecount = 0
                        
                        # Get the maximum value of each signal
                        self.max_af3 = max(af3smooth)
                        self.max_f7 = max(f7smooth)
                        self.max_f8 = max(f8smooth)
                        self.max_af4 = max(af4smooth)
                        self.max_fc6 = max(fc6smooth)
                        self.max_t7 = max(t7smooth)

                        # Calculate the mean over the whole liftime of the signal
                        self.avg_af3 = (mean(af3smooth)+self.avg_af3)/2
                        self.avg_f7 = (mean(f7smooth)+self.avg_f7)/2
                        self.avg_t7 = (mean(t7smooth)+self.avg_t7)/2
                        self.avg_f8 = (mean(f8smooth)+self.avg_f8)/2
                        self.avg_af4 = (mean(af4smooth)+self.avg_af4)/2
                        self.avg_fc6 = (mean(fc6smooth)+self.avg_fc6)/2
                        
                        
                        
                        # Calculate the covariance for each event                       
                        cov_af3_f7 = cov(af3smooth,f7smooth) #left wink
                        cov_f8_af4 = cov(f8smooth,af4smooth) # right wink
                        cov_t7_fc6 = cov(t7smooth,fc6smooth) #clench teeth
                        cov_af3_af4 = cov(af3smooth,af4smooth) #raise eyebrows


                        # EXPLAIN IF POSSIBLE IN ONE SENTENCE bas mesh darory 5ales enty 2adra
                        listofvalues =[]
                        l = int(abs(cov_af3_f7)) #left wink
                        ri = int(abs(cov_f8_af4)) # right wink
                        ra1 = int(abs(cov_af3_af4)) #raise eyebrows
                        cl = int(abs(cov_t7_fc6)) #clench teeth
                        
                        listofvalues.append(l)
                        listofvalues.append(ri)
                        listofvalues.append(ra1)
                        listofvalues.append(cl)


                        # If a new value is present from the slider, update the slider variables
                        if len(slidersend) > 0:
                            raise_p = ((slidersend[0])/100)
                            left_p = ((slidersend[1])/100)
                            right_p = ((slidersend[2])/100)
                            clench_p = ((slidersend[7])/100)            

                        # Calculate the total covariance of all events
                        total = (l + ri) + (ra1 + cl)
                        tot = 0

                        
                        if n > 0: # At n = 0, skip the first window until you have previous covariance values to comapre with
                            if prevtotal < total: # if the total covariances of the previous sample are less than the current total,
                                        # to further make sure there are never any double detections/false positives

                                if max(listofvalues)/total > 0.5: # If the Covariance value is greater than 50% of all Covariances
                                                                # it will never be the Raise covariance as all covariances increase
                                                                # when a Raise occurs
                                    if listofvalues[0] == max(listofvalues) and l> 5000+(10000*left_p): #if the current events
                                                        #covariance is the maximum and its crossed the
                                                        #threshold value
                                        print "left"
                                        clientSocket.send('a')
                                        #time.sleep(0.5)
                                    elif listofvalues[1] == max(listofvalues) and   ri> 5000+(10000*right_p):
                                        print "right"
                                        clientSocket.send('d')
                                        #time.sleep(0.5)
                                    elif listofvalues[3] == max(listofvalues) and  cl> 5000+(10000*clench_p):
                                        print "clench"
                                        clientSocket.send('e')
                                        #time.sleep(0.6)
                                else:                               
                                    lri = l + ri >= ra1 + cl # lri(left and right flag) is equal one if left("l")+right("ri")
                                                             #covariances >= ra1(raise) + cl (clench) covariances. Else it is zero
                                    lra = l + ra1 >= ri + cl # lra (left and raise flag)
                                    lch = l + cl >= ra1 + ri # lch (left and clench flag)
                                    if lri and lra and lch and l> 5000+(10000*left_p):
                                        print "left2"
                                        clientSocket.send('a')
                                        #time.sleep(0.5)
                                    elif lri and not lra and not lch and  ri> 5000+(10000*right_p) :
                                        print "right2"
                                        clientSocket.send('d')
                                        #time.sleep(0.5)
                                    elif not lri and not lra and lch and  cl> 5000+(10000*clench_p):
                                        print "clench2"
                                        clientSocket.send('e')
                                        #time.sleep(0.6)
                                    elif  (ra1> 5000+(10000*raise_p)):
                                    
                                        print "raise "
                                        clientSocket.send('x')
                                        time.sleep(0.4)
                        
                                
                        prevtotal = total
                        
            
                        n = 1

                        af3smooth = []
                        af4smooth = []
                        f7smooth = []
                        t7smooth = []
                        f8smooth = []
                        fc6smooth = []
            
    

            # Error Handling from EPOC headset
            except EPOCTurnedOffError, ete:
                print ete
            # Error Handling from a keyboard interrupt
            except KeyboardInterrupt, ki:
                e.disconnect()
                return 0          
            # Exception handling for other errors
            except:
                print 'Unexpected Error: ',sys.exc_info()[0]
                
# The Main Function that is responsible for starting our program
def main():

        host , port = "127.0.0.1",10160
	clientSocket = socket.socket()
	clientSocket.connect((host,port))
	try:
		clientSocket.send('clientoutput','ah')
		chartext = clientSocket.recv(1024)
		print chartext
	except:
		print "server close"
        try :
        	program = Detect()
        	program.expressive(1,clientSocket)
        except:
                print 'dsa    ',sys.exc_info()[0]
        finally:
            print 'It is down' 
            clientSocket.send("Exit")
            clientSocket.close()
            time.sleep(10)

# Create epoc object, used for reading raw data
e = EPOC()

# Run main function
if __name__ == "__main__": 
    import sys
    sys.exit(main())
