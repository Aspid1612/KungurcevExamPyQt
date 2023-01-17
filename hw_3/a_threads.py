"""
Модуль в котором содержаться потоки Qt
"""
import json
import time
import requests
import psutil
from PySide6 import QtCore
from PySide6.QtCore import Signal


class SystemInfo(QtCore.QThread):
    CpuInfoReceived = QtCore.Signal(list)
    RamInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None

    def run(self) -> None:
        if self.delay is None:
            self.delay = 1

        while True:
            cpu_value = psutil.cpu_percent()
            ram_value = psutil.virtual_memory().percent
            self.CpuInfoReceived.emit([cpu_value])
            self.RamInfoReceived.emit([ram_value])
            time.sleep(self.delay)


class WeatherHandler(QtCore.QThread):
    # TODO Пропишите сигналы, которые считаете нужными
    weatherDataReceived = QtCore.Signal(str)
    StatusCodeReceived = QtCore.Signal(dict)

    def __init__(self, lat = None, lon = None, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?"
        self.__delay = 10
        self.__status = True
        self.geo_date = {"latitude":lat, "longitude":lon, "current_weather": True }



    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay


    def run(self) -> None:
        self.started.emit()
        self.status = True

        while self.__status:
            response = requests.get(self.__api_url, params = self.geo_date)
            data = response.json()
            status = response.status_code
            self.weatherDataReceived.emit(status)
            self.StatusCodeReceived.emit(data["current_weather"])
            time.sleep(self.__delay)

        self.finished.emit()
