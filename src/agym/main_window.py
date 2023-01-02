import pygame

from agym.dtos import (
    Color,
    Event,
    KeyCode,
    KeyDownEvent,
    QuitEvent,
    Shift,
    Size,
)
from agym.game_monitor import GameMonitor
from agym.protocols import IEventHandler, IEventSource, IRenderKit
from agym.renderers import GameMonitorRenderer


class MainWindow(IEventHandler):
    def __init__(
        self,
        window_size: Size,
        render_kit: IRenderKit,
        game_monitor: GameMonitor,
        event_source: IEventSource,
        game_monitor_renderer: GameMonitorRenderer,
    ):
        pygame.display.set_caption("Arcanoid")

        self._render_kit = render_kit
        self.screen = self._render_kit.create_display(window_size)

        self._event_source = event_source

        self.game_monitor = game_monitor
        self._game_monitor_renderer = game_monitor_renderer

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
        for event in self._event_source.get_events():
            handled = self.try_handle_event(event)
            if not handled:
                print("Unhandled event", event)

    def update(self) -> None:
        self.game_monitor.update()

    def blit(self) -> None:
        self.screen.fill(Color(255, 255, 255))

        gm_screen = self._game_monitor_renderer.render()

        self.screen.blit(gm_screen, Shift(0, 0))

        self._render_kit.flip_display()

    def try_handle_event(self, event: Event) -> bool:
        handled = self._try_consume_event(event)
        handled = handled or self._try_delegate_event(event)

        return handled

    def _try_consume_event(self, event: Event) -> bool:
        if isinstance(event, QuitEvent) or (
            isinstance(event, KeyDownEvent) and event.key.code == KeyCode.ESCAPE
        ):
            self.deactivate()
            return True

        return False

    def _try_delegate_event(self, event: Event) -> bool:
        return self.game_monitor.try_handle_event(event)
