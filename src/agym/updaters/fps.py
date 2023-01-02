from agym.gui import TextLabel
from agym.protocols import IClock


class FPSUpdater:
    def __init__(self, label: TextLabel, clock: IClock):
        self._label = label
        self._clock = clock

    def update(self) -> None:
        fps_str = "FPS AVG: {:5.2f}".format(self._clock.get_framerate())
        # fps0_5_str = "FPS 50%: {:5.2f}".format(self._clock.get_framerate(0.5))
        fps0_1_str = "FPS 10%: {:5.2f}".format(self._clock.get_framerate(0.1))
        fps0_01_str = "FPS  1%: {:5.2f}".format(self._clock.get_framerate(0.01))
        fps0_001_str = "FPS .1%: {:5.2f}".format(
            self._clock.get_framerate(0.001)
        )

        text = "\n".join(
            [
                fps_str,
                # fps0_5_str,
                fps0_1_str,
                fps0_01_str,
                fps0_001_str,
            ]
        )
        self._label.text = text
