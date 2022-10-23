import enum
import math
from itertools import product, combinations
from typing import List, Iterable

from agym.games.breakout.geom import (
    Point,
    Circle,
    Rectangle,
)
from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
    Wall,
)
from agym.utils import profile
from .dtos import (
    Collision,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
    CollisionBallBall,
)

EPS = 1e-4


def calculate_colls(
    walls: List[Wall],
    platforms: List[Platform],
    balls: List[Ball],
    blocks: List[Block],
    dt: float,
) -> Iterable[Collision]:
    yield from calculate_balls_balls_colls(balls, dt)
    yield from calculate_platforms_walls_colls(platforms, walls, dt)
    yield from calculate_balls_walls_colls(balls, walls, dt)
    yield from calculate_balls_platforms_colls(balls, platforms, dt)
    yield from calculate_balls_blocks_colls(balls, blocks, dt)


def calculate_balls_blocks_colls(balls: List[Ball], blocks: List[Block], dt: float) -> Iterable[CollisionBallBlock]:
    for ball, block in product(balls, blocks):
        yield from calculate_ball_block_colls(ball, block, dt)


def calculate_balls_platforms_colls(balls: List[Ball], platforms: List[Platform], dt: float) -> Iterable[CollisionBallPlatform]:
    for ball, platform in product(balls, platforms):
        yield from calculate_ball_platform_colls(ball, platform, dt)


def calculate_balls_walls_colls(balls: List[Ball], walls: List[Wall], dt: float) -> Iterable[CollisionBallWall]:
    for ball, wall in product(balls, walls):
        yield from calculate_ball_wall_colls(ball, wall, dt)


def calculate_platforms_walls_colls(platforms: List[Platform], walls: List[Wall], dt: float) -> Iterable[CollisionPlatformWall]:
    for platform, wall in product(platforms, walls):
        yield from calculate_platform_wall_colls(platform, wall, dt)


def calculate_balls_balls_colls(balls: List[Ball], dt: float) -> Iterable[CollisionBallBall]:
    for ball1, ball2 in combinations(balls, 2):
        yield from calculate_ball_ball_colls(ball1, ball2, dt)


def calculate_ball_block_colls(ball: Ball, block: Block, dt: float) -> Iterable[CollisionBallBlock]:
    ball_radius = ball.radius
    ball_bp, ball_ep = ball.fake_update(dt)

    w, h = block.rect.w, block.rect.h
    diag = (w ** 2 + h ** 2) ** 0.5
    min_dist = (diag / 2 + ball.radius +
                ball.speed * dt)

    dist = (block.rect.center - ball.rect.center).norm()

    if dist > min_dist + EPS:
        return

    is_coll, point = False, None
    is_coll, point = collide_circle_rect(ball_ep, 
                                         block.rect, ball_radius)

    if not is_coll:
        is_coll, point = collide_thick_segment_rect(
            [ball_bp, ball_ep],
            block.rect,
            ball_radius,
        )

    if is_coll:
        yield CollisionBallBlock(
            point=point,
            ball=ball,
            block=block,
        )


def calculate_ball_platform_colls(ball: Ball, platform: Platform, dt: float) -> Iterable[CollisionBallPlatform]:
    ball_radius = ball.radius
    ball_bp, ball_ep = ball.fake_update(dt)
    b_rect, e_rect = platform.fake_update(dt)

    if ball.thrown:
        is_coll, point = False, None
        for circle, rect in product([ball_bp, ball_ep], [b_rect, e_rect]):
            is_coll, point = collide_circle_rect(circle, rect, ball_radius)

            if is_coll:
                break

        if not is_coll:
            for rect in [b_rect, e_rect]:
                is_coll, point = collide_thick_segment_rect(
                    [ball_bp, ball_ep],
                    rect,
                    ball_radius
                )

        if is_coll:
            yield CollisionBallPlatform(
                point=point,
                ball=ball,
                platform=platform,
            )


def calculate_ball_wall_colls(ball: Ball, wall: Wall, dt: float) -> Iterable[CollisionBallWall]:
    ball_bp, ball_ep = ball.fake_update(dt)
    begin_circle = Circle(center=ball_bp, radius=ball.radius)
    end_circle = Circle(center=ball_ep, radius=ball.radius)

    ball_coll_rect = begin_circle.bounding_box.union(end_circle.bounding_box)


    if ball_coll_rect.is_intersected(wall.rect):
        if end_circle.bounding_box.is_intersected(wall.rect):
            coll_rect = intersect_rects(end_circle.bounding_box, wall.rect)
        else:
            coll_rect = intersect_rects(ball_coll_rect, wall.rect)

        yield CollisionBallWall(
            point=coll_rect.center,
            ball=ball,
            wall=wall,
        )

def intersect_rects(r1: Rectangle, r2: Rectangle) -> Rectangle:
    left = max(r1.left, r2.left)
    right = min(r1.right, r2.right)
    top = max(r1.top, r2.top)
    bottom = min(r1.bottom, r2.bottom)

    right = max(left, right)
    bottom = max(top, bottom)

    return Rectangle(
        left=left,
        top=top,
        width=right-left,
        height=bottom-top,
    )


def calculate_platform_wall_colls(platform: Platform, wall: Wall, dt: float) -> Iterable[CollisionPlatformWall]:
    b_rect, e_rect = platform.fake_update(dt)
    platform_coll_rect = b_rect.union(e_rect)

    if platform_coll_rect.is_intersected(wall.rect):
        coll_rect = intersect_rects(platform_coll_rect, wall.rect)

        yield CollisionPlatformWall(
            point=coll_rect.center,
            platform=platform,
            wall=wall,
        )


