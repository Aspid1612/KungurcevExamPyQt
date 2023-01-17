"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
import time
import psutil
from PySide6 import QtWidgets, QtCore
from hw_3.a_threads import SystemInfo

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.InitUi()
        self.InitSignals()
        #self.InitThreads()


    #def InitThreads(self):



    def InitUi(self):
        self.CpuPlaintextEdit = QtWidgets.QPlainTextEdit()
        self.CpuPlaintextEdit.setReadOnly(True)
        self.RamPlaintextEdit = QtWidgets.QPlainTextEdit()
        self.RamPlaintextEdit.setReadOnly(True)

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.CpuPlaintextEdit, 'Процессор')
        self.tabWidget.addTab(self.RamPlaintextEdit, 'Оперативная память')

        self.spinBoxLadel = QtWidgets.QLabel("Обновления")
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setRange(1, 50)

        spinboxLayout = QtWidgets.QHBoxLayout()
        spinboxLayout.addWidget(self.spinBoxLadel)
        spinboxLayout.addWidget(self.spinBox)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.tabWidget)

        self.setLayout(mainLayout)
        self.setMinimumSize(700, 300)
        self.tabWidget.setMinimumSize(700, 300)

        self.systemInfoThread = SystemInfo()
        self.systemInfoThread.start()


    def InitSignals(self):
        self.systemInfoThread.CpuInfoReceived.connect(self.updateCpuInfo)
        self.systemInfoThread.RamInfoReceived.connect(self.updateRamInfo)

    def updateCpuInfo(self, data):
        self.CpuPlaintextEdit.clear()
        for i in data:
            self.CpuPlaintextEdit.appendPlainText(str(i))

    def updateRamInfo(self, data):
        self.RamPlaintextEdit.clear()
        for i in data:
            self.RamPlaintextEdit.appendPlainText(str(i))




if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
