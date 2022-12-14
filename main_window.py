import sys
import os

import subprocess

from PyQt5 import QtCore, QtWidgets



class Ui_MainWindow(object):
    def setupUi(self, MainWindow, commit_dialog, edit_file_window, repo_path):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 787)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_list.setGeometry(QtCore.QRect(10, 30, 181, 721))
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
        self.commit_tree.setGeometry(QtCore.QRect(210, 30, 661, 671))
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
        self.commit_tree.setReadOnly(True)
        self.commit_info.setReadOnly(True)

        self.commit_dialog = commit_dialog
        self.edit_window = edit_file_window
        
        self.repo_path = repo_path
        self.path_now = repo_path

        self.commit_btn.clicked.connect(self.create_commit_dialog)
        self.get_info_btn.clicked.connect(self.get_info_on_commit)
        self.checkout_btn.clicked.connect(self.checkout_dialog)
        self.file_list_btn.clicked.connect(self.dot_dot_slash)
        self.file_list.itemDoubleClicked.connect(self.essene_open)

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
        self.commit_dialog.main_w = self
        self.commit_dialog.set_branches()
        self.commit_dialog.show()
    
    def checkout_btn_click(self, btn):
        if btn.text() == 'OK':
            # ?????????????????? ????????????, ?????????????? ?? cmd ???????? ?????????????? ???? checkout
            os.chdir(self.repo_path)
            hash = self.lineEdit.text()
            res = subprocess.run(['git', 'checkout', hash])
            if res.returncode == 0:
                self.statusbar.showMessage(f'sucsess. command "git checkout {hash}" completed')
            else:
                self.statusbar.showMessage(f'wrong commit hash')
            return None

    def get_info_on_commit(self):
        hash = self.lineEdit.text()
        os.chdir(self.repo_path)
        try:
            info = subprocess.check_output(f'git log -n 1 {hash}').decode('utf-8')
            self.commit_info.setText(info)
        except subprocess.CalledProcessError:
            self.statusbar.showMessage('wrong commit hash')
        
    def get_dir_content(self, dir_path):
        try:
            os.chdir(dir_path)
            res = os.listdir(dir_path)
            return res
        except FileNotFoundError:
            return []
    
    def show_list_dir(self, dir_path):
        res = self.get_dir_content(dir_path)
        self.file_list.clear()
        for i in res:
            self.file_list.addItem(i)

    def dot_dot_slash(self):
        os.chdir(self.path_now)
        os.chdir('..')
        self.path_now = os.getcwd()
        self.show_list_dir(self.path_now)
    
    def essene_open(self, item):
        essene_name = item.text()
        try:
            croc = os.listdir(os.path.join(self.path_now, essene_name))
            self.path_now = os.path.join(self.path_now, essene_name)    
            self.show_list_dir(self.path_now)
        except NotADirectoryError:
            self.open_edit_window(os.path.join(self.path_now, essene_name))
            
        
    def open_edit_window(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.edit_window.textEdit.setText(text)
                self.edit_window.file_path = file_path
            self.edit_window.show()
        except FileNotFoundError or FileExistsError:
            self.statusbar.showMessage('there is no such file')
        except UnicodeDecodeError:
            self.statusbar.showMessage('you can\'t decode this file in utf-8')
        



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, commit_dialog, edit_file_window, repo_path=''):
        super().__init__()
        self.setupUi(self, commit_dialog, edit_file_window, repo_path)
    
    def rerender(self):
        self.setWindowTitle(self.repo_path)
        tree = subprocess.check_output('git log --all --graph --oneline --abbrev-commit')
        tree = tree.decode('utf-8')
        self.show_list_dir(self.repo_path)
        self.commit_tree.setText(tree)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

