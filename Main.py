from PyQt5.QtWidgets import QApplication
import sys
from MainMenu import MainMenu


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.showMaximized()
    sys.exit(app.exec_())

