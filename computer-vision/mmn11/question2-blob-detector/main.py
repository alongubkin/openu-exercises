import cv2
import numpy as np
import matplotlib.pyplot as plt
from LoG_filter import log_filt

INITIAL_SIGMA = 2
K = 2 ** 0.25
LEVELS = 15
THRESHOLD = 0.7
SLIDING_WINDOW_SIZE = (20, 20)
SLIDING_WINDOW_STEP_SIZE = 20


def sliding_window(image):
	for y in range(0, image.shape[0], SLIDING_WINDOW_STEP_SIZE):
		for x in range(0, image.shape[1], SLIDING_WINDOW_STEP_SIZE):
			yield (x, y, image[y:y + SLIDING_WINDOW_SIZE[1], x:x + SLIDING_WINDOW_SIZE[0]])


def generate_filters():
  for level in range(0, LEVELS + 1):
    sigma = INITIAL_SIGMA * (K ** level)
    filt_size = 2 * np.ceil(3 * sigma) + 1

    yield np.multiply(log_filt(filt_size, sigma), (sigma ** 2))


def get_scale_space(image):
  return np.dstack([cv2.filter2D(image, -1, kernel) for kernel in generate_filters()])


def main():
  # Read the image
  image = cv2.imread('sunflowers.jpg')
  
  # Convert it into grayscale
  grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Generate the scale space (h * w * n tensor)
  scale_space = get_scale_space(grayscale)

  # Non-maximum suppression using sliding window
  max_value = scale_space.max()
  for x, y, window in sliding_window(scale_space):
    center = window.argmax()
    center_y, center_x, level = np.unravel_index(center, window.shape)

    # If the current local maximum wins the threshold, draw a circle around it.
    if window.max() > THRESHOLD * max_value:
      cv2.circle(image, (x + center_x, y + center_y), 2 * (level+1), [0, 0, 255])

  # Save the image
  cv2.imwrite('sunflowers_blobs.jpg', image)

  # Show it
  plt.imshow(image[:,:,::-1])
  plt.show()


if __name__ == "__main__":
  main()