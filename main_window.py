import sys
import os

import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_MainWindow(object):
    def setupUi(self, MainWindow, commit_dialog, repo_path):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 787)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_list.setGeometry(QtCore.QRect(10, 30, 121, 721))
        self.file_list.setObjectName("file_list")
        self.file_list_btn = QtWidgets.QPushButton(self.centralwidget)
        self.file_list_btn.setGeometry(QtCore.QRect(10, -1, 51, 31))
        self.file_list_btn.setObjectName('file_list_btn')
        self.commit_info = QtWidgets.QTextEdit(self.centralwidget)
        self.commit_info.setGeometry(QtCore.QRect(900, 150, 201, 201))
        self.commit_info.setObjectName("commit_info")
        self.commit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.commit_btn.setGeometry(QtCore.QRect(900, 690, 201, 51))
        self.commit_btn.setObjectName("commit_btn")
        self.checkout_btn = QtWidgets.QPushButton(self.centralwidget)
        self.checkout_btn.setGeometry(QtCore.QRect(1000, 100, 101, 31))
        self.checkout_btn.setObjectName("checkout_btn")
        self.commit_tree = QtWidgets.QTextEdit(self.centralwidget)
        self.commit_tree.setGeometry(QtCore.QRect(150, 30, 721, 671))
        self.commit_tree.setObjectName("commit_info_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(900, 50, 201, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.get_info_btn = QtWidgets.QPushButton(self.centralwidget)
        self.get_info_btn.setGeometry(QtCore.QRect(900, 100, 81, 31))
        self.get_info_btn.setObjectName("get_info_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1130, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #  self.file_list.doubleClicked.connect(self.essene_open)

        self.commit_dialog = commit_dialog
        
        self.repo_path = repo_path
        self.path_now = repo_path

        self.commit_btn.clicked.connect(self.create_commit_dialog)
        self.get_info_btn.clicked.connect(self.get_info_on_commit)
        self.checkout_btn.clicked.connect(self.checkout_dialog)
        self.file_list_btn.clicked.connect(self.dot_dot_slash)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.commit_btn.setText(_translate("MainWindow", "Commit"))
        self.checkout_btn.setText(_translate("MainWindow", "Checkout"))
        self.get_info_btn.setText(_translate("MainWindow", "Get info"))
        self.file_list_btn.setText(_translate("MainWindow", "<-"))
    
    def checkout_dialog(self):
        tonq = QtWidgets.QMessageBox()
        tonq.setText('Do you really want checkout to this commit?')
        tonq.setIcon(QtWidgets.QMessageBox.Warning)
        tonq.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        tonq.buttonClicked.connect(self.checkout_btn_click)
        tonq.exec_()
        #  self.checkout_dialog.exec_()
    
    def create_commit_dialog(self):
        self.commit_dialog.repo_path = self.repo_path
        self.commit_dialog.set_branches()
        self.commit_dialog.show()
    
    def checkout_btn_click(self, btn):
        if btn.text() == 'OK':
            # некоторая логика, которая в cmd даёт команду на checkout
            os.chdir(self.repo_path)
            hash = self.lineEdit.text()
            res = subprocess.run(['git', 'checkout', hash])

            return None

    def get_info_on_commit(self):
        hash = self.lineEdit.text()
        os.chdir(self.repo_path)
        info = subprocess.check_output(f'git log -n 1 {hash}').decode('utf-8')
        self.commit_info.setText(info)
    
    def get_dir_content(self, dir_path):
        os.chdir(dir_path)
        cont = subprocess.check_output('dir').decode('utf-8').split('\n')
        for i in cont:
            if dir_path in cont:
                cont = cont[i + 4:-2]
                break
        res = []
        for i in cont:
            if '<DIR>' in i:
                res.append(i.split()[-1] + ' <DIR>')
            else:
                res.append(i.split()[-1])
        return res
    
    def dot_dot_slash(self):
        print(self.get_dir_content(self.repo_path))



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, commit_dialog, repo_path=''):
        super().__init__()
        self.setupUi(self, commit_dialog, repo_path)
    
    def rerender(self):
        self.setWindowTitle(self.repo_path)
        tree = subprocess.check_output('git log --all --graph --oneline --abbrev-commit')
        tree = tree.decode('utf-8')
        self.commit_tree.setText(tree)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

