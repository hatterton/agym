from agym.gui import TextLabel
from agym.protocols import IClock
from agym.utils import profile


class FPSUpdater:
    def __init__(self, label: TextLabel, clock: IClock):
        self.label = label
        self._clock = clock

    def update(self) -> None:
        fps_str = "FPS AVG: {:5.2f}".format(self._clock.get_framerate())
        fps0_01_str = "FPS  1%: {:5.2f}".format(self._clock.get_framerate(0.01))
        fps0_001_str = "FPS .1%: {:5.2f}".format(
            self._clock.get_framerate(0.001)
        )

        text = "\n".join(
            [
                fps_str,
                fps0_01_str,
                fps0_001_str,
            ]
        )
        self.label.text = text
