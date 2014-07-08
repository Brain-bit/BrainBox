# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
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

from epoclibrary import *

#from BrainBoxGUI import *



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

def smooth_fun(lst,lstsmoothed):
	num = 5
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


	max_af3 = 0
	max_f7 = 0
	
	max_p7 = 0
	max_p8 = 0
	max_f3 = 0
	max_fc5 = 0
	max_t7 = 0
	max_s01 = 0
	max_s02 = 0
	max_t8 = 0
	max_f8 = 0
	max_af4 = 0
	max_fc6 = 0
	max_f4 = 0
	max_qu = 0
	
	data = []
	#def send(result):

	def affective(self,run):
		global slidersender
		global e
		count = 0
		count2 = 0
		af3smooth = []
		f7smooth = []

		f8smooth = []
		af4smooth = []

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
		f4_std = 0

		slider = []

		raise_slider = 0

		raise_p = 0
		left_p = 0
		
		raise_small_sigs_avg = []

		raise_small_sigs_smooth = []

		raise_small_sigs_std = 0

		raise_small_sigs_max = 0
		
		cov_af3_f7 = 0  #for left wink

		cov_f8_af4 = 0  #for right wink

		cov_af3_af4 = 0 #for raise eyebrows

		#cov_af3_f8 = 0  #for furrow

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
					#self.f3_s.append(self.data[0])
					#self.t7_s.append(self.data[4])
					self.p7_s.append(self.data[5])
					#self.s01_s.append(self.data[6])
					#self.s02_s.append(self.data[7])
					#self.p8_s.append(self.data[8])
					#self.t8_s.append(self.data[9])
					self.f8_s.append(self.data[10])
					self.af4_s.append(self.data[11])
					self.fc6_s.append(self.data[12])
					self.f4_s.append(self.data[13])
					#self.qu_s.append(self.data[14])
					count = count+1
					count2 = count2 +1
					"""

					if count2 == 300:
						print "MEASURE"
						print "af3", self.af3_s
						'''
						print "#################"
						print "F7", self.f7_s
						print "#################"
						print "p7",self.p7_s 
						print "#################"
						print "p8",self.p8_s
						print "#################"
						print "f3",self.f3_s 
						print "fc5", self.fc5_s
						print "t7",self.t7_s
						print "01",self.s01_s 
						print "02", self.s02_s
						print "t8", self.t8_s
						print "f8", self.f8_s
						print "af4",self.af4_s 
						print "fc6",self.fc6_s
						print "f4",self.f4_s
						count2 = 0
						'''
					"""
					if count == 5:
						count = 0
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

						fc5smooth = smooth_fun(self.fc5_s,fc5smooth)
						self.fc6_s = []

						p7smooth = smooth_fun(self.p7_s,p7smooth)
						self.p7_s = []

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
						self.max_f4 = max(f4smooth)



						#print 'af3 smooth',af3smooth,'max',self.max_af3

						"""
						self.max_fc5 = max(self.fc5_s)
						self.max_f3 = max(self.f3_s)
						self.max_t7 = max(self.t7_s)
						self.max_s01 = max(self.s01_s)
						self.max_s02 = max(self.s02_s)
						self.max_t8 = max(self.t8_s)
					
						self.max_f8 = max(self.f8_s)
						self.max_af4 = max(self.af4_s)
						self.max_fc6 = max(self.fc6_s)
						self.max_f4 = max(self.f4_s)
					
						self.max_qu = max(self.qu_s)
						"""
						#self.max_fc6 = max(self.fc6_s)
						#print 'maxf7',self.max_f7
						#print 'maxaf3',self.max_af3


						self.avg_af3 = mean(af3smooth)
						self.avg_f7 = mean(f7smooth)
						self.avg_f8 = mean(f8smooth)
						self.avg_af4 = mean(af4smooth)
						self.avg_fc6 = mean(fc6smooth)
						self.avg_fc5 = mean(fc5smooth)
						self.avg_p7 = mean(p7smooth)
						self.avg_f4 = mean(f4smooth)

						raise_small_sigs_smooth = fc5smooth + f8smooth

						raise_small_sigs_max = max(raise_small_sigs_smooth)


						raise_small_sigs_avg = self.avg_fc5+self.avg_f8

						raise_small_sigs_std = std_dev(raise_small_sigs_smooth,raise_small_sigs_avg)
						
						af3_std = std_dev(af3smooth,self.avg_af3)
						#print 'af3 std dev', af3_std
						f7_std = std_dev(f7smooth,self.avg_f7)

						f8_std = std_dev(f8smooth,self.avg_f8)
						af4_std = std_dev(af4smooth,self.avg_af4)

						fc6_std = std_dev(fc6smooth,self.avg_fc6)
						f4_std = std_dev(f4smooth,self.avg_f4)


						cov_af3_f7 = cov(af3smooth,f7smooth) #left wink
						cov_f8_af4 = cov(f8smooth,af4smooth) # right wink
						cov_af3_af4 = cov(af3smooth,af4smooth) #raise eyebrows
						cov_af3_f8 = cov(af3smooth,f8smooth) #furrow
						#cov_fc6_f4 = cov(fc6smooth,f4smooth)
						
						#print 'avgf7',self.avg_f7
						
						#print 'avgaf3',self.avg_af3
						"""
						self.avg_fc5 = sum(self.fc5_s)/len(self.fc5_s)
						self.avg_f3 = sum(self.f3_s)/len(self.f3_s)
						self.avg_t7 = sum(self.t7_s)/len(self.t7_s)
						self.avg_s01 = sum(self.s01_s)/len(self.s01_s)
						self.avg_s02 = sum(self.s02_s)/len(self.s02_s)
						self.avg_t8 = sum(self.t8_s)/len(self.t8_s)
						self.avg_f8 = sum(self.f8_s)/len(self.f8_s)
						self.avg_af4 = sum(self.af4_s)/len(self.af4_s)
						self.avg_fc6 = sum(self.fc6_s)/len(self.fc6_s)
						self.avg_f4 = sum(self.f4_s)/len(self.f4_s)
						self.avg_qu = sum(self.qu_s)/len(self.qu_s)

						self.avg_fc6 = sum(self.fc6_s)/len(self.fc6_s)
						"""
						
						raise_small_sigs_smooth = []	
						af3smooth = []
						f7smooth = []

						f8smooth = []
						af4smooth = []

						fc6smooth = []
						fc5smooth = []
						p7smooth = []
						f4smooth = []
						"""
						self.fc6 = []
						
						self.fc5 =[]
						self.f3 = []
						self.t7 = []
						self.s01 = []
						self.s02 = []
						self.t8 = []
						self.f8 = []
						self.af4 = []
						self.fc6 = []
						self.f4 = []
						self.qu = []
						
			
						"""
						"""
						print 'cov', cov_af3_f7  #left
						print "Af3 max", self.max_af3
						print "Af3 avg", self.avg_af3
						print "F7 max", self.max_f7
						print "F7 avg", self.avg_f7
						"""
						"""
						"""
						'''
						print 'cov', cov_af3_af4  #raise

						print 'max_af3',self.max_af3
						print 'VALUE *2 af3', (af3_std*2) + self.avg_af3
						print 'max_af4', self.max_af4
						print 'VALUE *2 af4', (af4_std*2) + self.avg_af4

						print 'max_af3',self.max_af3
						print 'VALUE af3', (af3_std*1.4) + self.avg_af3
						print 'max_af4', self.max_af4
						print 'VALUE af4', (af4_std*1.4) + self.avg_af4
						'''
						'''
						print "raise small sigs max" , raise_small_sigs_max
						print "raise small sigs avg" , raise_small_sigs_avg
						print "raise small sigs std" , raise_small_sigs_std
						'''
						

						#print 2*af3_std + self.avg_af3
						#if self.max_af3 < ((1.1*af3_std)+self.avg_af3): #not really neutral state
							#print " neutral state"

					#	slider = slidersender()
						
						

						#raise_slider = 0
						if len(globalslidersend.slidersend) > 0:
							#raise_slider = globalslidersend.slidersend[0]
							raise_p = ((globalslidersend.slidersend[0]/100))
							left_p = ((globalslidersend.slidersend[1]/100))
							


						if self.max_af3 >(((2+(1*raise_p)) * af3_std)+self.avg_af3) and af3_std>((0.03+(0.03*raise_p))*self.avg_af3) and self.max_af4 > (((2+(1*raise_p))*af4_std)+self.avg_af4) and af4_std  > ((0.03+(0.03*raise_p)) * self.avg_af4) and (cov_af3_af4 > 500+(500*raise_p) or cov_af3_af4 <-500+(-500*raise_p)):
							print "Raise eyebrows detected1"
							time.sleep(0.5)

						
						elif (cov_af3_af4 > 1000+(1000*raise_p) or cov_af3_af4<-1000+(1000*-raise_p)) and self.max_af3 > ((1.1*af3_std)+self.avg_af3) and af3_std > ((0.03+(.03*raise_p))*self.avg_af3) and self.max_af4 > ((1.1*af4_std)+self.avg_af4) and af4_std  > ((0.03+(0.03*raise_p))*self.avg_af4):
							print "Raise eyebrows detected2"
							time.sleep(0.5)
					

						elif self.max_af3 > ((2*af3_std)+self.avg_af3) and af3_std > (0.007*self.avg_af3) and self.max_f7 > ((2*f7_std)+self.avg_f7) and f7_std  > (0.007*self.avg_f7) and (cov_af3_f7 > 500+(1000*left_p) or cov_af3_f7 <-500+(1000*-left_p)):
								#print 'af3 max', self.max_af3, 'std', af3_std, 'avg',self.avg_af3
							print "Left wink detected1"
							time.sleep(0.5)

						elif cov_af3_f7 > 2000 and self.max_af3 > ((1.5*af3_std)+self.avg_af3) and af3_std > (0.007*self.avg_af3) and self.max_f7 > ((1.5*f7_std)+self.avg_f7) and f7_std  > (0.007*self.avg_f7):
							print "Left wink detected2"
							time.sleep(0.5)	
						

						elif self.max_f8 >((2 * f8_std)+self.avg_f8) and f8_std>(0.007*self.avg_f8) and self.max_af4 > ((2*af4_std)+self.avg_af4) and af4_std  > (0.007 * self.avg_af4) and cov_f8_af4 > 4000:
							print "Right wink detected1"
							time.sleep(0.5)

						elif cov_f8_af4 > 1000 and self.max_f8 > ((1.5*f8_std)+self.avg_f8) and f8_std > (0.007*self.avg_f8) and self.max_af4 > ((1.5*af4_std)+self.avg_af4) and af4_std  > (0.007*self.avg_af4):
							print "Right wink detected2"
							time.sleep(0.5)



						"""
						elif self.max_af3 >((2 * af3_std)+self.avg_af3) and af3_std>(0.007*self.avg_af3) and self.max_f8 > ((2*f8_std)+self.avg_f8) and f8_std  > (0.007 * self.avg_f8) and cov_af3_f8 > 500:
							print "Furrow eyebrows detected"
							time.sleep(0.5)

						elif cov_af3_f8 > 1000 and self.max_af3 > ((1.5*af3_std)+self.avg_af3) and af3_std > (0.007*self.avg_f8) and self.max_f8 > ((1.5*f8_std)+self.avg_f8) and f8_std  > (0.007*self.avg_f8):
							print "Furrow eyebrows detected"
							time.sleep(0.5)

						"""
			
	


			except EPOCTurnedOffError, ete:
			    print ete
			except KeyboardInterrupt, ki:
			    e.disconnect()
			    return 0              
def main():
	program = Detect()
	program.affective(1)

e = EPOC()
	
if __name__ == "__main__":
    import sys
    sys.exit(main())
	


