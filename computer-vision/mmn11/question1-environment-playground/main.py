import numpy as np
import cv2
import matplotlib.pyplot as plt

def random_gaussian_image(mean, sd, size, show=True):
  # Generate a random matrix with the specified size, mean and standard deviation
  # This random matrix might contain negative values, and also floating-point values,
  # so we need to do some processing before making it an image.
  matrix = np.random.normal(loc=mean, scale=sd, size=size) 

  # Create an image from the matrix by rounding all values to their closest integer, and overflowing
  # any negative values.  Examples: (I) 30.3 => 30,  (II) -1 => 255,  (II) -2.7 => -3 => 253.
  image = matrix.round().astype(np.uint8)

  # Save the grayscale image to a png file.
  # NOTE: Image values must be np.uint8 in order for OpenCV to treat them as grayscale.
  width, height = size
  image_name = 'gaussian_{}x{}_mean{}_sd{}'.format(width, height, mean, sd)
  cv2.imwrite('output/{}.png'.format(image_name), image)

  if show:
    cv2.imshow(image_name, image)
    cv2.waitKey(0)

  # Compute a histogram for the original matrix and save it
  # NOTE: We're assuming that most of the samples are within 4 standard deviations from the mean.
  bins = np.linspace(mean - 4 * sd, mean + 4 * sd, 30)
  histogram, bins = np.histogram(matrix, bins)

  # Plot the histogram
  plt.figure(figsize=(6, 4))
  plt.plot(bins[:-1], histogram)
  plt.savefig('output/{}_histogram.png'.format(image_name))

  if show:
    cv2.imshow('histogram', cv2.imread('output/{}_histogram.png'.format(image_name)))
    cv2.waitKey(0)


def edges_and_corners_detection(image_path, show=True):
  # Read the colored image
  image = cv2.imread(image_path)
  if show:
    cv2.imshow(image_path, image)
    cv2.waitKey(0)

  # Grayscale it
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  if show:
    cv2.imshow('grayscale', gray)
    cv2.waitKey(0)

  # Run Canny edges detector with different parameters
  for min_val, max_val in [(50, 100), (50, 50), (75, 125)]:
    edges = cv2.Canny(gray, min_val, max_val)
    cv2.imwrite('output/edges_min{}_max{}.png'.format(min_val, max_val), edges)

    if show:
      cv2.imshow('edges (min = {}, max = {})'.format(min_val, max_val), edges)
      cv2.waitKey(0)

  # Run Harris corners algorithm with different parameters
  for block_size, ksize, k in [(6, 3, 0.06), (2, 5, 0.04)]:
    corners = cv2.cornerHarris(np.float32(gray), block_size, ksize, k)

    image_with_corners = image.copy()
    image_with_corners[corners > 0.0001 * corners.max()] = [0, 0, 255]

    cv2.imwrite('output/corners_blocksize{}_ksize{}_k{}.png'.format(
      block_size, ksize, k), image_with_corners)

    if show:
      cv2.imshow('corners (block_size={}, ksize={}, k={})'.format(
        block_size, ksize, k), image_with_corners)
      cv2.waitKey(0)
  

def main():
  random_gaussian_image(mean=10, sd=5, size=(100, 100))
  cv2.destroyAllWindows()

  edges_and_corners_detection('golden-retriever.png')
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()