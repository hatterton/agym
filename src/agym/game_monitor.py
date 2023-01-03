from agym.dtos import Event
from agym.protocols import IClock, IEventHandler, IModel, IUpdater
from envs.protocols import IGameEnvironment
from timeprofiler import profile


class GameMonitor(IEventHandler, IUpdater):
    def __init__(
        self,
        env: IGameEnvironment,
        model: IModel,
        clock: IClock,
        log_updater: IUpdater,
        audio_handler,
        tps: int,
    ):
        self._clock = clock

        self._model = model
        self._env = env
        self._env.reset()

        self._log_updater = log_updater
        self._audio_handler = audio_handler
        # self._audio_handler.play_background()

        self._ticks_per_second = tps

    @profile("game_event")
    def try_handle_event(self, event: Event) -> bool:
        handled = False
        handled = handled or self._model.try_handle_event(event)

        return handled

    @profile("game_update")
    def update(self) -> None:
        state = self._env.state

        action = self._model.get_action(state)

        dt = self._clock.do_frame_tick() * self._ticks_per_second
        is_done = self._env.step(action, dt)

        events = self._env.pop_events()
        self._audio_handler.handle_events(events)

        if is_done:
            self._env.reset()

        self._log_updater.update()
