# Uncomment the next two lines if you want to save the animation
#import matplotlib #matplotlib.use("Agg")

import numpy
import socket
#from matplotlib.pylab import *
#from mpl_toolkits.axes_grid1 import host_subplot
#import matplotlib.animation as animation
#import threading


"""\
This module provides the EPOC class for accessing Emotiv EPOC
EEG headsets.
"""

import os
import globalslidersend


from Crypto.Cipher import AES

import usb.core
import usb.util

import numpy as np

import utils
from math import *
import time

from epoc import *




def std_dev(lst,mean):
	n = len(lst)
	variance = 0
	for i in range(n):
		itemVariance = ((lst[i]-mean)**2)/(n-1)
		variance = variance + itemVariance
	std_dev = sqrt(variance)
	return std_dev



def mean(lst):
	mean = sum(lst)/len(lst)
	return mean

def cov(x,y):
	covariance = 0
	meanx = mean(x)
	meany = mean(y)
	n = len(x)
	for i in range(n):
		itemCovariance = ((x[i]-meanx)*(y[i]-meany))/(n+1)
		covariance = covariance + itemCovariance
	return covariance

def cor(lst1,lst2):
	covariance = 0
	meanx = mean(lst1)
	meany = mean(lst2)
	n = len(lst1)
	variance = 0
	variance2 = 0
	for i in range(n):
		itemCovariance = ((lst1[i]-meanx)*(lst2[i]-meany))/(n+1)
		covariance = covariance + itemCovariance

	
		itemVariance2 = ((lst1[i]-meanx)**2)/(n-1)
		variance = variance + itemVariance2

		itemVariance3 = ((lst2[i]-meany)**2)/(n-1)
		variance2 = variance2 + itemVariance3

	if variance >0 and variance2 >0:
		return covariance/(variance*variance2)
	else:
		return 0

def smooth_fun(lst,lstsmoothed):
	smooth = 0
	smooth = sum(lst)/4
	lstsmoothed.append(smooth)
	return lstsmoothed
	

def slope(lst,lstsmoothed):
	num = 4
	smooth = 0
	smooth = sum(lst)/num
	lstsmoothed.append(smooth)
	return lstsmoothed
	


