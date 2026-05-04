# Jogo do Milhão — Millionaire Trivia Game

A "Who Wants to Be a Millionaire" style trivia game built with Python and Pygame, featuring a modular OOP architecture with clearly separated responsibilities across all game components.

## 🧩 About

This project started as a procedural script and was fully refactored into an Object-Oriented architecture with separate modules for each game concern — making it easy to add new question sets, change difficulty, or modify the UI without touching unrelated code.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Game Engine | Pygame |
| Architecture | Modular OOP |
| Version Control | Git / GitHub |

## ⚙️ Features

- ✅ Interactive trivia gameplay with multiple choice answers
- ✅ Lives system — lose a life for each wrong answer
- ✅ Hints system to help the player
- ✅ Subject selection menu
- ✅ Tutorial screen for new players
- ✅ Modular OOP design — separated game logic, questions, lives, hints, and UI rendering

## 📁 Project Structure

```
Jogo_do_Milhao/
├── src/
│   ├── game/           # Core game loop and state management
│   ├── questions/      # Question loading and management
│   ├── ui/             # Screen rendering and components
│   ├── lives/          # Lives system logic
│   └── hints/          # Hints system logic
├── assets/             # Images, fonts, sounds
├── main.py             # Entry point
└── requirements.txt
```

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/pleomoreno/Jogo_do_Milhao.git
cd Jogo_do_Milhao

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

**Requirements:** Python 3.8+, Pygame

## 👤 Authors

**Leonardo Alves Moreno**  
**Santiago Ciapina Martinez Salazar**  
**Juliano Galhardo de Oliveira**  
**Erik Kenji Sakura**  
**João Carlos Soares Sartorelli**
