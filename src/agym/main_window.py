import pygame
from pygame.event import Event

from agym.dtos import Color, Shift, Size
from agym.game_monitor import GameMonitor
from agym.gui.render_kits.pygame import PygameScreen
from agym.protocols import IEventHandler, IRenderKit


class MainWindow:
    def __init__(
        self,
        window_size: Size,
        render_kit: IRenderKit,
        game_monitor: GameMonitor,
    ):
        pygame.display.set_caption("Arcanoid")

        self._render_kit = render_kit
        self.screen = self._render_kit.create_display(window_size)
        self.game_monitor = game_monitor

        self.gm_screen_rect = game_monitor.screen.get_rect()
        self.gm_screen_rect.centerx = window_size.width // 2
        self.gm_screen_rect.bottom = window_size.height

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
        self.screen.fill(Color(255, 255, 255))

        self.game_monitor.blit()
        gm_screen = PygameScreen(self.game_monitor.screen)

        self.screen.blit(gm_screen, Shift(0, 0))

        self._render_kit.flip_display()

    def try_handle_event(self, event: Event) -> bool:
        handled = self._try_consume_event(event)
        handled = handled or self._try_delegate_event(event)

        return handled

    def _try_consume_event(self, event: Event) -> bool:
        if event.type == pygame.QUIT:
            self.active = False
            return True

        if event.type == pygame.KEYDOWN and (
            event.key == pygame.K_q or event.key == pygame.K_ESCAPE
        ):
            self.active = False
            return True

        return False

    def _try_delegate_event(self, event: Event) -> bool:
        return self.game_monitor.try_handle_event(event)
