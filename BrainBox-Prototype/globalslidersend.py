def init():
        #####
        global slidersend , indexuser ,userdatalist , usernamepassword #, userdata
        slidersend = []
        userdatalist = []
        userdatafile = open("UserData.txt",'r+')
        userdata = userdatafile.readlines()
        userloginfile = open("UserLogin.txt",'r')
        userlogin = userloginfile.readlines()
        usernamepassword = {}
                
        #print userdatalist
        for x in range(len(userdata)):
                #print userdata[x]
                if userdata[x] != '\n' or userdata[x] != '':
                        userdatalist.append([])
                        userdalist = userdata[x].strip().split(',')
                #userlist.append(userdalist[0])
                #print userdalist
                        for y in range(len(userdalist)):
                                userdatalist[x].append(userdalist[y])
        #pritn
        for x in range(len(userlogin)):
                userdatalist.append([])
                userdalist = userlogin[x].strip().split(',')
                usernamepassword[userdalist[0]] = userdalist[1]
                
       # print usernamepassword
       # print userdatalist
#
##  print userdatalist
##  username =  raw_input("Enter your username : ")
##  if username in userlist:
##      indexuser = userlist.index(username)
##      for x in range(1,len(userdatalist[indexuser])):
##          #print userdatalist[indexuser][x]
##          #print
##          slidersend.append(float(userdatalist[indexuser][x]))
##      #print slidersend
##  else :
##      userdatafile.write('\n'+"%s,0,0,0,0,0,0,0,0,0,0,0"%username)
##      userlist.append(username)
##      indexuser = userlist.index(username)
##      slidersend = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 ]
##  userdatafile.close()

        #####

#init()
