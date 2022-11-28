import pygame

from .di import Application
from .settings import Settings


def create_app() -> Application:
    pygame.init()
    pygame.font.init()

    settings = Settings()

    app = Application(settings)

    return app


def run_app(application: Application) -> None:
    application.windows.main.run()
