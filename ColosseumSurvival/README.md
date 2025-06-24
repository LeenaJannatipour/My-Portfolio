# AI Game Agent - Colosseum Survival
A Python agent built for the turn-based strategy game Colosseum Survival using Monte Carlo Tree Search (MCTS). Developed for McGill’s COMP424 (Fall 2023).

## The Game

Colosseum Survival is a 2-player turn-based strategy game played on an M × M grid. Players take turns placing barriers and moving until they're sealed into separate zones. The player controlling the larger zone wins. Sample game board and gameplay can be found in [Gameboard](Gameboard.png) and [Gameplay](Gameplay.gif) respectively. Our AI agent can be found here: [Student Agent](agents/student_agent.py)

## Playing a game

To simulate a game between two random agents:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent
```

To visualize a game between two random agents:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --display
```

You can adjust the speed of visualization with the --display_delay flag.

To play against an agent yourself:

```bash
python simulator.py --player_1 human_agent --player_2 random_agent --display
```

## About our AI Agent

Our custom agent uses a custom Monte Carlo Tree Search algorithm with heuristic-guided rollouts to make efficient, aggressive decisions in real time. It runs within a 2-second time limit per move and consistently beats the random agent.

Each node in the search tree represents a game state, including player positions and barriers. The agent expands the tree using valid moves and runs simulations to evaluate outcomes. To make smarter decisions, our rollouts are guided by a tracking heuristic that prioritizes enclosing the opponent and staying close to them.

We also use the UCT (Upper Confidence Tree) policy to choose which moves to explore. To avoid long simulations, each rollout is capped at 20 moves. Overall, the agent is tuned to play aggressively and take control of space early.
