from generator import Generator
from generator import Training
import numpy as np

generator = Generator('exercises.db')
printer = Training(generator)

training1 = printer.print_training(1, 12)
