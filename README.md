# mcts-search

蒙特卡洛树搜索（UCB1 + 随机对局 + 回传），只在 Nim 上演示，用 Python 标准库。

```
python3 -m mctssearch.cli --pile 7 --iterations 500 --seed 1
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **选择公式要用 UCB1**：`value/visits + c * sqrt(ln(parent_visits) / visits)`（c 取 1.4 左右），
  没访问过的孩子优先。现在只用平均收益，所有孩子并列时永远挑第一个：
  `--pile 7 --iterations 500` 给 `visits=500,0,0`，按口径三个动作都该被访问到（每个 ≥ 50 次）。
- **回传要沿路径累加**：一次模拟结束后，把胜负从叶子一路加回根（父节点 visits 与 value 都要更新）。
  现在只更新叶子，根孩子的平均收益全是 0。
- 胜负判定：`--pile 7` 时先手必胜（Nim 的标准结论），MCTS 给出的 `best` 必须等于
  `minimax_winning_move(7)`（也就是 3）；`--pile 4` 时先手必败，`minimax` 给 None，
  MCTS 不能选出「胜率最高」的假象来（要如实反映）。
- 确定性：同一个 `--seed` 重复运行给出完全相同的访问分布与 best。
- 不变量：任何时刻所有孩子的访问次数之和等于模拟次数；每个孩子的 value ≤ visits；
  每次模拟都是合法对局（拿走的火柴数在 1..3 且不超过剩余）。
- 规模：10^5 次模拟 2 秒内跑完，内存 O(树上节点数)；不许每次模拟都重建整棵树。

## 现在的行为

- 选择只用 `child.value / child.visits`（没访问过按 0），并列取第一个 → 只访问一个孩子。
- 模拟结束只更新叶子节点的 visits 与 value，根节点的统计永远停在 0。
- 因此 `--pile 7` 给 `best=1 winning=false visits=500,0,0`（正确是 `best=3`）。

## 计划新增的能力

```
--pile N         初始火柴数
--iterations N   模拟次数
--seed N         随机种子
```

## 输出

```
best=3 winning=true minimax=3
visits=180,140,180
```

## 目录

```
mctssearch/mcts.py   UCB1 与对局
mctssearch/cli.py    命令行入口
tests/               unittest 用例
```
