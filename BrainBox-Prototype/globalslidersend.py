def init():

        global slidersend , indexuser ,userdatalist , usernamepassword #, userdata
        slidersend = []
        userdatalist = []
        userdatafile = open("UserData.txt",'r+')
        userdata = userdatafile.readlines()
        userloginfile = open("UserLogin.txt",'r')
        userlogin = userloginfile.readlines()
        usernamepassword = {}

        for x in range(len(userdata)):
                if userdata[x] != '\n' or userdata[x] != '':
                        userdatalist.append([])
                        userdalist = userdata[x].strip().split(',')

                        for y in range(len(userdalist)):
                                userdatalist[x].append(userdalist[y])

        for x in range(len(userlogin)):
                userdatalist.append([])
                userdalist = userlogin[x].strip().split(',')
                usernamepassword[userdalist[0]] = userdalist[1]

