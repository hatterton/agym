from agym.gui import TextLabel
from agym.utils import FPSLimiter, profile

class FPSUpdater:
    def __init__(self, label: TextLabel, fps_limiter: FPSLimiter):
        self.label = label
        self.fps_limiter = fps_limiter

    def update(self) -> None:
        fps_str = "FPS AVG: {:5.2f}".format(self.fps_limiter.get_fps())
        # fps0_5_str = "FPS 50%: {:5.2f}".format(self.fps_limiter.get_fps(0.5))
        fps0_1_str = "FPS 10%: {:5.2f}".format(self.fps_limiter.get_fps(0.1))
        fps0_01_str = "FPS  1%: {:5.2f}".format(self.fps_limiter.get_fps(0.01))
        fps0_001_str = "FPS .1%: {:5.2f}".format(self.fps_limiter.get_fps(0.001))

        text = "\n".join(
            [
                fps_str,
                # fps0_5_str,
                fps0_1_str,
                fps0_01_str,
                fps0_001_str,
            ]
        )
        self.label.text = text

