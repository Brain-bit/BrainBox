def init():
	#####
	global slidersend , indexuser ,userdata,username
	slidersend = []
	userdatalist = []
	userdatafile = open("UserData.txt",'r+')
	userdata = userdatafile.readlines()
	userlist = []
	#print userdata
	for x in range(len(userdata)):
		#print userdata[x]
		userdatalist.append([])
		userdalist = userdata[x].strip().split(',') 
		userlist.append(userdalist[0]) 
		for y in range(len(userdalist)):	
			userdatalist[x].append(userdalist[y])
	
	print userdatalist
	username =  raw_input("Enter your username : ")
	if username in userlist:
		indexuser = userlist.index(username)
		for x in range(1,len(userdatalist[indexuser])):
			#print userdatalist[indexuser][x]
			#print 
			slidersend.append(float(userdatalist[indexuser][x]))
		#print slidersend
	else : 
		userdatafile.write('\n'+"%s,0,0,0,0,0,0,0,0,0,0,0"%username)
		userlist.append(username) 
		indexuser = userlist.index(username)
		slidersend = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 ]
	userdatafile.close()	

	#####


