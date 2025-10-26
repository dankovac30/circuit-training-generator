from generator import Training
import numpy as np

database = Training('exercises.json')

training = database.print_training(1, 12)
