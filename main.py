from main_window import MainWindow, Ui_MainWindow
from checkout_dialog import CheckoutDialog, Ui_CheckoutDialog
from commit_dialog import CommitDialog, Ui_CommitDialog
from index_window import IndexWindow, Ui_IndexWindow
from edit_file_window import EditFileWindow, Ui_EditFileWindow

import sys
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = IndexWindow(MainWindow(CommitDialog(), EditFileWindow()))
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

