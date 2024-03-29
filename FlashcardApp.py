import sys
from random import shuffle
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *
from PySide6.QtWidgets import QWidget
from functools import partial
from PySide6.QtGui import *


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

    addDeck = QPushButton("Create Deck", self)
    
    

    sidebarWidget.setLayout(self.sidebarLayout)
    self.sidebarLayout.setAlignment(Qt.AlignTop)

    self.sidebarLayout.addWidget(addDeck)
    

    self.sidebarCount = self.sidebarLayout.count()
    addDeck.clicked.connect(partial(self.createPopup, NameDeckPopup))
    

    mainLayout.addWidget(sidebarWidget)
    
    self.studyButton = QPushButton("Click to study active deck")
    self.studyButton.clicked.connect(partial(self.createPopup, StudyDeckPopup))
    self.studyButton.setMaximumSize(500, 200)
    # button for adding card to deck
    self.addCard = QPushButton("Click to add card to deck.")
    self.addCard.clicked.connect(partial(self.createPopup, AddCardPopup))
    self.removeCard = QPushButton("Click to remove card")
    self.removeCard.clicked.connect(partial(self.createPopup, EditDeckPopup))
    
    mainLayout.addWidget(self.studyButton)
    cardWidgit = QWidget()
    cardLayout = QVBoxLayout()
    cardWidgit.setLayout(cardLayout)
    cardLayout.addWidget(self.addCard)
    cardLayout.addWidget(self.removeCard)
    mainLayout.addWidget(cardWidgit)

    self.activeDeckLabel = QLabel("Active Deck: " + self.activeDeckName)
    mainLayout.addWidget(self.activeDeckLabel)
    
    self.setWindowTitle("Flashcard App")
    
    self.show()

  def setActiveDeck(self, deckName):
    self.activeDeckName = deckName
    self.activeDeckLabel.setText("Active Deck: " + self.activeDeckName)
    self.activeDeckLabel.update()

  
  def createPopup(self, PopupClass):
    popup = PopupClass(self)
    popup.show()

  
  def createDeck(self, deckName):
    # creates the new button on the sidebar
    newDeckButton = QPushButton(deckName, self)
    self.sidebarCount+=1
    # connect the button to the set active deck function
    newDeckButton.clicked.connect(partial(self.setActiveDeck, deckName))
    newDeckButton.customContextMenuRequested.connect(self.editDeckButton)
    # add the widget to the sidebar
    self.sidebarLayout.addWidget(newDeckButton, alignment=Qt.AlignTop)
    # create the new deck
    newDeck = Deck()
    # put it in deck container
    self.deckContainer[deckName] = newDeck
    self.setActiveDeck(deckName)

  def addToDeck(self, front, back):
    activeDeck = self.deckContainer[self.activeDeckName]
    activeDeck.addCard(front, back)
  
  def editDeckButton(self):
    print("test")

class StudyDeckPopup(QMainWindow):
  
  def __init__(self, parent=None):
    super(StudyDeckPopup, self).__init__(parent)
    

    # set up
    
    self.main = QWidget(self)
    self.setCentralWidget(self.main)
    # window title
    self.setWindowTitle("Study Deck")

    self.activeDeckName = window.activeDeckName
    
    self.activeDeck = window.deckContainer[self.activeDeckName].getCards()
    self.ogDeck = self.activeDeck.copy()
    shuffle(self.activeDeck)
    
    self.cardCounter = 0
    self.activeCard = self.activeDeck[self.cardCounter]
    # front of card text
    self.frontLabel = QLabel(self.activeCard["front"])
    
    # back of card text
    self.backLabel = QLabel(self.activeCard["back"])

    # next card buttoon
    nextCardButon = QPushButton("Next Card")
    nextCardButon.clicked.connect(self.nextCard)

    # show card button
    self.showButton = QPushButton("Show")
    self.showButton.clicked.connect(self.showBack)
    # create main layout
    self.mainLayout = QVBoxLayout(self)
    
    # idk what this is for
    parent = self.parentWidget()

    # set geometry and move to middle
    self.setGeometry(0, 0, 600, 300)
    self.move(parent.geometry().center() - self.rect().center())
    
    # layout for the inputs so they are bundled
    frontLayout = QHBoxLayout(self)
    # make the input widget
    self.frontWidget = QWidget(self)
    # add the edit and button to layout
    frontLayout.addWidget(self.frontLabel)

    self.frontWidget.setLayout(frontLayout)
    
    # layout for the inputs so they are bundled
    backLayout = QHBoxLayout(self)
    # make the input widget
    self.backWidget = QWidget(self)
    # add the edit and button to layout
    backLayout.addWidget(self.backLabel)
    backLayout.addWidget(nextCardButon)

    self.backWidget.setLayout(backLayout)
    self.backWidget.hide()

    self.endWidget = QWidget();
    endLayout = QVBoxLayout()

    endOfDeckLabel = QLabel("You have reached the end of this deck.")
    endLayout.addWidget(endOfDeckLabel)
    

    studyAgainButton = QPushButton("Study Again")
    studyAgainButton.clicked.connect(self.studyAgainReset)
    endLayout.addWidget(studyAgainButton)
    

    closeButton = QPushButton("Close")
    closeButton.clicked.connect(self.close)
    endLayout.addWidget(closeButton)
    

    
    
    self.endWidget.setLayout(endLayout)
    self.endWidget.hide()

    # set the main layout
    self.mainLayout.addWidget(self.frontWidget, alignment=Qt.AlignBottom)
    self.mainLayout.addWidget(self.showButton, alignment=Qt.AlignTop)
    self.mainLayout.addWidget(self.backWidget)
    
    self.mainLayout.addWidget(self.endWidget)
    self.main.setLayout(self.mainLayout)
    #self.resetCards()

    print(self.cardCounter)
    print(self.activeCard)
  
  def showBack(self):
    """Shows the backside of the card."""
    self.frontWidget.hide()
    self.showButton.hide()
    self.mainLayout.addWidget(self.backWidget, alignment=Qt.AlignBottom)
    self.backWidget.show()

  def nextCard(self):
    self.cardCounter += 1
    if self.cardCounter >= len(self.activeDeck):
      self.endOfDeck()
      return None

    # set the active card to the next card in the deck
    self.activeCard = self.activeDeck[self.cardCounter]
    
    # change labels
    self.frontLabel.setText(self.activeCard["front"])
    self.backLabel.setText(self.activeCard["back"])
    # show and hide labels
    self.backWidget.hide()
    self.frontWidget.show()
    self.showButton.show()

  def endOfDeck(self):
    """Shows that the user has reached the end of the deck."""
    self.backWidget.hide()
    self.endWidget.show()

  def studyAgainReset(self):
    """Resets the study window back to the start and randomizes the cards."""
    shuffle(self.activeDeck)
    self.cardCounter = 0
    self.endWidget.hide()
    self.frontWidget.show()
    self.showButton.show()

  def resetCards(self):
    for card in self.activeDeck.getCards():
      card["active"] = False
    print(self.activeDeck.getCards())

