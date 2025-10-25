from generator import Generator
import numpy as np

generator_treninku = Generator('exercises.json')



trenink = generator_treninku.generate_training(13, 1)

print([ex.name for ex in trenink])
