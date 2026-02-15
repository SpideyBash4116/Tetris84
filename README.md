Terminal Tetris (Modern Edition)
This is a high-performance, terminal-based Tetris clone that blends the classic 1984 ASCII aesthetic with modern competitive mechanics. Built in Python, it features a robust translation system and advanced gameplay logic found in modern "Guideline" Tetris titles.

✨ Key Features
Modern Gameplay Logic: Includes the 7-bag randomization system to ensure fair piece distribution and Basic Wall Kicks for smoother rotations.

Advanced Scoring: Master the game with T-Spin detection, Back-to-Back bonuses, and Combo multipliers.

Customizable Experience: Toggle the Ghost Piece for precision, choose from 4 difficulty levels (Easy to Extreme), and track your progress with persistent High Score saving.

Multilingual Support: Fully localized in English, Spanish, Russian, Ukrainian, Belarusian, and Kazakh.

Flicker-Free Rendering: Uses ANSI escape codes to update the terminal efficiently without full-screen erasures.

🕹️ Controls
Action	Key
Move Left / Right	Left / Right Arrow
Rotate	Up Arrow
Soft Drop	Down Arrow
Hard Drop	Space
Hold Piece	Shift
Pause / Resume	P
Show/Hide Controls	H
Restart / Quit	R / Q
🛠️ Technical Details
Version: rc-1.02.00.

Language: Python 3.x.

Dependencies: keyboard (requires root/administrative privileges on some systems to capture global key events).

Board Dimensions: 10x20 (Standard).

🛠️ Technical Requirements
Python 3.x: Ensure you have a modern version of Python installed.

keyboard Library: This script relies on the keyboard module to handle real-time inputs without blocking the game loop.

Install: pip install keyboard

Permissions (Elevated Privileges):

Windows: You must run your terminal or IDE as an Administrator.

Linux/macOS: You must run the script with sudo (e.g., sudo python game.py).

Why? The keyboard library hooks into global system events to detect key presses even if the terminal loses focus for a split second, which requires OS-level permission.

ANSI-Compatible Terminal: The game uses ANSI escape codes (like \033[H) to move the cursor and update the screen without flickering.

Recommended: Windows Terminal, PowerShell (modern versions), iTerm2 (macOS), or standard Linux terminals (GNOME, xterm).

Avoid: The basic Windows cmd.exe or older IDE "Output" windows (like some basic versions of IDLE) may not render the colors or cursor movements correctly.

💡 Recommendations for the Best Experience
Terminal Size: Make sure your terminal window is at least 30 lines high and 50 columns wide to accommodate the board, the "Next Piece" preview (which shows 5 pieces!), and the stats sidebar.

Font Choice: Use a Monospaced font (like Cascadia Code, Consolas, or Fira Code). Since the game uses characters like [] and .. to represent blocks, a non-monospaced font will cause the board to look "wavy" or misaligned.

Disable Key Repeat Delay: If you find the pieces moving too slowly when holding down the arrows, you may want to lower your OS "Key Repeat Delay" in your keyboard settings for faster "DAS" (Delayed Auto Shift).

File Permissions: Ensure the script has write access to its own folder so it can create/update the highscore.json file to save your progress.

Final Check: Always remember to bring an ID with you—not for the game, just as a general rule!

🚀 Getting Started
Ensure you have the keyboard library installed:

pip install keyboard

Run the script:

python game.py

Note: Depending on your OS, you may need to run the script with sudo or as an Administrator to allow the keyboard library to function.

🚀 Quick Start Command
Bash

# Install dependency
pip install keyboard

# Run with required permissions
sudo python game.py  # Linux/macOS
# OR run your Command Prompt as Admin and then:
python game.py       # Windows
