from agym.gui import BaseLabel
from agym.utils import FPSLimiter, profile

class FPSLabel(BaseLabel):
    def __init__(self, x: int, y: int, fps_limiter: FPSLimiter):
        self.fps_limiter = fps_limiter

        super().__init__(x=x, y=y)

    @profile("fps_update")
    def update(self) -> None:
        fps_str = "FPS AVG: {:5.2f}".format(self.fps_limiter.get_fps())
        fps0_5_str = "FPS 50%: {:5.2f}".format(self.fps_limiter.get_fps(0.5))
        fps0_1_str = "FPS 10%: {:5.2f}".format(self.fps_limiter.get_fps(0.1))
        fps0_01_str = "FPS  1%: {:5.2f}".format(self.fps_limiter.get_fps(0.01))

        text = "\n".join(
            [
                fps_str,
                fps0_5_str,
                fps0_1_str,
                fps0_01_str,
            ]
        )
        self.text = text
