from selenium import webdriver
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
import time
import subprocess
from win32process import CREATE_NO_WINDOW
import re
#from subprocess import open
from random import randrange
import uuid
import sys
import os
import pickle
import zipfile
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QAction, QMenu, QStyle, qApp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ctypes


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Proxie():
    def __init__(self, name, list):
        self.name = name
        self.list = list

class Profile():
    def __init__(self, name, nameOnCard, cardNumber, cardExpiration, cardCVV, email, phoneNumber,
                shippingFirstName, shippingLastName, shippingAddress1, shippingAddress2, shippingCountry, shippingCity, shippingPostal, shippingState,
                billingFirstName, billingLastName, billingAddress1, billingAddress2, billingCountry, billingCity, billingPostal, billingState):
        self.name = name
        self.nameOnCard = nameOnCard
        self.cardNumber = cardNumber
        self.cardExpiration = cardExpiration
        self.cardCVV = cardCVV
        self.email = email
        self.phoneNumber = phoneNumber
        self.shippingFirstName = shippingFirstName
        self.shippingLastName = shippingLastName
        self.shippingAddress1 = shippingAddress1
        self.shippingAddress2 = shippingAddress2
        self.shippingCountry = shippingCountry
        self.shippingCity = shippingCity
        self.shippingPostal = shippingPostal
        self.shippingState =  shippingState
        self.billingFirstName = billingFirstName
        self.billingLastName = billingLastName
        self.billingAddress1 = billingAddress1
        self.billingAddress2 = billingAddress2
        self.billingCountry = billingCountry
        self.billingCity = billingCity
        self.billingPostal = billingPostal
        self.billingState =  billingState

class Task():
    def __init__(self, name, site, mode, profile, account, proxie, productLink, quantity, directoryName, statusLabel):
        self.name = name
        self.site = site
        self.mode = mode
        self.profile = profile
        self.account = account
        self.proxie = proxie
        self.productLink = productLink
        self.quantity = quantity
        self.directoryName = directoryName
        self.statusLabel = statusLabel


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

defaultList = Proxie("Default List"," ")
serviceProxyList = []
serviceProxyList.append(defaultList)

defaultProfile = Profile("Default Profile", "John Doe", "4119288803779911", "12/26", "591", "JohnDoe@gmail.com", "8003336688",
                "John", "Doe", "1234 Peoples Drive", "APT# 1", "United States", "Compton","91234", "California",
                "John", "Doe", "1234 Peoples Drive", "APT# 1", "United States", "Compton","91234", "California")
serviceProfileList = []
serviceProfileList.append(defaultProfile)

site1 = "B&H Photo"
site2 = "Walmart"
site3 = "Gamenerdz"
site4 = "Asus"
serviceSiteList = []
serviceSiteList.append(site1)
serviceSiteList.append(site2)
serviceSiteList.append(site3)
serviceSiteList.append(site4)

mode1 ="Monitor"
mode2 ="Monitor & Buy"

serviceGamenerdzModes =[]
serviceWalmartModes =[]
serviceBHPhotoModes =[]
serviceAsusModes =[]
serviceAsusModes.append(mode1)
serviceAsusModes.append(mode2)
serviceAsusModes.append("Expiremental")
serviceWalmartModes.append(mode1)
serviceWalmartModes.append(mode2)
serviceBHPhotoModes.append(mode1)
serviceBHPhotoModes.append(mode2)
serviceGamenerdzModes.append(mode1)
serviceGamenerdzModes.append(mode2)

serviceAccountsWalmart = ""
serviceAccountsBHPhoto = ""
serviceAccountsGamenerdz = ""
serviceAccountsAsus = ""

serviceTaskList = []

defaultTask = Task("Default Task", site1, "Monitor", "Default Profile", "johndoe@gmail.com", "ISP", "bandH.com/3070ti", 1, "none", "none")
#serviceTaskList.append(defaultTask)

serviceHighlightedTask = defaultTask
serviceHighlightedProfile = defaultProfile

def interceptor(request):
    # Block PNG, JPEG and GIF images
    if request.path.endswith(('.png', '.jpg', '.gif', '.woff', '.php', '.woff2?v=4.4.0')):
        request.abort()

class updaterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        time.sleep(3)
        foreverLoop = True
        while foreverLoop:
            #print ("Thread Messages every 1.5 seconds")
            time.sleep(1.5)
            for task in serviceTaskList:
                if task.directoryName != 'none':
                    statusDataName= "status.txt"
                    statusPath = os.path.join(task.directoryName, statusDataName)
                    statusFile = open(statusPath)
                    statusInfo = statusFile.readline()
                    task.statusLabel.setText(statusInfo)

class AsusMonitorThread(threading.Thread):
    productNotInStock = True
    webhookImage = "blank"
    webhookTitle = "blank"
    webhookLink = "https://discord.com/api/webhooks/803304991028281370/2oznki3M59Cb22A6GCE3hO1aBBCesysCnAR6Uh5SJwTazPO-O_gD7C3rDTlNOXxqT3ET"
    def __init__(self, productLink, proxyLink, proxyUser, proxyPass, statusPath, commandsPath):
        threading.Thread.__init__(self)
        self.productLink = productLink
        self.proxyLink = proxyLink
        self.proxyUser = proxyUser
        self.proxyPass = proxyPass
        self.statusPath = statusPath
        self.commandsPath = commandsPath

    def checkCommands(self):
            print("Checking Command..")
            commandsFile = open(self.commandsPath)
            command = commandsFile.readline()
            stopTask = False
            print("Command: " + command)
            if command == "STOP":
                stopTask = True
                statusFile = open(self.statusPath, 'w')
                statusFile.truncate()
                statusFile.write("Stopped")
                statusFile.close()
            while stopTask == True:
                commandsFile = open(self.commandsPath)
                command = commandsFile.readline()
                if command != "STOP":
                    stopTask = False
                    break
                time.sleep(1)


    def checkStock(self, driver):
        wait = WebDriverWait(driver, 10)

        driver.get(self.productLink)
        time.sleep(4)
        driver.get_screenshot_as_file("screenshots/productPage.png")
        #
        try:
            arrivalNotice = wait.until(EC.element_to_be_clickable((By.ID, "item_notify")))
            statusFile = open(self.statusPath, 'w')
            statusFile.truncate()
            statusFile.write("Monitoring....")
            statusFile.close()


        except:
            self.productNotInStock = False


    def run(self):
        #phantom_service = PhantomJSDriverService.

        driver = webdriver.PhantomJS(executable_path=resource_path("./driver/phantomjs.exe"),
                                    service_args=['--ignore-ssl-errors=true',
                                        '--ssl-protocol=any',
                                        '--proxy=' + self.proxyLink,
                                        '--proxy-type=http',
                                        '--proxy-auth={}:{}'.format(self.proxyUser, self.proxyPass)])

        wait = WebDriverWait(driver, 15)
        notAsleep = True
        while notAsleep:
            AsusMonitorThread.checkStock(self, driver)
            #self.checkStock(driver)
            if self.productNotInStock == False:
                print("Product Back in Stock!")
                statusFile = open(self.statusPath, 'w')
                statusFile.truncate()
                statusFile.write("Product Back in Stock!")
                statusFile.close()
                #Grab Title
                time.sleep(1.5)
                wait.until(EC.presence_of_element_located((By.ID, "pro_title")))
                productTitle = driver.find_element_by_id("pro_title")
                titleText = productTitle.text
                webhookTitle = titleText
                #Grab Image
                productImage = driver.find_element_by_id("item_photo")
                imageSrc = productImage.get_attribute("src")
                webhookImage = imageSrc
                webhook = DiscordWebhook(url=self.webhookLink)
                embed = DiscordEmbed(title=webhookTitle, description='Product Back in Stock!', color=366909)
                embed.set_thumbnail(url = webhookImage)
                embed.add_embed_field(name="Product Link", value="{}".format(self.productLink))
                webhook.add_embed(embed)
                response = webhook.execute()
                time.sleep(15)
                self.productNotInStock = True
            self.checkCommands()
            time.sleep(2)
            statusFile = open(self.statusPath, 'w')
            statusFile.truncate()
            statusFile.write("Monitoring...")
            statusFile.close()
            self.checkCommands()
            time.sleep(2)
            statusFile = open(self.statusPath, 'w')
            statusFile.truncate()
            statusFile.write("Monitoring..")
            statusFile.close()
            self.checkCommands()
            time.sleep(2)
            statusFile = open(self.statusPath, 'w')
            statusFile.truncate()
            statusFile.write("Monitoring.")
            statusFile.close()
            self.checkCommands()
            time.sleep(2)
            statusFile = open(self.statusPath, 'w')
            statusFile.truncate()
            statusFile.write("Monitoring..")
            statusFile.close()



def threadGetTaskInfo():
   windowActive = True
   while windowActive:
       print("Getting Task Data Every 1.5 seconds")
       time.sleep(1.5)
       if windowActive == False:
           break

def monitorOne(value):
    print("Launching Monitor One")
    print(value)
    subprocess.Popen(['python', 'MonitorCommanded.py', value])
    return

def monitorTwo(value):
    print("Launching Monitor Two")
    print(value)
    subprocess.Popen(['python', 'MonitorCommanded.py', value])
    return

def monitorThree(value):
    print("Launching Monitor Three")
    print(value)
    subprocess.Popen(['python', 'MonitorCommanded.py', value])
    return

def monitorFour(value):
    print("Launching Monitor Four")
    print(value)
    subprocess.Popen(['python', 'MonitorCommanded.py', value])
    return

def monitorFive(value):
    print("Launching Monitor Five")
    print(value)
    subprocess.Popen(['python', 'MonitorCommanded.py', value])
    return

