# Student agent: Add your own agent here
import math
from random import shuffle
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time


class MCT_Node:
    def __init__(self, state, parent, barrier):
        self.state = state
        self.parent = parent
        self.children = []
        self.uct = 0
        self.wins = 0
        self.visited = 0
        self.barrier = barrier
        
        if parent is None:
            self.isPlayer1 = True
        else:
            self.isPlayer1 = not parent.isPlayer1
        return

    def compute_uct(self, root):
        if self is not root:
            self.uct = self.wins/self.visited + math.sqrt(2*math.log(root.visited+10)/self.visited)
        else:
            self.uct = self.wins/self.visited + math.sqrt(2*math.log(root.visited)/self.visited)


class MCT:
    def __init__(self, state, max_step):
        self.tree = MCT_Node(state, None, -1)
        self.max_step = max_step
        self.board_size = state[0].shape[0]
        self.startTime = time.time()
        if(self.board_size == 6):
            self.num_sim=20
        elif(self.board_size == 7):
            self.num_sim=20
        elif(self.board_size == 8):
            self.num_sim=15
        elif(self.board_size == 9):
            self.num_sim=8
        elif(self.board_size == 10):
            self.num_sim=5
        elif(self.board_size == 11):
            self.num_sim=3
        else:
            self.num_sim=2

    def best_action(self, state):
        self.startTime=time.time()
        chess_board = state[0]
        for i in range(state[0].shape[0]):
            for j in range(state[0].shape[1]):
                if chess_board[i, j, 0]== True and i-1>=0:
                    chess_board[i-1, j, 2] = True
                if chess_board[i, j, 1]== True and j+1<state[0].shape[1]:
                    chess_board[i, j+1,3]  = True
                if chess_board[i, j, 2]== True and i+1<state[0].shape[0]:
                    chess_board[i+1, j, 0] = True
                if chess_board[i, j, 3]== True and j-1>=0:
                    chess_board[i, j-1, 1] = True
        self.monte_carlo()
        newChild = self.bestChild(self.tree)
        return newChild.state[1], newChild.barrier
    
    def monte_carlo(self):
        leaf = self.tree
        leaf.children = self.expand(leaf)
        while time.time()-self.startTime <1.80:
            child = leaf.children[np.random.randint(0, len(leaf.children))]
            total_wins = 0
            for _ in range(self.num_sim):
                winner = self.simulate(child)
                total_wins += winner
            self.backpropagate(total_wins, child)
        

    def select(self):
        cur_node = self.tree
        cur_max_uct_node = None

        cur_node.children.sort(key=lambda child: child.uct, reverse=True)
        cur_max_uct_node = cur_node.children[0] if cur_node.children else None
        while cur_node.children:
            for child in cur_node.children:
                if (cur_max_uct_node is None or child.uct > cur_max_uct_node.uct):
                    cur_max_uct_node = child
            cur_node = cur_max_uct_node
            cur_max_uct_node = None
        
        return cur_node
    
    def expand(self, leaf):
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        child_list = self.bfs(leaf.state, self.max_step)
        
        for child in child_list:
            copy_chessboard= deepcopy(leaf.state[0])
            copy_chessboard[child[0][0], child[0][1], child[1]] = True

            if child[1] ==0 and child[0][0]-1>=0:
                new_r = child[0][0]-1
                new_bar = 2
                copy_chessboard[new_r, child[0][1], new_bar] = True
            if child[1] ==1 and child[0][1]+1<self.board_size:
                new_c = child[0][1]+1
                new_bar = 3
                copy_chessboard[child[0][0], new_c, new_bar] = True
            if child[1] ==2 and child[0][0]+1<self.board_size:
                new_r = child[0][0]+1
                new_bar = 0
                copy_chessboard[new_r, child[0][1], new_bar] = True
            if child[1] ==3  and child[0][1]-1>=0:
                new_c = child[0][1]-1
                new_bar = 1
                copy_chessboard[child[0][0], new_c, new_bar] = True
            leaf.children.append(MCT_Node((copy_chessboard, child[0], leaf.state[2]), leaf, child[1]))
        return leaf.children

    def bfs(self, state, maxsteps):
        possible_moves = []
        chess_board, my_pos, adv_pos = state

        visited = np.zeros((self.board_size, self.board_size), dtype=bool)
        visited[my_pos[0]][my_pos[1]] = True

        queue = [(my_pos, 0)]
        for i in range(4):
            if(chess_board[my_pos[0]][my_pos[1]][i] == False):
                possible_moves.append([my_pos, i])
        while queue:
            current_pos, steps = queue.pop(0)

            for move in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])

                if 0 <= new_pos[0] < self.board_size and 0 <= new_pos[1] < self.board_size and not visited[new_pos[0]][new_pos[1]] and new_pos != adv_pos:
                    if (move == (-1, 0) and not chess_board[current_pos[0]][current_pos[1]][0] and not chess_board[new_pos[0]][new_pos[1]][2]) or \
                    (move == (0, 1) and not chess_board[current_pos[0]][current_pos[1]][1] and not chess_board[new_pos[0]][new_pos[1]][3]) or \
                    (move == (1, 0) and not chess_board[current_pos[0]][current_pos[1]][2] and not chess_board[new_pos[0]][new_pos[1]][0]) or \
                    (move == (0, -1) and not chess_board[current_pos[0]][current_pos[1]][3] and not chess_board[new_pos[0]][new_pos[1]][1]):
                        visited[new_pos[0]][new_pos[1]] = True
                        for i in range(4):
                            if(not chess_board[new_pos[0]][new_pos[1]][i]):
                                possible_moves.append([new_pos, i])
                        if steps + 1 < maxsteps:
                            queue.append((new_pos, steps + 1))

        return possible_moves

    def simulate(self, child):
        node_sim = deepcopy(child)
        max_simulations = 20
        simulation_step = 0
        while simulation_step < max_simulations:
            is_endgame, winner = self.check_endgame(node_sim)
            if is_endgame:
                return winner
            simulation_step += 1
            node_sim = self.best_move(node_sim)
        return 0
            
    def backpropagate(self, winner, MCT_node):
        while MCT_node is not None:
            MCT_node.visited +=self.num_sim
            MCT_node.wins += winner
            MCT_node.compute_uct(self.tree)
            MCT_node = MCT_node.parent

    def best_move(self, node_sim):
        # Moves (Up, Right, Down, Left)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        if node_sim.isPlayer1:
            chess_board, my_pos, adv_pos = node_sim.state
        else:
            chess_board, adv_pos, my_pos = node_sim.state
        # Pick steps within allowable moves
        updated_pos = my_pos
        for _ in range(self.max_step):
            r, c = updated_pos
            allowed_dirs=[]
            for d in range(4):
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and \
                        not chess_board[r,c,d] and not adv_pos == (r, c):
                        if (abs(moves[d][0]) + abs(moves[d][1])) <= self.max_step and not chess_board[r, c, d]:
                            allowed_dirs.append(d)
            if not allowed_dirs:
                break

            random_dir = np.random.choice(allowed_dirs)
            # Update position based on heuristic move
            m_r, m_c = moves[random_dir]
            updated_pos = (r + m_r, c + m_c)

        move_towards_heuristic = self.chase_adversary(chess_board, updated_pos, adv_pos)
        if move_towards_heuristic and len(move_towards_heuristic) > 0:
            barrier_dir = move_towards_heuristic[0]
        else:
            barrier_dir = None
            valid_barrier_dirs = self.get_valid_barrier_positions(chess_board, updated_pos, adv_pos)
            if not valid_barrier_dirs:
                return node_sim
            barrier_dir = np.random.choice(valid_barrier_dirs)


        if not self.check_valid_step(node_sim.state[1], updated_pos, barrier_dir):
            return node_sim
        
        # Final portion, pick where to put our new barrier, at random
        r, c = updated_pos
        allowed_barriers=[]
        for dir in range(4):
            if not chess_board[r, c, dir] and adv_pos != (r, c):
                #To avoid enclosing barriers around student agent
                if not self.encloses_agent(updated_pos, chess_board, dir):
                    allowed_barriers.append(dir) 
        if not allowed_barriers:
            return node_sim
 
        new_chess_board = np.copy(chess_board)
        new_chess_board[r, c, barrier_dir] = True
        new_r, new_c = updated_pos

        if barrier_dir ==0:
            new_r = r-1
            new_bar = 2
            new_chess_board[new_r, c, new_bar] = True
        elif barrier_dir ==1:
            new_c = c+1
            new_bar = 3
            new_chess_board[r, new_c, new_bar] = True
        elif barrier_dir ==2:
            new_r = r+1
            new_bar = 0
            new_chess_board[new_r, c, new_bar] = True
        elif barrier_dir ==3:
            new_c = c-1
            new_bar = 1
            new_chess_board[r, new_c, new_bar] = True
        

        # Create a new child node with the updated state
        if node_sim.isPlayer1:
            child_node = MCT_Node([new_chess_board, updated_pos, adv_pos], node_sim, barrier_dir)
        else:
            child_node = MCT_Node([new_chess_board, adv_pos, updated_pos], node_sim, barrier_dir)
        node_sim.children.append(child_node)

        return child_node

    def chase_adversary(self, chess_board, my_pos, adv_pos):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        valid_moves = []
        for index, move in enumerate(moves):
            new_pos = (my_pos[0] + move[0], my_pos[1] + move[1])
            if ((0 <= new_pos[0] < self.board_size and 0 <= new_pos[1] < self.board_size and new_pos != adv_pos and (abs(move[0]) + abs(move[1]) <= self.max_step) and not chess_board[new_pos[0], new_pos[1], index])):
                valid_moves.append(moves.index(move))
        if not valid_moves:
            return []
        distances = []
        for move in valid_moves:
            distance = self.minimize_distance(new_pos, adv_pos)
            
            distances.append(distance)
        if len(distances) == 0:
            return valid_moves
        min_distance = min(distances)
        best_moves = [valid_moves[i] for i in range(len(valid_moves)) if distances[i] == min_distance]
        return best_moves

    def encloses_agent(self, pos, chess_board, barrier_dir):
    # Check if placing a barrier in the specified direction would enclose the agent
        r, c = pos
        if barrier_dir == 0 and r - 1 >= 0:
            return chess_board[r - 1, c, 2] or chess_board[r-1, c, 3] or chess_board[r,c,0]
        elif barrier_dir == 1 and c + 1 < self.board_size:
            return chess_board[r, c + 1, 3] or chess_board[r, c+1, 0] or chess_board[r,c,1]
        elif barrier_dir == 2 and r + 1 < self.board_size:
            return chess_board[r + 1, c, 0] or chess_board[r+1, c, 1] or chess_board[r,c,2]
        elif barrier_dir == 3 and c - 1 >= 0:
            return chess_board[r, c - 1, 1] or chess_board[r, c-1, 2] or chess_board[r,c,3]
        return False
    
    def get_valid_barrier_positions(self, chess_board, my_pos, adv_pos):
        #valid positions that are not self-enclosing
        valid_positions = []
        moves = [(-1,0), (0,1), (1,0), (0,-1)]

        for dir in range(4):
            cur_pos = (my_pos[0] + moves[dir][0], my_pos[1] + moves[dir][1])
            if not self.encloses_agent(cur_pos, chess_board, dir):
                valid_positions.append(dir)
        #Return list b/w 0-3 representing barrier positions of next move that are not self-enclosing
        #Return [] if all barrier positions of next move are enclosing
        return valid_positions
    
    def minimize_distance(self, sim_pos, adv_pos):
        distance = math.sqrt((adv_pos[0] - sim_pos[0]) ** 2 + (adv_pos[1] - sim_pos[1]) ** 2)
        return distance
    

    def bestChild(self, parent):
        bestChild = None

        for child in parent.children:
            if bestChild is None or bestChild.uct < child.uct:
                bestChild = child
        return bestChild

    def check_valid_step(self, start_pos, end_pos, barrier_dir):
        #True = valid step
        """
        Check if the step the agent takes is valid (reachable and within max steps).

        Parameters
        ----------
        start_pos : tuple
            The start position of the agent.
        end_pos : np.ndarray
            The end position of the agent.
        barrier_dir : int
            The direction of the barrier.
        """
        start_pos = tuple(start_pos)
        chess_board, p0_pos, p1_pos = deepcopy(self.tree.state)
        # Moves (Up, Right, Down, Left)
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # Endpoint already has barrier or is border
        new_r, new_c = end_pos
        if chess_board[new_r, new_c, barrier_dir]:
            return False
        if np.array_equal(start_pos, end_pos):
            return True


        # BFS
        state_queue = [(start_pos, 0)]
        visited = {tuple(start_pos)}
        is_reached = False
        while state_queue and not is_reached:
            cur_pos, cur_step = state_queue.pop(0)
            r, c = cur_pos
            if cur_step == self.max_step:
                break
            for dir, move in enumerate(moves):
                if chess_board[r, c, dir]:
                    continue

                next_pos = (r + move[0], c + move[1])
                if np.array_equal(next_pos, p1_pos) or tuple(next_pos) in visited:
                    continue
                if np.array_equal(next_pos, end_pos):
                    is_reached = True
                    break

                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return is_reached
    #Function from world.py
    def check_endgame(self, node_sim):
        """
        Check if the game ends and compute the current score of the agents.

        Returns
        -------
        is_endgame : bool
            Whether the game ends.
        player_1_score : int
            The score of player 1.
        player_2_score : int
            The score of player 2.
        """

        chess_board, p0_pos, p1_pos = deepcopy(node_sim.state)
        # Moves (Up, Right, Down, Left)
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # Union-Find
        father = dict()
        for r in range(chess_board.shape[0]):
            for c in range(chess_board.shape[1]):
                father[(r, c)] = (r, c)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(chess_board.shape[0]):
            for c in range(chess_board.shape[1]):
                for dir, move in enumerate(
                    moves[1:3]
                ):  # Only check down and right
                    if chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(chess_board.shape[0]):
            for c in range(chess_board.shape[1]):
                find((r, c))
        p0_r = find(tuple(p0_pos))
        p1_r = find(tuple(p1_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, -1
        if p0_score > p1_score:
            return True, 1
        else:
            return True, 0
 

@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
        self.MTC = None
      
    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        state = [chess_board, my_pos, adv_pos]
        self.MTC = MCT(state, max_step)
        next_position, barrier_dir = self.MTC.best_action(state)
        return next_position, barrier_dir
