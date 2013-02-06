import sys
from PySide.QtGui import *
from PySide.QtCore import *
from wordMethods.haiku import *

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
	
		editMenu = menubar.addMenu('&Edit')
		validHaikuAction = QAction('Validate Haiku',self)
		validHaikuAction.triggered.connect(self.haikuValidate)
		
		editMenu.addAction(validHaikuAction)
		
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
		
	def haikuValidate(self):
		cWidget = self.centralWidget()
		#print isHaiku(cWidget.textEdit.toPlainText())
		text = cWidget.textEdit.toPlainText()
		print isHaiku(text)
	
class MainContent(QWidget):
    
	def __init__(self):
		super(MainContent, self).__init__()
        	self.initUI()
        
    	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)   
        	
		self.textLabel = QLabel("Data:")
		self.textEdit = QTextEdit()
		self.comboBox = QComboBox()
		
		self.comboBox.addItem("Haiku")
		self.comboBox.addItem("Limerick")
		

		grid.addWidget(self.textLabel,0,0)
		grid.addWidget(self.textEdit,1,0)
		grid.addWidget(self.comboBox,0,1)

def main():
    	app = QApplication(sys.argv)
    	main = Main()
   	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
