from generator import Generator
from generator import Training
from generator import GenerationFailedError
from generator import DatabaseError
import numpy as np
import sys
import os


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_difficulty_level():

    difficulty_table = {
        'lehká': 0, 'lehka': 0,
        'střední': 1, 'stredni': 1,
        'těžká': 2, 'tezka': 2,
        'extremni': 3, 'extrémní': 3
    }

    while True:
        print("Zvolte obtížnost")
        
        entry = input("(lehká, střední, těžká, extrémní): ")

        difficulty = difficulty_table.get(entry.lower())

        if difficulty is not None:
            
            return difficulty
        
        else:
            print("--- Neplatná volba, zkuste to prosím znovu. ---")

def get_number_of_exercises(min=8, max=15):

    while True:
        entry = input(f"Zadejte počet stanovišť ({min}-{max}):")

        try:
            
            number_of_exercises = int(entry)

            if min <= number_of_exercises <= max:
                return number_of_exercises
            
            else: print(f"--- Číslo musí být v rozmezí {min}-{max}. ---")

        except:
            print("--- Musíte zadat platné číslo. ---")



if __name__ == '__main__':
    
    try:

        database_location = resource_path('exercises.db')
        generator = Generator(database_location)
        printer = Training(generator)

        while True:
            
            difficulty_level = get_difficulty_level()
            number_of_exercises = get_number_of_exercises()

            print('\n... Generuji trénink ...')
            printer.print_training(difficulty_level, number_of_exercises)

        
            next = input("Chcete vygenerovat další trénink? (ano/ne): ")

            if next.lower() != 'ano':
                break

    except DatabaseError as e:
        print(f"FATÁLNÍ CHYBA: Nepodařilo se načíst databázi: {e}")
    except KeyboardInterrupt:
        print("\nUkončeno uživatelem.")