from typing import Optional, Protocol


class IClock(Protocol):
    def get_framerate(self, percentile: Optional[float] = None) -> float:
        pass

    def do_frame_tick(self) -> float:
        pass

    @property
    def last_frame_duration(self) -> float:
        pass

    def get_global_time(self) -> float:
        pass
