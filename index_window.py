import sys
import subprocess
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IndexWindow(object):
    def setupUi(self, Dialog, main_window):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 320)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.open_tab = QtWidgets.QWidget()
        self.open_tab.setObjectName("open_tab")
        self.open_path_label = QtWidgets.QLabel(self.open_tab)
        self.open_path_label.setGeometry(QtCore.QRect(10, 10, 331, 31))
        self.open_path_label.setObjectName("open_path_label")
        self.open_path_line = QtWidgets.QLineEdit(self.open_tab)
        self.open_path_line.setGeometry(QtCore.QRect(10, 60, 331, 41))
        self.open_path_line.setObjectName("open_path_line")
        self.open_path_button = QtWidgets.QPushButton(self.open_tab)
        self.open_path_button.setGeometry(QtCore.QRect(230, 120, 111, 31))
        self.open_path_button.setObjectName("open_path_button")
        self.open_button = QtWidgets.QPushButton(self.open_tab)
        self.open_button.setGeometry(QtCore.QRect(230, 230, 111, 31))
        self.open_button.setObjectName("open_button")
        self.tabWidget.addTab(self.open_tab, "")
        self.init_tab = QtWidgets.QWidget()
        self.init_tab.setObjectName("init_tab")
        self.init_path_label = QtWidgets.QLabel(self.init_tab)
        self.init_path_label.setGeometry(QtCore.QRect(10, 10, 331, 31))
        self.init_path_label.setObjectName("init_path_label")
        self.init_path_line = QtWidgets.QLineEdit(self.init_tab)
        self.init_path_line.setGeometry(QtCore.QRect(10, 60, 331, 41))
        self.init_path_line.setObjectName("init_path_line")
        self.init_path_button = QtWidgets.QPushButton(self.init_tab)
        self.init_path_button.setGeometry(QtCore.QRect(230, 120, 111, 31))
        self.init_path_button.setObjectName("init_path_button")
        self.init_button = QtWidgets.QPushButton(self.init_tab)
        self.init_button.setGeometry(QtCore.QRect(230, 230, 111, 31))
        self.init_button.setObjectName("init_button")
        self.tabWidget.addTab(self.init_tab, "")
        self.error_label = QtWidgets.QLabel(Dialog)
        self.error_label.setGeometry(QtCore.QRect(14, 290, 381, 31))
        self.error_label.setObjectName("error_label")

        self.init_path_button.clicked.connect(self.folder)
        self.open_path_button.clicked.connect(self.folder)
        self.open_button.clicked.connect(self.open_repo)
        self.init_button.clicked.connect(self.init_repo)

        self.main_window = main_window

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_path_label.setText(_translate("Dialog", "select dir to open your repo"))
        self.open_path_button.setText(_translate("Dialog", "open folder"))
        self.open_button.setText(_translate("Dialog", "Open"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.open_tab), _translate("Dialog", "       OPEN      "))
        self.init_path_label.setText(_translate("Dialog", "select dir to init your repo"))
        self.init_path_button.setText(_translate("Dialog", "open folder"))
        self.init_button.setText(_translate("Dialog", "Init"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.init_tab), _translate("Dialog", "       INIT      "))
        self.error_label.setText(_translate("Dialog", ""))
    
    def folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'aboba')
        if self.sender() == self.open_path_button:
            self.open_path_line.setText(folder_path)
        else:
            self.init_path_line.setText(folder_path)
    
    def open_repo(self):
        #print(f'cd {self.open_path_line.text()}')
        os.chdir(self.open_path_line.text())
        
        # res2 = subprocess.check_output('git status').decode('cp866').split('\n')
        res2 = subprocess.run(['git', 'status'])

        #print(res2)
        if res2.returncode == 0:
            print('ABOBA')
            self.main_window.repo_path = self.open_path_line.text()
            self.go_to_main()
        #if 'not a git repository' not in res2:
            #print('ABOBA')
        
    def init_repo(self):
        os.chdir(self.init_path_line.text())
        res2 = subprocess.run(['git', 'status'])
        #  print(res2.returncode)
        if res2.returncode == 128:
            print('ABOBA22')
            self.main_window.repo_path = self.init_path_line.text()
            self.go_to_main
    
    def go_to_main(self):
        self.main_window.rerender()
        self.main_window.show()
        self.close()
        

class IndexWindow(QtWidgets.QDialog, Ui_IndexWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self, main_window)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = IndexWindow()
    ex.show()
    sys.exit(app.exec_())

