# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application and then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QColorDialog, QGraphicsColorizeEffect, QRadioButton, QInputDialog, QGridLayout, QCheckBox, \
    QSlider
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap, QColor, QFont, QImage
import sys
import csv, random
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize
from PyQt6.uic.Compiler.qtproxies import QtGui, QtWidgets, QtCore

class PictionaryGame(QMainWindow):  # documentation https://doc.qt.io/qt-6/qwidget.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()
        # set window title
        self.setWindowTitle("Pictionary Game - A2 Template")
        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setStyleSheet("background-color: #5B768C;")  # change the bg color
        self.setGeometry(top, left, width, height)
        self.setMinimumWidth(width)
        # set the icon
        # windows version i need to declare it in main on mac to show
        self.setWindowIcon(
            QIcon("./icons/paint-brush.png"))  # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QPixmap("./icons/pictionary.jpeg")  # documentation: https://doc.qt.io/qt-6/qpixmap.html
         # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(" File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size")  # add the "Brush Size" menu to the menu bar
        rulesMenu = mainMenu.addMenu("Help")

        helpAction = QAction(QIcon('./icons/question.png'), "Help", self)
        helpAction.triggered.connect(self.help)
        rulesMenu.addAction(helpAction)
        # rules
        rulesAction = QAction(QIcon('./icons/rules.png'), "Rules", self)
        rulesAction.triggered.connect(self.rules)
        rulesMenu.addAction(rulesAction)
        # open menu item
        openAction = QAction(QIcon("./icons/open.webp"), "Open", self)  # create a open action with a png as an icon
        openAction.setShortcut("Ctrl+O")  # connect this open action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(openAction)  # add the open action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        openAction.triggered.connect(self.open)  # when the menu option is selected or the shortcut is used the save slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)  # create a save action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        saveAction.setShortcut("Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(saveAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        saveAction.triggered.connect(self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered
        # CLOSE
        closeAction = QAction(QIcon("./icons/quit.png"), "Quit", self)  # create a close action with a png as an icon
        closeAction.setShortcut("Ctrl+Q")  # connect this close action to a keyboard shortcut
        fileMenu.addAction(closeAction)  # add this action to the file menu
        closeAction.triggered.connect(
        self.close)  # when the menu option is selected or the shortcut is triggered
        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # creating a button
        self.button = QPushButton("START", self)
        # setting up the geometry
        # connecting method when button get clicked
        self.button.setStyleSheet('QPushButton {background-color: #5B768C; color: white;}')
        self.button.show()
        self.button.clicked.connect(self.clickme)
        # Side Dock
        self.dockInfo = QDockWidget("Score", self)
        self.dockInfo.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        # NOT ALLOWING TO MOVE OR CLOSE OR EXPAND THE DOCKWIDGET
        self.dockInfo.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        # creating label to show the seconds
        self.label = QLabel("60", self)
        # setting font to the label
        self.label.setFont(QFont('Times', 30))
        # creating a timer object and starting when game start
        self.count = 600
        self.start = False
        self.space = False
        timer = QTimer(self)
        # adding action to timer
        timer.timeout.connect(self.showTime)
        # update the timer every tenth second
        timer.start(100)
        #widget inside the Dock
        playerInfo = QWidget()
        self.score1 = QLabel("0")
        self.score2 = QLabel("0")
        self.vbdock = QVBoxLayout()
        #sublayout for the colors on the dock
        sublayout = QGridLayout()
        #buttons with colors
        yellow = QPushButton()
        yellow.setStyleSheet("background: yellow")
        # adding action to a button
        yellow.clicked.connect(self.yellow)

        red = QPushButton()
        red.setStyleSheet("background: Red")
        # adding action to a button
        red.clicked.connect(self.red)

        green = QPushButton()
        green.setStyleSheet("background: Green")
        # adding action to a button
        green.clicked.connect(self.green)

        black = QPushButton()
        black.setStyleSheet("background: Black")
        # adding action to a button
        black.clicked.connect(self.black)

        white = QPushButton()
        white.setStyleSheet("background: white")
        # adding action to a button
        white.clicked.connect(self.white)

        orange = QPushButton()
        orange.setStyleSheet("background: orange")
        # adding action to a button
        orange.clicked.connect(self.orange)

        blue = QPushButton()
        blue.setStyleSheet("background: Blue")
        # adding action to a button
        blue.clicked.connect(self.blue)

        purple = QPushButton()
        purple.setStyleSheet("background: Medium Purple")
        # adding action to a button
        purple.clicked.connect(self.purple)

        pink = QPushButton()
        pink.setStyleSheet("background: Magenta")
        # adding action to a button
        pink.clicked.connect(self.pink)

        mySlider = QSlider(Qt.Orientation.Horizontal, self)
        mySlider.setRange(3, 20)

        mySlider.valueChanged.connect(self.changeValue)

        lime = QPushButton()
        lime.setStyleSheet("background: Lime")
        # adding action to a button
        lime.clicked.connect(self.lime)

        multi = QPushButton("Edit colors")
        # setting geometry of button
        multi.setFixedSize(60, 60)
        multi.setStyleSheet("background-image: url(./icons/rainbow.png);"
                            " background-repeat: no-repeat;"
                            "background-position: center;"
                            "font-size: 11px;"
                            "border: none;"
                            "text-align:top;")
        # adding action to a button
        multi.clicked.connect(self.morec)
        self.currentC = QPushButton()
        # setting geometry of button
        self.currentC.setFixedSize(40, 40)
        self.currentC.setStyleSheet("background: Black;"
                                    "border : none")
        # adding qlabe
        size = QLabel("Brush size: ")
        size.setStyleSheet("font-size: 11px;")

        playerInfo.setLayout(self.vbdock)
        playerInfo.setMaximumSize(100, self.height())
        #add controls to custom widget
        self.vbdock.addWidget(self.button)
        self.currentturn = QLabel("Player 1")
        self.mode = QLabel()
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(QLabel("Scores:"))
        self.player1 = QLabel()
        self.player1.setText("Player 1:    0")
        self.vbdock.addWidget(self.player1)
        self.player2 = QLabel()
        self.player2.setText("Player 2:    0")
        self.vbdock.addWidget(self.player2)
        self.vbdock.addStretch(1)
        self.vbdock.addLayout(sublayout)
        sublayout.addWidget(black, 0, 0)
        sublayout.addWidget(white, 0, 1)
        sublayout.addWidget(yellow, 1, 0)
        sublayout.addWidget(orange, 1, 1)
        sublayout.addWidget(pink, 2, 0)
        sublayout.addWidget(red, 2, 1)
        sublayout.addWidget(purple, 3, 0)
        sublayout.addWidget(blue, 3, 1)
        sublayout.addWidget(green, 4, 0)
        sublayout.addWidget(lime, 4, 1)
        self.vbdock.addWidget(multi, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbdock.addWidget(self.currentC, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbdock.addWidget(size)
        self.vbdock.addWidget(mySlider)
        self.vbdock.addStretch(1)
        self.vbdock.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        # creating a button
        self.skipBut = QPushButton("Skip turn", self)
        self.skipBut.setStyleSheet('QPushButton {background-color: #5B768C; color: white;}')
        self.vbdock.addWidget(self.skipBut)
        self.vbdock.addLayout(sublayout)
        #Setting colour of dock to gray
        playerInfo.setAutoFillBackground(True)
        playerInfo.setStyleSheet("background-color: #A3C1DA; color: black")
        self.number = QLabel("0")
        #set widget for dock
        self.dockInfo.setWidget(playerInfo)
        # setting status bar message
        self.statusBar().showMessage(" ")
        # adding label to status bar
        self.statusBar().addPermanentWidget(self.mode)

    # action method
    def clickme(self):
         # hiding the button
        self.button.hide()
        self.skipBut.clicked.connect(self.skip)
        self.skipBut.show()
        self.startGame()
        # printing pressed
        print("pressed")
    #ON KEY RELEASE EVENT IF USER GUES CORRECTLY PRESS SPACE SKIP S
    def keyReleaseEvent(self, event):
        print (event.text())
        if event.text() == " ":
            if self.start:
               self.teamWON()
               print("SPACE")
        if event.text() == "s":
            self.skip()
            print("s")
        event.accept()

    # event handlers
    def mousePressEvent(self, event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
       if  self.number.text() == "1":
         if event.button() == Qt.MouseButton.LeftButton:    # if the pressed button is the left button
                self.drawing = True  # enter drawing mode
                print(self.brushColor)
                self.start = True  # start timer
                self.space = True # allowing space
                self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
                print(self.lastPoint)  # print the lastPoint for debugging purposes
       else:
           self.clickme()

    def mouseMoveEvent(self, event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            # setting status bar message
            self.statusBar().showMessage(self.currentturn.text() + " drawing...")
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):  # when the mouse is released, documentation: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button, documentation: https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode
            # setting status bar message
            if self.number.text() == "1":
               self.statusBar().showMessage(self.currentturn.text())
    #SETING SIZ OF VRUSH
    def changeValue(self, value):
        self.brushSize = value

  #FOR SHOWING AND STARTING , FINISHING TIME
    def showTime(self):
        # checking if flag is true
        if self.start:
            # incrementing the counter
            self.count -= 1
            # timer is completed
            if self.count == 0:
               self.teamWON()
        if self.start:
            # getting text from count
            text = str(self.count / 10)
            # showing text
            self.label.setText(text)

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(QPoint(), self.image)  # draw the image , documentation: https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path
        #if saved file message
        self.statusBar().showMessage("The file have been saved...", 3000)

    def clear(self):
        self.image.fill(
            Qt.GlobalColor.white)  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class
    # CLOSE EVENT FOR CLOSING APPLICATION
    def closeEvent(self, event):
        self.statusBar().showMessage("Exit application")
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:

            event.accept()
        else:

            event.ignore()
            self.statusBar().showMessage(" ")

    #SKIP THE TURN BUTTON
    def skip(self):
        if self.currentturn.text() == "Player 1":
            self.currentturn.setText("Player 2")
            self.label.setText("End")
            self.start = False
            self.reset()
        else:
            self.currentturn.setText("Player 1")
            self.label.setText("End")
            self.start = False
            self.reset()
    # deciding who won counting and changing turns
    def teamWON(self):
        # making flag false
        self.start = False
        self.count = 600
        # New turn start
        self.label.setText("End")
        if self.currentturn.text() == "Player 1":
            # IF QUESSED CORRECTLY ADDING PONTS
            if self.timeUp() == QMessageBox.StandardButton.Yes:
                scorecount = str(int(self.score1.text()) + 1)
                scorecount2 = str(int(self.score2.text()) + 2)
                self.score1.setText(scorecount)
                self.score2.setText(scorecount2)
                self.player1.setText("Player 1:   " + scorecount)
                self.player2.setText("Player 2:   " + scorecount2)
                self.currentturn.setText("Player 2")
                if int(scorecount) >= 10:
                    if int(scorecount2) < int(scorecount):
                        self.player1won()
                    else:
                        self.player2won()
                elif int(scorecount2) >= 10:
                    self.player2won()
                else:
                    self.reset()
            else:
                self.currentturn.setText("Player 2 turn")
                self.reset()

        else:
            self.currentturn.setText("Player 2")
            if self.timeUp() == QMessageBox.StandardButton.Yes:
                # IF QUESSED CORRECTLY ADDING PONTS
                scorecount = str(int(self.score1.text()) + 2)
                scorecount2 = str(int(self.score2.text()) + 1)
                self.score1.setText(scorecount)
                self.score2.setText(scorecount2)
                self.player1.setText("Player 1:   " + scorecount)
                self.player2.setText("Player 2:   " + scorecount2)
                self.currentturn.setText("Player 1")
                if int(scorecount2) >= 10:
                    if int(scorecount2) > int(scorecount):
                        self.player2won()
                    else:
                       self.player1won()
                elif int(scorecount) >= 10:
                    self.player1won()
                else:
                    self.reset()
            else:
                self.currentturn.setText("Player 1")
                self.reset()

    # PLAYER 1 WINS
    def player1won(self):
        guessBox1 = QMessageBox()
        guessBox1.setText("GAME FINISHED"
                          "\nPlayer 1 WON!")
        guessBox1.setStyleSheet("background-color: #A3C1DA; color: black")
        guessBox1.exec()
        self.restart()
    # PLAYER 2 WINS
    def player2won(self):
        guessBox2 = QMessageBox()
        guessBox2.setText("GAME FINISHED"
                          "\nPlayer 2 WON!")
        guessBox2.setStyleSheet("background-color: #A3C1DA; color: black")
        guessBox2.exec()
        self.restart()

    # starting the game
    def startGame(self):
        optionsLayout = QVBoxLayout()
        self.setLayout(optionsLayout)
        dialog = QMessageBox()
        dialog.setText("Welcome to Pictionary!")
        dialog.setInformativeText("Please select mode")
        # Add some checkboxes to the layout
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        buttonY = dialog.button(QMessageBox.StandardButton.No )
        buttonY.setText("Easy mode")
        buttonN = dialog.button(QMessageBox.StandardButton.Yes)
        buttonN.setText("Hard mode")
        image =QImage("./icons/paint-brush.png")
        pixmap = QPixmap(image)
        dialog.setIconPixmap(pixmap)
        dialog.setStyleSheet("background-color: #A3C1DA; color: black")
        ret = dialog.exec()
        if ret == QMessageBox.StandardButton.Yes:
            self.getList("hard")
            self.mode.setText("Hard mode")
            print("hard")
        else:
            self.getList("easy")
            self.mode.setText("Easy mode")
            print("easy")
        self.number.setText("1")
        self.rules()
        self.reset()
    # HELP
    def help(self):
        information = QMessageBox()
        image2 = QImage("./icons/question.png")
        pixmap2 = QPixmap(image2)
        information.setText("Help and shortcuts!")
        information.setInformativeText("-Ctrl + Q - Quit game!\n"
                                       "\n- Ctrl + S - Save picture! \n"
                                        "\n- Ctrl + O - Open folder!\n"
                                       "\n- Space- Stop turn and see if quess is correct!\n"
                                       "\n- Points: Award 1 point to guesser and 2 points to drawer on"
                                       "correct guess \n"
                                       "\n - S - Skip turn!")
        information.setIconPixmap(pixmap2)
        information.setStyleSheet("background-color: #A3C1DA; color: black")
        information.exec()

    #RULES OF THE GAME
    def rules(self):
        information = QMessageBox()
        image2 = QImage("./icons/rules.png")
        pixmap2 = QPixmap(image2)
        information.setText("Rules of Pictionary Game!")
        information.setInformativeText("-Player who get 10 points faster win the game!\n"
                                       "\n- Points: Award 1 point to guesser and 2 points to drawer on"
                                       "correct guess \n"
                                       "\n- You have exactly 60 second for draw ang guess.\n"
                                       "\n- If you guess correctly before times run out press space.\n"
                                       "Your score will be automatically added.\n"
                                       "\n - If you wish to skip the turn press tu button 'Skip turn' "
                                       "or just press 's'")
        information.setIconPixmap(pixmap2)
        information.setStyleSheet("background-color: #A3C1DA; color: black")
        information.exec()

    def reset(self):
        # RESET FOR after each round
        self.clear()
        self.brushSize = 3
        self.currentC.setStyleSheet("background: black;"
                                     "border : none;")
        self.brushColor = Qt.GlobalColor.black
        self.currentWord = self.getWord()
        self.gettheWord()

    def restart(self):
        # RESTART GAME From Beginning
        self.currentturn.setText("Player 1")
        self.player1.setText("Player 1:    " + "0")
        self.player2.setText("Player 2:    " + "0")
        self.score1.setText("0")
        self.score2.setText("0")
        self.currentC.setStyleSheet("background: black;"
                                     "border : none;")
        # hiding the button
        self.button.show()
        self.skipBut.hide()
        self.number.setText("0")
        # RESET FOR A NEW PLAYER
        self.label.setText("60")
        self.clear()
        self.image = QPixmap("./icons/pictionary.jpeg")
    # getting the word with message box
    def gettheWord(self):
        guessBox = QMessageBox()
        guessBox.setText(self.currentturn.text() + " See your word!")
        guessBox.setInformativeText("Don't let anyone to see! Press Details")
        guessBox.setDetailedText(self.currentWord);
        guessBox.setStyleSheet("background-color: #A3C1DA; color: black")
        guessBox.exec()

    def timeUp(self):
        #WHEN TIME IS UP ASK IF THEY QUESSED OR NOT
        self.statusBar().showMessage(" ")
        guessBox = QMessageBox()
        guessBox.setStyleSheet("background-color: #A3C1DA; color: black")
        guessBox.setText("Last quess! Did you guessed correctly?")
        guessBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        ret = guessBox.exec()
        #RETURN VALUE OF THE QUESTION
        return ret

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):
        self.currentC.setStyleSheet("background: black;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.black

    def red(self):
        self.currentC.setStyleSheet("background: red;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.red

    def green(self):
        self.currentC.setStyleSheet("background: green;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.darkGreen

    def lime(self):
         self.currentC.setStyleSheet("background: lime;"
                                    "border : none")
         self.brushColor = Qt.GlobalColor.green

    def white(self):
        self.currentC.setStyleSheet("background: white;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.white

    def orange(self):
        self.currentC.setStyleSheet("background: #ff9900;"
                                    "border : none")
        self.brushColor = QColor("#ff9900")

    def purple(self):
        self.currentC.setStyleSheet("background: darkMagenta;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.darkMagenta

    def pink(self):
        self.currentC.setStyleSheet("background: magenta;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.magenta

    def yellow(self):
        self.currentC.setStyleSheet("background: yellow;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.yellow

    def blue(self):
        self.currentC.setStyleSheet("background: blue;"
                                    "border : none")
        self.brushColor = Qt.GlobalColor.blue

    def morec(self):
        # opening color dialog
        color = QColorDialog.getColor()
        # creating label to display the color
        label = QLabel(self)
        # setting geometry to the label
        label.setGeometry(100, 100, 200, 60)
        # making label multi line
        label.setWordWrap(True)
        # setting stylesheet of the label
        label.setStyleSheet("QLabel"
                            "{"
                            "border : 5px solid black;"
                            "}")
        # setting text to the label
        label.setText(str(color))
        # setting graphic effect to the label
        graphic = QGraphicsColorizeEffect(self)
        # setting color to the graphic
        graphic.setColor(color)
        # setting graphic to the label
        label.setGraphicsEffect(graphic)
        if color.isValid():
            print(color.name())
            self._color = color.name()
            self.currentC.setStyleSheet("border : none;"
                                        "background: %s;" % self._color)
            # SETTING UP BRUSH ACCORDING TO COLOR CHOSEN
            self.brushColor = QColor(color.name())


    #Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        print(randomWord)
        return randomWord

    #read word list from file
    def getList(self, mode):
        with open(mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                #print(row)
                self.wordList = row
                line_count += 1
            #print(f'Processed {line_count} lines.')



    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        self.statusBar().showMessage('Ready', 5000)
        # ALLOWING USER TO OPEN ONLY IMAGES FILES
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "Images(*.png *.gif *.webp *.jpg *.jpeg)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QMessageBox { background-color: #A3C1DA;}")
    app.setWindowIcon(
        QIcon("./icons/paint-brush.png"))
    QMessageBox().setStyleSheet("background-color: #A3C1DA; color: black")
    window = PictionaryGame()
    window.show()
    app.exec()  # start the event loop running
