Tetris84 🎮

Tetris in 1984 if it was more complex (and if it was made entirely in Python).

A terminal-based Tetris clone that blends classic 1984 ASCII aesthetics with modern Guideline-inspired mechanics — including advanced scoring, wall kicks, combo systems, and persistent high scores.

🚀 Features

🎯 Modern Tetris logic

7-Bag randomization for fair piece distribution

Basic wall kicks for smoother rotations

T-Spin detection & Back-to-Back bonuses

Combos and advanced scoring

🕹 Customizable Experience

Optional ghost piece

Four difficulty levels (Easy → Extreme)

⭐ Persistent High Scores

Saves player progress between sessions

💬 Multilingual UI

English, Spanish, Russian, Ukrainian, Belarusian, Kazakh, French, German, Italian, Georgian, Armenian, Azerbaijani/Azeri, Dutch, Flemish, Frisian

⚡ Flicker-Free Rendering

Efficient screen updates using ANSI escape codes

🛠️ Requirements

Python 3.x

keyboard module (for real-time input)

Install dependencies:

pip install keyboard


⚠️ Note: On most systems, the keyboard module may require elevated privileges to capture real-time key events.

▶️ How to Play

Clone the repository

Install the dependency (keyboard)

Run the game:

python game.py


On Windows: Run your terminal as Administrator

On Linux/macOS: Use sudo if needed

🎮 Controls
Action	Key
Move Left	←
Move Right	→
Rotate	↑
Soft Drop	↓
Hard Drop	Space
Hold Piece	Shift
Pause/Resume	P
Restart	R
Quit	Q
Show/Hide Controls	H
📐 Recommended Setup

Terminal size: ≥ 30 rows × 50 columns

Use a monospaced font (e.g., Consolas, Fira Code)

Lower key-repeat delay for better responsiveness

📦 Included Files

game.py — Main Tetris game logic

highscore.json — Persistent high score storage

LICENSE — MIT License

🧠 Notes

Designed for terminal play, not for IDE consoles (e.g., IDLE).

Scores and mechanics aim to bridge classic play with modern Tetris rules.

📜 License

MIT License — feel free to use, modify, and share!
