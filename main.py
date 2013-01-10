import sys
from PySide.QtGui import *
from PySide.QtCore import *
from wordMethods.sounds import Rhymer
from wordMethods.sounds import SyllableCounter

class Main(QMainWindow):
	def __init__(self):
		super(Main,self).__init__()
		self.initUI()
	
	def initUI(self):
		mainContent = MainContent()
		self.createMenu()
		self.setWindowTitle('Poetry in motion')
		self.resize(300,200)
		self.setCentralWidget(mainContent)
		self.show()	
	
	def createMenu(self):
		menubar = self.menuBar()
		
		fileMenu = menubar.addMenu('&File')
		openAction = QAction('&Open',self)
		openAction.triggered.connect(self.openFile)
		exitAction = QAction('E&xit',self)
		exitAction.triggered.connect(self.close)
		
		fileMenu.addAction(openAction)
		fileMenu.addAction(exitAction)
	
	def openFile(self):
		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setViewMode(QFileDialog.Detail)
		
		if dialog.exec_():
			fileNames = dialog.selectedFiles()
		
		cWidget = self.centralWidget()
		someFile = open(fileNames[0],'r')
		
		for line in someFile:
			cWidget.textEdit.append(line)
		
class MainContent(QWidget):
    
	def __init__(self):
		super(MainContent, self).__init__()
        	self.initUI()
        
    	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)   
        	
		self.textLabel = QLabel("Data")
		self.textEdit = QTextEdit()
		
		grid.addWidget(self.textLabel)
		grid.addWidget(self.textEdit)
		
def main():
    	app = QApplication(sys.argv)
    	main = Main()
   	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
