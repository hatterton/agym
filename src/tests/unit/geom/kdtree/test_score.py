import pytest

from agym.games.breakout.geom.kdtree.scores import get_score


@pytest.mark.kdtree
@pytest.mark.score
class TestScores:
    def test_balance(self):
        l, m, r = 10, 0, 10
        assert get_score(l, m, r) > get_score(l + 1, m, r - 1)
        assert get_score(l, m, r) > get_score(l - 1, m, r + 1)

        l, m, r = 10, 0, 0
        assert get_score(l, m, r) < get_score(l - 1, m, r + 1)

        l, m, r = 0, 0, 10
        assert get_score(l, m, r) < get_score(l + 1, m, r - 1)

    def test_load(self):
        l, m, r = 10, 1, 10
        assert get_score(l, m, r) > get_score(l, m + 1, r - 1)
        assert get_score(l, m, r) > get_score(l - 1, m + 1, r)
        assert get_score(l, m, r) < get_score(l, m - 1, r + 1)
        assert get_score(l, m, r) < get_score(l + 1, m - 1, r)

    def test_load_balance_tradeoff(self):
        l1, m1, r1 = 10, 10, 20
        l2, m2, r2 = 33, 2, 5

        alpha = 0.2
        assert get_score(l1, m1, r1, alpha=alpha) > get_score(
            l2, m2, r2, alpha=alpha
        )

        alpha = 0.8
        assert get_score(l1, m1, r1, alpha=alpha) < get_score(
            l2, m2, r2, alpha=alpha
        )