def window():

    print("in window")
    app = QApplication(sys.argv)
    win = QMainWindow()
    #win.setGeometry(xpos, ypos, width, height)
    win.setGeometry(200, 160, 1400, 800)
    win.setWindowTitle("7EVEN")

    #makes it so windows recognizes as app
    myappid = '7even.Alpha' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    #Sets Window image and taskbar image
    win.setWindowIcon(QIcon("icons/logo.png"))


    #Launch window
    win.show()

    print("window started")

    #Make background widget
    backgroundWidget = Color('grey')
    backgroundWidget.resize(1400,800)
    win.layout().addWidget(backgroundWidget)

    headerWidget = Color('black')
    headerWidget.resize(1400,75)
    win.layout().addWidget(headerWidget)

    footerWidget = Color('black')
    footerWidget.move(0,725)
    footerWidget.resize(1400,75)
    win.layout().addWidget(footerWidget)


    colorBackground = QLabel()
    colorBackground.move(0,40)
    #colorBackground.resize(400,400)
    pixelMap2 = QPixmap("icons/color-1.png")
    colorBackground.setPixmap(pixelMap2)
    colorBackground.resize(pixelMap2.width(), pixelMap2.height())
    colorBackground.setStyleSheet("background-color: darkgrey;border: 2px solid purple;color: purple")
    win.layout().addWidget(colorBackground)

    imageTest = QLabel()
    imageTest.move(100,100)
    #imageTest.resize(400,400)
    pixelMap = QPixmap("icons/background.png")
    imageTest.setPixmap(pixelMap)
    imageTest.resize(pixelMap.width(), pixelMap.height())
    imageTest.setStyleSheet("background-color: darkgrey;border: 2px solid purple;color: purple")
    win.layout().addWidget(imageTest)

    titleImage = QLabel()
    titleImage.move(565,10)
    #colorBackground.resize(400,400)
    pixelMap3 = QPixmap("icons/title2.png")
    titleImage.setPixmap(pixelMap3)
    titleImage.resize(pixelMap3.width(), pixelMap3.height())
    titleImage.setStyleSheet("background-color: darkgrey;border: 2px solid purple;color: purple")
    win.layout().addWidget(titleImage)
    #create buttons
    proxieButton = QPushButton()
    proxieButton.clicked.connect(lambda: showProxiePage(proxyFrame, taskFrame, profileFrame, settingsFrame))
    proxieButton.move(350,740)
    proxieButton.resize(100,40)
    proxieButton.setText("Proxies")
    proxieButton.setFont(QFont('Corsiva', 18))
    proxieButton.setStyleSheet("background-color: darkgrey;border: 2px solid black")
    win.layout().addWidget(proxieButton)

    tasksButton = QPushButton()
    tasksButton.clicked.connect(lambda: showTaskPage(proxyFrame, taskFrame, profileFrame, settingsFrame))
    tasksButton.move(550,740)
    tasksButton.resize(100,40)
    tasksButton.setText("Tasks")
    tasksButton.setFont(QFont('Corsiva', 18))
    tasksButton.setStyleSheet("background-color: darkgrey;border: 2px solid black")
    win.layout().addWidget(tasksButton)

    profilesButton = QPushButton()
    profilesButton.clicked.connect(lambda: showProfilePage(proxyFrame, taskFrame, profileFrame, settingsFrame))
    profilesButton.move(750,740)
    profilesButton.resize(100,40)
    profilesButton.setText("Profiles")
    profilesButton.setFont(QFont('Corsiva', 18))
    profilesButton.setStyleSheet("background-color: darkgrey;border: 2px solid black")
    win.layout().addWidget(profilesButton)

    settingssButton = QPushButton()
    settingssButton.clicked.connect(lambda: showSettingsPage(proxyFrame, taskFrame, profileFrame, settingsFrame))
    settingssButton.move(950,740)
    settingssButton.resize(100,40)
    settingssButton.setText("Settings")
    settingssButton.setFont(QFont('Corsiva', 18))
    settingssButton.setStyleSheet("background-color: darkgrey;border: 2px solid black")
    win.layout().addWidget(settingssButton)

    #
    #Creating Frames for different Pages and setting them up
    #
    proxyFrame =  QtWidgets.QFrame()
    proxyFrame.move(15,85)
    proxyFrame.resize(1360,625)
    proxyLayout = QtWidgets.QGridLayout()
    proxyLayout.columnStretch(10)
    proxyFrame.setLayout(proxyLayout)
    proxyFrame.setStyleSheet("background-color: lightblack;border: 2px solid green")
    setUpProxyPage(proxyLayout)

    settingsFrame =  QtWidgets.QFrame()
    settingsFrame.move(15,85)
    settingsFrame.resize(1360,625)
    settingsLayout = QtWidgets.QGridLayout()
    #settingsLayout.columnStretch(10)
    settingsFrame.setLayout(settingsLayout)
    settingsFrame.setStyleSheet("background-color: lightblack;border: 2px solid green")
    setUpSettingsPage(settingsLayout)

    taskFrame =  QtWidgets.QFrame()
    taskFrame.move(15,85)
    taskFrame.resize(1360,625)
    taskLayout = QtWidgets.QGridLayout()
    taskLayout.columnStretch(10)
    taskFrame.setLayout(taskLayout)
    taskFrame.setStyleSheet("background-color: lightblack;border: 2px solid green")
    setUpTaskPage(taskLayout)

    profileFrame =  QtWidgets.QFrame()
    profileFrame.move(15,85)
    profileFrame.resize(1360,625)
    profileLayout = QtWidgets.QGridLayout()
    #profileFrame.columnStretch(10)
    profileFrame.setLayout(profileLayout)
    profileFrame.setStyleSheet("background-color: lightblack;border: 2px solid green")
    setUpProfilePage(profileLayout)




    win.layout().addWidget(proxyFrame)
    win.layout().addWidget(taskFrame)
    win.layout().addWidget(profileFrame)
    win.layout().addWidget(settingsFrame)

    proxyFrame.hide()
    taskFrame.hide()
    profileFrame.hide()
    settingsFrame.hide()
    # proxyFrame.setFrameShape(QFrame.StyledPanel)
    # proxyFrame.setLineWidth(0.6)


    #win.layout().addFrame(proxyFrame)

    sys.exit(app.exec_())
    print("ending window")

def showProxiePage(proxiePage, taskPage, profilePage, settingsPage):
    print("showing proxie page")
    taskPage.hide()
    profilePage.hide()
    settingsPage.hide()
    proxiePage.show()

def showTaskPage(proxiePage, taskPage, profilePage, settingsPage):
    print("showing Task page")
    profilePage.hide()
    settingsPage.hide()
    proxiePage.hide()
    taskPage.show()

def showProfilePage(proxiePage, taskPage, profilePage, settingsPage):
    print("showing Profile page")
    taskPage.hide()
    settingsPage.hide()
    proxiePage.hide()
    profilePage.show()

def showSettingsPage(proxiePage, taskPage, profilePage, settingsPage):
    print("showing Settings page")
    taskPage.hide()
    profilePage.hide()
    proxiePage.hide()
    settingsPage.show()

def setUpProxyPage(layout):
    print("Setting Up proxy Page")
    global serviceProxyList
    #
    #Creating Proxy page
    #
    proxyTitle = QLabel()
    proxyTitle.move(0, 4)
    proxyTitle.setText("Proxie List:")
    proxyTitle.resize(100,50)
    proxyTitle.setStyleSheet("color: white;border: 2px solid black")
    proxyTitle.setFont(QFont('Corsiva', 22))
    #proxyFrame.addWidget(proxyTitle)
    layout.addWidget(proxyTitle, 0, 1, 1, 1)

    proxyName = QLineEdit()
    proxyName.setText("Default List")
    proxyName.resize(100,50)
    proxyName.setStyleSheet("color: black;border: 2px solid purple;background-color: lightgrey")
    proxyName.setFont(QFont('Corsiva', 22))
    #proxyFrame.addWidget(proxyTitle)
    layout.addWidget(proxyName, 0, 3, 1, 1)

    saveProxiesButton = QPushButton()
    saveProxiesButton.resize(100,40)
    saveProxiesButton.clicked.connect(lambda: saveProxieList(proxyName.text(), proxyListTextEditor.toPlainText(), selectListComboBox ) )
    saveProxiesButton.setText("Save Proxies")
    saveProxiesButton.setFont(QFont('Corsiva', 18))
    saveProxiesButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(saveProxiesButton, 18, 1, 1, 1)

    clearListButton = QPushButton()
    clearListButton.resize(100,40)
    clearListButton.clicked.connect(lambda: clearProxieList(proxyListTextEditor))
    clearListButton.setText("Clear List")
    clearListButton.setFont(QFont('Corsiva', 18))
    clearListButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(clearListButton, 18, 2, 1, 1)

    proxyListTextEditor = QPlainTextEdit()
    proxyListTextEditor.setStyleSheet("color: black;border: 3px solid darkgreen;background-color: darkgrey")
    proxyListTextEditor.resize(300,400)
    layout.addWidget(proxyListTextEditor, 1, 1, 15, 6)

    selectListComboBox = QComboBox()
    #selectListComboBox.addItem(" ")
    selectListComboBox.currentTextChanged.connect(lambda: updateProxiePage(proxyName, proxyListTextEditor, (selectListComboBoxUpdate(selectListComboBox.currentText() ) )  ) )
    # selectListComboBox.addItem("Oculus DC")
    # selectListComboBox.addItem("LEAF Footlocker")
    # selectListComboBox.addItem("Cookie DC")
    selectListComboBox.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(selectListComboBox, 1, 11, 1, 5)

    selectListComboBoxLabel = QLabel("Select List")
    selectListComboBoxLabel.setStyleSheet("color: white;border: 2px solid black")
    selectListComboBoxLabel.setFont(QFont('Corsiva', 14))
    layout.addWidget(selectListComboBoxLabel, 0, 13, 1, 1)

    # loadList = QPushButton()
    # loadList.resize(100,40)
    # loadList.setText("Load List")
    # loadList.setFont(QFont('Corsiva', 18))
    # loadList.setStyleSheet("color: white;border: 2px solid darkgrey;background-color: grey")
    # layout.addWidget(loadList, 3, 13, 1, 1)

    deleteListButton = QPushButton()
    deleteListButton.resize(100,40)
    deleteListButton.clicked.connect(lambda: deleteProxieList(proxyName.text(),selectListComboBox)  )
    deleteListButton.setText("Delete List")
    deleteListButton.setFont(QFont('Corsiva', 18))
    deleteListButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey;border-radius: 50")
    layout.addWidget(deleteListButton, 5, 13, 1, 1)

    newListButton = QPushButton()
    newListButton.resize(100,40)
    newListButton.clicked.connect(lambda: newProxieList(proxyName.text(), proxyListTextEditor.toPlainText(), selectListComboBox)  )
    newListButton.setText("Create New List")
    newListButton.setFont(QFont('Corsiva', 18))
    newListButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey;border-radius: 50")
    layout.addWidget(newListButton, 7, 13, 1, 1)


    #Create blank widgets to make grid layout
    topLeftCorner = QLabel()
    topLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(topLeftCorner, 0, 0, 20, 1)
    bottomLeftCorner = QLabel()
    bottomLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(bottomLeftCorner, 20, 0, 1, 20)


    loadProxieData()


    for obj in serviceProxyList:
        selectListComboBox.addItem(obj.name)

    if len(serviceProxyList) == 0:
        blankProxie = Proxie("Default List", " ")
        serviceProxyList.append(blankProxie)

    #saveProxieList("test3", "Listasdadsasdasf")


