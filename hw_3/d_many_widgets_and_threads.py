"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""

from hw_3 import b_systeminfo_widget, c_weatherapi_widget
from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitUi()


    def InitUi(self):
        self.systemInfo = b_systeminfo_widget.Window()
        self.weatherApi = c_weatherapi_widget.Window()


        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(self.systemInfo)
        mainLayout.addWidget(self.weatherApi)
        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()