import sys

from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
 
class App(QWidget): 
    def __init__(self):
        super().__init__()
        self.title = 'tiger'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 280
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        QToolTip.setFont(QFont('SansSerif',10))
        self.setToolTip('test tooltip')
		
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)  

        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