def setUpTaskPage(layout):
    print("Setting Up Task Page")

    taskTitle = QLabel()
    taskTitle.setText("Tasks")
    taskTitle.resize(100,50)
    taskTitle.setFont(QFont('Corsiva', 22))
    taskTitle.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(taskTitle, 0, 9, 1, 1)

    newTaskButton = QPushButton()
    newTaskButton.resize(100,40)
    #newTaskButton.clicked.connect(lambda: newTask(scrollLayout))
    newTaskButton.clicked.connect(lambda: createNewTask(taskCreatorFrame, profileListComboBox, proxieListComboBox, siteListComboBox, accountListComboBox,
                                    taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                                    saveNewTaskButton, createNewTaskButton) )
    newTaskButton.setText("New Task")
    newTaskButton.setFont(QFont('Corsiva', 18))
    newTaskButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(newTaskButton, 19, 4, 1, 2)

    editAllButton = QPushButton()
    editAllButton.resize(100,40)
    editAllButton.setText("Edit All")
    editAllButton.setFont(QFont('Corsiva', 18))
    editAllButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(editAllButton, 19, 9, 1, 2)

    clearAllButton = QPushButton()
    clearAllButton.clicked.connect(lambda: clearAllTasks(scrollLayout) )
    clearAllButton.setText("Clear All")
    clearAllButton.setFont(QFont('Corsiva', 18))
    clearAllButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(clearAllButton, 19, 14, 1, 2)

    #Set Titles for Task layout
    taskName = QLabel()
    taskName.setText("Task Name")
    taskName.resize(100,50)
    taskName.setFont(QFont('Corsiva', 18))
    taskName.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(taskName, 1, 2, 1, 1)

    taskProxie = QLabel()
    taskProxie.setText("Proxie")
    taskProxie.resize(100,50)
    taskProxie.setFont(QFont('Corsiva', 18))
    taskProxie.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(taskProxie, 1, 4, 1, 1)

    taskProfileLabel = QLabel()
    taskProfileLabel.setText("Profile")
    taskProfileLabel.resize(100,50)
    taskProfileLabel.setFont(QFont('Corsiva', 18))
    taskProfileLabel.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(taskProfileLabel, 1, 8, 1, 1)

    taskStatusLabel = QLabel()
    taskStatusLabel.setText("Status")
    taskStatusLabel.resize(100,50)
    taskStatusLabel.setFont(QFont('Corsiva', 18))
    taskStatusLabel.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(taskStatusLabel, 1, 11, 1, 1)

    #add scrollable task page
    taskScrollable = QScrollArea()
    taskScrollable.setStyleSheet("color: white;border: 2px solid green;background-color: lightpurple")
    layout.addWidget(taskScrollable, 2, 1, 14, 18)
    taskScrollable.setWidgetResizable(True)
    scrollContent = QWidget(taskScrollable)
    scrollLayout = QVBoxLayout(scrollContent)
    scrollContent.setLayout(scrollLayout)

    taskScrollable.setWidget(scrollContent)
    taskScrollable.setStyleSheet("border: 2px solid purple")

    topLeftCorner = QLabel()
    topLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(topLeftCorner, 0, 0, 20, 1)
    # topRightCorner = QLabel()
    # layout.addWidget(topRightCorner, 0, 20, 20, 1)
    bottomLeftCorner = QLabel()
    bottomLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(bottomLeftCorner, 20, 0, 1, 20)
    # bottomRightCorner = QLabel()
    # layout.addWidget(bottomRightCorner, 22, 20, 1, 20)


    #Create Frame for task Creation
    taskCreatorFrame =  QtWidgets.QFrame()
    taskCreatorFrame.resize(1000,1200)
    taskCreatorLayout = QtWidgets.QGridLayout()
    taskCreatorFrame.setLayout(taskCreatorLayout)
    taskCreatorFrame.setStyleSheet("background-color: grey;border: 0px solid white")
    layout.addWidget(taskCreatorFrame, 1, 1, 20, 18)
    taskCreatorFrame.hide()

    siteLabel = QLabel()
    siteLabel.setText("Site")
    siteLabel.resize(100,50)
    siteLabel.setFont(QFont('Corsiva', 22))
    siteLabel.setStyleSheet("color: black;border: 2px solid black")
    taskCreatorLayout.addWidget(siteLabel, 1, 1, 1, 3)

    siteListComboBox = QComboBox()
    for sites in serviceSiteList:
        siteListComboBox.addItem(sites)
    siteListComboBox.currentTextChanged.connect(lambda: updateTaskAccountModeSelection(siteListComboBox.currentText(), accountListComboBox, modeListComboBox ) )
    #siteListComboBox.addItem("Game Nerdz")
    siteListComboBox.setFont(QFont('Corsiva', 20))
    siteListComboBox.setStyleSheet("color: black;border: 2px solid black;background-color: lightgrey")
    taskCreatorLayout.addWidget(siteListComboBox, 1, 5, 1, 5)

    modeLabel = QLabel()
    modeLabel.setText("Mode")
    modeLabel.resize(100,50)
    modeLabel.setFont(QFont('Corsiva', 22))
    modeLabel.setStyleSheet("color: black;border: 2px solid black")
    taskCreatorLayout.addWidget(modeLabel, 2, 1, 1, 3)

    modeListComboBox = QComboBox()
    for modes in serviceBHPhotoModes:
        modeListComboBox.addItem(modes)
    #modeListComboBox.addItem("Test Mode")
    # modeListComboBox.currentTextChanged.connect(lambda: updateTaskModeSelection(modeListComboBox.currentText(), accountListComboBox ) )
    #modeListComboBox.addItem("Game Nerdz")
    modeListComboBox.setFont(QFont('Corsiva', 20))
    modeListComboBox.setStyleSheet("color: black;border: 2px solid black;background-color: lightgrey")
    taskCreatorLayout.addWidget(modeListComboBox, 2, 5, 1, 5)

    profileLabel = QLabel()
    profileLabel.setText("Profile")
    profileLabel.resize(100,50)
    profileLabel.setFont(QFont('Corsiva', 22))
    profileLabel.setStyleSheet("color: black;border: 2px solid black")
    taskCreatorLayout.addWidget(profileLabel, 3, 1, 1, 3)

    profileListComboBox = QComboBox()
    for profile in serviceProfileList:
        profileListComboBox.addItem(profile.name)
    #profileListComboBox.currentTextChanged.connect(lambda: updateProxiePage(proxyName, proxyListTextEditor, (selectListComboBoxUpdate(selectListComboBox.currentText() ) )  ) )
    #profileListComboBox.addItem("ENO-2")
    profileListComboBox.setFont(QFont('Corsiva', 20))
    profileListComboBox.setStyleSheet("color: black;border: 2px solid black;background-color: lightgrey")
    taskCreatorLayout.addWidget(profileListComboBox, 3, 5, 1, 5)

    accountLabel = QLabel()
    accountLabel.setText("Account")
    accountLabel.resize(100,50)
    accountLabel.setFont(QFont('Corsiva', 22))
    accountLabel.setStyleSheet("color: black;border: 2px solid black")
    taskCreatorLayout.addWidget(accountLabel, 4, 1, 1, 3)

    accountListComboBox = QComboBox()
    for account in serviceAccountsBHPhoto.splitlines():
        accountListComboBox.addItem(account)
    accountListComboBox.setFont(QFont('Corsiva', 20))
    accountListComboBox.setStyleSheet("color: black;border: 2px solid black;background-color: lightgrey")
    taskCreatorLayout.addWidget(accountListComboBox, 4, 5, 1, 5)

    proxieLabel = QLabel()
    proxieLabel.setText("Proxie")
    proxieLabel.resize(100,50)
    proxieLabel.setFont(QFont('Corsiva', 22))
    proxieLabel.setStyleSheet("color: black;border: 2px solid black")
    taskCreatorLayout.addWidget(proxieLabel, 5, 1, 1, 3)

    proxieListComboBox = QComboBox()
    for proxie in serviceProxyList:
        proxieListComboBox.addItem(proxie.name)
    #proxieListComboBox.currentTextChanged.connect(lambda: updateProxiePage(proxyName, proxyListTextEditor, (selectListComboBoxUpdate(selectListComboBox.currentText() ) )  ) )
    #proxieListComboBox.addItem("LEAF-FTL")
    proxieListComboBox.setFont(QFont('Corsiva', 20))
    proxieListComboBox.setStyleSheet("color: black;border: 2px solid black;background-color: lightgrey")
    taskCreatorLayout.addWidget(proxieListComboBox, 5, 5, 1, 5)



    productLinkLabel = QLabel()
    productLinkLabel.setText("Product Link")
    productLinkLabel.setFont(QFont('Corsiva', 20))
    productLinkLabel.setStyleSheet("color: Black;")
    taskCreatorLayout.addWidget(productLinkLabel, 6, 1, 1, 1)

    productLinkLineEdit = QLineEdit()
    productLinkLineEdit.setText("")
    productLinkLineEdit.setFixedWidth(480)
    productLinkLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black")
    productLinkLineEdit.setFont(QFont('Corsiva', 12))
    taskCreatorLayout.addWidget(productLinkLineEdit, 6, 2, 1, 2)

    quantityLabel = QLabel()
    quantityLabel.setText("Quantity")
    quantityLabel.setFont(QFont('Corsiva', 20))
    quantityLabel.setStyleSheet("color: Black;")
    taskCreatorLayout.addWidget(quantityLabel, 7, 1, 1, 1)

    quantityLineEdit = QLineEdit()
    quantityLineEdit.setText("")
    quantityLineEdit.setFixedWidth(20)
    quantityLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black")
    quantityLineEdit.setFont(QFont('Corsiva', 12))
    taskCreatorLayout.addWidget(quantityLineEdit, 7, 2, 1, 1)

    taskNameLabel = QLabel()
    taskNameLabel.setText("Task Name")
    taskNameLabel.setFont(QFont('Corsiva', 20))
    taskNameLabel.setStyleSheet("color: Black;")
    taskCreatorLayout.addWidget(taskNameLabel, 8, 1, 1, 1)

    taskNameLineEdit = QLineEdit()
    taskNameLineEdit.setText("")
    taskNameLineEdit.setFixedWidth(480)
    taskNameLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black")
    taskNameLineEdit.setFont(QFont('Corsiva', 20))
    taskCreatorLayout.addWidget(taskNameLineEdit, 8, 2, 1, 2)

    createNewTaskButton = QPushButton()
    createNewTaskButton.resize(100,40)
    createNewTaskButton.clicked.connect(lambda: verifyTask(taskNameLineEdit.text(), siteListComboBox.currentText(), modeListComboBox.currentText(), profileListComboBox.currentText(),
                                        accountListComboBox.currentText(), proxieListComboBox.currentText(), productLinkLineEdit.text(), quantityLineEdit.text(),
                                        scrollLayout, taskCreatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox,
                                        taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                                        saveNewTaskButton, createNewTaskButton) )
    createNewTaskButton.setText(" Create New Task ")
    createNewTaskButton.setFont(QFont('Corsiva', 22))
    createNewTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: darkgrey")
    taskCreatorLayout.addWidget(createNewTaskButton, 12, 3, 1, 4)

    saveNewTaskButton = QPushButton()
    saveNewTaskButton.resize(100,40)
    saveNewTaskButton.clicked.connect(lambda: saveTaskEdit(taskNameLineEdit.text(), siteListComboBox.currentText(), modeListComboBox.currentText(), profileListComboBox.currentText(),
                                        accountListComboBox.currentText(), proxieListComboBox.currentText(), productLinkLineEdit.text(), quantityLineEdit.text(),
                                        scrollLayout, taskCreatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox,
                                        taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                                        saveNewTaskButton, createNewTaskButton) )
    saveNewTaskButton.setText(" Save Task ")
    saveNewTaskButton.setFont(QFont('Corsiva', 22))
    saveNewTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: darkgrey")
    taskCreatorLayout.addWidget(saveNewTaskButton, 13, 3, 1, 4)
    saveNewTaskButton.hide()

    cancelTaskButton = QPushButton()
    cancelTaskButton.setText("Cancel")
    cancelTaskButton.clicked.connect(lambda: hideCreateNewTask(taskCreatorFrame) )
    cancelTaskButton.setFont(QFont('Corsiva', 22))
    cancelTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: darkgrey")
    taskCreatorLayout.addWidget(cancelTaskButton, 15, 3, 1, 4)

    topLeftCorner = QLabel()
    taskCreatorLayout.addWidget(topLeftCorner, 0, 0, 20, 1)
    bottomLeftCorner = QLabel()
    taskCreatorLayout.addWidget(bottomLeftCorner, 20, 0, 1, 20)

    loadTaskData(scrollLayout, taskCreatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                saveNewTaskButton, createNewTaskButton)

    resetTaskTempData()
    #verifyTask("New custom task", "Gamenerdz", "ENO-1", "jeebus@gmail.com", "BART RESI", "gamenerdz.com/pid/600823", 1, scrollLayout, taskCreatorFrame )


