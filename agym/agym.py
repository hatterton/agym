import pygame
import enum

# from agym.gui import Menu
from agym.config import Config
from agym.games import (
    IGameEnviroment,
    BreakOutEnv,
)
from agym.models import (
    IModel,
    ManualControlModel,
)
from agym.model_wrappers import (
    IModelWrapper,
    EmptyWrapper,
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

        self.env = BreakOutEnv(config.env_width, config.env_height)
        self.env.reset()

        # Setup model
        model = ManualControlModel()
        self.model_wrapper = EmptyWrapper(model)

        # self.menu = Menu()
        # Setup menu
        self.menu = self.env

        # self.state_type = MonitorState.MENU
        self.state_type = MonitorState.GAME
        self.visualizing_flag = True
        self.is_active = False
        # print(pygame.display.get_wm_info())

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


    def _update_state(self, dt: float) -> None:
        if self.state_type == MonitorState.MENU:
            self.menu.update()
        elif self.state_type == MonitorState.GAME:
            # TODO
            state = self.env.get_visual_state()
            action = self.model_wrapper.get_action(state)
            next_state, reward, is_done = self.env.step(action, dt)
            self.model_wrapper.post_action(next_state, reward, is_done)

            if is_done:
                self.env.reset()

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

    def run(self) -> None:
        self.is_active = True

        while self.is_active:
            self._check_events()
            self._update_state(1.0)
            self._blit()


def run_app():
    app = GameMonitor()
    app.run()
    
    #pygame.mouse.set_visible(False)
    # arg = ut.init()
    
    # arg.tm.sing_up("before all", "after all", "check + update + blit")
    # arg.timemanager.sing_up("be print", "af ", "")

    # while True:
    #     # arg.tm.write_down("be all")
    #     gf.check_events(arg)
    #     # arg.tm.write_down("af ch_ev")
    #     gf.update_state(arg)
    #     # arg.tm.write_down("af up_state")
    #     gf.blit_screen(arg)
    #     # arg.tm.write_down("af bliting")

        # arg.tm.update_sing_ups()
        
        # ut.reduce_fps(arg)
        # arg.tm.write_down("af up_sing_ups")
        # ut.print_debug(arg)
