import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        super().__init__()
        # 전체 폼 박스
        self.formbox = QHBoxLayout()
        self.setLayout(self.formbox)

        # 좌, 우 레이아웃박스
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()

        self.formbox.addLayout(self.left)
        self.formbox.setStretchFactor(self.left, 0)
        self.formbox.addLayout(self.right)
        self.formbox.setStretchFactor(self.right, 0)

        # 그룹박스1a 생성 및 좌 레이아웃 배치
        gb1a = QGroupBox('groups')
        self.left.addWidget(gb1a)
        # 그룹박스1a 에서 사용할 레이아웃
        box1a = QVBoxLayout()


        # 그룹박스1b 생성 및 좌 레이아웃 배치
        gb1b = QGroupBox('command')
        self.left.addWidget(gb1b)
        box1b = QVBoxLayout()


        # 그룹박스2a 생성 및 좌 레이아웃 배치
        gb2a = QGroupBox('space')
        self.right.addWidget(gb2a)
        box2a = QHBoxLayout()

        # 그룹박스2b 생성 및 좌 레이아웃 배치
        gb2b = QGroupBox('functions')
        self.right.addWidget(gb2b)
        box2b = QHBoxLayout()

        self.rbtn1a1=QRadioButton("Group 1", self)
        box1a.addWidget(self.rbtn1a1)
        self.rbtn1a2 = QRadioButton("Group 2", self)
        box1a.addWidget(self.rbtn1a2)
        self.rbtn1a3 = QRadioButton("Group 3", self)
        box1a.addWidget(self.rbtn1a3)

        self.btn1b1=QPushButton("Record",self)
        box1b.addWidget(self.btn1b1)
        self.btn1b2 = QPushButton("Delete", self)
        box1b.addWidget(self.btn1b2)
        self.btn1b3 = QPushButton("Test", self)
        box1b.addWidget(self.btn1b3)


        #grid setting
        grid2a1=QGridLayout()
        gb2a.setLayout(grid2a1)

        self.btn2a00 = QPushButton("P1", self)
        grid2a1.addWidget(self.btn2a00,0,0)
        self.btn2a01 = QPushButton("P2", self)
        grid2a1.addWidget(self.btn2a01, 0, 1)
        self.btn2a02 = QPushButton("P3", self)
        grid2a1.addWidget(self.btn2a02, 0, 2)
        self.btn2a03 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a03, 0, 3)
        self.btn2a04 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a04, 0, 4)

        self.btn2a10 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a10,1,0)
        self.btn2a11 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a11, 1, 1)
        self.btn2a12 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a12, 1, 2)
        self.btn2a13 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a13, 1, 3)
        self.btn2a14 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a14, 1, 4)

        self.btn2a20 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a20,2,0)
        self.btn2a21 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a21, 2, 1)
        self.btn2a22 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a22, 2, 2)
        self.btn2a23 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a23, 2, 3)
        self.btn2a24 = QPushButton("empty", self)
        grid2a1.addWidget(self.btn2a24, 2, 4)



        #group box setting
        gb1a.setLayout(box1a)
        gb1b.setLayout(box1b)
        gb2a.setLayout(box2a)
        gb2b.setLayout(box2b)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())