from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    # Функция импортирующая сигналы при инициализации приложения
    def ready(self):
        import images.signals