class EditDeckPopup(QMainWindow):
  def __init__(self, parent=None):
    super(EditDeckPopup, self).__init__(parent)
    # set up
    self.main = QWidget(self)
    self.setCentralWidget(self.main)
    

    self.activeDeckName = window.activeDeckName
    self.activeDeck = window.deckContainer[self.activeDeckName].getCards()

    # window title
    self.setWindowTitle("Edit " + self.activeDeckName)

    deckLabel = QLabel("Active Deck: " + self.activeDeckName)

    self.searchBar = QLineEdit()
    self.searchBar.setPlaceholderText("Search Cards...")
    self.searchBar.textChanged.connect(self.search)
    

    self.mainTable = QTableView()
    self.model = QStandardItemModel(len(self.activeDeck), 2)

    self.initializeTable()

    self.proxyModel = QSortFilterProxyModel(self.mainTable)
    self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
    self.proxyModel.filterAcceptsColumn(0)
    self.proxyModel.setSourceModel(self.model)
    self.mainTable.setModel(self.proxyModel)

    #self.mainTable.setRowCount(len(self.activeDeck))
    #self.mainTable.setColumnCount(3)
    #self.mainTable.setHorizontalHeaderLabels(["Front", "Back", "Delete Card"])
    
    closeButton = QPushButton("Close")
    closeButton.clicked.connect(self.close)

    # table widget
    

    layout = QVBoxLayout()
    layout.addWidget(deckLabel)
    layout.addWidget(self.searchBar)
    layout.addWidget(self.mainTable)
    layout.addWidget(closeButton)

    self.main.setLayout(layout)
    
    #self.mainTable.itemChanged.connect(self.confirm)

    self.mainTable.show()


    
    
    
    
  def initializeTable(self):
    """Fills information from the current deck."""

    


    count = 0
    for card in self.activeDeck:
      
      front = QStandardItem(card["front"])
      back = QStandardItem(card["back"])
      #delete = QPushButton("Delete")
      #delete.clicked.connect(partial(window.deckContainer[self.activeDeckName].removeCard, count))
      #delete.clicked.connect(partial(self.removeCard, count))
      
      if count % 2 == 1:
        front.setBackground(QColor(225, 225, 225))
        back.setBackground(QColor(225, 225, 225))
 
      self.model.setItem(count, 0, front)
      self.model.setItem(count, 1, back)
      #self.mainTable.setCellWidget(count, 2, delete)

      count += 1;

    

    #width = self.mainTable.horizontalHeader().length() + self.mainTable.verticalHeader().length() + 5
    #height = self.mainTable.verticalHeader().length() + self.mainTable.horizontalHeader().height() + 5
    #self.resize(width, height)


    #self.mainTable.resizeColumnsToContents()
    #self.mainTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    #self.mainTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    #geometry = self.screen().geometry()
    #self.setMaximumWidth(geometry.width())
    
    

    

  def confirm(self, item):
    """Saves the changes made to the cards."""
    face = "front" if item.column() == 0 else "back"

    self.activeDeck[item.row()][face] = item.text()

  def removeCard(self, index):
    """Removes card from the table."""
    self.mainTable.removeRow(index)
    
  def search(self, string):
    self.proxyModel.setFilterFixedString(string)
    
        
  

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
    okay.clicked.connect(self.confirmCard)
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

  def confirmCard (self):
    # gets the text in the input field
    front = self.frontEdit.text()
    back = self.backEdit.text()
    # call createDeck
    window.addToDeck(front, back)
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
  deckName = None
  cards = None
  def __init__(self):
    self.cards = []

  def getCards(self):
    return self.cards

  def addCard(self, front, back):
    self.cards.append({"front": front, "back": back, "active": False})

  def removeCard(self, index):
    self.cards.pop(index)


class FlashCard:
  front = None
  back = None
  def __init__(self, front, back):
    self.front = front
    self.back = back
  

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = FlashcardApp()
  window.show()
  sys.exit(app.exec())


