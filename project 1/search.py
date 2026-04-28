# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # Khởi tạo Stack để chứa các node (state, path_to_state)
    fringe = util.Stack()
    
    # Danh sách các state đã khám phá để tránh lặp (Graph Search)
    visited = set()
    
    # Đẩy trạng thái bắt đầu và danh sách hành động trống vào fringe
    start_state = problem.getStartState()
    fringe.push((start_state, []))
    
    while not fringe.isEmpty():
        # Lấy node hiện tại ra khỏi fringe
        current_state, actions = fringe.pop()
        
        # Nếu đã đến đích, trả về danh sách các hành động
        if problem.isGoalState(current_state):
            return actions
            
        # Kiểm tra nếu state chưa được khám phá (Graph Search)
        if current_state not in visited:
            visited.add(current_state)
            
            # Lấy các successor (trạng thái kế tiếp, hành động, chi phí)
            successors = problem.getSuccessors(current_state)
            
            for successor_state, action, cost in successors:
                if successor_state not in visited:
                    # Tạo đường đi mới bằng cách cộng thêm hành động hiện tại
                    new_actions = actions + [action]
                    fringe.push((successor_state, new_actions))
                    
    return [] # Trả về trống nếu không tìm thấy đường đi

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # Khởi tạo Queue cho BFS (FIFO) [cite: 65]
    fringe = util.Queue()
    
    # Tập hợp lưu các trạng thái đã khám phá (Graph Search) 
    visited = []
    
    # Đẩy trạng thái bắt đầu và danh sách hành động trống vào fringe [cite: 62]
    start_state = problem.getStartState()
    fringe.push((start_state, []))
    
    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        
        # Kiểm tra nếu đã đạt trạng thái đích [cite: 63]
        if problem.isGoalState(current_state):
            return actions
            
        # Chỉ mở rộng nếu trạng thái này chưa từng được khám phá 
        if current_state not in visited:
            visited.append(current_state)
            
            successors = problem.getSuccessors(current_state)
            for successor_state, action, cost in successors:
                if successor_state not in visited:
                    # Lưu đường đi mới cùng với trạng thái kế tiếp [cite: 376]
                    new_actions = actions + [action]
                    fringe.push((successor_state, new_actions))
                    
    return []

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Khởi tạo PriorityQueue để lưu trữ (trạng thái, danh sách hành động, chi phí tích lũy)
    # Ưu tiên dựa trên chi phí tích lũy thấp nhất
    fringe = util.PriorityQueue()
    
    # Tập hợp lưu các trạng thái đã khám phá (Graph Search)
    visited = {}
    
    # Đẩy trạng thái bắt đầu vào fringe với chi phí là 0
    start_state = problem.getStartState()
    fringe.push((start_state, [], 0), 0)
    
    while not fringe.isEmpty():
        # Lấy nút có chi phí thấp nhất ra khỏi fringe
        current_state, actions, current_cost = fringe.pop()
        
        # Nếu đã đến đích, trả về danh sách các hành động
        if problem.isGoalState(current_state):
            return actions
            
        # Kiểm tra Graph Search
        # Trong UCS, ta chỉ mở rộng nếu chưa thăm hoặc tìm thấy đường đi rẻ hơn
        if (current_state not in visited) or (current_cost < visited[current_state]):
            visited[current_state] = current_cost
            
            successors = problem.getSuccessors(current_state)
            for successor_state, action, step_cost in successors:
                new_actions = actions + [action]
                new_cost = current_cost + step_cost
                # Đẩy vào PriorityQueue với ưu tiên là tổng chi phí mới
                fringe.update((successor_state, new_actions, new_cost), new_cost)
                    
    return []

    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