def calculate_ball_ball_colls(ball1: Ball, ball2: Ball, dt: float) -> Iterable[CollisionBallBall]:
    radius = ball1.radius
    s1, f1 = ball1.fake_update(dt)
    s2, f2 = ball2.fake_update(dt)

    is_coll, point = False, None
    # is_coll, point = collide_circle_circle(f1, f2, radius)

    if not is_coll:
        v1 = f1 - s1
        v2 = f2 - s2
        a = s1 - s2
        b = v1 - v2

        t = -a.scalar(b)
        t = max(0, min(t, b.norm2()))

        shift = a * b.norm2() + b * t

        if shift.norm2() < ((2 * radius - EPS) * b.norm2()) ** 2:
            is_coll, point = True, (f1 + f2) / 2

    # if not is_coll:
    #     is_coll, point = collide_circle_circle(s1, f2, radius)

    # if not is_coll:
    #     is_coll, point = collide_circle_circle(f1, s2, radius)

    # if not is_coll:
    #     is_coll, point = collide_circle_circle(f1, f2, radius)

    if is_coll:
        yield CollisionBallBall(
            ball1=ball1,
            ball2=ball2,
            point=point,
        )


def norm(vec):
    # return vec.norm()
    result = 0

    result = sum(item ** 2 for item in vec) ** 0.5

    return result


def normalize(vec):
    # return vec / vec.norm()
    mod_vec = norm(vec)

    result_vec = [item / mod_vec for item in vec]

    return result_vec


def sum_vec(a, b):
    # return a + b
    result = [a[i] + b[i] for i in range(2)]

    return result


def make_line(p1, p2):
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = - a * p1[0] - b * p1[1]

    return [a, b, c]


def place_in_line(line, point):
    result = line[0] * point[0] + line[1] * point[1] + line[2]

    return result


def collide_seg_seg(first, second):
    first_line = make_line(*first)
    second_line = make_line(*second)

    first_place_in = [place_in_line(first_line, second[i]) for i in range(2)]
    second_place_in = [place_in_line(second_line, first[i]) for i in range(2)]

    result = False
    if (first_place_in[0] * first_place_in[1] < 0 and
        second_place_in[0] * second_place_in[1] < 0):
        result = True

    return result, [0, 0]


def collide_thick_segment_rect(segment, rect, thick):
    vec = [segment[1][i] - segment[0][i] for i in range(2)]
    if norm(vec) < EPS:
        return False, None
    vec = normalize(vec)

    rect_segs = []
    xs = [rect.left, rect.right]
    ys = [rect.bottom, rect.top]
    rect_segs.append([[xs[0], ys[0]], [xs[0], ys[1]]])
    rect_segs.append([[xs[0], ys[0]], [xs[1], ys[0]]])
    rect_segs.append([[xs[1], ys[1]], [xs[0], ys[1]]])
    rect_segs.append([[xs[1], ys[1]], [xs[1], ys[0]]])

    seg_segs = []
    normal = [vec[1] * thick, -vec[0] * thick]
    tps = [sum_vec(segment[i], normal) for i in range(2)]

    normal = [-item for item in normal]
    bps = [sum_vec(segment[i], normal) for i in range(2)]

    seg_segs.append([bps[0], bps[1]])
    seg_segs.append([tps[0], tps[1]])
    seg_segs.append([bps[0], tps[0]])
    seg_segs.append([bps[1], tps[1]])
    # seg_segs.append([[bps[0], tps[0]], [bps[0], [tps[1]]]])
    # seg_segs.append([[bps[0], tps[0]], [bps[1], [tps[0]]]])
    # seg_segs.append([[bps[1], tps[1]], [bps[0], [tps[1]]]])
    # seg_segs.append([[bps[1], tps[1]], [bps[1], [tps[0]]]])

    result = False
    for rect_seg, seg_seg in product(rect_segs, seg_segs):
        result, coll_point = collide_seg_seg(rect_seg, seg_seg)
        if result:
            break

    if not result:
        return False, None

    return True, Point.from_list(coll_point)


def collide_circle_rect(circle, rect, radius):
    coll_point = None
    if rect.left < circle[0] < rect.right:
        if math.fabs(circle[1] - rect.top) < radius:
            coll_point = [circle[0], rect.top]
        elif math.fabs(circle[1] - rect.bottom) < radius:
            coll_point = [circle[0], rect.bottom]
    elif rect.top < circle[1] < rect.bottom:
        if math.fabs(circle[0] - rect.left) < radius:
            coll_point = [rect.left, circle[1]]
        elif math.fabs(circle[0] - rect.right) < radius:
            coll_point = [rect.right, circle[1]]
    else:

        for side_1 in [rect.left, rect.right]:
            for side_2 in [rect.top, rect.bottom]:
                if is_point_in_circle((side_1, side_2), circle, radius):
                    coll_point = [side_1, side_2]

    if coll_point is None:
        return False, None

    return True, Point.from_list(coll_point)


def is_point_in_circle(point, circle, radius) -> bool:
    dist2 = (circle[0] - point[0])**2 + (circle[1] - point[1])**2

    return dist2 < radius**2


def collide_circle_circle(p1, p2, radius):
    shift = p2 - p1
    if shift.norm2() < (2 * radius - EPS) ** 2:
        return True, p1 + shift / 2

    return False, None
