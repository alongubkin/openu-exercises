Requirements:
  - Python 3 (https://www.python.org/downloads/)
  - pygame (pip install pygame)

Usage:

  Environments are saved as JSON files.

  In order to train an environment, use the following script:
    python train.py <input-environment> <output-solution-environment>

  For example:
    python train.py environment_size10_2.json test.json

  Then, you can play it using:
    python play.py test.json