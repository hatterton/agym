import os
from enum import Enum, auto
from typing import Dict

from agym.dtos import Color, Rect, Shift, Size
from agym.games import BreakoutEnv
from agym.games.breakout.dtos import Ball, Block, Item, Platform, Wall
from agym.games.breakout.geom import Rectangle
from agym.protocols import IRenderer, IRenderKit, IScreen

from .kdtree import KDTreeRenderer


class ItemType(Enum):
    BALL = auto()
    BLOCK_RED = auto()
    BLOCK_YELLOW = auto()
    BLOCK_BLUE = auto()
    PLATFORM = auto()


class EnvRenderer(IRenderer):
    def __init__(
        self,
        screen_size: Size,
        image_dir: str,
        env: BreakoutEnv,
        kdtree_renderer: IRenderer,
        render_kit: IRenderKit,
    ):
        self._env = env
        self._kdtree_renderer = kdtree_renderer

        self._render_kit = render_kit
        self._screen_size = screen_size

        self._block_font = self._render_kit.create_font("Hack", 18)

        self._item2image: Dict[ItemType, IScreen] = dict()
        self._load_images(image_dir)

    def _load_images(self, image_dir: str) -> None:
        ball_path = os.path.join(image_dir, "ball_aparture 20x20.png")
        block_red_path = os.path.join(image_dir, "block_red 60x20.png")
        block_yellow_path = os.path.join(image_dir, "block_yellow 60x20.png")
        block_blue_path = os.path.join(image_dir, "block_blue 60x20.png")
        platform_path = os.path.join(image_dir, "platform 120x20.png")

        self._item2image[ItemType.BALL] = self._render_kit.load_image(ball_path)
        self._item2image[ItemType.BLOCK_RED] = self._render_kit.load_image(
            block_red_path
        )
        self._item2image[ItemType.BLOCK_YELLOW] = self._render_kit.load_image(
            block_yellow_path
        )
        self._item2image[ItemType.BLOCK_BLUE] = self._render_kit.load_image(
            block_blue_path
        )
        self._item2image[ItemType.PLATFORM] = self._render_kit.load_image(
            platform_path
        )

    def render(self) -> IScreen:
        state = self._env.state

        screen = self._render_kit.create_screen(self._screen_size)

        screen.fill(Color(30, 20, 10))

        for ball in state.balls:
            self._render_ball_on(screen, ball)

        for block in state.blocks:
            self._render_block_on(screen, block)

        for platform in state.platforms:
            self._render_platform_on(screen, platform)

        for wall in state.walls:
            self._render_wall_on(screen, wall)

        kdtree_screen = self._kdtree_renderer.render()
        screen.blit(kdtree_screen, Shift(0, 0))

        return screen

    def _render_ball_on(self, screen: IScreen, ball: Ball) -> None:
        rect = self._convert_rectangle_to_rect(ball.rect)
        image = self._item2image[ItemType.BALL]

        ball_screen = image.resize(rect.size)
        screen.blit(ball_screen, rect.shift)

    def _render_block_on(self, screen: IScreen, block: Block) -> None:
        rect = self._convert_rectangle_to_rect(block.rect)

        if block.health < 5:
            primary_image = self._item2image[ItemType.BLOCK_RED]
            secondary_image = self._item2image[ItemType.BLOCK_YELLOW]
            alpha = int((block.health - 1) / 5 * 255)

        elif block.health >= 5 and block.health < 10:
            primary_image = self._item2image[ItemType.BLOCK_YELLOW]
            secondary_image = self._item2image[ItemType.BLOCK_BLUE]
            alpha = int((block.health - 5) / 5 * 255)

        else:
            primary_image = self._item2image[ItemType.BLOCK_BLUE]
            secondary_image = self._item2image[ItemType.BLOCK_BLUE]
            alpha = 0

        block_screen = self._render_kit.create_screen(primary_image.size)
        secondary_block_screen = self._render_kit.create_screen(
            primary_image.size
        )

        health_screen = self._block_font.render(
            text=str(block.health),
            foreground_color=Color(20, 20, 20),
            background_color=Color(200, 100, 100, 50),
            # foreground_color=Color(200, 200, 200),
            # background_color=Color(20, 20, 20, 100),
        )
        health_rect = health_screen.rect
        health_rect.center = block_screen.rect.center

        block_screen.blit(primary_image, Shift(0, 0))

        secondary_block_screen.blit(secondary_image, Shift(0, 0))
        secondary_block_screen.alpha = alpha
        block_screen.blit(secondary_block_screen, Shift(0, 0))

        block_screen.blit(health_screen, health_rect.shift)

        block_screen = block_screen.resize(rect.size)
        screen.blit(block_screen, rect.shift)

    def _render_platform_on(self, screen: IScreen, platform: Platform) -> None:
        rect = self._convert_rectangle_to_rect(platform.rect)
        image = self._item2image[ItemType.PLATFORM]

        platform_screen = image.resize(rect.size)
        screen.blit(platform_screen, rect.shift)

    def _render_wall_on(self, screen: IScreen, wall: Wall) -> None:
        rect = self._convert_rectangle_to_rect(wall.rect)

        self._render_kit.draw_rect(
            screen=screen,
            rect=rect,
            color=Color(150, 50, 50),
        )

    def _convert_rectangle_to_rect(self, rect: Rectangle) -> Rect:
        return Rect.from_sides(
            left=int(rect.left),
            top=int(rect.top),
            right=int(rect.right),
            bottom=int(rect.bottom),
        )
