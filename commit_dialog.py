import sys
import os

import subprocess
from PyQt5 import QtCore, QtWidgets


class Ui_CommitDialog(object):
    def setupUi(self, Dialog, repo_path):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.branch_menu = QtWidgets.QComboBox(Dialog)
        self.branch_menu.setGeometry(QtCore.QRect(130, 20, 251, 31))
        self.branch_menu.setObjectName("branch_menu")
        self.branch_label = QtWidgets.QLabel(Dialog)
        self.branch_label.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.branch_label.setAlignment(QtCore.Qt.AlignCenter)
        self.branch_label.setObjectName("branch_label")
        self.add_label = QtWidgets.QLabel(Dialog)
        self.add_label.setGeometry(QtCore.QRect(10, 80, 91, 31))
        self.add_label.setAlignment(QtCore.Qt.AlignCenter)
        self.add_label.setObjectName("add_label")
        self.comment_label = QtWidgets.QLabel(Dialog)
        self.comment_label.setGeometry(QtCore.QRect(10, 150, 91, 31))
        self.comment_label.setAlignment(QtCore.Qt.AlignCenter)
        self.comment_label.setObjectName("comment_label")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(130, 150, 251, 101))
        self.textEdit.setObjectName("textEdit")
        self.add_button = QtWidgets.QPushButton(Dialog)
        self.add_button.setGeometry(QtCore.QRect(130, 80, 251, 41))
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_file)
        self.repo_path = repo_path
        self.main_w = None

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.branch_label.setText(_translate("Dialog", "branch"))
        self.add_label.setText(_translate("Dialog", "add"))
        self.comment_label.setText(_translate("Dialog", "description"))
        self.add_button.setText(_translate("Dialog", "add"))
    
    def accept(self):
        try:
            branch = self.branch_menu.currentText()
            desc = self.textEdit.toPlainText()
            if not branch.startswith('* '):
                result1 = subprocess.run(['git', 'checkout', branch])
            if desc != '':
                result2 = subprocess.run(['git', 'commit', '-m', f'"{desc}"'])
            else:
                resilt2 = subprocess.run(['git', 'commit'])
            self.main_w.statusbar.showMessage('sucsessfuly commited')
        except subprocess.CalledProcessError:
            self.main_w.statusbar.showMessage('something went wrong, try again later')
        self.main_w.rerender()
        self.reject()
    
    def set_branches(self):
        os.chdir(self.repo_path)
        branches = subprocess.check_output('git branch -a').decode('utf-8').split('\n')
        for i in branches:
            if not ('remotes/' in i or i == ''):
                self.branch_menu.addItem(i)
        

    def add_file(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'select file to add', '')[0]
        print(file_path)
        try:
            if file_path != '':
                res = subprocess.run(['git', 'add', file_path.split('/')[-1]])
                print(res.returncode, 'aboba')
        except FileNotFoundError:
            message = 'something went wrong while adding files, try again later'
            self.main_w.statusbar.showMessage(message)
            self.main_w.rerender()
            self.reject()
        except subprocess.CalledProcessError:
            message = 'something went wrong while adding, try again later'
            self.main_w.statusbar.showMessage(message)
            self.main_w.rerender()
            self.reject()


class CommitDialog(QtWidgets.QDialog, Ui_CommitDialog):
    def __init__(self, repo_path=''):
        super().__init__()
        self.setupUi(self, repo_path)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = CommitDialog()
    ex.show()
    sys.exit(app.exec_())