def setUpProfilePage(layout):
    print("Setting Up Profile Page")
    profileTitle = QLabel()
    profileTitle.setText("Profiles")
    profileTitle.resize(100,50)
    profileTitle.setStyleSheet("color: white;border: 2px solid black")
    profileTitle.setFont(QFont('Corsiva', 22))
    layout.addWidget(profileTitle, 0, 8, 1, 1)

    # newProfile = QPushButton()
    # newProfile.resize(100,40)

    # newProfile.setText("New Profile")
    # newProfile.setFont(QFont('Corsiva', 18))
    # newProfile.setStyleSheet("color: white;border: 2px solid darkgrey;background-color: grey")
    # layout.addWidget(newProfile, 19, 4, 1, 2)

    createProfileButton = QPushButton()
    createProfileButton.resize(100,40)
    createProfileButton.clicked.connect(lambda: createNewProfile(profileCreatorLayout, profileCreatorFrame, saveNewProfileButton, saveProfileEditButton,
                                        profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                                        cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                                        shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                                        shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                                        billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                                        billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit) )
    createProfileButton.setText("CreateProfile")
    createProfileButton.setFont(QFont('Corsiva', 18))
    createProfileButton.setStyleSheet("color: white;border: 2px solid purple;background-color: grey")
    layout.addWidget(createProfileButton, 19, 8, 1, 2)

    #Set Titles for Profile Layout
    profileNameTitle = QLabel()
    profileNameTitle.setText("Name")
    profileNameTitle.resize(100,50)
    profileNameTitle.setFont(QFont('Corsiva', 18))
    profileNameTitle.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(profileNameTitle, 2, 3, 1, 1)

    nameOnCardTitle = QLabel()
    nameOnCardTitle.setText("   Name on Card")
    nameOnCardTitle.resize(100,50)
    nameOnCardTitle.setFont(QFont('Corsiva', 18))
    nameOnCardTitle.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(nameOnCardTitle, 2, 6, 1, 1)

    lastFourTitle = QLabel()
    lastFourTitle.setText("   Last 4 on Card")
    lastFourTitle.resize(100,50)
    lastFourTitle.setFont(QFont('Corsiva', 18))
    lastFourTitle.setStyleSheet("color: white;border: 2px solid black")
    layout.addWidget(lastFourTitle, 2, 8, 1, 1)

    #add scrollable profile page
    profileScrollable = QScrollArea()
    layout.addWidget(profileScrollable, 3, 2, 12, 16)
    profileScrollable.setWidgetResizable(True)
    profileScrollable.setStyleSheet("color: black;border: 2px solid purple;background-color: darkgrey")
    scrollContent = QWidget(profileScrollable)
    profileScrollLayout = QVBoxLayout(scrollContent)
    scrollContent.setLayout(profileScrollLayout)

    profileScrollable.setWidget(scrollContent)

    topLeftCorner = QLabel()
    topLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(topLeftCorner, 0, 0, 20, 1)
    # topRightCorner = QLabel()
    # layout.addWidget(topRightCorner, 0, 20, 20, 1)
    bottomLeftCorner = QLabel()
    bottomLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(bottomLeftCorner, 20, 0, 1, 20)

    #Create Frame for profile Creation
    profileCreatorFrame =  QtWidgets.QFrame()
    profileCreatorFrame.resize(1000,1000)
    profileCreatorLayout = QtWidgets.QGridLayout()
    profileCreatorFrame.setLayout(profileCreatorLayout)
    profileCreatorFrame.setStyleSheet("background-color: grey;border: 0px solid white")
    layout.addWidget(profileCreatorFrame, 2, 2, 18, 16)
    profileCreatorFrame.hide()

    cancelCreationButton = QPushButton()
    cancelCreationButton.resize(100,40)
    cancelCreationButton.clicked.connect(lambda: closeProfileCreator(profileCreatorFrame))
    cancelCreationButton.setText("Cancel")
    cancelCreationButton.setFont(QFont('Corsiva', 18))
    cancelCreationButton.setStyleSheet("color: white;border: 2px solid lightgrey;background-color: grey")
    profileCreatorLayout.addWidget(cancelCreationButton, 19, 2, 1, 2)

    saveNewProfileButton = QPushButton()
    saveNewProfileButton.resize(100,40)
    saveNewProfileButton.clicked.connect(lambda: verifyProfile(profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                                        cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                                        shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                                        shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                                        billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                                        billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                                        saveNewProfileButton, saveProfileEditButton) )
    saveNewProfileButton.setText(" Save Profile ")
    saveNewProfileButton.setFont(QFont('Corsiva', 18))
    saveNewProfileButton.setStyleSheet("color: white;border: 2px solid lightgrey;background-color: grey")
    profileCreatorLayout.addWidget(saveNewProfileButton, 19, 8, 1, 2)

    saveProfileEditButton = QPushButton()
    saveProfileEditButton.resize(100,40)
    saveProfileEditButton.clicked.connect(lambda: saveProfileEdit(profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                                        cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                                        shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                                        shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                                        billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                                        billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                                        saveNewProfileButton, saveProfileEditButton ) )
    saveProfileEditButton.setText(" Update Profile ")
    saveProfileEditButton.setFont(QFont('Corsiva', 18))
    saveProfileEditButton.setStyleSheet("color: white;border: 2px solid lightgrey;background-color: grey")
    profileCreatorLayout.addWidget(saveProfileEditButton, 19, 8, 1, 2)
    saveProfileEditButton.hide()

    #Create labels and buttons for Shipping Info
    #
    shippingInfoLabel = QLabel()
    shippingInfoLabel.setText("Shipping Info")
    shippingInfoLabel.resize(100,50)
    shippingInfoLabel.setFont(QFont('Corsiva', 18))
    shippingInfoLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingInfoLabel, 0, 6, 1, 1)

    shippingFirstNameLabel = QLabel()
    shippingFirstNameLabel.setText("First Name")
    shippingFirstNameLabel.setFont(QFont('Corsiva', 16))
    shippingFirstNameLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingFirstNameLabel, 1, 5, 1, 1)

    shippingFirstNameLineEdit = QLineEdit()
    shippingFirstNameLineEdit.setText(" ")
    shippingFirstNameLineEdit.setFixedWidth(160)
    shippingFirstNameLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingFirstNameLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingFirstNameLineEdit, 1, 6, 1, 1)

    shippingLastNameLabel = QLabel()
    shippingLastNameLabel.setText("Last Name")
    shippingLastNameLabel.setFont(QFont('Corsiva', 16))
    shippingLastNameLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingLastNameLabel, 2, 5, 1, 1)

    shippingLastNameLineEdit = QLineEdit()
    shippingLastNameLineEdit.setText(" ")
    shippingLastNameLineEdit.setFixedWidth(160)
    shippingLastNameLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingLastNameLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingLastNameLineEdit, 2, 6, 1, 1)

    shippingAddress1Label = QLabel()
    shippingAddress1Label.setText("Address 1")
    shippingAddress1Label.setFont(QFont('Corsiva', 16))
    shippingAddress1Label.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingAddress1Label, 3, 5, 1, 1)

    shippingAddress1LineEdit = QLineEdit()
    shippingAddress1LineEdit.setText(" ")
    shippingAddress1LineEdit.setFixedWidth(160)
    shippingAddress1LineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingAddress1LineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingAddress1LineEdit, 3, 6, 1, 1)

    shippingAddress2Label = QLabel()
    shippingAddress2Label.setText("Address 2")
    shippingAddress2Label.setFont(QFont('Corsiva', 16))
    shippingAddress2Label.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingAddress2Label, 4, 5, 1, 1)

    shippingAddress2LineEdit = QLineEdit()
    shippingAddress2LineEdit.setText(" ")
    shippingAddress2LineEdit.setFixedWidth(160)
    shippingAddress2LineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingAddress2LineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingAddress2LineEdit, 4, 6, 1, 1)

    shippingCountryLabel = QLabel()
    shippingCountryLabel.setText("Country")
    shippingCountryLabel.setFont(QFont('Corsiva', 16))
    shippingCountryLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingCountryLabel, 5, 5, 1, 1)

    shippingCountryLineEdit = QLineEdit()
    shippingCountryLineEdit.setText(" ")
    shippingCountryLineEdit.setFixedWidth(160)
    shippingCountryLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingCountryLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingCountryLineEdit, 5, 6, 1, 1)

    shippingCityLabel = QLabel()
    shippingCityLabel.setText("City")
    shippingCityLabel.setFont(QFont('Corsiva', 16))
    shippingCityLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingCityLabel, 6, 5, 1, 1)

    shippingCityLineEdit = QLineEdit()
    shippingCityLineEdit.setText(" ")
    shippingCityLineEdit.setFixedWidth(160)
    shippingCityLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingCityLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingCityLineEdit, 6, 6, 1, 1)

    shippingPostalLabel = QLabel()
    shippingPostalLabel.setText("Postal Code")
    shippingPostalLabel.setFont(QFont('Corsiva', 16))
    shippingPostalLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingPostalLabel, 7, 5, 1, 1)

    shippingPostalLineEdit = QLineEdit()
    shippingPostalLineEdit.setText(" ")
    shippingPostalLineEdit.setFixedWidth(160)
    shippingPostalLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingPostalLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingPostalLineEdit, 7, 6, 1, 1)

    shippingStateLabel = QLabel()
    shippingStateLabel.setText("State")
    shippingStateLabel.setFont(QFont('Corsiva', 16))
    shippingStateLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(shippingStateLabel, 8, 5, 1, 1)

    shippingStateLineEdit = QLineEdit()
    shippingStateLineEdit.setText(" ")
    shippingStateLineEdit.setFixedWidth(160)
    shippingStateLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    shippingStateLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(shippingStateLineEdit, 8, 6, 1, 1)

    #Create labels and buttons for Billing Info
    billingInfoLabel = QLabel()
    billingInfoLabel.setText("Billing Info")
    billingInfoLabel.setFont(QFont('Corsiva', 18))
    billingInfoLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingInfoLabel, 0, 12, 1, 1)

    billingFirstNameLabel = QLabel()
    billingFirstNameLabel.setText("First Name")
    billingFirstNameLabel.setFont(QFont('Corsiva', 16))
    billingFirstNameLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingFirstNameLabel, 1, 11, 1, 1)

    billingFirstNameLineEdit = QLineEdit()
    billingFirstNameLineEdit.setText(" ")
    billingFirstNameLineEdit.setFixedWidth(160)
    billingFirstNameLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingFirstNameLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingFirstNameLineEdit, 1, 12, 1, 1)

    billingLastNameLabel = QLabel()
    billingLastNameLabel.setText("Last Name")
    billingLastNameLabel.setFont(QFont('Corsiva', 16))
    billingLastNameLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingLastNameLabel, 2, 11, 1, 1)

    billingLastNameLineEdit = QLineEdit()
    billingLastNameLineEdit.setText(" ")
    billingLastNameLineEdit.setFixedWidth(160)
    billingLastNameLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingLastNameLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingLastNameLineEdit, 2, 12, 1, 1)

    billingAddress1Label = QLabel()
    billingAddress1Label.setText("Address 1")
    billingAddress1Label.setFont(QFont('Corsiva', 16))
    billingAddress1Label.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingAddress1Label, 3, 11, 1, 1)

    billingAddress1LineEdit = QLineEdit()
    billingAddress1LineEdit.setText(" ")
    billingAddress1LineEdit.setFixedWidth(160)
    billingAddress1LineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingAddress1LineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingAddress1LineEdit, 3, 12, 1, 1)

    billingAddress2Label = QLabel()
    billingAddress2Label.setText("Address 2")
    billingAddress2Label.setFont(QFont('Corsiva', 16))
    billingAddress2Label.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingAddress2Label, 4, 11, 1, 1)

    billingAddress2LineEdit = QLineEdit()
    billingAddress2LineEdit.setText(" ")
    billingAddress2LineEdit.setFixedWidth(160)
    billingAddress2LineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingAddress2LineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingAddress2LineEdit, 4, 12, 1, 1)

    billingCountryLabel = QLabel()
    billingCountryLabel.setText("Country")
    billingCountryLabel.setFont(QFont('Corsiva', 16))
    billingCountryLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingCountryLabel, 5, 11, 1, 1)

    billingCountryLineEdit = QLineEdit()
    billingCountryLineEdit.setText(" ")
    billingCountryLineEdit.setFixedWidth(160)
    billingCountryLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingCountryLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingCountryLineEdit, 5, 12, 1, 1)

    billingCityLabel = QLabel()
    billingCityLabel.setText("City")
    billingCityLabel.setFont(QFont('Corsiva', 16))
    billingCityLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingCityLabel, 6, 11, 1, 1)

    billingCityLineEdit = QLineEdit()
    billingCityLineEdit.setText(" ")
    billingCityLineEdit.setFixedWidth(160)
    billingCityLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingCityLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingCityLineEdit, 6, 12, 1, 1)

    billingPostalLabel = QLabel()
    billingPostalLabel.setText("Postal Code")
    billingPostalLabel.setFont(QFont('Corsiva', 16))
    billingPostalLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingPostalLabel, 7, 11, 1, 1)

    billingPostalLineEdit = QLineEdit()
    billingPostalLineEdit.setText(" ")
    billingPostalLineEdit.setFixedWidth(160)
    billingPostalLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingPostalLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingPostalLineEdit, 7, 12, 1, 1)

    billingStateLabel = QLabel()
    billingStateLabel.setText("State")
    billingStateLabel.setFont(QFont('Corsiva', 16))
    billingStateLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(billingStateLabel, 8, 11, 1, 1)

    billingStateLineEdit = QLineEdit()
    billingStateLineEdit.setText(" ")
    billingStateLineEdit.setFixedWidth(160)
    billingStateLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    billingStateLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(billingStateLineEdit, 8, 12, 1, 1)

    billingSameAsShipping = QCheckBox("Billing Same as shipping?")
    billingSameAsShipping.setChecked(True)
    profileCreatorLayout.addWidget(billingSameAsShipping, 10, 12, 1, 1)
    #Create Labels and buttons for generic profile info
    profileNameLabel = QLabel()
    profileNameLabel.setText("Profile Name")
    profileNameLabel.setFont(QFont('Corsiva', 16))
    profileNameLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(profileNameLabel, 1, 1, 1, 1)

    profileNameLineEdit = QLineEdit()
    profileNameLineEdit.setText("test")
    profileNameLineEdit.setFixedWidth(160)
    profileNameLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    profileNameLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(profileNameLineEdit, 1, 2, 1, 1)

    nameOnCardLabel = QLabel()
    nameOnCardLabel.setText("Name on Card")
    nameOnCardLabel.setFont(QFont('Corsiva', 16))
    nameOnCardLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(nameOnCardLabel, 2, 1, 1, 1)

    nameOnCardLineEdit = QLineEdit()
    nameOnCardLineEdit.setText("test")
    nameOnCardLineEdit.setFixedWidth(160)
    nameOnCardLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    nameOnCardLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(nameOnCardLineEdit, 2, 2, 1, 1)

    cardNumberLabel = QLabel()
    cardNumberLabel.setText("Card Number")
    cardNumberLabel.setFont(QFont('Corsiva', 16))
    cardNumberLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(cardNumberLabel, 3, 1, 1, 1)

    cardNumberLineEdit = QLineEdit()
    cardNumberLineEdit.setText("test")
    cardNumberLineEdit.setFixedWidth(160)
    cardNumberLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    cardNumberLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(cardNumberLineEdit, 3, 2, 1, 1)

    cardExpirationLabel = QLabel()
    cardExpirationLabel.setText("Expiration Date")
    cardExpirationLabel.setFont(QFont('Corsiva', 16))
    cardExpirationLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(cardExpirationLabel, 4, 1, 1, 1)

    cardExpirationLineEdit = QLineEdit()
    cardExpirationLineEdit.setText("")
    cardExpirationLineEdit.setFixedWidth(160)
    cardExpirationLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    cardExpirationLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(cardExpirationLineEdit, 4, 2, 1, 1)

    cardCVVLabel = QLabel()
    cardCVVLabel.setText("CVV")
    cardCVVLabel.setFont(QFont('Corsiva', 16))
    cardCVVLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(cardCVVLabel, 5, 1, 1, 1)

    cardCVVLineEdit = QLineEdit()
    cardCVVLineEdit.setText(" ")
    cardCVVLineEdit.setFixedWidth(100)
    cardCVVLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    cardCVVLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(cardCVVLineEdit, 5, 2, 1, 1)

    emailLabel = QLabel()
    emailLabel.setText("Email")
    emailLabel.setFont(QFont('Corsiva', 16))
    emailLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(emailLabel, 6, 1, 1, 1)

    emailLineEdit = QLineEdit()
    emailLineEdit.setText(" ")
    emailLineEdit.setFixedWidth(160)
    emailLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    emailLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(emailLineEdit, 6, 2, 1, 1)

    phoneLabel = QLabel()
    phoneLabel.setText("Phone Number")
    phoneLabel.setFont(QFont('Corsiva', 16))
    phoneLabel.setStyleSheet("color: white;")
    profileCreatorLayout.addWidget(phoneLabel, 7, 1, 1, 1)

    phoneNumberLineEdit = QLineEdit()
    phoneNumberLineEdit.setText(" ")
    phoneNumberLineEdit.setFixedWidth(160)
    phoneNumberLineEdit.setStyleSheet("color: black;background-color: lightgrey;border: 2px solid black;")
    phoneNumberLineEdit.setFont(QFont('Corsiva', 12))
    profileCreatorLayout.addWidget(phoneNumberLineEdit, 7, 2, 1, 1)

    topLeftCorner = QLabel()
    profileCreatorLayout.addWidget(topLeftCorner, 0, 0, 20, 1)
    bottomLeftCorner = QLabel()
    profileCreatorLayout.addWidget(bottomLeftCorner, 20, 0, 1, 20)

    loadProfileData(profileScrollLayout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                saveNewProfileButton, saveProfileEditButton)

    # saveProfileEdit(profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
    #                                     cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
    #                                     shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
    #                                     shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
    #                                     billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
    #                                     billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
    #                                     saveNewProfileButton, saveProfileEditButton )
    # verifyProfile(profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
    #             cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
    #             shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
    #             shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
    #             billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
    #             billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
    #             saveNewProfileButton, saveProfileEditButton )

