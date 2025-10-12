from generator import Generator
import numpy as np

generator_treninku = Generator('exercises.json')



num = 1

rpe_list = []

while num < 10000:

    training = generator_treninku.generate_training(12, 0)
    training = training.mean()
    rpe_list.append(training)

    num += 1

rpe_array = np.array(rpe_list)

print(rpe_array.mean())
print(rpe_array.max())
print(rpe_array.min())
