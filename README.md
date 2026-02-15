🎮 Terminal Tetris (Modern Edition)

Terminal Tetris (Modern Edition) is a high-performance, terminal-based Tetris clone that blends the classic 1984 ASCII aesthetic with modern competitive mechanics. Written in Python, it features advanced gameplay logic inspired by modern Guideline Tetris titles, along with a robust multilingual system and flicker-free rendering.

✨ Key Features
🧠 Modern Gameplay Logic

7-Bag randomization for fair and predictable piece distribution

Basic Wall Kicks for smoother, more forgiving rotations

🏆 Advanced Scoring System

T-Spin detection

Back-to-Back (B2B) bonuses

Combo multipliers for high-skill play

⚙️ Customizable Experience

Optional Ghost Piece for precise placement

4 difficulty levels: Easy → Extreme

Persistent High Score saving

🌍 Multilingual Support

Fully localized UI in:

- English

- Spanish

- Russian

- Ukrainian

- Belarusian

- Kazakh

⚡ Flicker-Free Rendering

Uses ANSI escape codes to efficiently update the screen without full clears

🕹️ Controls
Move Left / Right	← / →
Rotate	↑
Soft Drop	↓
Hard Drop	Space
Hold Piece	Shift
Pause / Resume	P
Show / Hide Controls	H
Restart / Quit	R / Q
🛠️ Technical Details

Version: rc-1.02.00

Language: Python 3.x

Board Size: 10 × 20 (Standard)

Dependency: keyboard (used for real-time, non-blocking input)

🛠️ Technical Requirements
🐍 Python

Python 3.x (recommended: latest stable version)

⌨️ keyboard Library

This game uses the keyboard module to capture real-time key input.

pip install keyboard


⚠️ Elevated Permissions Required

Windows: Run your terminal or IDE as Administrator

Linux / macOS: Run with sudo

Why?
The keyboard library hooks into global system input events to ensure reliable gameplay—even if the terminal briefly loses focus—which requires OS-level permissions.

🖥️ Terminal Compatibility

The game relies on ANSI escape codes (e.g. \033[H) for cursor control and color output.

Recommended terminals

Windows Terminal

Modern PowerShell

iTerm2 (macOS)

GNOME Terminal / xterm (Linux)

Avoid

Legacy cmd.exe

Older IDE output consoles (e.g. basic IDLE windows)

💡 Best Experience Tips

Terminal Size:
At least 30 rows × 50 columns to fit:

Game board

5-piece “Next” preview

Stats sidebar

Font:
Use a monospaced font (Cascadia Code, Consolas, Fira Code).
Proportional fonts will cause block misalignment.

Key Repeat Settings:
Lower your OS Key Repeat Delay for faster DAS when holding arrow keys.

File Permissions:
Ensure the game directory is writable so highscore.json can be created and updated.

Final Check:
Always remember to bring an ID with you—not for the game, just in general 😉

🚀 Getting Started

Install the dependency:

pip install keyboard


Run the game:

python game.py


Note: You may need to run the command with elevated privileges depending on your OS.

🚀 Quick Start (Recommended)
# Install dependency
pip install keyboard

# Run with required permissions
sudo python game.py   # Linux / macOS
# OR run your terminal as Administrator, then:
python game.py        # Windows

Screenshots
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/556107ca-6fd8-47eb-86a9-86b9f1c04d36" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/71f52699-ec8d-4e80-abc3-0aaeb167b696" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/682f8c44-9544-4f5f-bd52-57ace905e10e" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6f98bb55-55af-4100-a7bd-1873d5fe06d4" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9426bf89-2c07-4cd0-a0a8-37b83fef9fd2" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9dc33847-4d72-4e66-8afd-ae7d5bd2b68b" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bf8220bc-c05c-4141-85ff-bb4fb27a5660" />