def setUpSettingsPage(layout):
    print("Setting Up Settings Page")
    settingsTitle = QLabel()
    settingsTitle.move(0, 4)
    settingsTitle.setText("Settings")
    settingsTitle.resize(100,50)
    settingsTitle.setStyleSheet("color: white;border: 2px solid black")
    settingsTitle.setFont(QFont('Corsiva', 22))
    layout.addWidget(settingsTitle, 0, 4, 1, 1)

    accountsTitle = QLabel()
    accountsTitle.setText("Accounts")
    accountsTitle.setStyleSheet("color: white;border: 2px solid black")
    accountsTitle.setFont(QFont('Corsiva', 22))
    layout.addWidget(accountsTitle, 0, 12, 1, 1)

    siteListComboBox = QComboBox()
    for sites in serviceSiteList:
        siteListComboBox.addItem(sites)
    siteListComboBox.currentTextChanged.connect(lambda: updateAccountsPage(accountListTextEditor, siteListComboBox.currentText()  ) )
    siteListComboBox.setFont(QFont('Corsiva', 20))
    siteListComboBox.setStyleSheet("color: black;border: 2px solid purple;background-color: darkgrey")
    layout.addWidget(siteListComboBox, 2, 12, 1, 4)

    accountListTextEditor = QPlainTextEdit()
    accountListTextEditor.setStyleSheet("color: black;border: 2px solid purple;background-color: darkgrey")
    layout.addWidget(accountListTextEditor, 3, 12, 8, 4)

    saveAccountListButton = QPushButton()
    saveAccountListButton.clicked.connect(lambda: saveAccountList(accountListTextEditor, siteListComboBox.currentText()) )
    saveAccountListButton.setText("Save Account List")
    saveAccountListButton.setFont(QFont('Corsiva', 18))
    saveAccountListButton.setStyleSheet("color: black;border: 2px solid purple;background-color: grey")
    layout.addWidget(saveAccountListButton, 12, 12, 1, 4)

    webhookLabel = QLabel()
    webhookLabel.setText("WebHook")
    webhookLabel.resize(100,50)
    webhookLabel.setStyleSheet("color: white;border: 2px solid black")
    webhookLabel.setFont(QFont('Corsiva', 18))
    layout.addWidget(webhookLabel, 2, 2, 1, 1)

    webhookInput = QLineEdit()
    webhookInput.setStyleSheet("color: black;border: 2px solid purple;background-color: lightgrey")
    layout.addWidget(webhookInput, 2, 3, 1, 4)

    webhookSave = QPushButton()
    webhookSave.resize(100,40)
    webhookSave.clicked.connect(lambda: saveWebhook(webhookInput.text()))
    webhookSave.setText("Save")
    webhookSave.setFont(QFont('Corsiva', 18))
    webhookSave.setStyleSheet("color: black;border: 2px solid purple;background-color: lightgrey")
    layout.addWidget(webhookSave, 2, 7, 1, 1)

    webhookTest = QPushButton()
    webhookTest.resize(100,40)
    webhookTest.clicked.connect(lambda: testWebhook(webhookInput.text()))
    webhookTest.setText("Test")
    webhookTest.setFont(QFont('Corsiva', 18))
    webhookTest.setStyleSheet("color: black;border: 2px solid purple;background-color: lightgrey")
    layout.addWidget(webhookTest, 2, 8, 1, 1)



    licenseKeyLabel = QLabel()
    licenseKeyLabel.setText("License Key")
    licenseKeyLabel.resize(100,50)
    licenseKeyLabel.setStyleSheet("color: white;border: 2px solid black")
    licenseKeyLabel.setFont(QFont('Corsiva', 18))
    layout.addWidget(licenseKeyLabel, 4, 2, 1, 1)

    licenseKey = QLabel()
    licenseKey.setText("12GD-JLMI-9113-KMSS")
    licenseKey.resize(100,50)
    licenseKey.setStyleSheet("color: white;border: 2px solid black")
    licenseKey.setFont(QFont('Corsiva', 18))
    layout.addWidget(licenseKey, 4, 3, 1, 4)

    topLeftCorner = QLabel()
    topLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(topLeftCorner, 0, 0, 20, 1)

    bottomLeftCorner = QLabel()
    bottomLeftCorner.setStyleSheet("border: 2px solid black")
    layout.addWidget(bottomLeftCorner, 20, 0, 1, 20)

    #settingsData = loadSettingsData()
    loadSettingsData(webhookInput)

    accountListTextEditor.clear()
    accountListTextEditor.appendPlainText(serviceAccountsBHPhoto)

    #accountListTextEditor.clear()
    #accountListTextEditor.appendPlainText("email:pass")

    #saveAccountList(accountListTextEditor, siteListComboBox.currentText())
    #accountListTextEditor.setText(serviceAccountsBHPhoto)
    #webhookInput.setText(settingsData)

