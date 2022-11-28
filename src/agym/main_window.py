import pygame
from pygame.event import Event

from agym.game_monitor import GameMonitor
from agym.interfaces import IEventHandler


class MainWindow(IEventHandler):
    def __init__(self, width: int, height: int, game_monitor: GameMonitor):
        pygame.display.set_caption("Arcanoid")
        self.screen = pygame.display.set_mode((width, height))
        self.game_monitor = game_monitor

        screen_rect = self.screen.get_rect()
        self.gm_screen_rect = game_monitor.screen.get_rect()
        self.gm_screen_rect.centerx = screen_rect.centerx
        self.gm_screen_rect.bottom = screen_rect.bottom

        self.active: bool

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def run(self):
        self.activate()
        while self.active:
            self.check_events()
            self.update()
            self.blit()

    def check_events(self) -> None:
        for event in pygame.event.get():
            handled = self.try_handle_event(event)
            if not handled:
                print("Unhandled event", event)

    def update(self) -> None:
        self.game_monitor.update()

    def blit(self) -> None:
        self.screen.fill((255, 255, 255))

        self.game_monitor.blit()
        self.screen.blit(self.game_monitor.screen, self.gm_screen_rect)

        pygame.display.flip()

    def try_consume_event(self, event: Event) -> bool:
        if event.type == pygame.QUIT:
            self.active = False
            return True

        if event.type == pygame.KEYDOWN and (
            event.key == pygame.K_q or event.key == pygame.K_ESCAPE
        ):
            self.active = False
            return True

        return False

    def try_delegate_event(self, event: Event) -> bool:
        return self.game_monitor.try_handle_event(event)
