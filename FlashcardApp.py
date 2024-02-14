import sys
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtCharts import *
from PySide6.QtWidgets import QWidget
from functools import partial


class FlashcardApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.welcomeButton = QPushButton("Click to make flashcards")
    self.title = QLabel("Welcome to flashcard app")
    self.activeDeckName = "None"

    self.mainWidget = QWidget(self)
    self.setCentralWidget(self.mainWidget)

    mainLayout = QHBoxLayout(self.mainWidget)
    # stores the head of each deck list
    self.deckContainer = {}
    

    sidebarWidget = QWidget(self)
    self.sidebarLayout = QVBoxLayout(sidebarWidget)
    sidebarWidget.setFixedWidth(self.width() // 6)
    sidebarWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    self.sidebarLayout.setContentsMargins(0, 0, 0, 0)
    self.sidebarLayout.setSpacing(0)
    self.sidebarLayout.setAlignment(Qt.AlignTop)

    #button1 = QPushButton("Deck 1", self)
    ##button1.clicked.connect(partial(self.setActiveDeck, 1))
    #button2 = QPushButton("Deck 2", self)
    #button2.clicked.connect(partial(self.setActiveDeck, 2))
    #button3 = QPushButton("Deck 3", self)
    #button3.clicked.connect(partial(self.setActiveDeck, 3))
    addDeck = QPushButton("Create Deck", self)
    
    

    sidebarWidget.setLayout(self.sidebarLayout)
    self.sidebarLayout.setAlignment(Qt.AlignTop)

    self.sidebarLayout.addWidget(addDeck)
    

    self.sidebarCount = self.sidebarLayout.count()
    addDeck.clicked.connect(partial(self.createPopup, NameDeckPopup))
    

    mainLayout.addWidget(sidebarWidget)
    
    self.studyButton = QPushButton("Click to study active deck")
    self.studyButton.clicked.connect(partial(self.openDeck, self.activeDeckName))
    self.studyButton.setMaximumSize(500, 200)
    # button for adding card to deck
    self.addCard = QPushButton("Click to add card to deck.")
    self.addCard.clicked.connect(partial(self.createPopup, AddCardPopup))
    
    mainLayout.addWidget(self.studyButton)
    mainLayout.addWidget(self.addCard)

    self.activeDeckLabel = QLabel("Active Deck: " + self.activeDeckName)
    mainLayout.addWidget(self.activeDeckLabel)
    
    self.setWindowTitle("Flashcard App")
    self.setGeometry(500, 500, 1080, 720)
    
  
  def setActiveDeck(self, deckName):
    print(deckName)
    self.activeDeckName = deckName
    self.activeDeckLabel.setText("Active Deck: " + self.activeDeckName)
    self.activeDeckLabel.update()


  def openDeck(self, deckName):
    print("Deck", self.activeDeckName)
  
  def createPopup(self, PopupClass):
    popup = PopupClass(self)
    popup.show()
  
  def createDeck(self, deckName):
    # creates the new button on the sidebar
    newDeckButton = QPushButton(deckName, self)
    self.sidebarCount+=1
    # connect the button to the set active deck function
    newDeckButton.clicked.connect(partial(self.setActiveDeck, deckName))
    # add the widget to the sidebar
    self.sidebarLayout.addWidget(newDeckButton, alignment=Qt.AlignTop)
    # create the new deck
    newDeck = Deck()
    # put it in deck container
    self.deckContainer[deckName] = newDeck
    print(deckName)

class AddCardPopup(QMainWindow):
  def __init__(self, parent=None):
    super(AddCardPopup, self).__init__(parent)
    # set up
    self.main = QWidget(self)
    self.setCentralWidget(self.main)
    # window title
    self.setWindowTitle("Add Card")
    # title for the text field
    frontLabel = QLabel("Front:")
    # line edit
    self.frontEdit = QLineEdit()
    self.frontEdit.setMaxLength(200)
    
    # title for the text field
    backLabel = QLabel("Back:")
    # line edit
    self.backEdit = QLineEdit()
    self.backEdit.setMaxLength(200)

    # confirm button
    okay = QPushButton("Okay")
    okay.clicked.connect(self.setDeckName)
    # create main layout
    mainLayout = QVBoxLayout(self)
    
    # idk what this is for
    parent = self.parentWidget()

    # set geometry and move to middle
    self.setGeometry(0, 0, 600, 300)
    self.move(parent.geometry().center() - self.rect().center())
    
    # layout for the inputs so they are bundled
    frontLayout = QHBoxLayout(self)
    # make the input widget
    frontWidget = QWidget(self)
    # add the edit and button to layout
    frontLayout.addWidget(frontLabel)
    frontLayout.addWidget(self.frontEdit)

    frontWidget.setLayout(frontLayout)
    
    # layout for the inputs so they are bundled
    backLayout = QHBoxLayout(self)
    # make the input widget
    backWidget = QWidget(self)
    # add the edit and button to layout
    backLayout.addWidget(backLabel)
    backLayout.addWidget(self.backEdit)

    backWidget.setLayout(backLayout)
    # set the main layout
    mainLayout.addWidget(frontWidget, alignment=Qt.AlignBottom)
    mainLayout.addWidget(backWidget, alignment=Qt.AlignTop)
    mainLayout.addWidget(okay, alignment=Qt.AlignTop)
    self.main.setLayout(mainLayout)

  def setDeckName (self):
    # gets the text in the input field
    deckName = self.edit.text()
    # call createDeck
    window.createDeck(deckName)
    # close window
    self.close()

class NameDeckPopup(QMainWindow):
  def __init__(self, parent=None):
    super(NameDeckPopup, self).__init__(parent)
    # set up
    self.main = QWidget(self)
    self.setCentralWidget(self.main)
    # window title
    self.setWindowTitle("Deck Name")
    # title for the popup
    title = QLabel("What would you like to name this deck?")
    # line edit
    self.edit = QLineEdit()
    self.edit.setMaxLength(20)
    
    # confirm button
    okay = QPushButton("Okay")
    okay.clicked.connect(self.setDeckName)
    # create main layout
    layout = QVBoxLayout(self)
    
    # idk what this is for
    parent = self.parentWidget()

    # set geometry and move to middle
    self.setGeometry(0, 0, 300, 100)
    self.move(parent.geometry().center() - self.rect().center())
    
    # layout for the inputs so they are bundled
    inputLayout = QHBoxLayout(self)
    # make the input widget
    inputWidget = QWidget(self)
    # add the edit and button to layout
    inputLayout.addWidget(self.edit, alignment=Qt.AlignRight)
    inputLayout.addWidget(okay, alignment=Qt.AlignLeft)
    inputWidget.setLayout(inputLayout)
    # set the main layout
    layout.addWidget(title, alignment=Qt.AlignCenter)
    layout.addWidget(inputWidget, alignment=Qt.AlignCenter)
    self.main.setLayout(layout)

  def setDeckName (self):
    # gets the text in the input field
    deckName = self.edit.text()
    # call createDeck
    window.createDeck(deckName)
    # close window
    self.close()

class Deck:
  deckID = None
  deckName = None
  def __init__(self):
    self.head = None
    self.id = None

  def addCard(self, question, answer):
    newCard = FlashCard(question, answer)
    newCard.nextCard = self.head
    self.head = newCard

  def __repr__(self):
    cards = []
    current = self.head

    while current:
      if current is self.head:
        cards.append("[Head: %s]" % current.question)
      elif current.nextCard is None:
        cards.append("[Tail: %s]" % current.question)
      else:
        cards.append("[%s]" % current.question)

      current = current.nextCard
    return '->'.join(cards)


class FlashCard:
  question = None
  answer = None
  nextCard = None
  def __init__(self, question, answer):
    self.question = question
    self.answer = answer
  
  
  
class SaveFile:
  def __init__(self):
    print("test")

    

class LoadFile:
  def __init__(self):
    print("test")



if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = FlashcardApp()
  window.show()
  sys.exit(app.exec())