def createTask(task, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                saveTaskButton, createNewTaskButton):
    print("Creating Task")

    #Test creating grid layout for tasks
    taskLayout = QtWidgets.QGridLayout()

    #taskLayout.setStyleSheet("border: 2px solid purple")
    taskName = QLabel()
    taskName.setFixedWidth(225)
    taskName.setStyleSheet("color: black; border: 2px solid black")
    taskName.setText(task.name)
    taskName.setFont(QFont('Corsiva', 14))
    taskLayout.addWidget(taskName, 0, 0, 1, 1)

    taskProxie = QLabel()
    taskProxie.setFixedWidth(200)
    taskProxie.setStyleSheet("color: black;border: 2px solid black")
    taskProxie.setText(task.proxie)
    taskProxie.setFont(QFont('Corsiva', 18))
    taskLayout.addWidget(taskProxie, 0, 2, 1, 1)

    taskProfile = QLabel()
    taskProfile.setFixedWidth(200)
    taskProfile.setStyleSheet("color: black;border: 2px solid black")
    taskProfile.setText(task.profile)
    taskProfile.setFont(QFont('Corsiva', 18))
    taskLayout.addWidget(taskProfile, 0, 4, 1, 1)

    taskStatusLabel = QLabel()
    taskStatusLabel.setFixedWidth(200)
    taskStatusLabel.setStyleSheet("color: black;border: 2px solid black")
    taskStatusLabel.setText("Not Active")
    taskStatusLabel.setFont(QFont('Corsiva', 14))
    taskLayout.addWidget(taskStatusLabel, 0, 5, 1, 1)
    task.statusLabel = taskStatusLabel

    startTaskButton = QPushButton()
    startTaskButton.setText("Start")
    startTaskButton.clicked.connect(lambda: launchTask(task) )
    startTaskButton.setFixedWidth(75)
    startTaskButton.setFont(QFont('Corsiva', 18))
    startTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: white")
    taskLayout.addWidget(startTaskButton, 0, 6, 1, 1)

    stopTaskButton = QPushButton()
    stopTaskButton.setFixedWidth(75)
    stopTaskButton.clicked.connect(lambda: pauseTask(task) )
    stopTaskButton.setText("Stop")
    stopTaskButton.setFont(QFont('Corsiva', 18))
    stopTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: white")
    taskLayout.addWidget(stopTaskButton, 0, 7, 1, 1)

    editTaskButton = QPushButton()
    editTaskButton.setFixedWidth(75)
    editTaskButton.clicked.connect(lambda: editTask(task, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox,
                                    taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                                    saveTaskButton, createNewTaskButton) )
    editTaskButton.setText("Edit")
    editTaskButton.setFont(QFont('Corsiva', 18))
    editTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: white")
    taskLayout.addWidget(editTaskButton, 0, 8, 1, 1)

    deleteTaskButton = QPushButton()
    deleteTaskButton.setFixedWidth(75)
    deleteTaskButton.clicked.connect(lambda: deleteTask(task, layout, creatorFrame, siteListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox,
                                        taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                                        saveTaskButton, createNewTaskButton) )
    deleteTaskButton.setText("Delete")
    deleteTaskButton.setFont(QFont('Corsiva', 18))
    deleteTaskButton.setStyleSheet("color: black;border: 2px solid black;background-color: white")
    taskLayout.addWidget(deleteTaskButton, 0, 9, 1, 1)



    blankWidget = QWidget()
    blankWidget.setLayout(taskLayout)
    blankWidget.setStyleSheet("background-color: darkgrey; border: 2px solid purple")

    layout.addWidget(blankWidget)

def newProxieList(name,list,comboBox):
    global serviceProxyList
    for obj in serviceProxyList:
        if obj.name == name :
            return
    if name == "":
        return
    myProxie = Proxie(name , list)
    serviceProxyList.append(myProxie)
    print("List Created")
    comboBox.addItem(name)
    pickle_out = open("data/proxieList.txt", "wb")
    pickle.dump(serviceProxyList, pickle_out)
    pickle_out.close()
    return
    #ComboBox.addItem(myProxie.name)
    #reloadProxiePage()

def createProfile(tempProfile, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
            cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
            shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
            shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
            billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
            billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
            saveNewProfileButton, saveProfileEditButton):
    #Test creating grid layout for tasks
    profileLayout = QtWidgets.QGridLayout()

    profileName = QLabel()
    profileName.setText(tempProfile.name)
    profileName.setStyleSheet("color: black")
    profileName.setFont(QFont('Corsiva', 18))
    profileLayout.addWidget(profileName, 0, 0, 1, 2)

    profileCardName = QLabel()
    profileCardName.setText(tempProfile.nameOnCard)
    profileCardName.setStyleSheet("color: black")
    profileCardName.setFont(QFont('Corsiva', 18))
    profileLayout.addWidget(profileCardName, 0, 2, 1, 2)

    profileFour = QLabel()
    profileFour.setText(tempProfile.cardNumber)
    profileFour.setStyleSheet("color: black")
    profileFour.setFont(QFont('Corsiva', 18))
    profileLayout.addWidget(profileFour, 0, 4, 1, 2)

    editProfileButton = QPushButton()
    editProfileButton.clicked.connect(lambda: editProfile(tempProfile, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                saveNewProfileButton, saveProfileEditButton) )
    editProfileButton.setText("Edit")
    editProfileButton.setFont(QFont('Corsiva', 18))
    editProfileButton.setStyleSheet("color: black;border: 2px solid darkgrey;background-color: white")
    profileLayout.addWidget(editProfileButton, 0, 6, 1, 1)

    copyProfile = QPushButton()
    copyProfile.setText("Copy")
    copyProfile.setFont(QFont('Corsiva', 18))
    copyProfile.setStyleSheet("color: black;border: 2px solid darkgrey;background-color: white")
    profileLayout.addWidget(copyProfile, 0, 8, 1, 1)

    deleteProfileButton = QPushButton()
    deleteProfileButton.clicked.connect(lambda: deleteProfile(tempProfile, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                saveNewProfileButton, saveProfileEditButton) )
    deleteProfileButton.setText("Delete")
    deleteProfileButton.setFont(QFont('Corsiva', 18))
    deleteProfileButton.setStyleSheet("color: black;border: 2px solid darkgrey;background-color: white")
    profileLayout.addWidget(deleteProfileButton, 0, 10, 1, 1)


    blankWidget = QWidget()
    blankWidget.setLayout(profileLayout)
    blankWidget.setStyleSheet("background-color: grey;border: 2px solid black")

    layout.addWidget(blankWidget)
    saveProfileData()

    # editProfile(tempProfile, layout, profileName, nameOnCard, cardNumber, cardExpiration, cardCVV, email, phoneNumber,
    #             shippingFirstName, shippingLastName, shippingAddress1, shippingAddress2,
    #             shippingCountry, shippingCity,shippingPostal, shippingState,
    #             billingFirstName, billingLastName, billingAddress1, billingAddress2,
    #             billingCountry, billingCity,billingPostal, billingState, profileScrollLayout, profileCreatorFrame,
    #             saveNewProfileButton, saveProfileEditButton)
    #editProfile(tempProfile, layout, creatorFrame)

def createNewProfile(creatorLayout, creatorFrame, saveNewProfileButton, saveProfileEditButton,
                    profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                    cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                    shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                    shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                    billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                    billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit):
    print("Starting Profile Window")
    creatorFrame.show()
    saveProfileEditButton.hide()
    saveNewProfileButton.show()
    profileNameLineEdit.setText("")
    nameOnCardLineEdit.setText("")
    cardNumberLineEdit.setText("")
    cardExpirationLineEdit.setText("")
    cardCVVLineEdit.setText("")
    emailLineEdit.setText("")
    phoneNumberLineEdit.setText("")
    shippingFirstNameLineEdit.setText("")
    shippingLastNameLineEdit.setText("")
    shippingAddress1LineEdit.setText("")
    shippingAddress2LineEdit.setText("")
    shippingCountryLineEdit.setText("")
    shippingCityLineEdit.setText("")
    shippingPostalLineEdit.setText("")
    shippingStateLineEdit.setText("")

def createNewTask(creatorFrame, profileComboBox, proxieComboBox, siteComboBox, accountComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                    saveNewTaskButton, createNewTaskButton):
    print("Starting Task Creator Window")
    creatorFrame.show()
    saveNewTaskButton.hide()
    createNewTaskButton.show()
    profileComboBox.clear()
    for profile in serviceProfileList:
        profileComboBox.addItem(profile.name)
    profileComboBox.setCurrentIndex(0)
    proxieComboBox.clear()
    for proxy in serviceProxyList:
        proxieComboBox.addItem(proxy.name)
    proxieComboBox.setCurrentIndex(0)
    siteComboBox.setCurrentIndex(0)
    accountComboBox.setCurrentIndex(0)
    taskNameLineEdit.setText("")
    productLinkLineEdit.setText("")
    quantityLineEdit.setText("")

def hideCreateNewTask(creatorFrame):
    print("Hiding task Creator Window")
    creatorFrame.hide()

def saveWebhook(string):
    print("Webhook: " + string)
    pickle_out = open("data/webhook.txt", "wb")
    pickle.dump(string, pickle_out)
    pickle_out.close()

def saveProxieList(name, list, comboBox):
    print("Saving Proxie List")
    global serviceProxyList
    for obj in serviceProxyList:
        if obj.name == name :
            obj.list = list
            pickle_out = open("data/proxieList.txt", "wb")
            pickle.dump(serviceProxyList, pickle_out)
            pickle_out.close()
            return
    newProxie = Proxie(name, list)
    comboBox.addItem(name)
    serviceProxyList.append(newProxie)
    pickle_out = open("data/proxieList.txt", "wb")
    pickle.dump(serviceProxyList, pickle_out)
    pickle_out.close()

def saveProfileData():
    print("Saving Profile List")
    global serviceProfileList
    pickle_out = open("data/profileList.txt", "wb")
    pickle.dump(serviceProfileList, pickle_out)
    pickle_out.close()

def saveTaskData():
    print("Saving Tasks")
    global serviceTaskList
    modifiedServiceTaskList = []
    for task in serviceTaskList:
        tempTask = Task(task.name, task.site, task.mode, task.profile, task.account, task.proxie, task.productLink, task.quantity, "none", "none")
        modifiedServiceTaskList.append(tempTask)
    pickle_out = open("data/taskList.txt", "wb")
    pickle.dump(modifiedServiceTaskList, pickle_out)
    pickle_out.close()

def saveAccountData():
    print("saving account Data")
    global serviceAccountsBHPhoto
    pickle_out = open("data/accountsBH.txt", "wb")
    pickle.dump(serviceAccountsBHPhoto, pickle_out)
    pickle_out.close()
    global serviceAccountsWalmart
    pickle_out = open("data/accountsWalmart.txt", "wb")
    pickle.dump(serviceAccountsWalmart, pickle_out)
    pickle_out.close()
    global serviceAccountsGamenerdz
    pickle_out = open("data/accountsGamenerdz.txt", "wb")
    pickle.dump(serviceAccountsGamenerdz, pickle_out)
    pickle_out.close()
    global serviceAccountsAsus
    pickle_out = open("data/accountsAsus.txt", "wb")
    pickle.dump(serviceAccountsAsus, pickle_out)
    pickle_out.close()

def saveAccountList(newAccountListTextEditor, site):
    print("Saving new account data for: " + site)
    global serviceAccountsBHPhoto
    if site == "B&H Photo":
        serviceAccountsBHPhoto = newAccountListTextEditor.toPlainText()
    global serviceAccountsWalmart
    if site == "Walmart":
        serviceAccountsWalmart = newAccountListTextEditor.toPlainText()
    global serviceAccountsGamenerdz
    if site == "Gamenerdz":
        serviceAccountsGamenerdz = newAccountListTextEditor.toPlainText()
    global serviceAccountsAsus
    if site == "Asus":
        serviceAccountsAsus = newAccountListTextEditor.toPlainText()
    saveAccountData()

