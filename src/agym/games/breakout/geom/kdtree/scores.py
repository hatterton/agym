
def get_score(l: int, m: int, r: int, alpha: float = 0.5) -> float:
    return alpha * get_load_score(l, m, r) + (1 - alpha) * get_gini_score(l, r)


def get_gini_score(l: int, r: int) -> float:
    n = l + r
    score =  4 * l * r / n**2

    return score


def get_load_score(l: int, m: int, r: int) -> float:
    n = l + m + r
    score = 1 - 4 * (l + r) * m / n**2

    return score
