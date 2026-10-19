# Модуль абстракций и конфигураций базы данных приложения Planner
# Предназначен для подключения к СУБД в последующих работах

class DatabaseConnection:
    """Конфигурация подключения к базе данных"""
    def __init__(self, connection_url: str = "sqlite:///./planner.db"):
        self.connection_url = connection_url

    def connect(self):
        return True
