import os
import pygame
import enum
import torch

# from agym.gui import Menu
from agym.config import Config
from agym.games import (
    IGameEnviroment,
    BreakoutEnv,
    ManualBreakoutModel,
)
from agym.models import (
    IModel,
    ConvQValuesModel,
)
from agym.model_wrappers import (
    IModelWrapper,
    EmptyWrapper,
    SarsaWrapper,
)
from agym.utils import (
    FPSLimiter,
)
# from agym.gui import (
#     IMenu,
#     MainMenu,
# )


class MonitorState(enum.Enum):
    MENU = 1
    GAME = 2

class GameMonitor:
    def __init__(self):
        pygame.init()

        config = Config()
        self.screen = pygame.display.set_mode(
            (config.window_screen_width,
             config.window_screen_height)
        )
        pygame.display.set_caption("Arcanoid")

        # Setup env
        self.inner_screen = pygame.Surface(
            (config.env_width,
             config.env_height)
        )
        self.inner_screen_rect = self.inner_screen.get_rect()
        self.inner_screen_rect.centerx = self.screen.get_rect().centerx
        self.inner_screen_rect.bottom = self.screen.get_rect().bottom

        self.env = BreakoutEnv(
            config.env_width,
            config.env_height,
            map_shape=[6, 6]
        )
        self.env.reset()

        # Setup model
        model = ManualBreakoutModel()
        self.model_wrapper = EmptyWrapper(model)
        # n_actions = self.env.n_actions
        # model = ConvQValuesModel(
        #     n_actions=n_actions,
        #     filters_list=[6, 16, 32],
        #     hidden_units_list=[],
        # )

        # self.model_path = "/home/anton/model.db"
        # if os.path.exists(self.model_path):
        #     model.model.load_state_dict(torch.load(self.model_path))

        # self.model_wrapper = SarsaWrapper(
        #     model=model,
        #     n_actions=n_actions,
        #     eps=0.3,
        # )


        # Setup menu
        # self.menu = Menu()
        self.menu = self.env

        self.fps_limiter = FPSLimiter(config.max_fps)

        # self.state_type = MonitorState.MENU
        self.state_type = MonitorState.GAME
        self.visualizing_flag = True
        self.is_active = False
        self.score: int

    def _try_event(self, event) -> bool:
        if (event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and (
                event.key == pygame.K_q or
                event.key == pygame.K_ESCAPE
            )):
            self.deactive()
        else:
            return False

        return True

    def _check_events(self) -> None:
        for event in pygame.event.get():
            print(event.type)
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                print(event.key)
            print()


            if self._try_event(event):
                continue

            if self.state_type == MonitorState.MENU:
                if self.menu.try_event(event):
                    continue
                else:
                    pass

            elif self.state_type == MonitorState.GAME:
                if self.model_wrapper.try_event(event):
                    continue
                elif self.env.try_event(event):
                    continue
                else:
                    pass

    def _update_state(self) -> None:
        if self.state_type == MonitorState.MENU:
            self.menu.update()
        elif self.state_type == MonitorState.GAME:
            state = self.env.get_visual_state()

            action = self.model_wrapper.get_action(state)

            dt = self.fps_limiter.cicle() / 60

            reward, is_done = self.env.step(action, dt)
            next_state = self.env.get_visual_state()
            self.model_wrapper.post_action(next_state, reward, is_done)
            self.score += reward

            if is_done:
                print("Session reward =", self.score)
                self.score = 0
                self.env.reset()
                self.fps_limiter.reset()

    def _blit(self) -> None:
        self.inner_screen.fill((255, 255, 255))
        if self.state_type == MonitorState.MENU:
            self.menu.blit(self.inner_screen)
        elif self.state_type == MonitorState.GAME:
            self.env.blit(self.inner_screen)
        self.screen.blit(self.inner_screen, self.inner_screen_rect)

        pygame.display.flip()

    def set_game(self, env: IGameEnviroment) -> None:
        self.env = env

    # def set_menu(self, menu: IMenu) -> None:
    #     self.menu= menu

    def deactive(self) -> None:
        self.is_active = False
        # torch.save(
        #     self.model_wrapper.model.model.state_dict(), self.model_path)

    def run(self) -> None:
        self.score = 0
        self.is_active = True

        self.env.reset()
        self.fps_limiter.reset()
        while self.is_active:
            self._check_events()
            self._update_state()
            self._blit()


def run_app():
    app = GameMonitor()
    app.run()

