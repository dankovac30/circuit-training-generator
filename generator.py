import json
import math
import random
import numpy as np

class Exercise:
    def __init__(self, name, category, rpe):
        self.name = name
        self.category = category
        self.rpe = rpe


class Training:
    def __init__(self, difficulty_level):
        self.difficulty_level = difficulty_level
        self.exercise_list = []


class Generator:
    def __init__(self, database_location):
        self.database = []

        with open(database_location, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)


            for data in raw_data:
                exercise = Exercise(**data)
                self.database.append(exercise)

    def generate_training(self, number_of_exercises, difficulty):
        
        rules = [
        (0.75, 0.25, 0.00),
        (0.40, 0.55, 0.05),
        (0.15, 0.65, 0.20),
        (0.00, 0.60, 0.40)
        ]

        if not (0 <= difficulty <= 3):
            raise ValueError("Neplatná obtížnost")

        low, core, high = rules[difficulty]


        if not (8 <= number_of_exercises <= 15):
            raise ValueError("Nesprávný počet stanovišť")
        
        low_count = number_of_exercises * low
        low_floor = math.floor(low_count)

        core_count = number_of_exercises * core
        core_floor = math.floor(core_count)

        high_count = number_of_exercises * high
        high_floor = math.floor(high_count)

        floor_sum = low_floor + core_floor + high_floor
        missing_count = number_of_exercises - floor_sum

        low_excess = low_count - low_floor
        core_excess = core_count - core_floor
        high_excess = high_count - high_floor

        excesses = [
            ("low", low_excess),
            ("core", core_excess),
            ("high", high_excess)
        ]

        random.shuffle(excesses)
        excesses.sort(key=lambda x: x[1], reverse=True)

        counts = {
            'low': low_floor,
            'core': core_floor,
            'high': high_floor
        }

        for i in range(missing_count):

            category_to_add = excesses[i][0]
            counts[category_to_add] += 1


        rpe_ranges = {
            'low': [4, 5],
            'core': [6, 7, 8],
            'high': [9, 10]
        }

        training_rpe = []

        for category, count in counts.items():
            
            if count > 0:
                possible_values = rpe_ranges[category]
            
                generated_values = np.random.choice(possible_values, size=count, replace=True)

                training_rpe.extend(generated_values.tolist())
    
        random.shuffle(training_rpe)

        training_array = np.array(training_rpe)

        current_average = np.mean(training_array)

        difficulty_rpe = [5.1, 6.1, 7.1, 8.1]
        tolerance = 0.25
        target_average = difficulty_rpe[difficulty]

        while abs(current_average - target_average) > tolerance:
            
            if current_average > target_average:

                possible_indices = np.where(training_array > 4)[0]

                index_to_change = np.random.choice(possible_indices)

                training_array[index_to_change] -= 1

            elif current_average < target_average:

                possible_indices = np.where(training_array < 10)[0]

                index_to_change = np.random.choice(possible_indices)

                training_array[index_to_change] += 1

            
            current_average = np.mean(training_array)

        
        final_training_array = training_array

        return final_training_array