class Detect:
	counter =0
	af3_s = []
	f7_s = []

	p7_s = []
	p8_s = []
	f3_s = []
	fc5_s = []
	t7_s = []
	s01_s = []
	s02_s = []
	t8_s = []
	f8_s = []
	af4_s = []
	fc6_s = []
	f4_s = []
	qu_s = []
	
	avg_af3 = 0 #memoryless avg
	avg_f7 = 0

	avg_p7 = 0
	avg_p8 = 0
	avg_f3 = 0
	avg_fc5 = 0
	avg_t7 = 0
	avg_s01 = 0
	avg_s02 = 0
	avg_t8 = 0
	avg_f8 = 0
	avg_af4 = 0
	avg_fc6 = 0
	avg_f4 = 0
	avg_qu = 0

	
	data = []
	#def send(result):
	def affective(self,run,clientSocket):
		global slidersender
		global e
		count = 0
		count2 = 0
		af3smooth = []
		f7smooth = []

		f8smooth = []
		f3smooth = []
		af4smooth = []
		t7smooth = []
		t8smooth = []

		fc6smooth = []
		fc5smooth = []
		p7smooth = []
		f4smooth = []

		af3_std= 0
		f7_std = 0

		f8_std= 0
		af4_std = 0

		fc6_std= 0
		fc5_std= 0
		p7_std = 0
		t7_std = 0
		t8_std = 0
		f4_std = 0
		f3_std = 0
	

		slider = []

		raise_p = 0
		left_p = 0
		right_p = 0
		clench_p = 0

		r_f = 0
		rw_f = 0
		lw_f = 0
		c_f = 0
		
		cov_af3_f7 = 0  #for left wink

		cov_f8_af4 = 0  #for right wink

		cov_af3_af4 = 0 #for raise eyebrows

		corr_fc5_fc6 = 0
		cov_fc5_f8 = 0
		cov_fc6_f8 = 0
		cov_fc5_fc6 = 0
		#cov_af3_f8 = 0  #for furrow
		old_cnt = 0
		flag = 0
		
		old_af4_m = 0
		old_f4_m = 0
		old_af3_m = 0
		old_f8_m = 0
		old_f7_m = 0
		old_fc5_m = 0
		old_fc6_m = 0
		old_f3_m = 0
		old_t7_m = 0
		old_t8_m = 0
		old_p7_m = 0
		
		n = 0
	
		
		
		l , ri ,ral,cl,cl2 = 0,0,0,0,0
		smooth = 0
		print "ready, set, do something with your face"
		while run:
                        try:
				self.data = e.get_sample()
				if self.data:

					self.counter = self.counter+1
					self.af3_s.append(self.data[2]) #appends signals
					self.f7_s.append(self.data[3])
					self.fc5_s.append(self.data[1])
					self.f3_s.append(self.data[0])
					self.t7_s.append(self.data[4])
					self.p7_s.append(self.data[5])
					#self.s01_s.append(self.data[6])
					#self.s02_s.append(self.data[7])
					#self.p8_s.append(self.data[8])
					self.t8_s.append(self.data[9])
					self.f8_s.append(self.data[10])
					self.af4_s.append(self.data[11])
					self.fc6_s.append(self.data[12])
					self.f4_s.append(self.data[13])
					#self.qu_s.append(self.data[14])
					count = count+1
					old_cnt = old_cnt+1

	
					if count == 4:
						count = 0
						af3smooth = smooth_fun(self.af3_s,af3smooth)
						#print af3smooth
						self.af3_s = []

						f7smooth = smooth_fun(self.f7_s,f7smooth)
						self.f7_s = []

						f3smooth = smooth_fun(self.f3_s,f3smooth)
						self.f3_s = []

						f8smooth = smooth_fun(self.f8_s,f8smooth)
						self.f8_s = []

						af4smooth = smooth_fun(self.af4_s,af4smooth)
						self.af4_s = []

						fc6smooth = smooth_fun(self.fc6_s,fc6smooth)
						self.fc6_s = []

						fc5smooth = smooth_fun(self.fc5_s,fc5smooth)
						self.fc5_s = []

						p7smooth = smooth_fun(self.p7_s,p7smooth)
						self.p7_s = []

						t7_smooth = smooth_fun(self.t7_s,t7smooth)
						self.t7_s = []

						t8_smooth = smooth_fun(self.t8_s,t8smooth)
						self.t8_s = []

						f4smooth = smooth_fun(self.f4_s,f4smooth)
						self.f4_s = []

						
					if self.counter == 100:
						self.counter = 0
						self.max_af3 = max(af3smooth)
						self.max_f7 = max(f7smooth)
						self.max_f8 = max(f8smooth)
						self.max_af4 = max(af4smooth)
						self.max_fc6 = max(fc6smooth)
						self.max_fc5 = max(fc5smooth)
						self.max_p7 = max(p7smooth)
						self.max_t7 = max(t7smooth)
						#self.max_t8 = max(t8smooth)
						self.max_f4 = max(f4smooth)
						self.max_f3 = max(f3smooth)



						self.avg_af3 = (mean(af3smooth)+self.avg_af3)/2
						self.avg_f3 = mean(f3smooth)
						self.avg_f7 = (mean(f7smooth)+self.avg_f7)/2
						self.avg_t7 = (mean(t7smooth)+self.avg_t7)/2
						self.avg_f8 = (mean(f8smooth)+self.avg_f8)/2
						self.avg_af4 = (mean(af4smooth)+self.avg_af4)/2
						self.avg_fc5 = (mean(fc5smooth)+self.avg_fc6)/2
						self.avg_fc6 = (mean(fc6smooth)+self.avg_fc6)/2
						self.avg_f4 = (mean(f4smooth)+self.avg_f4)/2
						
				
						#############################
					
						af3_std = std_dev(af3smooth,self.avg_af3)
						f7_std = std_dev(f7smooth,self.avg_f7)

						f8_std = std_dev(f8smooth,self.avg_f8)
						f3_std = std_dev(f3smooth,self.avg_f3)
						t7_std = std_dev(t7smooth,self.avg_t7)
						#t8_std = std_dev(t8smooth,self.avg_t8)
						af4_std = std_dev(af4smooth,self.avg_af4)

						fc6_std = std_dev(fc6smooth,self.avg_fc6)
						fc5_std = std_dev(fc5smooth,self.avg_fc5)
						f4_std = std_dev(f4smooth,self.avg_f4)
					
					
	
						###################################
						
						totalprev = l + ri +ral+cl+cl2

						cov_af3_f7 = cov(af3smooth,f7smooth) #left wink
						cov_f8_af4 = cov(f8smooth,af4smooth) # right wink
						cov_fc5_f7 = cov(fc5smooth,f7smooth) #raise eyebrows
						cov_fc5_t7 = cov(fc5smooth,t7smooth) #raise eyebrows
						cov_af4_fc6 = cov(af4smooth,fc6smooth) #raise eyebrows
						cov_fc5_f8 = cov(fc5smooth,f8smooth) #clench 
						#cov_af3_fc5 = cov(af3smooth,fc5smooth) #clench 
						
						#print int(cov_af3_f7) , int(cov_f8_af4) ,int(cov_fc5_f7) ,int(cov_fc5_t7) ,int(cov_af4_fc6) ,int(cov_t8_f8) 

						cov_t7_fc6 = cov(t7smooth,fc6smooth) #raise eyebrows
						cov_af4_fc5 = cov(af4smooth,fc5smooth) #raise eyebrows
						cov_af3_af4 = cov(af3smooth,af4smooth) #raise eyebrows
						
						listofvalues =[]
						l = int(abs(cov_af3_f7)) #left wink
						ri = int(abs(cov_f8_af4)) # right wink
						ra1 = int(abs(cov_af3_af4)) #raise eyebrows
						cl = int(abs(cov_t7_fc6)) #clench
						#cl2 = abs(cov_af3_fc5) #clench
						
						listofvalues.append(l)
						listofvalues.append(ri)
						listofvalues.append(ra1)
						listofvalues.append(cl)
						#listofvalues.append(cl2)
						'''
						print "left", l
						print "right",ri
						print "raise",ra1
						print "clench",cl
						'''
						#print "clench2",cl2
						#print listofvalues
		
						ra2 = abs(cov_fc5_f7) #raise eyebrows
						ra3 = abs(cov_t7_fc6)#raise eyebrows
						ra4 = abs(cov_af4_fc6) #raise eyebrows
						ra5 = abs(cov_af4_fc5) #raise eyebrows

						
						#print 'cov', cov_af3_af4  #raise
					


						if len(globalslidersend.slidersend) > 0:
							raise_p = ((globalslidersend.slidersend[0])/100)
							left_p = ((globalslidersend.slidersend[1])/100)
							right_p = ((globalslidersend.slidersend[2])/100)
							clench_p = ((globalslidersend.slidersend[7])/100)			

						#print l ,'   ',ri,'   ' ,ra1,'   ' ,ra5 

	
					
						
						total = (l + ri) + (ra1 + cl) #+cl2
						#print l , ri , ra1 , cl , total
						cf = 0
						lf = 0
						rif = 0
						rf = 0
						tot = 0

						
						
						if n > 0:
	 						if prevtotal < total: #if the total covariances of the previous sample are less than the current total,
										#to further make sure there are never any double detections/false positives

								if max(listofvalues)/total > 0.5: #if the Covariance value is greater than 50% of all Covariances
												# it will never be the Raise covariance as all covariances increase
												#when a Raise occurs
									if listofvalues[0] == max(listofvalues) and l> 5000+(10000*left_p): #if the current events
														#covariance is the maximum and its crossed the
														#threshold value
										print "left"
										clientSocket.send('a')
										time.sleep(0.5)
									elif listofvalues[1] == max(listofvalues) and   ri> 5000+(10000*right_p):
										print "right"
										clientSocket.send('d')
										time.sleep(0.5)
									elif listofvalues[3] == max(listofvalues) and  cl> 5000+(10000*clench_p):
										print "clench"
										clientSocket.send('e')
										time.sleep(0.6)
								else: 								
									lri = l + ri >= ra1 + cl #lri(left and right flag) is equal one if left("l")+right("ri")
												#covariances >= ra1(raise) + cl (clench) covariances. Else it is zero
									lra = l + ra1 >= ri + cl #lra (left and raise flag)
									lch = l + cl >= ra1 + ri #lch (left and clench flag)
									if lri and lra and lch and l> 5000+(10000*left_p):
										print "left2"
										clientSocket.send('a')
										time.sleep(0.5)
									elif lri and not lra and not lch and  ri> 5000+(10000*right_p) :
										print "right2"
										clientSocket.send('d')
										time.sleep(0.5)
									elif not lri and not lra and lch and  cl> 5000+(10000*clench_p):
										print "clench2"
										clientSocket.send('e')
										time.sleep(0.6)
									elif  (ra1> 5000+(10000*raise_p)):
									
										print "raise "
										clientSocket.send('x')
										time.sleep(1)
						
								
						prevtotal = total
						
			
						n = 1

						af3smooth = []
						af4smooth = []
						f7smooth = []
						t7smooth = []
						p7smooth = []

						f8smooth = []
						fc6smooth = []
						fc5smooth = []
						f4smooth = []
			
	


			except EPOCTurnedOffError, ete:
			    print ete
			except KeyboardInterrupt, ki:
			    e.disconnect()
			    return 0          
def main():
        host , port = "127.0.0.1",10146
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
                program.affective(1,clientSocket)
        finally:
            print 'It is down' 
            clientSocket.send("Exit")
            clientSocket.close()
            time.sleep(10)        
    


e = EPOC()
	
if __name__ == "__main__":
    import sys
    sys.exit(main())
	


