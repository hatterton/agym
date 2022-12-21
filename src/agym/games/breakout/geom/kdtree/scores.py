def get_score(l: int, m: int, r: int, alpha: float = 0.5) -> float:
    return alpha * get_load_score(l, m, r) + (1 - alpha) * get_gini_score(
        l, m, r
    )


def get_gini_score(l: int, m: int, r: int) -> float:
    n = l + m + r

    score = 4 * l * r / (n * n)

    return score


def get_load_score(l: int, m: int, r: int) -> float:
    n = l + m + r
    score = 1 - m / n

    return score
