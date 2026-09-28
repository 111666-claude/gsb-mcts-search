"""蒙特卡洛树搜索（UCB1 + 随机对局），只用标准库。

缺陷：选择时只用平均收益（没有 UCB1 的探索项），回传也只更新叶子，没沿路径累加。
"""

import math
import random


class MctsError(ValueError):
    """输入不合法。缺陷：不带局面信息。"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def moves(pile):
    """一次可拿 1..3 根火柴，拿最后一根的人赢。"""
    return [take for take in (1, 2, 3) if take <= pile]


def winner_for(pile):
    """标准玩法：pile % 4 != 0 时先手必胜。"""
    return pile % 4 != 0


def minimax_winning_move(pile):
    """用极小化极大找必胜手；没有就返回 None。"""
    for take in moves(pile):
        rest = pile - take
        if rest == 0:
            return take
        if minimax_winning_move(rest) is None:
            return take
    return None


class Node:
    def __init__(self, pile):
        self.pile = pile
        self.children = {}
        self.visits = 0
        self.value = 0.0


def _playout(pile, rng):
    """随机对局，返回先手是否获胜。"""
    turn = True
    while pile > 0:
        take = rng.choice(moves(pile))
        pile -= take
        if pile == 0:
            return turn
        turn = not turn
    return False


def search(pile, iterations, seed=1):
    """跑 MCTS，返回根节点与访问分布。"""
    if pile <= 0 or iterations <= 0:
        raise MctsError("局面与迭代次数都必须为正")
    rng = random.Random(seed)
    root = Node(pile)
    for take in moves(pile):
        root.children[take] = Node(pile - take)
    for _ in range(iterations):
        # 缺陷：只用平均收益挑孩子，没有 UCB1 的探索项
        best_take, best_node = None, None
        for take in sorted(root.children):
            child = root.children[take]
            score = child.value / child.visits if child.visits else 0.0
            if best_node is None or score > best_node:
                best_take, best_node = take, score
        child = root.children[best_take]
        child.visits += 1
        won = _playout(child.pile, rng)
        # 缺陷：只更新叶子，没有沿路径回传
        if won:
            child.value += 1.0
    return root


def best_move(root):
    """取访问次数最多的动作。"""
    best_take, best_visits = None, -1
    for take in sorted(root.children):
        if root.children[take].visits > best_visits:
            best_take, best_visits = take, root.children[take].visits
    return best_take
