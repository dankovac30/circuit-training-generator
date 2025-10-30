# Circuit Training Generator

## About

A simple app for generating random circuit training routines. Built with Python, using Tkinter for the GUI.

You can choose the difficulty and number of exercises, and the app will create randomized workout based on RPE (Rating of Perceived Exertion).

---

## Features

* Generates workouts with 8 to 15 exercises.
* 4 difficulty levels (easy, medium, hard, extreme).
* Balanced full-body workouts 
* Smart "brute-force" logic to get randomized and non-repetitive workouts.
* Database uses Czech names

---

## Roadmap

* [ ] Add collisions to some exercises.
* [ ] Option to switch between CZ/EN.
* [ ] Expand exercise database.

---

## Changelog

### 1.0.0
* Initial Release

---

## Installation & Usage

1.  Clone the repository:
    ```bash
    git clone
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the version you want:

    **GUI Version:**
    ```bash
    python main_gui.py
    ```
    **Command-Line Version:**
    ```bash
    python main_cli.py
    ```