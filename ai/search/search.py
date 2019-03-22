# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

class Node(object):
  def __init__(self, state, path=[], path_cost=0):
    self.state = state
    self.path = path
    self.path_cost = path_cost

def graphSearch(problem, frontier):
  if problem.isGoalState(problem.getStartState()):
    return []
  
  frontier_lookup_table = {}

  # Add the initial node to the frontier.
  initial_node = Node(problem.getStartState())
  frontier.push(initial_node)
  frontier_lookup_table[initial_node.state] = initial_node

  # A set that remembers every expanded node
  explored = []

  while not frontier.isEmpty():
    # Choose a leaf node and remove it from the frontier.
    node = frontier.pop()

    if node.state in explored:
      continue

    # Check if the chosen node contains a goal state.
    # NOTE: When steps costs are ignored, like in BFS and DFS, it would be more efficient to check this
    #   when the node is first generated, rather than before it is selected for expansion.
    if problem.isGoalState(node.state):
      return node.path
    
    explored.append(node.state)

    # Expand the chosen node.
    for child_state, action, step_cost in problem.getSuccessors(node.state):
      child = Node(state=child_state, 
                   path=node.path + [action],
                   path_cost=node.path_cost + step_cost)

      # Add the child node to the frontier if it wasn't visited and wasn't already there.
      if child.state not in explored and child.state not in frontier_lookup_table:
        frontier.push(child)
        frontier_lookup_table[child.state] = child

      # If a better path is found to a node currently on the frontier, update it.    
      # NOTE: This is not really relevant when steps costs are ignored, like in BFS and DFS.
      elif frontier_lookup_table[child.state].path_cost > child.path_cost:
        frontier_lookup_table[child.state].path = child.path
        frontier_lookup_table[child.state].path_cost = child.path_cost

  raise Exception('No solution to the search problem was found.')
  
def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  return graphSearch(problem, util.Stack())

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  return graphSearch(problem, util.Queue())
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  cost = lambda node: problem.getCostOfActions(node.path[1:])
  return graphSearch(problem, util.PriorityQueueWithFunction(cost))

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  cost = lambda node: problem.getCostOfActions(node.path) + heuristic(node.state, problem)
  return graphSearch(problem, util.PriorityQueueWithFunction(cost))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch