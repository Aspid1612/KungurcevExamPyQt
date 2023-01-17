import psutil
import platform
import time
import win32com.client

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.InitThreads()
        self.InitSignals()
        self.InitUi()

    def InitThreads(self):
        self.systemInfoThread = SystemViewerThread()
        self.systemInfoThread.start()
        self.processInfoThread = ProcessInfoThread()
        self.processInfoThread.start()
        self.serviseInfoThread = ServiseInfoThread()
        self.serviseInfoThread.start()
        self.taskInfoThread = TaskInfoThread()

    def InitSignals(self):
        self.systemInfoThread.systeminfoRecieved.connect(self.updateSystenInfo)
        self.processInfoThread.processinfoRecieved.connect(self.updateProcessInfo)
        self.serviseInfoThread.serviseinfoRecieved.connect(self.updateServiceInfo)

    def InitUi(self):
        self.systemPlaintextEdit = QtWidgets.QPlainTextEdit()
        self.systemPlaintextEdit.setReadOnly(True)
        self.processPlaintextEdit = QtWidgets.QPlainTextEdit()
        self.processPlaintextEdit.setReadOnly(True)
        self.servisePlaintextEdit = QtWidgets.QPlainTextEdit()
        self.servisePlaintextEdit.setReadOnly(True)
        self.taskPlaintextEdit = QtWidgets.QPlainTextEdit()

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.systemPlaintextEdit, 'Система')
        self.tabWidget.addTab(self.processPlaintextEdit, 'Процессы')
        self.tabWidget.addTab(self.servisePlaintextEdit, 'Сервисы')
        self.tabWidget.addTab(self.taskPlaintextEdit, 'Задачи')

        self.spinBoxLadel = QtWidgets.QLabel("Обновления")
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setRange(1, 50)
        self.spinBox.valueChanged.connect(self.onSpinBoxValueChanged)

        spinboxLayout = QtWidgets.QHBoxLayout()
        spinboxLayout.addWidget(self.spinBoxLadel)
        spinboxLayout.addWidget(self.spinBox)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addLayout(spinboxLayout)

        self.setLayout(mainLayout)
        self.setMinimumSize(700, 500)

    def updateSystenInfo(self, data):
        self.systemPlaintextEdit.clear()
        for i in data:
            self.systemPlaintextEdit.appendPlainText(f"{i} {data[i]}")

    def updateProcessInfo(self, data):
        self.processPlaintextEdit.clear()
        for i in data:
            self.processPlaintextEdit.appendPlainText(str(i))

    def updateServiceInfo(self, data):
        self.servisePlaintextEdit.clear()
        for i in data:
            self.servisePlaintextEdit.appendPlainText(str(i))

    def updateTaskInfo(self, data):
        self.taskPlaintextEdit.clear()
        for i in data:
            self.taskPlaintextEdit.appendPlainText(str(i))

    def onSpinBoxValueChanged(self, value):
        self.systemInfoThread.delay = value
        self.processInfoThread.delay = value
        self.serviseInfoThread.delay = value
        self.taskInfoThread.delay = value


class SystemViewerThread(QtCore.QThread):
    systeminfoRecieved = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.delay = None

    def run(self) -> None:
        if self.delay is None:
            self.delay = 20

        while True:
            self.data["Процессор"] = platform.processor()
            self.data["Логические ядра"] = psutil.cpu_count(logical=True)
            self.data["Физические ядра"] = psutil.cpu_count(logical=False)
            self.data["Загрузка процессора %"] = psutil.cpu_percent()
            self.data["Оперативная память Гб"] = round(psutil.virtual_memory().total)
            self.data["Использовано памяти %"] = psutil.virtual_memory()
            self.data["Кол-во дисков"] = len(psutil.disk_partitions())
            self.systeminfoRecieved.emit(self.data)
            time.sleep(self.delay)


class ProcessInfoThread(QtCore.QThread):
    processinfoRecieved = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.delay = None

    def run(self) -> None:
        if self.delay is None:
            self.delay = 20

        while True:
            self.data = psutil.process_iter(['pid', 'name', 'username'])
            self.processinfoRecieved.emit(self.data)
            time.sleep(self.delay)


class ServiseInfoThread(QtCore.QThread):
    serviseinfoRecieved = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.delay = None

    def run(self) -> None:
        if self.delay is None:
            self.delay = 20

        while True:
            self.data = psutil.win_service_iter()
            self.serviseinfoRecieved.emit(self.data)
            time.sleep(self.delay)


class TaskInfoThread(QtCore.QThread):
    taskInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None

    def run(self) -> None:
        if self.delay is None:
            self.delay = 20

        while True:
            scheduler = win32com.client.Dispatch('Schedule.Service')
            scheduler.Connect()
            self.taskInfoReceived.emit(scheduler)
            time.sleep(self.delay)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()