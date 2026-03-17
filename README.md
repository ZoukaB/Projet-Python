# Projet POO — Jeu au tour par tour (Pygame)

Group: IPS-SMR - 3

- BARAJAS OLAN Itzel María
- BUCLET Zeca
- PHILIPPE Paul Etienne

Description
-----------
This project was carried out as part of a course unit and offers a fun and open-ended framework for applying various object-oriented programming concepts. The project was required to include at least two inheritance relationships as well as at least two other relationships (simple association, composition, or aggregation).  The complete instructions can be found in the repo. Although constrained by time, this project was very enjoyable to work on and a great way to get hands-on experience with OOP in Python.

The game is a turn-based two-player game developed in Python using Pygame. Players build a team of characters and must defeat the opposing team by using each character's unique skills and abilities.

Key points
----------
- Inheritance from a common `Unit` class to centralize attributes and behaviors (HP, movement, attack, defense, energy, etc.).
- Multiple playable characters with special abilities and combat/movement logic.
- Display/UI features for main menu, character selection, stat/capacity panels and attack animations.

Requirements
------------
- Python 3.8+ (3.10+ recommended)
- Pygame

Installation (suggested)
------------------------
1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install pygame 
```

Running the game
----------------
The main code is located in the `RenduFinal/` folder. To run the final version of the game :

```powershell
python "RenduFinal\GameFinal.py"
```

Repository structure
-------------------------------
Below is a compact tree-style view of the repository similar to the example you attached. Image folders contain PNG UI assets and are shown as single-line entries. `RenduFinal/` is expanded with short comments.

```
Project root
├─ Images_armes/        # PNG assets for weapons / UI
├─ Images_display/      # PNG assets for UI display elements
├─ Images_persos/       # PNG assets for character portraits / sprites
├─ PersosBoard/         # PNG assets for board / UI backgrounds
└─ RenduFinal/
   ├─ DisplayFinal.py        # display and UI helper functions/classes
   ├─ GameFinal.py           # main game loop / entry point (recommended)
   ├─ PersonnagesFinal.py    # character definitions and abilities
   ├─ UnitFinal.py           # base Unit class and shared logic
   └─ __pycache__/           # compiled Python bytecode

Notes:
- The image folders contain PNG files only (UI assets), so they aren't expanded here.
```

Contact
-------
For questions, contact the authors listed above.