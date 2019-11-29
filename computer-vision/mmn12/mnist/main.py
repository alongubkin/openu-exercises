import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn import neighbors
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from scipy.spatial.distance import euclidean


DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Load data set
with gzip.open('mnist.pkl.gz', 'rb') as f:
  u = pickle._Unpickler(f)
  u.encoding = 'latin1'
  train_set, valid_set, test_set = u.load()
x_train, y_train = train_set
x_test, y_test = test_set


# PART 1 - General question
def show_digits_histogram():
  # The first bin is [0, 1), the second bin is [1, 2), etc. 
  # 10 is added so that the last bin will be [9, 10).
  bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

  hist_train, _ = np.histogram(y_train, bins=bins)
  hist_test, _ = np.histogram(y_test, bins=bins)
  
  digits_histogram = dict(zip(DIGITS, hist_train + hist_test))

  plt.bar(range(len(digits_histogram)), list(digits_histogram.values()), align='center')
  plt.xticks(range(len(digits_histogram)), list(digits_histogram.keys()))
  plt.show()

# PART 1 - General question
def show_first_images():
  fig = plt.figure(figsize=(8, 8))
  columns = 4
  rows = 3
  for i in range(1, columns * rows + 1):
      img = np.reshape(x_train[i - 1], (28, 28))
      fig.add_subplot(rows, columns, i)
      plt.imshow(img, cmap='gray', interpolation='nearest')

  plt.show()

# QUESTION 1
def measure_knn_performance(x_train, y_train, x_test, y_test):
  k_performance = {}
  for k in range(1, 11):
    print('Testing KNN classifier with k = ', k)
    clf = neighbors.KNeighborsClassifier(k, weights='distance')
    clf.fit(x_train, y_train)
    k_performance[k] = clf.score(x_test, y_test)

    print(' -> Score:', k_performance[k])

  print('Result:')
  print(k_performance)
  
  plt.bar(range(len(k_performance)), list(k_performance.values()), align='center')
  plt.ylim([min(k_performance.values()) - 0.01, max(k_performance.values()) + 0.005])
  plt.xticks(range(len(k_performance)), list(k_performance.keys()))
  plt.show()

# QUESTION 1 (check KNN's behaviour with even k)
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

  
# QUESTION 2 (b - g)
def pca():
  print('Training PCA model...')
  pca = PCA()
  pca.fit(x_train)

  # -- b --
  print('Showing mean image')
  plt.figure()
  plt.imshow(pca.mean_.reshape(28, 28), cmap='gray', interpolation='nearest')
  plt.show()

  print('Showing first 6 principal components')
  fig = plt.figure(figsize=(8, 8))
  columns = 3
  rows = 2
  for i in range(1, columns * rows + 1):
    img = np.reshape(pca.components_[i - 1], (28, 28))
    fig.add_subplot(rows, columns, i)
    plt.imshow(img, cmap='gray', interpolation='nearest')
  plt.show()

  # -- c -- 
  print('Showing explained variance for each component')
  plt.plot(range(1, len(pca.explained_variance_) + 1), pca.explained_variance_)
  plt.show()

  # -- d --
  print('# Bases for 95% variance:', PCA(0.95).fit(x_train).n_components_)
  print('# Bases for 80% variance:', PCA(0.8).fit(x_train).n_components_)

  # -- e --
  print('Showing 2d transformations for each digit image')
  transformed_2d = PCA(n_components=2).fit_transform(x_train)
  plt.scatter(transformed_2d[:,0], transformed_2d[:,1], s=0.1,
    c=cm.nipy_spectral(np.linspace(0, 1, len(transformed_2d))))
  plt.show()

  # -- f --
  for dim in (2, 10, 20):
    print('Repeating question 1 with dim =', dim)
    pca2 = PCA(n_components=dim).fit(x_train)
    measure_knn_performance(pca2.transform(x_train), y_train, 
      pca2.transform(x_test), y_test)

  # -- g --
  for k in (2, 5, 10, 50, 100, 150):
    print('Showing image after transforming and inverse-transforming with for k =', k)
    pca2 = PCA(n_components=k).fit(x_train)
    img, = pca2.inverse_transform(pca2.transform([x_train[300]]))
    plt.imshow(img.reshape(28, 28), cmap='gray', interpolation='nearest')
    plt.show()


# QUESTION 2 (h)
def pca_for_each_digit():
  # Build 10 PCAs - one for each digit
  pcas = [PCA(0.95).fit([
    image for i, image in enumerate(x_train) if y_train[i] == digit
  ]) for digit in DIGITS]

  # Show first 6 principal components of each PCA
  # -- h1 --
  for digit, pca in enumerate(pcas):
    print('Showing first 6 components for digit:', digit)
    fig = plt.figure(figsize=(8, 8))
    columns = 3
    rows = 2
    for i in range(1, columns * rows + 1):
      img = np.reshape(pca.components_[i - 1], (28, 28))
      fig.add_subplot(rows, columns, i)
      plt.imshow(img, cmap='gray', interpolation='nearest')
    plt.show()

  # Transform + inverse transform each image in the test set for every PCA, then
  # calculate distances and check what's the best PCA
  # -- h2 + h3 --
  inverse_transformed_images = [pca.inverse_transform(pca.transform(x_test)) for pca in pcas]

  # Show all inverse transformations of some image as an example
  print('Showing example image after transform + inverse transform for each PCA...')
  fig = plt.figure(figsize=(8, 8))
  columns = 5
  rows = 2
  for i in range(1, columns * rows + 1):
    img = np.reshape(inverse_transformed_images[i - 1][200], (28, 28))
    fig.add_subplot(rows, columns, i)
    plt.imshow(img, cmap='gray', interpolation='nearest')
  plt.show()

  # Show distances for the example image
  # -- h4 --
  print('Distances of the inversed transformed example image from the original image (for each PCA):', 
    [euclidean(x_test[200], pca_images[200]) for pca_images in inverse_transformed_images])

  # Calculate classifier performance

  # For each image in the test set, calculate its distance from itself after PCA transform
  # + inverse transform, and choose the digit of the best PCA.
  y_predicted = [
    np.argmin([euclidean(image, pca_images[i]) for pca_images in inverse_transformed_images])
    for i, image in enumerate(x_test)
  ]

  print('PCA for each digit-based classifier accuracy:', 
    accuracy_score(y_test, y_predicted))

  
def main():
  print('Showing digits histogram...')
  show_digits_histogram()

  print('First 12 digits in train set:', y_train[0:12], '- Showing them as images...')
  show_first_images()

  print('Measuring KNN performance on the dataset...')
  measure_knn_performance(x_train, y_train, x_test, y_test)

  print('Checking what happens with even k')
  check_knn_even_k()

  pca()
  pca_for_each_digit()


if __name__ == '__main__':
  main()