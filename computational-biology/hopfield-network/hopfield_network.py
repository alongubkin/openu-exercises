import numpy as np
import math

# Network hyperparameters
A = B = 100
C = 90
D = 60
SIGMA = 1

class HopfieldNetwork:
  "Specialized hopfield network for the couple matching problem."

  def __init__(self, preferences_matrix, max_iterations=10000):
    self.n = len(preferences_matrix)  # Amount of men / woman
    self.preferences_matrix = preferences_matrix
    self.network = np.zeros((self.n, self.n), dtype=np.uint8)
    self.max_iterations = max_iterations

    assert preferences_matrix.shape == (self.n, self.n), \
      "Invalid shape for preferences matrix"


  def update(self):
    # Choose a random woman w and random man m
    m = np.random.randint(0, self.n)
    w = np.random.randint(0, self.n)

    neuron = self.network[w, m]

    # Penalize networks that don't have one man for each woman (more than one 1 in a row).
    neuron -= A * np.sum([self.network[w, j] for j in range(self.n) if j != m])

    # Penalize networks that don't have one woman for each man (more than one 1 in a column).
    neuron -= B * np.sum([self.network[j, m] for j in range(self.n) if j != w])

    # Penalize networks that don't have all people present
    neuron -= C * (np.sum([self.network[y, j] 
      for y in range(self.n) for j in range(self.n)]) - (self.n + SIGMA))

    # Penalize networks with large distance between the woman's first preference and 
    # the chosen man
    neuron -= D * np.where(self.preferences_matrix[w] == m)[0][0]

    # Run activation function on the neuron
    self.network[w, m] = self.activate(neuron)

  def predict(self):
    for _ in range(self.max_iterations):
      self.update()
      if self.is_stable():
        return np.array([np.where(row == 1)[0][0] for row in self.network])

    return None

  def is_stable(self):
    # Make sure each row has exactly one 1
    if np.array([np.count_nonzero(row) != 1 for row in self.network]).any():
      return False

    # Make sure each column has exactly one 1 
    if np.array([np.count_nonzero(column) != 1 for column in self.network.T]).any():
      return False

    return True

  def activate(self, value):
    return (1 + math.tanh(3 * value)) / 2.0

