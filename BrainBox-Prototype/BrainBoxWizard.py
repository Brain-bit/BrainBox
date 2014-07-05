from PyQt4 import QtGui, QtCore
import os
def createIntroPage():
    page = QtGui.QWizardPage()
    page.setTitle("Introduction")

    label = QtGui.QLabel("Welcome to the BrainBox Wizard. Please follow the wizard in order to register your device and callibrate the BCI headset with your appplications. Please connect the headset into the USB port.")    
    label.setWordWrap(True)
    brainboximg= QtGui.QLabel()
    brainboximg.setPixmap(QtGui.QPixmap("brainboxwiz.png"))
    brainboximg.show() 
    layout = QtGui.QGridLayout()
    layout.addWidget(label,0,0)
    layout.addWidget(brainboximg,0,1)
    page.setLayout(layout)

    return page


def createRegistrationPage():
    page = QtGui.QWizardPage()
    page.setTitle("Registration")
    page.setSubTitle("Please fill both fields.")
    #f = open('userdata','rw+')
   
    nameLabel = QtGui.QLabel("Name:")
    nameLineEdit = QtGui.QLineEdit()
    
    emailLabel = QtGui.QLabel("Email address:")
    emailLineEdit = QtGui.QLineEdit()

    userLabel = QtGui.QLabel("Username:")
    userLineEdit = QtGui.QLineEdit()
    
    passLabel = QtGui.QLabel("Password:")
    passLineEdit = QtGui.QLineEdit()

    deviceidLabel = QtGui.QLabel("Device ID:")
    deviceidLineEdit = QtGui.QLineEdit()
    
    
    layout = QtGui.QGridLayout()
    layout.addWidget(nameLabel, 0, 0)
    layout.addWidget(nameLineEdit, 0, 1)
    layout.addWidget(emailLabel, 1, 0)
    layout.addWidget(emailLineEdit, 1, 1)
    layout.addWidget(userLabel, 2, 0)
    layout.addWidget(userLineEdit, 2, 1)
    layout.addWidget(passLabel, 3, 0)
    layout.addWidget(passLineEdit, 3, 1)
    layout.addWidget(deviceidLabel, 4, 0)
    layout.addWidget(deviceidLineEdit, 4, 1)
    page.setLayout(layout)

    return page


def createConclusionPage():
    page = QtGui.QWizardPage()
    page.setTitle("Conclusion")
    
    label = QtGui.QLabel("You are now successfully registered. Have a nice day!")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page

def writetouser(fieldin):
    print fieldin
##    f = open('USERDATA','a')
##    f.write(fieldin)
##    f.close()
    
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    wizard = QtGui.QWizard()
    wizard.addPage(createIntroPage())
    wizard.addPage(createRegistrationPage())
    wizard.addPage(createConclusionPage())

    wizard.setWindowTitle("BrainBox Wizard")
    wizard.show()

    sys.exit(wizard.exec_())
