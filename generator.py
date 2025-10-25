import json
import math
import random
import numpy as np
from collections import defaultdict

class Exercise:
    def __init__(self, name, category, rpe):
        self.name = name
        self.category = category
        self.rpe = rpe


class Training:
    def __init__(self, difficulty_level):
        self.difficulty_level = difficulty_level
        self.exercise_list = []


class GenerationFailedError(Exception):
    """Výjimka pro případ, kdy se nepodařilo vytvořit trénink"""
    pass

class DatabaseError(Exception):
    """Chyba databáze, žádné cviky k načtení"""
    pass


class Generator:
    def __init__(self, database_location):
        self.database = []

        with open(database_location, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

            for data in raw_data:
                try:   
                    exercise = Exercise(**data)
                    self.database.append(exercise)

                except TypeError:
                    raise DatabaseError


        self.rpe_ranges = {
            'low': [4, 5],
            'core': [6, 7, 8],
            'high': [9, 10]
        }

        self.target_rpe_averages = [5.1, 6.1, 7.1, 8.1]


    def generate_training(self, number_of_exercises, difficulty):

        if not (0 <= difficulty <= 3):
            raise ValueError("Neplatná obtížnost")

        if not (8 <= number_of_exercises <= 15):
            raise ValueError("Nesprávný počet stanovišť")
        

        while True:

            try:

                counts = self._calculate_rpe_counts(number_of_exercises, difficulty)

                initial_array = self._generate_initial_rpe_array(counts)

                optimized_array = self._optimize_rpe_array(initial_array, difficulty)

                quotas = self._calculate_exercises_quotas(number_of_exercises)

                final_training = self._assign_exercises(optimized_array, quotas)

                return final_training
            
            except GenerationFailedError:
                pass


    def _calculate_rpe_counts(self, number_of_exercises, difficulty):

        rules = [
        (0.75, 0.25, 0.00),
        (0.40, 0.55, 0.05),
        (0.15, 0.65, 0.20),
        (0.00, 0.60, 0.40)
        ]

        low, core, high = rules[difficulty]
      
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

        return counts
    
    
    def _generate_initial_rpe_array(self, counts):

        training_rpe = []

        for category, count in counts.items():
            
            if count > 0:
                possible_values = self.rpe_ranges[category]
            
                generated_values = np.random.choice(possible_values, size=count, replace=True)

                training_rpe.extend(generated_values.tolist())
    
        random.shuffle(training_rpe)

        training_array = np.array(training_rpe)

        return training_array


    def _optimize_rpe_array(self, training_array, difficulty):

        current_average = np.mean(training_array)

        tolerance = 0.25
        target_average = self.target_rpe_averages[difficulty]

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
    

    def _calculate_exercises_quotas(self, number_of_exercises):

        complex_count = self._complex_probability(number_of_exercises)
        lower_count = round(number_of_exercises * np.random.uniform(0.4, 0.5), 0)

        exesses_count = number_of_exercises - (complex_count + lower_count)
        exesses_half = exesses_count // 2
        exesses_remainder = exesses_count % 2

        upper_count = exesses_half + exesses_remainder
        trunk_count = exesses_half


        quotas = {
            'lower': lower_count,
            'upper': upper_count,
            'trunk': trunk_count,
            'complex': complex_count
        }


        return quotas


    def _complex_probability(self, number_of_exercises):

        if number_of_exercises <= 8:
            p = 0.4
        
        elif number_of_exercises >= 15:
            p = 1.0
        
        else:
            p = 0.4 + (number_of_exercises-8) / 7 * 0.6

        return np.random.choice([1, 0], p=[p, 1-p])


    def _assign_exercises(self, rpe_array, quotas):
        
        lower_count = quotas['lower']
        upper_count = quotas['upper']
        trunk_count = quotas['trunk']
        complex_count = quotas['complex']

        rpe_list = list(rpe_array)
        all_exercises = self.database.copy()
        selected_exercises = []

        complex_category = [exercise for exercise in all_exercises if exercise.category == 'complex']
        trunk_category = [exercise for exercise in all_exercises if exercise.category == 'trunk']
        upper_category = [exercise for exercise in all_exercises if exercise.category == 'upper']
        lower_category = [exercise for exercise in all_exercises if exercise.category == 'lower']

        result_complex = self._fill_category(rpe_list, complex_category, complex_count)
        selected_complex_exercises = result_complex['exercises']
        remaining_rpe_list = result_complex['remaining_rpe_list']
        selected_exercises.extend(selected_complex_exercises)

        result_trunk = self._fill_category(remaining_rpe_list, trunk_category, trunk_count)
        selected_trunk_exercises = result_trunk['exercises']
        remaining_rpe_list = result_trunk['remaining_rpe_list']
        selected_exercises.extend(selected_trunk_exercises)

        result_upper = self._fill_category(remaining_rpe_list, upper_category, upper_count)
        selected_complex_exercises = result_upper['exercises']
        remaining_rpe_list = result_upper['remaining_rpe_list']
        selected_exercises.extend(selected_trunk_exercises)

        result_lower = self._fill_category(remaining_rpe_list, lower_category, lower_count)
        selected_lower_exercises = result_lower['exercises']
        remaining_rpe_list = result_lower['remaining_rpe_list']
        selected_exercises.extend(selected_lower_exercises)

        return selected_exercises

    def _fill_category(self, rpe_list, exercises_by_category, quota):

        rpe_index = defaultdict(list)
        category_selected_exercises = []

        for exercise in exercises_by_category:
            rpe_index[exercise.rpe].append(exercise)

        while quota > 0:
            
            if set(rpe_list) & set(rpe_index.keys()):

                available_rpe = set(rpe_list) & set(rpe_index.keys())
                selected_rpe = random.choice(list(available_rpe))

                selected_exercise = random.choice(rpe_index[selected_rpe])
                category_selected_exercises.append(selected_exercise)
                rpe_index[selected_rpe].remove(selected_exercise)

                if not rpe_index[selected_rpe]:
                    del rpe_index[selected_rpe]

                quota -= 1
                rpe_list.remove(selected_rpe)


            else:
                raise GenerationFailedError
            
        result = {
            'exercises': category_selected_exercises,
            'remaining_rpe_list': rpe_list
        }

        return result