def loadProfileData(layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
            cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
            shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
            shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
            billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
            billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
            saveNewProfileButton, saveProfileEditButton):
    print("Loading Profile Data")
    global serviceProfileList
    pickle_in = open("data/profileList.txt", "rb")
    if os.path.getsize("data/profileList.txt") > 0:
        print("Initializing Proxy Lists")
        serviceProfileList = pickle.load(pickle_in)
    for obj in serviceProfileList:
        createProfile(obj, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                    cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                    shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                    shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                    billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                    billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                    saveNewProfileButton, saveProfileEditButton)
    #print("Profile saved has name" + serviceProfileList[0].name)

def loadSettingsData(webhookInputText):
    print("Loading Settings Data")
    pickle_in = open("data/webhook.txt", "rb")
    if os.path.getsize("data/webhook.txt") > 0:
        webhookData = pickle.load(pickle_in)
        webhookInputText.setText(webhookData)
    global serviceAccountsBHPhoto
    pickle_in = open("data/accountsBH.txt", "rb")
    if os.path.getsize("data/accountsBH.txt") > 0:
        serviceAccountsBHPhoto = pickle.load(pickle_in)
    global serviceAccountsGamenerdz
    pickle_in = open("data/accountsGamenerdz.txt", "rb")
    if os.path.getsize("data/accountsGamenerdz.txt") > 0:
        serviceAccountsGamenerdz = pickle.load(pickle_in)
    global serviceAccountsWalmart
    pickle_in = open("data/accountsWalmart.txt", "rb")
    if os.path.getsize("data/accountsWalmart.txt") > 0:
        serviceAccountsWalmart = pickle.load(pickle_in)
    global serviceAccountsAsus
    pickle_in = open("data/accountsAsus.txt", "rb")
    if os.path.getsize("data/accountsAsus.txt") > 0:
        serviceAccountsAsus = pickle.load(pickle_in)


def loadProxieData():
    global serviceProxyList
    print("Loading Proxie Data")
    pickle_in = open("data/proxieList.txt", "rb")
    if os.path.getsize("data/proxieList.txt") > 0:
        print("Initializing Proxy Lists")
        serviceProxyList = pickle.load(pickle_in)
        return

def loadTaskData(layout, creatorFrame, siteComboBox, modeListComboBox, profileComboBox, accountComboBox, proxieComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                saveTaskButton, createNewTaskButton):
    print("Loading Task Data")
    global serviceTaskList
    pickle_in = open("data/taskList.txt", "rb")
    if os.path.getsize("data/taskList.txt") > 0:
        serviceTaskList = pickle.load(pickle_in)
    tempWidget = QLabel()
    for task in serviceTaskList:
        task.directoryName = "none"
        task.statusLabel = tempWidget
        createTask(task, layout, creatorFrame, siteComboBox, modeListComboBox, profileComboBox, accountComboBox,proxieComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                    saveTaskButton, createNewTaskButton)


def verifyProfile(profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, layout, profileCreatorFrame,
                saveNewProfileButton, saveProfileEditButton):
            print("Validating Profile Data")
            if(profileNameLineEdit.text() == ""):
                print("Profile name cannot be blank")
                return
            if(nameOnCardLineEdit.text() == ""):
                print("Name on card cannot be blank")
                return
            if(cardNumberLineEdit.text() == ""):
                print("Card number cannot be blank")
                return
            #***********************************************
            #Need to add validation!!!!
            #Should be able to use QRegExpValidator on LineEdit widgets
            #Will need extensive work to prevent bugs
            #***********************************************

            for obj in serviceProfileList:
                if obj.name == profileNameLineEdit.text() :
                    print("Profile with same name already Exists")
                    return

            print("Creating Profile: " + profileNameLineEdit.text())
            newProfile = Profile(profileNameLineEdit.text(), nameOnCardLineEdit.text(), cardNumberLineEdit.text(), cardExpirationLineEdit.text(),
                            cardCVVLineEdit.text(), emailLineEdit.text(), phoneNumberLineEdit.text(), shippingFirstNameLineEdit.text(),
                            shippingLastNameLineEdit.text(), shippingAddress1LineEdit.text(), shippingAddress2LineEdit.text(), shippingCountryLineEdit.text(),
                            shippingCityLineEdit.text(), shippingPostalLineEdit.text(), shippingStateLineEdit.text(), billingFirstNameLineEdit.text(),
                            billingLastNameLineEdit.text(), billingAddress1LineEdit.text(), billingAddress2LineEdit.text(), billingCountryLineEdit.text(),
                            billingCityLineEdit.text(), billingPostalLineEdit.text(), billingStateLineEdit.text())
            # newProfile = Profile(profileName, "Enzo Arata", "4119288803779911", "12/26", "591", "enzoarata50@gmail.com", "5302774265",
            #     "Enzo", "Arata", "3331 fairway dr", "RM 2", "United States", "Sparks","94930", "Nevada",
            #     "Enzo", "Arata", "3331 fairway dr", "RM 2", "United States", "Sparks","94930", "Nevada")
            createProfile(newProfile, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                        cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                        shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                        shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                        billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                        billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, layout, profileCreatorFrame,
                        saveNewProfileButton, saveProfileEditButton)
            serviceProfileList.append(newProfile)
            saveProfileData()

            profileCreatorFrame.hide()

def verifyTask(taskName, siteName, mode, profileName, account, proxie, productLink, quantity, layout,
                creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox,
                taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                saveTaskButton, createNewTaskButton):
    print("Validating Task Data....")
    if (taskName == ""):
        print('Task name cannot be blank')
        return

    print("Creating Task: " + taskName)

    newTask = Task(taskName, siteName, mode, profileName, account, proxie, productLink, quantity, "none", "none")
    createTask(newTask, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
            saveTaskButton, createNewTaskButton)
    serviceTaskList.append(newTask)
    saveTaskData()
    creatorFrame.hide()

def testWebhook(string):
    print("Testing Webhook")
    #
    #Send Discord Notification
    #
    webhook = DiscordWebhook(url=string)
    embed = DiscordEmbed(title="WebHook Test", description='Test Successful', color=3093054)
    with open("icons/Godfather_puppetmaster.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='Godfather_puppetmaster.png')

    embed.set_thumbnail(url='attachment://Godfather_puppetmaster.png')
    #embed.add_embed_field(name="Product Link", value="{}".format(sys.argv[1]))
    webhook.add_embed(embed)
    response = webhook.execute()

def closeProfileCreator(profileCreatorFrame):
    print("Closing Profile Creator")
    profileCreatorFrame.hide()


def clearProxieList(list):
    print("clearing Proxie List")
    list.clear()

def selectListComboBoxUpdate(value):
    print("Combo Box changed to: " + value)
    for obj in serviceProxyList:
        if obj.name == value :
            print("Proxy list found")
            return obj
    blankProxie = Proxie(" "," ")
    return blankProxie

def updateTaskAccountModeSelection(site, accountListComboBox, modeListComboBox ):
    print("Updating Account Selection")
    accountListComboBox.clear()
    modeListComboBox.clear()
    if site == "B&H Photo":
        for account in serviceAccountsBHPhoto.splitlines():
            accountListComboBox.addItem(account)
        for mode in serviceBHPhotoModes:
            modeListComboBox.addItem(mode)
    if site == "Walmart":
        for account in serviceAccountsWalmart.splitlines():
            accountListComboBox.addItem(account)
        for mode in serviceWalmartModes:
            modeListComboBox.addItem(mode)
    if site == "Gamenerdz":
        for account in serviceAccountsGamenerdz.splitlines():
            accountListComboBox.addItem(account)
        for mode in serviceGamenerdzModes:
            modeListComboBox.addItem(mode)
    if site == "Asus":
        for account in serviceAccountsAsus.splitlines():
            accountListComboBox.addItem(account)
        for mode in serviceAsusModes:
            modeListComboBox.addItem(mode)

def updateAccountsPage(accountListTextEditor, site):
    print("Updating Account page")
    accountListTextEditor.clear()
    if site == "B&H Photo":
        accountListTextEditor.appendPlainText(serviceAccountsBHPhoto)
    if site == "Walmart":
        accountListTextEditor.appendPlainText(serviceAccountsWalmart)
    if site == "Gamenerdz":
        accountListTextEditor.appendPlainText(serviceAccountsGamenerdz)
    if site == "Asus":
        accountListTextEditor.appendPlainText(serviceAccountsAsus)

def updateProxiePage(proxyName, proxyList, proxy ):
    print("Updating Page")
    #proxyName.setText(proxy.name)
    proxyName.clear()
    proxyName.setText(proxy.name)
    proxyList.clear()
    proxyList.appendPlainText(proxy.list)

def deleteProxieList(listName, comboBox):
    if listName == "Default List":
        return
    print("Deleting List")
    for obj in serviceProxyList:
        if obj.name == listName :
            serviceProxyList.remove(obj)
            comboBox.clear()
            for item in serviceProxyList:
                comboBox.addItem(item.name)
                pickle_out = open("data/proxieList.txt", "wb")
                pickle.dump(serviceProxyList, pickle_out)
                pickle_out.close()

def deleteProfile(tempProfile, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
            cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
            shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
            shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
            billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
            billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
            saveNewProfileButton, saveProfileEditButton):
    print("Deleting Profile!")
    global serviceProfileList
    for obj in serviceProfileList:
        if obj.name == tempProfile.name:
            serviceProfileList.remove(obj)
            #layout.removeWidget(widget)
            #sip.delete(widget)
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
            saveProfileData()
            for item in serviceProfileList:
                createProfile(item, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                            cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                            shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                            shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                            billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                            billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                            saveNewProfileButton, saveProfileEditButton)

def deleteTask(tempTask, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                saveTaskButton, createNewTaskButton):
    print("Deleting Task!")
    global serviceTaskList
    for task in serviceTaskList:
        if task == tempTask:
            serviceTaskList.remove(task)
            #Remove all items from task page and re add them
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
            saveTaskData()
            for item in serviceTaskList:
                createTask(item, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                            saveTaskButton, createNewTaskButton)

def clearAllTasks(layout):
    print("Clearing all tasks")
    global serviceTaskList
    serviceTaskList.clear()
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)
    saveTaskData()

