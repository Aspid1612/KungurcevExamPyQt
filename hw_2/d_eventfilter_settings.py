"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore
from ui.c_signals_events_design import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()
        self.initUi()


    def initUi(self) -> None:
        self.ui.comboBox.addItem(["oct", "hex", "bin", "dec"])
        self.ui.comboBox.setCurrentText("dec")
        self.ui.comboBox.setCurrentIndexChanged.connect(self.comboBoxChanged)

        settings = QtCore.QSettings("Eventfilter")
        self.ui.comboBox.setCurrentText(settings.value("coboBoxvalue", "dec"))
        self.ui.horizontaSlider.setValue(settings.value("value"))


    def initSignals(self):
        self.ui.dial.valueChanged.connect(self.DialChamged)
        self.ui.horizontaSlider.valueChanged.connect(self.SliderChanged)


    def SladerChange(self):
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())
        self.ui.dial.setValue(self.ui.horizontalSlider.value())



    def DialChange(self):
        self.ui.lcdNumber.display(self.ui.dial.value())
        self.ui.dial.setValue(self.ui.dial.value())

        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Plus:
            self.ui.dial.setValue(self.ui.dial.value() + 1)
        elif event.key() == QtCore.Qt.Key.Key_Minus:
            self.ui.dial.setValue(self.ui.dial.value() - 1)

    def comboBoxEvent(self):
        if self.ui.comboBox.setCurrentText() == 'dec':
            self.ui.lcdNumber.setDecMode()
        elif self.ui.comboBox.setCurrentText() == 'oct':
            self.ui.lcdNumber.setOctMode()
        elif self.ui.comboBox.setCurrentText() == 'bin':
            self.ui.lcdNumber.setBinMode()
        else:
            self.ui.lcdNumber.setHexMode()


    def closeEvent(self):
        settings = QtCore.QSettings("Eventfilter")
        settings.setValue("value", self.ui.horizontalSlider.value())
        settings.setValue("comboBoxValue", self.ui.comboBox.currentText())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
