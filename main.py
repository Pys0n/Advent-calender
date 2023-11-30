from datetime import date
from random import shuffle
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *

from helper import *

class CalendarDoor(QPushButton):
    '''
    This is a door of your Chirstmas Calendar.\n
    `number` = number of the door\n
    `currentDay` = today's day (1 to 31)\n
    `currentMonth` = today's month (1 to 12)\n
    `present` = present behind the door
    '''
    def __init__(self, parent, number:int, currentDay:int, currentMonth:int, present:str, status:str):
        super(CalendarDoor, self).__init__()
        self.setParent(parent)
        self.__parent = parent
        self.__number = number
        self.__currentDay = currentDay
        self.__currentMonth = currentMonth
        self.__present = present
        self.__loadLayout()
        self.setStyleSheet('border-image: url('+getFullPath('door.png')+');')
        self.__status = status
        if status == 'open':
            if self.__number%3 == 0:
                self.setStyleSheet('border-image: url('+getFullPath('opendoor3.png')+');')
            elif self.__number%2 == 0:
                self.setStyleSheet('border-image: url('+getFullPath('opendoor2.png')+');')
            else:
                self.setStyleSheet('border-image: url('+getFullPath('opendoor1.png')+');')
        self.clicked.connect(self.__open)

    def __loadLayout(self):
        text = QLabel(str(self.__number))
        text.setFont(QFont('Arial', 25))
        text.setStyleSheet('border-image: None;\ncolor: #ffffff;')
        hLayout = QHBoxLayout()
        hLayout.addStretch(1)
        hLayout.addWidget(text)
        hLayout.addStretch(1)
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(hLayout)
        layout.addStretch(1)
        self.setLayout(layout)
        return

    def __open(self):
        def closeInfo():
            self.__parent.continue_btn.move(1500,0)
            self.__parent.infoScreen.move(1500,0)
            return
        if self.__currentMonth == 12  and self.__number <= self.__currentDay  and self.__status == 'close':
            self.__parent.doorData[str(self.__number)] = 'open'
            self.__parent.continue_btn.clicked.connect(closeInfo)        
            self.__parent.infoScreen.setText('You get: '+self.__present)
            self.__parent.continue_btn.move(588,703)
            self.__parent.infoScreen.move(88,73)
            self.__status = 'open'
            if self.__number%3 == 0:
                self.setStyleSheet('border-image: url('+getFullPath('opendoor3.png')+');')
            elif self.__number%2 == 0:
                self.setStyleSheet('border-image: url('+getFullPath('opendoor2.png')+');')
            else:
                self.setStyleSheet('border-image: url('+getFullPath('opendoor1.png')+');')
        return

    def getNumber(self):
        return self.__number
    
    def getPresent(self):
        return self.__present


