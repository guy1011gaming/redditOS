import sys
from PyQt6.QtWidgets import *
import reddit_user


class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = {}
        self.lineEdits = {}

        self.setWindowTitle("RedditOS")
        self.resize(200, 200)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.labels['Username'] = QLabel('Username')
        self.labels['Password'] = QLabel('Password')
        self.labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit("Username", self)
        self.lineEdits['Password'] = QLineEdit("Password", self)
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addWidget(self.labels['Username'],            0, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Username'],    0, 1, 1, 3)

        self.layout.addWidget(self.labels['Password'],            1, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Password'],    1, 1, 1, 3)

        button_login = QPushButton('&Log In', clicked=self.onLogin)
        self.layout.addWidget(button_login,                  2, 3, 1, 1)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        self.layout.addWidget(self.status, 3, 0, 1, 3)

    def onLogin(self):
        username = str(self.lineEdits['Username'].text())
        password = str(self.lineEdits['Password'].text())
        self.user = reddit_user.User(username, password)

def main():
    app = QApplication(sys.argv)
    _ = SimpleWindow()
    _.setVisible(True)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()