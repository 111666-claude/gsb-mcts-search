import unittest

from mctssearch.mcts import MctsError, best_move, minimax_winning_move, moves, search


class RuleTest(unittest.TestCase):
    def test_moves_are_bounded_by_pile(self):
        self.assertEqual(moves(2), [1, 2])
        self.assertEqual(moves(5), [1, 2, 3])

    def test_minimax_on_small_piles(self):
        self.assertIsNone(minimax_winning_move(4))
        self.assertEqual(minimax_winning_move(1), 1)

    def test_bad_input(self):
        with self.assertRaises(MctsError):
            search(0, 10)
        with self.assertRaises(MctsError):
            search(5, 0)


class SearchTest(unittest.TestCase):
    def test_returns_children(self):
        root = search(5, 50, seed=2)
        self.assertEqual(sorted(root.children), [1, 2, 3])

    def test_best_move_is_a_legal_move(self):
        root = search(5, 50, seed=3)
        self.assertIn(best_move(root), moves(5))

    def test_same_seed_same_result(self):
        first = search(6, 100, seed=5)
        second = search(6, 100, seed=5)
        self.assertEqual([first.children[t].visits for t in sorted(first.children)],
                         [second.children[t].visits for t in sorted(second.children)])


if __name__ == "__main__":
    unittest.main()
