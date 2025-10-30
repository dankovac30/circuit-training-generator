import tkinter as tk
from tkinter import ttk
from collections import defaultdict

from generator import (
    Generator, 
    Training,
    GenerationFailedError, 
    DatabaseError
)

difficulty_table = {
    'lehká': 0, 'lehka': 0,
    'střední': 1, 'stredni': 1,
    'těžká': 2, 'tezka': 2,
    'extremni': 3, 'extrémní': 3
}

category_translation = {
    'upper': 'Horní část těla',
    'lower': 'Spodní část těla',
    'trunk': 'Střed těla',
    'complex': 'Komplexní'
}


def start_generating():
    difficulty_text = var_difficulty.get()
    number_of_exercises = var_number_of_exercises.get()

    difficulty_number = difficulty_table[difficulty_text]

    result_text.delete("1.0", tk.END)

    generated_training = generator.generate_training(number_of_exercises, difficulty_number)

    categories = defaultdict(list)

    for ex in generated_training:
        categories[ex.category].append(ex)


    for cat, exercises in categories.items():
        cz_cat = category_translation.get(cat, cat)
        result_text.insert(tk.END, f'--- {cz_cat.upper()} ---\n')
        
        for ex in exercises:
            result_text.insert(tk.END, f'{ex.name:40} - RPE {ex.rpe}\n')
        result_text.insert(tk.END, '\n')


if __name__ == "__main__":

    try:
        database_location = ('exercises.db')
        generator = Generator(database_location)

    except DatabaseError as e:
        print(f"FATÁLNÍ CHYBA: {e}")
        exit()

    
    root = tk.Tk()
    root.title('Generátor tréninků')
    
    input_frame = ttk.Frame(root)
    input_frame.pack(fill=tk.X, padx=10)

    ttk.Label(input_frame, text='Zvolte obtížnost:').pack(anchor=tk.W)

    var_difficulty = tk.StringVar(value='lehká')

    ttk.Radiobutton(input_frame, text="Lehká", variable=var_difficulty, value="lehka").pack(anchor=tk.W)
    ttk.Radiobutton(input_frame, text="Střední", variable=var_difficulty, value="stredni").pack(anchor=tk.W)
    ttk.Radiobutton(input_frame, text="Těžká", variable=var_difficulty, value="tezka").pack(anchor=tk.W)
    ttk.Radiobutton(input_frame, text="Extrémní", variable=var_difficulty, value="extremni").pack(anchor=tk.W)

    ttk.Label(input_frame, text="Zvolte počet stanovišť (8-15):").pack(anchor=tk.W, pady=(10,0))
    var_number_of_exercises = tk.IntVar(value=10)

    spinbox_number = ttk.Spinbox(input_frame, from_=8, to=15, textvariable=var_number_of_exercises, width=5)
    spinbox_number.pack(anchor=tk.W)

    generate_button = ttk.Button(input_frame, text="Generovat trénink", command=start_generating)
    generate_button.pack(anchor=tk.W, pady=10)

    result_frame = ttk.Frame(root)
    result_frame.pack(pady=(0,10), padx=10)

    result_text = tk.Text(result_frame, width=50, height=24, wrap=tk.WORD)
    result_text.pack() 


root.mainloop()