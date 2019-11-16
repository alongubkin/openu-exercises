import numpy as np
from hopfield_network import HopfieldNetwork


# In a preferences matrix each row represents a woman; specifically, list of her preferences.
# For example, in the following example the first woman ranked man #4 in the second place.
PREFERENCES_MATRIX = np.array([
  [8, 4, 9, 1, 6, 0, 3, 7, 2, 5],
  [5, 0, 6, 8, 1, 9, 7, 2, 4, 3],
  [5, 9, 4, 3, 0, 8, 6, 1, 2, 7],
  [7, 6, 3, 5, 2, 8, 1, 9, 0, 4],
  [3, 2, 9, 0, 6, 7, 8, 5, 1, 4],
  [6, 7, 8, 5, 3, 0, 1, 4, 9, 2],
  [3, 4, 7, 0, 2, 6, 1, 5, 8, 9],
  [8, 7, 9, 4, 6, 0, 3, 5, 2, 1],
  [1, 0, 6, 3, 5, 9, 4, 8, 7, 2],
  [2, 3, 9, 6, 4, 8, 7, 5, 1, 0]
])

# Amount of times to run the network for stats
STATS_RUNS = 100


def average_preference_distance(matching):
  """
  Calculate the average distance between a woman's first preference to
  the man she was matched with.
  """
  return np.average([np.where(woman == matching[i])[0][0] 
    for i, woman in enumerate(PREFERENCES_MATRIX)])
    

def stats():
  scores = []

  for _ in range(STATS_RUNS):
    network = HopfieldNetwork(PREFERENCES_MATRIX)
    matching = network.predict()

    if matching is not None:
      scores.append(average_preference_distance(matching))

  return len(scores), np.average(scores)


def main():
  # Print the preferences matrix
  print('Testing with the following preferences matrix:\n')
  print('\t{}\n'.format('\t'.join(str(PREFERENCES_MATRIX).splitlines(True))))

  # Run the network one time and print the matching if found
  print('Running the network...\n')
  network = HopfieldNetwork(PREFERENCES_MATRIX)
  matching = network.predict()

  if matching is None:
    print('\tNo stable matching was found after {} iterations. Run again.'.format(network.max_iterations))
  else:
    print('\tMatching:', matching)
    print('\tAverage distance from a woman\'s first preference:', 
      average_preference_distance(matching))

  # Print network stats
  print('\nCalculating network stats... (this might take some time)\n')
  successful_runs, average_distance = stats()

  print('\tSuccessful runs: {}/{}'.format(successful_runs, STATS_RUNS))
  print('\tAverage distance from a woman\'s first preference in successful runs:', average_distance)

if __name__ == '__main__':
  main()