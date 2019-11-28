import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors

DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


with gzip.open('mnist.pkl.gz', 'rb') as f:
  u = pickle._Unpickler(f)
  u.encoding = 'latin1'
  train_set, valid_set, test_set = u.load()

# separete to data and labels:
x_train, y_train = train_set
x_test, y_test = test_set


def show_digits_histogram():
  # The first bin is [0, 1), the second bin is [1, 2), etc. 
  # 10 is added so that the last bin will be [9, 10).
  bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

  hist_train, _ = np.histogram(y_train, bins=bins)
  hist_test, _ = np.histogram(y_test, bins=bins)
  
  digits_histogram = dict(zip(DIGITS, hist_train + hist_test))

  plt.bar(range(len(digits_histogram)), list(digits_histogram.values()), align='center')
  # plt.ylim([1, 0.97])
  plt.xticks(range(len(digits_histogram)), list(digits_histogram.keys()))
  plt.show()


def show_first_images():
  fig = plt.figure(figsize=(8, 8))
  columns = 4
  rows = 3
  for i in range(1, columns * rows + 1):
      img = np.reshape(x_train[i - 1], (28, 28))
      fig.add_subplot(rows, columns, i)
      plt.imshow(img)

  plt.show()


def measure_knn_performance():
  k_performance = {}
  for k in range(1, 11):
    print('Testing KNN calssifier with k = ', k)
    clf = neighbors.KNeighborsClassifier(k, weights='distance')
    clf.fit(x_train, y_train)
    k_performance[k] = clf.score(x_test, y_test)

    print(' -> Score:', k_performance[k])

  print('Result:')
  print(k_performance)
  
  plt.bar(range(len(k_performance)), list(k_performance.values()), align='center')
  plt.ylim([0.96, 0.97])
  plt.xticks(range(len(k_performance)), list(k_performance.keys()))
  plt.show()


def check_knn_even_k():
  # Choose 2 points from the training set and fit two kNN on them in different dataset order 
  #  (k=2)
  clf1 = neighbors.KNeighborsClassifier(n_neighbors=2, weights='distance')
  clf2 = neighbors.KNeighborsClassifier(n_neighbors=2, weights='distance')
  clf1.fit([x_train[0], x_train[1]], [y_train[0], y_train[1]])
  clf2.fit([x_train[1], x_train[0]], [y_train[1], y_train[0]])

  # Some sanity checks
  assert clf1.predict([x_train[0]]) == clf2.predict([x_train[0]]) == y_train[0]
  assert clf1.predict([x_train[1]]) == clf2.predict([x_train[1]]) == y_train[1]
  
  # Calculate midpoint and make sure its distance is the same from every neighbor
  midpoint = (x_train[0] + x_train[1]) / 2

  (distances1,), _ = clf1.kneighbors(np.array([midpoint]))
  (distances2,), _ = clf2.kneighbors(np.array([midpoint]))
  assert distances1[0] == distances1[1] == distances2[0] == distances2[1]

  # Print predictions
  print('First kNN dataset order (y):', [y_train[0], y_train[1]],
    'Prediction of midpoint:', clf1.predict([midpoint])[0])
  print('Second kNN dataset order (y):', [y_train[1], y_train[0]],
    'Prediction of midpoint:', clf2.predict([midpoint])[0])

  # y_train[1] < y_train[0], therefore the prediction of both kNNs is y_train[1]. 
  # Try to run this with y_train[1] = 13 and see what happens.


def main():
  print('Showing digits histogram...')
  show_digits_histogram()

  print('First 12 digits in train set:', y_train[0:12], '- Showing them as images...')
  show_first_images()

  print('Measuring KNN performance on the dataset...')
  measure_knn_performance()

  print('Checking what happens with even k')
  check_knn_even_k()

if __name__ == '__main__':
  main()