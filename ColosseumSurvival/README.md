# AI Game Agent Colosseum Survival using Monte Carlo Simulations
Colosseum Survival AI Game Agent using MCTS for the COMP424 project (Fall 2023).

![Gameboard](Colosseum-Survival-main/Gameboard.png)
<img src="https://github.com/LeenaJannatipour/My-Portfolio/blob/da63039a0975c7e60cbc1017fec3d9795da95b7a/ColosseumSurvival/Colosseum-Survival-main/Gameboard.png)" width="48">

## The Game

Colosseum Survival is a 2-player turn-based strategy game in which two players move in an M x M chessboard and put barriers around them until they are separated in two closed zones. M can have any value greater than 1. Each player will try to maximize the number of blocks in its zone to win the game. Sample game board and gameplay can be found in [Gameboard](Gameboard.png) and [Gameplay](Gameplay.gif) respectively. Our AI agent can be found here: [Student Agent](agents/student_agent.py)

## Playing a game

To start playing a game, we will run the simulator and specify which agents should complete against eachother. To start, several agents are given to you, and you will add your own following the same game interface. For example, to play the game using two copies of the provided random agent (which takes a random action every turn), run the following:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent
```

This will spawn a random game board of size NxN, and run the two agents of class [RandomAgent](agents/random_agent.py). You will be able to see their moves in the console.

## Visualizing a game

To visualize the moves within a game, use the `--display` flag. You can set the delay (in seconds) using `--display_delay` argument to better visualize the steps the agents take to win a game.

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --display
```

## Play on your own!

To take control of one side of the game and compete against the random agent yourself, use a [`human_agent`](agents/human_agent.py) to play the game.

```bash
python simulator.py --player_1 human_agent --player_2 random_agent --display
```



