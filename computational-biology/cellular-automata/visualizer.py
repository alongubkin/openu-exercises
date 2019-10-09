import matplotlib.pyplot as plt

class CellularAutomataVisualizer:
  def __init__(self, ca):
    self.ca = ca

    plt.figure(figsize=(6, 6))

    self.image = plt.imshow(self.to_rgb())
    plt.axis('off')
    plt.tight_layout()

  def update(self):
    self.image.set_data(self.to_rgb())
    plt.draw()

  def to_rgb(self):
    matrix = [[(255, 255, 255) for i in range(self.ca.size)] for j in range(self.ca.size)]
    for x in range(self.ca.size):
      for y in range(self.ca.size):
        entity = self.ca.matrix[x][y]
        if entity is None:
          continue

        matrix[x][y] = entity.get_color()

    return matrix