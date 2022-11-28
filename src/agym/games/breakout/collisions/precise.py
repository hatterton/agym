from typing import Optional

from agym.games.breakout.dtos import Ball, CollisionBallBall

EPS = 1e-4


def calculate_ball_ball_colls(
    ball1: Ball, ball2: Ball, dt: float
) -> Optional[CollisionBallBall]:
    radius = ball1.radius
    s1, f1 = ball1.fake_update(dt)
    s2, f2 = ball2.fake_update(dt)

    v1 = f1 - s1
    v2 = f2 - s2
    a = s1 - s2
    b = v1 - v2

    t = -a.scalar(b)
    t = max(0, min(t, b.norm2()))

    shift = a * b.norm2() + b * t

    if shift.norm2() < ((2 * radius - EPS) * b.norm2()) ** 2:
        point = (f1 + f2) / 2

        return CollisionBallBall(
            ball1=ball1,
            ball2=ball2,
            point=point,
        )

    return None
