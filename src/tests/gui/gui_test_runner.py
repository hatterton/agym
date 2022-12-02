from contextlib import contextmanager
from functools import wraps
from threading import Thread, Timer
from typing import Callable, Generator

import pygame as pg
from pygame.event import Event

from agym.games.breakout import BreakoutEnv
from agym.main_window import MainWindow
from tests.gui.game_model import DummyModel


@contextmanager
def patch_events(
    try_handle_event: Callable[[Event], bool]
) -> Generator[None, None, None]:
    try:
        old_event_get = pg.event.get

        @wraps(old_event_get)
        def monkey_event_get():
            for event in old_event_get():
                handled = try_handle_event(event)
                if not handled:
                    yield event

        pg.event.get = monkey_event_get  # type: ignore
        yield

    finally:
        pg.event.get = old_event_get


TICKS_PER_SECOND = 20


class GUITestRunner:
    def __init__(self, window: MainWindow, env: BreakoutEnv, model: DummyModel):
        self._window = window
        self._env = env
        self._model = model

        self._test_counter: int = 0
        self._active: bool = False

    @property
    def test_counter(self) -> int:
        return self._test_counter

    @test_counter.setter
    def test_counter(self, value: int) -> None:
        self._test_counter = max(0, value)

    def deactivate(self) -> None:
        self._active = False

    def run(self, test_cases) -> None:
        self._active = True

        self.test_conter = 0
        while self._active and self.test_counter < len(test_cases):
            test_case = test_cases[self.test_counter]

            with patch_events(self.try_handle_event):
                self.run_test(test_case)

    def run_test(self, test_case) -> None:
        level, action, ticks = test_case
        t = ticks / TICKS_PER_SECOND

        self._env.reset()
        self._env.import_state(level.copy())

        self._model.set_action(action)

        t_test_starter = Thread(target=self.start_test)
        t_test_finisher = Timer(t, self.finish_test)

        t_test_starter.start()
        t_test_finisher.start()

        t_test_starter.join()
        t_test_finisher.cancel()

    def start_test(self) -> None:
        self._window.run()

    def finish_test(self) -> None:
        self.abort_test()
        self.test_counter += 1

    def abort_test(self) -> None:
        self._window.deactivate()

    def try_handle_event(self, event: Event) -> bool:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.abort_test()
                self.deactivate()
                return True

            elif event.key == pg.K_RIGHT:
                self.abort_test()
                self.test_counter += 1
                return True

            elif event.key == pg.K_LEFT:
                self.abort_test()
                self.test_counter -= 1
                return True

            elif event.key == pg.K_r:
                self.abort_test()
                return True

        return False
