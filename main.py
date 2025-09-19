import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        screens = QtWidgets.QApplication.screens()
        screen = screens[1].geometry()
        self.setGeometry(screen)
        self.keys_pressed: dict[int, bool] = {}

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 2

        # Outline
        qp.setBrush(Qt.black)
        qp.setPen(Qt.NoPen)
        qp.drawEllipse(
            center_x - radius - 1,
            center_y - radius - 1,
            (radius + 1) * 2,
            (radius + 1) * 2,
        )

        # Dot
        qp.setBrush(Qt.red)
        qp.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)


class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self, overlay, app):
        icon = app.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon)
        super().__init__(icon, app)

        menu = QtWidgets.QMenu()
        toggle_action = menu.addAction("Toggle Overlay")
        quit_action = menu.addAction("Quit")

        toggle_action.triggered.connect(self.toggleOverlay)
        quit_action.triggered.connect(app.quit)

        self.setContextMenu(menu)
        self.overlay = overlay
        self.show()

    def toggleOverlay(self):
        if self.overlay.isVisible():
            self.overlay.hide()
        else:
            self.overlay.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = Overlay()
    overlay.showFullScreen()

    tray = Tray(overlay, app)

    sys.exit(app.exec_())
