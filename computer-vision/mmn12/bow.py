import os
import cv2
import numpy as np
import time
from hashlib import sha1
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import pairwise_distances_argmin, roc_auc_score, accuracy_score
from sklearn.preprocessing import LabelBinarizer
from sklearn.cluster import MiniBatchKMeans
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.layers import Input
import matplotlib.pyplot as plt
from tqdm import tqdm

TOTAL_CATEGORIES = 8
RANDOM_STATE = 42
DENSE_SIFT_STEP_SIZE = 5
USE_VGG16_FEATURE_EXTRACTION = False


def load_data(path='spatial_envelope_256x256_static_8outdoorcategories/'):
  x = []
  y = []

  for filename in tqdm(os.listdir(path)):
    if not filename.endswith('.jpg'):
      continue

    image = cv2.imread(os.path.join(path, filename))
    assert image is not None

    category = filename.split('_')[0]

    # Only grayscale if using SIFT.
    if USE_VGG16_FEATURE_EXTRACTION:
      x.append(image)
    else:
      x.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    y.append(category)
  
  assert len(np.unique(y)) == TOTAL_CATEGORIES

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
    random_state=RANDOM_STATE)

  return x_train, x_test, y_train, y_test

  
class BagOfWordsClassifier:
  def __init__(self, K):
    self._K = K
    self._sift = cv2.xfeatures2d.SIFT_create()
    self._keypoints = None
    self._vgg16 = None
  
  def learn_codebook(self, x_train):
    # Learn the codebook (or 'visual vocabulary').
    self._kmeans = MiniBatchKMeans(n_clusters=self._K, random_state=RANDOM_STATE)
    self._x_frequencies = []

    for image in tqdm(x_train):
      # Extract image features and partially fit the KMeans algorithm
      features = self._extract_features(image)
      self._kmeans.partial_fit(features)

      # Predict the closest code in the codebook for this image
      self._x_frequencies.append(np.histogram(self._kmeans.predict(features),
        bins=range(0, self._K + 1))[0])

  def fit_svm(self, y_train, C=1.0):
    assert len(self._x_frequencies) == len(y_train)

    # Train an SVM where the input data is the frequencies of "visual words" of an image,
    # and the output data is the image's category
    self._classifier = LinearSVC(C=C, max_iter=10000, random_state=RANDOM_STATE)
    self._classifier.fit(self._x_frequencies, y_train)

  def train(self, x_train, y_train):
    self.learn_codebook(x_train)
    self.fit_svm(y_train)

  def predict(self, x):
    def image_to_frequencies(image):
      features = self._extract_features(image)
      return np.histogram(self._kmeans.predict(features), bins=range(0, self._K + 1))[0]

    return self._classifier.predict(list(map(image_to_frequencies, x)))

  def _extract_features(self, image):
    if USE_VGG16_FEATURE_EXTRACTION:
      return self._extract_features_vgg16(image)
    else:
      return self._extract_features_sift(image)

  def _extract_features_vgg16(self, image):
    "Uses ImageNet-based network to extract image features."
    if self._vgg16 is None:
      input_tensor = Input(shape=(None, None, 3))
      self._vgg16 = VGG16(input_tensor=input_tensor, weights='imagenet', include_top=False)

    features = self._vgg16.predict([preprocess_input(np.expand_dims(image, axis=0))])
    return features[0].reshape((features.shape[1] * features.shape[2], features.shape[3]))

  def _extract_features_sift(self, image):
    "Uses dense-SIFT to extract image features."

    if self._keypoints is None:
      # Cache keypoints
      self._keypoints = [cv2.KeyPoint(x, y, DENSE_SIFT_STEP_SIZE) 
        for y in range(0, image.shape[0], DENSE_SIFT_STEP_SIZE)
        for x in range(0, image.shape[1], DENSE_SIFT_STEP_SIZE)]

    _, features = self._sift.compute(image, self._keypoints)
    return features


def multiclass_roc_auc_score(y_test, y_pred, average="macro"):
  # Based on https://medium.com/@plog397/auc-roc-curve-scoring-function-for-multi-class-classification-9822871a6659
  label_binarizer = LabelBinarizer()
  label_binarizer.fit(y_test)
  
  y_test = label_binarizer.transform(y_test)
  y_pred = label_binarizer.transform(y_pred)
  
  return roc_auc_score(y_test, y_pred, average=average)


def main():
  print('Loading data...')
  x_train, x_test, y_train, y_test = load_data()
  
  x_train = x_train[0:10]
  x_test = x_test[0:10]
  y_train = y_train[0:10]
  y_test = y_test[0:10]

  K = 500 if not USE_VGG16_FEATURE_EXTRACTION else 64

  classifier = BagOfWordsClassifier(K)

  print('Learning visual vocabulary of {} words...'.format(K))
  classifier.learn_codebook(x_train)

  C_values = [0.000001, 0.00001, 0.00005, 0.0001, 0.01, 0.1, 1.0, 5.0, 10.0]
  auc_roc_scores = []
  
  for C in C_values:
    classifier.fit_svm(y_train, C=C)
    y_pred = classifier.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    auc_roc = multiclass_roc_auc_score(y_test, y_pred)

    print('Score for SVM(C={}): Accuracy={}, AUCROC={}'.format(C, accuracy, auc_roc))
    auc_roc_scores.append(auc_roc)

  plt.plot(list(range(len(C_values))), auc_roc_scores)
  plt.xticks(list(range(len(C_values))), C_values)
  plt.show()

if __name__ == '__main__':
  main()
