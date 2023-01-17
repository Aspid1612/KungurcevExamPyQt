"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""


import json
from PySide6 import QtWidgets, QtCore, QtGui
from hw_3.a_threads import WeatherHandler




class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitUi()
        self.InitThreads()
        self.InitSignals()


    def InitUi(self):
        self.delayInsert = QtWidgets.QSpinBox()
        self.delayInsert.setRange(1, 60)
        self.delaylabel = QtWidgets.QLabel("Обновление")

        self.longitubeInsert = QtWidgets.QDoubleSpinBox()
        self.longitubeInsert.setRange(-180, 180)
        self.longitubeInsert.setValue(83)
        self.longitubeLabel = QtWidgets.QLabel("Долгота")

        self.latitubeInsert = QtWidgets.QDoubleSpinBox()
        self.latitubeInsert.setRange(-90, 90)
        self.latitubeInsert.setValue(53)
        self.latitubeLabel = QtWidgets.QLabel("Широта")

        self.pushButton = QtWidgets.QPushButton("Старт")
        self.pushButton.setCheckable(True)

        self.weatherInfo = QtWidgets.QPlainTextEdit()
        self.weatherInfo.setReadOnly(True)

        delayLayout = QtWidgets.QHBoxLayout()
        delayLayout.addWidget(self.delaylabel)
        delayLayout.addWidget(self.delayInsert)

        longitubeLayout = QtWidgets.QHBoxLayout()
        longitubeLayout.addWidget(self.longitubeLabel)
        longitubeLayout.addWidget(self.longitubeInsert)


        latitubeLayout = QtWidgets.QHBoxLayout()
        latitubeLayout.addWidget(self.latitubeLabel)
        latitubeLayout.addWidget(self.latitubeInsert)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(delayLayout)
        mainLayout.addLayout(longitubeLayout)
        mainLayout.addLayout(latitubeLayout)
        mainLayout.addWidget(self.pushButton)
        mainLayout.addWidget(self.weatherInfo)

        self.setLayout(mainLayout)
        self.setMinimumSize(300, 300)

    def InitThreads(self):
        self.thread = WeatherHandler()


    def InitSignals(self):
        self.pushButton.clicked.connect(self.onPushButtonClicked)
        self.thread.finished.connect(self.onTreadFinished)
        self.thread.StatusCodeReceived.connect(self.onStatusCodeReceived)
        self.thread.weatherDataReceived.connect(self.onWeatherDataReceived)


    def onStatusCodeReceived(self, value):
        self.weatherInfo.appendPlainText(f"code Receive{value}")


    def onWeatherDataReceived(self, data):
        self.weatherInfo.appendPlainText(f"Температура:{data['temperature']}/n/"
                                         f"Скорость ветра:{data['windspeed']}/n/"
                                         f"Напрвление  ветра:{data['winddirection']}/n/"
                                         )



    def onPushButtonClicked(self, status):
        if status:
            self.thread.geo_date["longitude"] = self.longitubeInsert.value()
            self.thread.geo_date["latitude"] = self.latitubeInsert.value()
            self.thread.setDelay(self.delayInsert.value())
            self.pushButton.setText("Стоп")
            self.thread.start()
        else:
            self.thread.status = False
            self.pushButton.setText("Старт")
            self.pushButton.setEnabled(False)


    def onTreadFinished(self):
        self.pushButton.setEnabled(True)
        self.delayInsert.setEnabled(True)
        self.longitubeInsert.setEnabled(True)
        self.latitubeInsert.setEnabled(True)

    def closeEvent(self, event: QtCore.QEvent) -> None:
        self.thread.terminate()



        
if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()