def editTask(task, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
            saveTaskButton, createNewTaskButton):
    createNewTaskButton.hide()
    saveTaskButton.show()
    global serviceHighlightedTask
    serviceHighlightedTask = task;
    print("Editing Task")
    global serviceProfileList
    global serviceAsusModes
    creatorFrame.show()
    counter = 0
    for site in serviceSiteList:
        if site == task.site:
            siteListComboBox.setCurrentIndex(counter)
        counter = counter + 1

    counter = 0
    if task.site == "B&H Photo":
        for account in serviceAccountsBHPhoto.splitlines():
            if account == task.account:
                accountListComboBox.setCurrentIndex(counter)
            counter = counter + 1
    if task.site == "Walmart":
        for account in serviceAccountsWalmart.splitlines():
            if account == task.account:
                accountListComboBox.setCurrentIndex(counter)
            counter = counter + 1
    if task.site == "Gamenerdz":
        for account in serviceAccountsGamenerdz.splitlines():
            if account == task.account:
                accountListComboBox.setCurrentIndex(counter)
            counter = counter + 1
    if task.site == "Asus":
        for account in serviceAccountsAsus.splitlines():
            if account == task.account:
                accountListComboBox.setCurrentIndex(counter)
            counter = counter + 1

    counter = 0
    profileListComboBox.clear()
    for profile in serviceProfileList:
        profileListComboBox.addItem(profile.name)
        if profile.name == task.profile:
            profileListComboBox.setCurrentIndex(counter)
        counter = counter + 1
    counter = 0

    proxieListComboBox.clear()
    for proxie in serviceProxyList:
        proxieListComboBox.addItem(proxie.name)
        if proxie.name == task.proxie:
            proxieListComboBox.setCurrentIndex(counter)
        counter = counter + 1
    counter = 0
    modeListComboBox.clear()
    modeListComboBox.addItem(task.mode)
    modeListComboBox.setCurrentIndex(0)
    # if task.site == "B&H Photo":
    #     for mode in serviceBHPhotoModes:
    #
    #         #modeListComboBox.addItem(mode)
    #         if mode == task.mode:
    #             modeListComboBox.setCurrentIndex(counter)
    #         counter = counter + 1
    # if task.site == "Walmart":
    #     for mode in serviceWalmartModes:
    #         if mode == task.mode:
    #             modeListComboBox.setCurrentIndex(counter)
    #         counter = counter + 1
    # if task.site == "Gamenerdz":
    #     for mode in serviceGamenerdzModes:
    #         if mode == task.mode:
    #             modeListComboBox.setCurrentIndex(counter)
    #         counter = counter + 1
    # if task.site == "Asus":
    #     for mode in serviceAsusModes:
    #         #modeListComboBox.addItem(mode)
    #
    #         if mode == task.mode:
    #             modeListComboBox.setCurrentIndex(counter)
    #         counter = counter + 1

    taskNameLineEdit.setText(task.name)
    productLinkLineEdit.setText(task.productLink)
    quantityLineEdit.setText("1")
    if task.quantity != "":
        quantityLineEdit.setText(task.quantity)

def saveTaskEdit(taskName, site, mode, profile,
                account, proxie, productLink, quantity,
                layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox,
                taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                saveNewTaskButton, createNewTaskButton):
        print("Saving Edit")
        global serviceHighlightedTask
        print("Edit for task "  + serviceHighlightedTask.name + " completed!")
        serviceHighlightedTask.name = taskName
        serviceHighlightedTask.site = site
        serviceHighlightedTask.mode = mode
        serviceHighlightedTask.profile = profile
        serviceHighlightedTask.account = account
        serviceHighlightedTask.productLink = productLink
        serviceHighlightedTask.quantity = quantity
        serviceHighlightedTask.proxie = proxie

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        for item in serviceTaskList:
            createTask(item, layout, creatorFrame, siteListComboBox, modeListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
                        saveNewTaskButton, createNewTaskButton)
        saveTaskData()
        creatorFrame.hide()

# editTask(task, layout, creatorFrame, siteListComboBox, profileListComboBox, accountListComboBox, proxieListComboBox, taskNameLineEdit, productLinkLineEdit, quantityLineEdit,
#             saveTaskButton, createNewTaskButton)
def editProfile(profile, layout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
            cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
            shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
            shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
            billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
            billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
            saveNewProfileButton, saveProfileEditButton):
    print("Editing Profile")
    profileCreatorFrame.show()
    saveNewProfileButton.hide()
    saveProfileEditButton.show()
    global serviceHighlightedProfile
    serviceHighlightedProfile = profile
    profileNameLineEdit.setText(profile.name)
    nameOnCardLineEdit.setText(profile.nameOnCard)
    cardNumberLineEdit.setText(profile.cardNumber)
    cardExpirationLineEdit.setText(profile.cardExpiration)
    cardCVVLineEdit.setText(profile.cardCVV)
    emailLineEdit.setText(profile.email)
    phoneNumberLineEdit.setText(profile.phoneNumber)
    shippingFirstNameLineEdit.setText(profile.shippingFirstName)
    shippingLastNameLineEdit.setText(profile.shippingLastName)
    shippingAddress1LineEdit.setText(profile.shippingAddress1)
    shippingAddress2LineEdit.setText(profile.shippingAddress2)
    shippingCountryLineEdit.setText(profile.shippingCountry)
    shippingCityLineEdit.setText(profile.shippingCity)
    shippingPostalLineEdit.setText(profile.shippingPostal)
    shippingStateLineEdit.setText(profile.shippingState)

def saveProfileEdit(profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                    cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                    shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                    shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                    billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                    billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                    saveNewProfileButton, saveProfileEditButton ):
            print("Saving Profile Edit")
            global serviceHighlightedProfile
            print("Edit for profile "  + serviceHighlightedProfile.name + " completed!")
            serviceHighlightedProfile.name = profileNameLineEdit.text()
            serviceHighlightedProfile.nameOnCard = nameOnCardLineEdit.text()
            serviceHighlightedProfile.cardNumber = cardNumberLineEdit.text()
            serviceHighlightedProfile.cardExpiration = cardExpirationLineEdit.text()
            serviceHighlightedProfile.cardCVV = cardCVVLineEdit.text()
            serviceHighlightedProfile.email = emailLineEdit.text()
            serviceHighlightedProfile.phoneNumber = phoneNumberLineEdit.text()
            serviceHighlightedProfile.shippingFirstName = shippingFirstNameLineEdit.text()
            serviceHighlightedProfile.shippingLastName = shippingLastNameLineEdit.text()
            serviceHighlightedProfile.shippingAddress1 = shippingAddress1LineEdit.text()
            serviceHighlightedProfile.shippingAddress2 = shippingAddress2LineEdit.text()
            serviceHighlightedProfile.shippingCountry  = shippingCountryLineEdit.text()
            serviceHighlightedProfile.shippingCity = shippingCityLineEdit.text()
            serviceHighlightedProfile.shippingPostalLabel = shippingPostalLineEdit.text()
            serviceHighlightedProfile.shippingState = shippingStateLineEdit.text()

            for i in reversed(range(profileScrollLayout.count())):
                profileScrollLayout.itemAt(i).widget().setParent(None)
            for profile in serviceProfileList:
                createProfile(profile, profileScrollLayout, profileNameLineEdit, nameOnCardLineEdit, cardNumberLineEdit,
                                cardExpirationLineEdit, cardCVVLineEdit, emailLineEdit, phoneNumberLineEdit,
                                shippingFirstNameLineEdit, shippingLastNameLineEdit, shippingAddress1LineEdit, shippingAddress2LineEdit,
                                shippingCountryLineEdit, shippingCityLineEdit,shippingPostalLineEdit, shippingStateLineEdit,
                                billingFirstNameLineEdit, billingLastNameLineEdit, billingAddress1LineEdit, billingAddress2LineEdit,
                                billingCountryLineEdit, billingCityLineEdit, billingPostalLineEdit, billingStateLineEdit, profileScrollLayout, profileCreatorFrame,
                                saveNewProfileButton, saveProfileEditButton)
            saveProfileData()
            profileCreatorFrame.hide()


def launchTask(task):
    global serviceProfileList
    if task.directoryName == 'none':
        parent_dir = "tempdata/"
        unique_filename = str(uuid.uuid4())
        path = os.path.join(parent_dir, unique_filename)
        os.mkdir(path)
        task.directoryName = path
        taskDataName= "task.txt"
        completeTaskDataPath = os.path.join(path, taskDataName)
        statusDataName= "status.txt"
        completeStatusDataPath = os.path.join(path, statusDataName)
        commandsDataName = "commands.txt"
        completeCommandsDataPath = os.path.join(path, commandsDataName)
        proxieString = "none"
        for proxie in serviceProxyList:
            if proxie.name == task.proxie and proxie.name != "Default List":
                splitProxies = proxie.list.splitlines()
                randomProxyNumber = randrange(len(splitProxies))
                proxieParts = re.split('[:]', splitProxies[randomProxyNumber])
                #'https://foqfoa:xqgjrj@192.214.179.204:17102'
                #myProxy = "mvqrdn:oooztk@216.173.122.27:17102"
                proxieString = ("http://"+proxieParts[0]+":"+proxieParts[1])
                proxyUser = proxieParts[2]
                proxyPass = proxieParts[3]
                # 'https': 'https://192.168.10.100:8889',

                print(proxieString)


        file1 = open(completeTaskDataPath, 'w')
        file1.write(task.name +"\n")
        file1.write(task.productLink+"\n")
        file1.write(task.quantity+"\n")
        file1.write(task.account+"\n")
        file1.write(proxieString + "\n")
        file1.write("Initializing" + "\n")
        file1.close()
        file1 = open(completeStatusDataPath, 'w')
        file1.write("Initializing" +"\n")
        file1.close()
        file1 = open(completeCommandsDataPath, 'w')
        file1.write("Running" +"\n")
        file1.close()
        profileDataName= "profile.txt"
        completeProfileDataPath = os.path.join(path, profileDataName)
        open(completeProfileDataPath, 'a').close()
        for profile in serviceProfileList:
            if profile.name == task.profile:
                taskProfile = profile
                pickle_out = open(completeProfileDataPath, "wb")
                pickle.dump(taskProfile, pickle_out)
                pickle_out.close()

        if task.site == "B&H Photo":
            print("Launching B&H Photo Task: "+ task.name + "!")
            subprocess.Popen([sys.executable, 'BHphotoTest.py', completeProfileDataPath, completeTaskDataPath, completeStatusDataPath])
        if task.site == "Gamenerdz":
            print("Launching Gamenerdz Task: "+ task.name + "!")
            subprocess.Popen([sys.executable, 'gameNerdzTest.py', completeProfileDataPath, completeTaskDataPath, completeStatusDataPath])
            #subprocess.Popen([sys.executable, 'gameNerdzTestFireFox.py', completeProfileDataPath, completeTaskDataPath])
        if task.site == "Asus":
            print("Launching Asus Task: "+ task.name + "!")
            newThread = AsusMonitorThread(task.productLink, proxieString, proxyUser, proxyPass, completeStatusDataPath, completeCommandsDataPath)
            newThread.setDaemon(True)
            newThread.start()
            #thread = AsusMonitorThread(taskProfile, task, proxieString, statusPath)
            #subprocess.Popen([sys.executable, 'AsusTest.py', completeProfileDataPath, completeTaskDataPath, completeStatusDataPath])
        if task.site == "Walmart":
            print("Launching Walmart Task: "+ task.name + "!")
        #serialize task data so it can be accesed by task
    else :
        commandsDataName = "commands.txt"
        completeCommandsDataPath = os.path.join(task.directoryName, commandsDataName)
        file1 = open(completeCommandsDataPath, 'w')
        file1.write("START")
        file1.close()
        statusDataName= "status.txt"
        completeStatusDataPath = os.path.join(task.directoryName, statusDataName)
        file1 = open(completeStatusDataPath, 'w')
        file1.write("Starting...")
        file1.close()

def pauseTask(task):
    commandsDataName = "commands.txt"
    completeCommandsDataPath = os.path.join(task.directoryName, commandsDataName)
    file1 = open(completeCommandsDataPath, 'w')
    file1.write("STOP")
    file1.close()

    statusDataName= "status.txt"
    completeStatusDataPath = os.path.join(task.directoryName, statusDataName)
    file1 = open(completeStatusDataPath, 'w')
    file1.write("Stopping Task...")
    file1.close()

def resetTaskTempData():
    import os, shutil
    folder = 'tempdata'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

print("starting window")
#
#updateThread = threading.Thread(target=threadGetTaskInfo())
#updateThread.start()
thread = updaterThread()
thread.setDaemon(True)
thread.start()
window()
