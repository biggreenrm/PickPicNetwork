from django.apps import AppConfig


# Регистрация имени конфига приложения, к которому происходит обращение
class ImagesConfig(AppConfig):
    name = 'images'

    # Функция импортирующая сигналы при инициализации приложения
    def ready(self):
        import images.signals