class Calendar(QWidget):
    def __init__(self):
        super(Calendar, self).__init__()

        self.__getDate()
        self.__loadData()
        self.__loadDoors()
        self.__loadBackground()

        self.setMinimumSize(screensize[0],screensize[1])
        self.setMaximumSize(screensize[0],screensize[1])
        self.setGeometry(100,100,screensize[0],screensize[1])
        self.setWindowTitle('Advent calendar '+str(self.__year))

    def closeEvent(self, event):
        self.__saveData()

    def __saveData(self):
        doorData = str()
        for data in self.doorData.values():
            if data == 'close':
                doorData += '_'
            elif data == 'open':
                doorData += 'x'
        presentList = str()
        run = 0
        for data in self.__presentList:
            if run != 0:
                presentList += ';'
            presentList += data
            run = 1

        with open('data.txt', 'w') as file:
            file.write('You can write your presents in the list behind the word "Presents", please write without \" or \' as with a string.\n')
            file.write('Information: The semicolon (;) separates all gifts.\n')
            file.write('If there 24 presents in the list, then is present 1 behind door 1 and if more or less then 24, then they are assigned to a random door.\n')
            file.write('Please do not change the values behind \"presentList\" and \"language\"!\n')
            file.write('\n')
            file.write(f'presents: {self.__presents}\n')
            file.write(f'presentList: {presentList}\n')
            file.write(f'language: en\n')
            file.write(f'doors: {doorData}\n')

    def __loadData(self):
        with open('data.txt', 'r') as file:
            for line in file:
                if 'presents: ' in line:
                    line = line.split('presents: ')
                    presents = line[1].split('\n')
                    self.__presents = presents[0]
                    presents = presents[0].split(';')
                elif 'presentList: ' in line:
                    line = line.split('presentList: ')
                    if line[1] == '\n':
                        if len(presents) < 24:
                            while True:
                                shuffle(presents)
                                presents.append(presents[-1])
                                if len(presents) == 24:
                                    break
                        elif len(presents) > 24:
                            while True:
                                shuffle(presents)
                                presents.remove(presents[-1])
                                if len(presents) == 24:
                                    break
                        self.__presentList = presents
                    else:
                        presentList = line[1].split('\n')[0].split(';')
                        self.__presentList = presentList
                elif 'language: ' in line:
                    line = line.split('language: ')
                    line = line[1].split('\n')
                    self.__language = line[0]
                elif 'doors: ' in line:
                    line = line.split('doors: ')
                    line = line[1].split('\n')
                    self.__doorData = line[0]  
            file.close()
        return

    def __getDate(self):
        todaysDate = date.today()
        todaysDate = str(todaysDate).split('-')
        self.__day = int(todaysDate[2])
        self.__month = int(todaysDate[1])
        self.__year = int(todaysDate[0])
        return
    
    def __loadBackground(self):
        image = QImage(getPath("calendar.png"))
        sImage = image.scaled(QSize(screensize[0],screensize[1])) 
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.infoScreen = QPushButton(self)
        self.infoScreen.setGeometry(1500,0,1200,700)
        self.continue_btn = QPushButton('Continue', self)
        self.continue_btn.setGeometry(1500,0,200,50)
        return

    def __loadDoors(self):
        self.doorData = dict()
        run = 1
        for data in self.__doorData:
            if data == '_':
                self.doorData[str(run)] = 'close'
            elif data == 'x':
                self.doorData[str(run)] = 'open'
            run += 1

        self.door1 = CalendarDoor(self, 1, self.__day, self.__month, self.__presentList[1-1], self.doorData['1'])
        self.door1.setGeometry(975, 20, 125, 125)
        self.door2 = CalendarDoor(self, 2, self.__day, self.__month, self.__presentList[2-1], self.doorData['2'])
        self.door2.setGeometry(550, 200, 125, 125)
        self.door3 = CalendarDoor(self, 3, self.__day, self.__month, self.__presentList[3-1], self.doorData['3'])
        self.door3.setGeometry(800, 500, 125, 125)
        self.door4 = CalendarDoor(self, 4, self.__day, self.__month, self.__presentList[4-1], self.doorData['4'])
        self.door4.setGeometry(20, 20, 125, 125)
        self.door5 = CalendarDoor(self, 5, self.__day, self.__month, self.__presentList[5-1], self.doorData['5'])
        self.door5.setGeometry(525, 375, 125, 125)
        self.door6 = CalendarDoor(self, 6, self.__day, self.__month, self.__presentList[6-1], self.doorData['6'])
        self.door6.setGeometry(100, 350, 125, 125)
        self.door7 = CalendarDoor(self, 7, self.__day, self.__month, self.__presentList[7-1], self.doorData['7'])
        self.door7.setGeometry(1200, 100, 125, 125)
        self.door8 = CalendarDoor(self, 8, self.__day, self.__month, self.__presentList[8-1], self.doorData['8'])
        self.door8.setGeometry(450, 20, 125, 125)
        self.door9 = CalendarDoor(self, 9, self.__day, self.__month, self.__presentList[9-1], self.doorData['9'])
        self.door9.setGeometry(700, 700, 125, 125)
        self.door10 = CalendarDoor(self, 10, self.__day, self.__month, self.__presentList[10-1], self.doorData['10'])
        self.door10.setGeometry(70, 170, 125, 125)
        self.door11 = CalendarDoor(self, 11, self.__day, self.__month, self.__presentList[11-1], self.doorData['11'])
        self.door11.setGeometry(725, 300, 125, 125)
        self.door12 = CalendarDoor(self, 12, self.__day, self.__month, self.__presentList[12-1], self.doorData['12'])
        self.door12.setGeometry(350, 270, 125, 125)
        self.door13 = CalendarDoor(self, 13, self.__day, self.__month, self.__presentList[13-1], self.doorData['13'])
        self.door13.setGeometry(1200, 700, 125, 125)
        self.door14 = CalendarDoor(self, 14, self.__day, self.__month, self.__presentList[14-1], self.doorData['14'])
        self.door14.setGeometry(300, 450, 125, 125)
        self.door15 = CalendarDoor(self, 15, self.__day, self.__month, self.__presentList[15-1], self.doorData['15'])
        self.door15.setGeometry(1000, 300, 125, 125)
        self.door16 = CalendarDoor(self, 16, self.__day, self.__month, self.__presentList[16-1], self.doorData['16'])
        self.door16.setGeometry(1050, 550, 125, 125)
        self.door17 = CalendarDoor(self, 17, self.__day, self.__month, self.__presentList[17-1], self.doorData['17'])
        self.door17.setGeometry(225, 125, 125, 125)
        self.door18 = CalendarDoor(self, 18, self.__day, self.__month, self.__presentList[18-1], self.doorData['18'])
        self.door18.setGeometry(70, 525, 125, 125)
        self.door19 = CalendarDoor(self, 19, self.__day, self.__month, self.__presentList[19-1], self.doorData['19'])
        self.door19.setGeometry(950, 700, 125, 125)
        self.door20 = CalendarDoor(self, 20, self.__day, self.__month, self.__presentList[20-1], self.doorData['20'])
        self.door20.setGeometry(250, 685, 125, 125)
        self.door21 = CalendarDoor(self, 21, self.__day, self.__month, self.__presentList[21-1], self.doorData['21'])
        self.door21.setGeometry(500, 575, 125, 125)
        self.door22 = CalendarDoor(self, 22, self.__day, self.__month, self.__presentList[22-1], self.doorData['22'])
        self.door22.setGeometry(1200, 400, 125, 125)
        self.door23 = CalendarDoor(self, 23, self.__day, self.__month, self.__presentList[23-1], self.doorData['23'])
        self.door23.setGeometry(30, 700, 125, 125)
        self.door24 = CalendarDoor(self, 24, self.__day, self.__month, self.__presentList[24-1], self.doorData['24'])
        self.door24.setGeometry(700, 20, 225, 225)
        return
        

    def open():
        '''
        This function starts the PyQt5 Advent calendar.
        '''
        app = QApplication(sys.argv)
        w = Calendar()
        w.show()
        sys.exit(app.exec_())
	
if __name__ == '__main__':
    Calendar.open()