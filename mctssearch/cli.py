"""命令行入口：在 Nim 上跑 MCTS。"""

import argparse
import sys

from .mcts import MctsError, best_move, minimax_winning_move, search


def build_parser():
    parser = argparse.ArgumentParser(prog="mcts-search", description="UCB1 树搜索")
    parser.add_argument("--pile", type=int, default=7, help="初始火柴数")
    parser.add_argument("--iterations", type=int, default=500, help="模拟次数")
    parser.add_argument("--seed", type=int, default=1, help="随机种子")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        root = search(args.pile, args.iterations, args.seed)
    except MctsError as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1
    move = best_move(root)
    target = minimax_winning_move(args.pile)
    visits = ",".join("%d:%d" % (take, root.children[take].visits) for take in sorted(root.children))
    print("best=%s winning=%s minimax=%s" % (move, move == target, target))
    print("visits=%s" % visits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
