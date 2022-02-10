import enum
import math
from itertools import product

from .dtos import CollisionType

EPS = 1e-4


class Collision:
    def __init__(self, coll_type, point, block=None):
        self.block = block
        self.type = coll_type
        self.point = point

    def __str__(self):
        result = str(self.type) + "  " + str(self.point)
        return result

    def __repr__(self):
        result = str(self.type) + "  " + str(self.point)
        return result

def calculate_colls(wall_rect, platform, ball, blocks, dt):
    ball_radius = ball.radius
    ball_bp, ball_ep = ball.fake_update(dt)
    ball_vec = [ball_ep[i] - ball_bp[i] for i in range(2)]
    b_rect, e_rect = platform.fake_update(dt)

    colls = []

    # Проверка на коллизии шар/блоки
    for block in blocks:
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
            coll = Collision(
                coll_type=CollisionType.BALL_BLOCK,
                point=point,
                block=block,
            )
            colls.append(coll)

    # Проверка на коллизии шар/платформа
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
            coll = Collision(
                coll_type=CollisionType.BALL_PLATFORM,
                point=point,
            )
            colls.append(coll)

    # Проверка на коллизии шар/стены
    is_coll, point = False, None
    if ball_ep[0] - ball_radius < wall_rect.left:
        is_coll, point = True, [wall_rect.left, ball_ep[1]]

    if ball_ep[0] + ball_radius > wall_rect.right:
        is_coll, point = True, [wall_rect.right, ball_ep[1]]

    if ball_ep[1] - ball_radius < wall_rect.top:
        is_coll, point = True, [ball_ep[0], wall_rect.top]

    # if ball_ep[1] + ball_radius > wall_rect.bottom:
    #     is_coll, point = True, [ball_ep[0], wall_rect.bottom]

    if is_coll:
        coll = Collision(
            coll_type=CollisionType.BALL_WALL,
            point=point,
        )
        colls.append(coll)

    # Проверка на коллизии платформа/стены 
    is_coll, point = False, None
    if e_rect.left <= wall_rect.left:
        is_coll = True
        point = [wall_rect.left, platform.rect.centery]

    if e_rect.right >= wall_rect.right:
        is_coll = True
        point = [wall_rect.right, platform.rect.centery]

    if is_coll:
        coll = Collision(
            coll_type=CollisionType.PLATFORM_WALL,
            point=point,
        )
        colls.append(coll)

    return colls

def norm(vec):
    result = 0

    result = sum(item ** 2 for item in vec) ** 0.5

    return result

def normalize(vec):
    mod_vec = norm(vec)

    result_vec = [item / mod_vec for item in vec]

    return result_vec

def sum_vec(a, b):
    result = [a[i] + b[i] for i in range(min(len(a), len(b)))]

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

    return result, None

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
        result, _ = collide_seg_seg(rect_seg, seg_seg)
        if result:
            break

    return result, None

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
        temp_func = lambda circle, point: True if (
            ((circle[0] - point[0])**2 + (circle[1] - point[1])**2) ** 0.5 < radius 
        ) else False

        for side_1 in [rect.left, rect.right]:
            for side_2 in [rect.top, rect.bottom]:
                if temp_func(circle, (side_1, side_2)):
                    coll_point = [side_1, side_2]

    return coll_point is not None, coll_point
