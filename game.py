import json
import random
import time
from pathlib import Path

import keyboard

WIDTH, HEIGHT = 10, 20
EMPTY = "  "
BLOCK = "[]"
GHOST = ".."

START_FALL_SPEED = 0.60
MIN_FALL_SPEED = 0.08
PREVIEW_COUNT = 5
HIGH_SCORE_FILE = Path(__file__).with_name("highscore.json")
DIFFICULTY_SPEEDS = {
    "easy": 0.80,
    "normal": 0.60,
    "hard": 0.45,
    "extreme": 0.30,
}

LINE_CLEAR_SCORES = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,
}

DEFAULT_OPTIONS = {
    "show_ghost": True,
    "language": "en",
    "difficulty": "normal",
}

LANGUAGE_ORDER = ["en", "es", "ru", "uk", "be", "kk"]

TEXTS = {
    "en": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Play",
        "version": "Version rc-1.02.00",
        "options": "Options",
        "exit": "Exit",
        "select_1_3": "Select an option (1-3): ",
        "select_1_4": "Select an option (1-4): ",
        "select_1_5": "Select an option (1-5): ",
        "select_1_7": "Select an option (1-7): ",
        "options_title": "--- OPTIONS ---",
        "ghost_piece": "Ghost Piece",
        "difficulty": "Difficulty",
        "language": "Language",
        "reset_defaults": "Reset Defaults",
        "back": "Back",
        "state_on": "ON",
        "state_off": "OFF",
        "language_title": "--- LANGUAGE ---",
        "language_current": "Current: {language}",
        "english": "English",
        "spanish": "Spanish",
        "russian": "Russian",
        "ukrainian": "Ukrainian",
        "belarusian": "Belarusian",
        "kazakh": "Kazakh",
        "difficulty_easy": "Easy",
        "difficulty_normal": "Normal",
        "difficulty_hard": "Hard",
        "difficulty_extreme": "Extreme",
        "game_header": "--- TETRIS --- SCORE: {score} | HIGH: {high} | LEVEL: {level} | LINES: {lines}",
        "hold": "HOLD:",
        "next": "NEXT:",
        "empty": "(empty)",
        "paused": "PAUSED - Press P to resume",
        "controls_1": "Up: Rotate | Left/Right: Move | Down: Soft drop | Space: Hard drop",
        "controls_2": "Shift: Hold | P: Pause | R: Restart | Q: Back to menu",
        "controls_hint": "Press H to show/hide controls",
        "game_over": "GAME OVER - Press R to restart or Q to go back to menu",
        "bye": "Bye",
    },
    "es": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Jugar",
        "version": "Versión cal-1.02.00",
        "options": "Opciones",
        "exit": "Salir",
        "select_1_3": "Selecciona una opcion (1-3): ",
        "select_1_4": "Selecciona una opcion (1-4): ",
        "select_1_5": "Selecciona una opcion (1-5): ",
        "select_1_7": "Selecciona una opcion (1-7): ",
        "options_title": "--- OPCIONES ---",
        "ghost_piece": "Pieza Fantasma",
        "difficulty": "Dificultad",
        "language": "Idioma",
        "reset_defaults": "Restablecer",
        "back": "Atras",
        "state_on": "ACTIVADO",
        "state_off": "DESACTIVADO",
        "language_title": "--- IDIOMA ---",
        "language_current": "Actual: {language}",
        "english": "Ingles",
        "spanish": "Espanol",
        "russian": "Ruso",
        "ukrainian": "Ucraniano",
        "belarusian": "Bielorruso",
        "kazakh": "Kazajo",
        "difficulty_easy": "Facil",
        "difficulty_normal": "Normal",
        "difficulty_hard": "Dificil",
        "difficulty_extreme": "Extremo",
        "game_header": "--- TETRIS --- PUNTOS: {score} | RECORD: {high} | NIVEL: {level} | LINEAS: {lines}",
        "hold": "GUARDADA:",
        "next": "SIGUIENTES:",
        "empty": "(vacio)",
        "paused": "PAUSA - Pulsa P para continuar",
        "controls_1": "Arriba: Girar | Izq/Der: Mover | Abajo: Caida suave | Espacio: Caida dura",
        "controls_2": "Shift: Guardar | P: Pausa | R: Reiniciar | Q: Volver al menu",
        "controls_hint": "Pulsa H para mostrar/ocultar controles",
        "game_over": "FIN DEL JUEGO - Pulsa R para reiniciar o Q para volver al menu",
        "bye": "Adios",
    },
    "ru": {
        "main_title": """
█████ ████   █████   ████  █████   ████
  █       █    █    █   █    █    █        
  █     ██     █     ████    █    █    
  █       █    █    █   █    █    █       
  █   ████     █    █   █  █████   ████ 
""",
        "version": "Версия КНР-1.02.00",
        "play": "Играть",
        "options": "Опции",
        "exit": "Выход",
        "select_1_3": "Выберите пункт (1-3): ",
        "select_1_4": "Выберите пункт (1-4): ",
        "options_title": "--- ОПЦИИ ---",
        "ghost_piece": "Призрак фигуры",
        "language": "Язык",
        "reset_defaults": "Сбросить",
        "back": "Назад",
        "state_on": "ВКЛ",
        "state_off": "ВЫКЛ",
        "language_title": "--- ЯЗЫК ---",
        "language_current": "Текущий: {language}",
        "english": "Английский",
        "spanish": "Испанский",
        "russian": "Русский",
        "game_header": "--- ТЕТРИС --- СЧЕТ: {score} | РЕКОРД: {high} | УРОВЕНЬ: {level} | ЛИНИИ: {lines}",
        "hold": "УДЕРЖАНИЕ:",
        "next": "СЛЕДУЮЩИЕ:",
        "empty": "(пусто)",
        "paused": "ПАУЗА - Нажмите P для продолжения",
        "controls_1": "Вверх: Поворот | Влево/Вправо: Движение | Вниз: Мягкий сброс | Пробел: Жесткий сброс",
        "controls_2": "Shift: Удержать | P: Пауза | R: Рестарт | Q: В меню",
        "controls_hint": "Нажмите H, чтобы показать/скрыть управление",
        "game_over": "ИГРА ОКОНЧЕНА - Нажмите R для рестарта или Q для меню",
        "bye": "Пока",
    },
    "uk": {
        "version": "Версія ЗК-1.02.00",
        "play": "Грати",
        "options": "Опції",
        "exit": "Вихід",
        "select_1_3": "Оберіть пункт (1-3): ",
        "select_1_4": "Оберіть пункт (1-4): ",
        "select_1_7": "Оберіть пункт (1-7): ",
        "options_title": "--- ОПЦІЇ ---",
        "ghost_piece": "Привид фігури",
        "language": "Мова",
        "reset_defaults": "Скинути",
        "back": "Назад",
        "state_on": "УВІМК",
        "state_off": "ВИМК",
        "language_title": "--- МОВА ---",
        "language_current": "Поточна: {language}",
        "english": "Англійська",
        "spanish": "Іспанська",
        "russian": "Російська",
        "ukrainian": "Українська",
        "belarusian": "Білоруська",
        "kazakh": "Казахська",
        "controls_hint": "Натисніть H, щоб показати/сховати керування",
        "game_over": "ГРУ ЗАКІНЧЕНО - Натисніть R для рестарту або Q для меню",
        "bye": "Бувай",
    },
    "be": {
        "version": "Версія КНВ-1.02.00",
        "play": "Гуляць",
        "options": "Налады",
        "exit": "Выйсці",
        "select_1_3": "Выберыце пункт (1-3): ",
        "select_1_4": "Выберыце пункт (1-4): ",
        "select_1_7": "Выберыце пункт (1-7): ",
        "options_title": "--- НАЛАДЫ ---",
        "ghost_piece": "Прывід фігуры",
        "language": "Мова",
        "reset_defaults": "Скінуць",
        "back": "Назад",
        "state_on": "УКЛ",
        "state_off": "ВЫКЛ",
        "language_title": "--- МОВА ---",
        "language_current": "Бягучая: {language}",
        "english": "Англійская",
        "spanish": "Іспанская",
        "russian": "Руская",
        "ukrainian": "Украінская",
        "belarusian": "Беларуская",
        "kazakh": "Казахская",
        "controls_hint": "Націсніце H, каб паказаць/схаваць кіраванне",
        "game_over": "ГУЛЬНЯ СКОНЧАНА - Націсніце R для рэстарту або Q для меню",
        "bye": "Пакуль",
    },
    "kk": {
        "version": "Нұсқа КБ-1.02.00",
        "play": "Ойнау",
        "options": "Баптаулар",
        "exit": "Шығу",
        "select_1_3": "Таңдаңыз (1-3): ",
        "select_1_4": "Таңдаңыз (1-4): ",
        "select_1_7": "Таңдаңыз (1-7): ",
        "options_title": "--- БАПТАУЛАР ---",
        "ghost_piece": "Елес фигура",
        "language": "Тіл",
        "reset_defaults": "Әдепкіге қайтару",
        "back": "Артқа",
        "state_on": "ҚОСУЛЫ",
        "state_off": "ӨШІРУЛІ",
        "language_title": "--- ТІЛ ---",
        "language_current": "Ағымдағы: {language}",
        "english": "Ағылшын",
        "spanish": "Испан",
        "russian": "Орыс",
        "ukrainian": "Украин",
        "belarusian": "Беларусь",
        "kazakh": "Қазақ",
        "controls_hint": "Басқаруды көрсету/жасыру үшін H басыңыз",
        "game_over": "ОЙЫН АЯҚТАЛДЫ - Қайта бастау үшін R, мәзір үшін Q",
        "bye": "Сау бол",
    },
}

SHAPES = {
    "I": [
        [(0, -1), (0, 0), (0, 1), (0, 2)],
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [(1, -1), (1, 0), (1, 1), (1, 2)],
        [(-1, 1), (0, 1), (1, 1), (2, 1)],
    ],
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    "T": [
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(0, -1), (0, 0), (1, 0), (0, 1)],
        [(-1, 0), (0, 0), (1, 0), (0, -1)],
        [(0, -1), (0, 0), (-1, 0), (0, 1)],
    ],
    "S": [[(0, 0), (1, 0), (0, 1), (-1, 1)], [(0, -1), (0, 0), (1, 0), (1, 1)]],
    "Z": [[(0, 0), (-1, 0), (0, 1), (1, 1)], [(0, -1), (0, 0), (-1, 0), (-1, 1)]],
    "J": [
        [(0, -1), (0, 0), (0, 1), (-1, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 0)],
        [(0, -1), (1, -1), (1, 0), (1, 1)],
        [(-1, 0), (0, 0), (1, 0), (1, -1)],
    ],
    "L": [
        [(0, -1), (0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, -1), (1, -1), (1, 0), (1, 1)],
        [(-1, 1), (0, 1), (1, 1), (1, 0)],
    ],
}


class Tetris:
    def __init__(self, options):
        self.options = dict(options)
        self.high_score = self.load_high_score()
        self.reset()

    def reset(self):
        self.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.base_fall_speed = DIFFICULTY_SPEEDS.get(
            self.options.get("difficulty", "normal"),
            START_FALL_SPEED,
        )
        self.fall_speed = self.base_fall_speed
        self.game_over = False

        self.held_piece = None
        self.hold_used = False

        self.combo = -1
        self.back_to_back = False
        self.last_move_was_rotate = False

        self.bag = []
        self.next_queue = []
        self._fill_next_queue(PREVIEW_COUNT + 1)

        self.shape_key = None
        self.rotation = 0
        self.x = WIDTH // 2
        self.y = 1
        self._last_rendered_lines = 0
        self.spawn_piece()

    def load_high_score(self):
        try:
            if HIGH_SCORE_FILE.exists():
                data = json.loads(HIGH_SCORE_FILE.read_text(encoding="utf-8"))
                return int(data.get("high_score", 0))
        except (OSError, json.JSONDecodeError, ValueError):
            pass
        return 0

    def save_high_score(self):
        try:
            HIGH_SCORE_FILE.write_text(
                json.dumps({"high_score": self.high_score}, indent=2), encoding="utf-8"
            )
        except OSError:
            pass

    def _refill_bag(self):
        pieces = list(SHAPES.keys())
        random.shuffle(pieces)
        self.bag.extend(pieces)

    def _pop_from_bag(self):
        if not self.bag:
            self._refill_bag()
        return self.bag.pop()

    def _fill_next_queue(self, size):
        while len(self.next_queue) < size:
            self.next_queue.append(self._pop_from_bag())

    def spawn_piece(self):
        self._fill_next_queue(PREVIEW_COUNT + 1)
        self.shape_key = self.next_queue.pop(0)
        self.rotation = 0
        self.x = WIDTH // 2
        self.y = 1
        self.hold_used = False
        self.last_move_was_rotate = False
        self._fill_next_queue(PREVIEW_COUNT + 1)
        if self.check_collision(0, 0, self.rotation):
            self.game_over = True
            self.update_high_score()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def get_current_coords(self, rotation=None):
        if rotation is None:
            rotation = self.rotation
        rotations = SHAPES[self.shape_key]
        return rotations[rotation % len(rotations)]

    def draw_piece_preview(self, shape_key):
        if shape_key is None:
            return [tr(self.options, "empty")]

        coords = SHAPES[shape_key][0]
        min_x = min(c[0] for c in coords)
        max_x = max(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        max_y = max(c[1] for c in coords)

        lines = []
        for y in range(min_y, max_y + 1):
            row = ""
            for x in range(min_x, max_x + 1):
                row += BLOCK if (x, y) in coords else EMPTY
            lines.append(row.rstrip() or EMPTY)
        return lines

    def get_ghost_y(self):
        ghost_y = self.y
        while not self.check_collision(0, ghost_y - self.y + 1, self.rotation):
            ghost_y += 1
        return ghost_y

    def draw(self, paused=False, show_controls=False):
        lines = []

        lines.append(
            tr(
                self.options,
                "game_header",
                score=self.score,
                high=self.high_score,
                level=self.level,
                lines=self.lines_cleared,
            )
        )

        held_lines = self.draw_piece_preview(self.held_piece)
        lines.append(tr(self.options, "hold"))
        for line in held_lines:
            lines.append(line)

        lines.append(tr(self.options, "next"))
        for i, piece in enumerate(self.next_queue[:PREVIEW_COUNT], start=1):
            lines.append(f"{i}.")
            for line in self.draw_piece_preview(piece):
                lines.append(line)

        display_board = [row[:] for row in self.board]

        if self.options.get("show_ghost", True):
            ghost_y = self.get_ghost_y()
            for dx, dy in self.get_current_coords():
                py, px = ghost_y + dy, self.x + dx
                if 0 <= py < HEIGHT and 0 <= px < WIDTH and display_board[py][px] == EMPTY:
                    display_board[py][px] = GHOST

        for dx, dy in self.get_current_coords():
            py, px = self.y + dy, self.x + dx
            if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                display_board[py][px] = BLOCK

        for row in display_board:
            lines.append("|" + "".join(row) + "|")
        lines.append("-" * (WIDTH * 2 + 2))

        if paused:
            lines.append(tr(self.options, "paused"))
        else:
            if show_controls:
                lines.append(tr(self.options, "controls_1"))
                lines.append(tr(self.options, "controls_2"))
            else:
                lines.append(tr(self.options, "controls_hint"))

        # Redraw in place without full-screen erase to avoid flicker.
        rendered = "\033[H" + "\n".join(f"{line}\033[K" for line in lines)
        extra = self._last_rendered_lines - len(lines)
        if extra > 0:
            rendered += "\n" + "\n".join("\033[K" for _ in range(extra))
        print(rendered, end="")
        self._last_rendered_lines = len(lines)

    def check_collision(self, dx, dy, rot):
        for bx, by in self.get_current_coords(rot):
            nx, ny = self.x + bx + dx, self.y + by + dy
            if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                return True
            if ny >= 0 and self.board[ny][nx] != EMPTY:
                return True
        return False

    def move(self, dx, dy, soft_drop=False):
        if not self.check_collision(dx, dy, self.rotation):
            self.x += dx
            self.y += dy
            self.last_move_was_rotate = False
            if dy > 0 and soft_drop:
                self.score += 1
                self.update_high_score()
            return True

        if dy > 0:
            self.lock_piece()
        return False

    def lock_piece(self):
        t_spin = self.is_t_spin()

        for dx, dy in self.get_current_coords():
            py, px = self.y + dy, self.x + dx
            if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                self.board[py][px] = BLOCK

        lines = self.clear_lines()
        self.apply_scoring(lines, t_spin=t_spin)
        self.spawn_piece()

    def is_t_spin(self):
        if self.shape_key != "T" or not self.last_move_was_rotate:
            return False

        cx, cy = self.x, self.y
        occupied_corners = 0
        for ox, oy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            px, py = cx + ox, cy + oy
            if px < 0 or px >= WIDTH or py >= HEIGHT:
                occupied_corners += 1
            elif py >= 0 and self.board[py][px] != EMPTY:
                occupied_corners += 1

        return occupied_corners >= 3

    def clear_lines(self):
        new_board = [row for row in self.board if EMPTY in row]
        lines_cleared = HEIGHT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [EMPTY for _ in range(WIDTH)])
        self.board = new_board
        return lines_cleared

    def apply_scoring(self, lines, t_spin=False):
        if t_spin:
            t_spin_scores = {0: 400, 1: 800, 2: 1200, 3: 1600}
            base = t_spin_scores.get(lines, 0) * self.level

            if lines > 0 and self.back_to_back:
                base = int(base * 1.5)

            self.score += base

            if lines > 0:
                self.combo += 1
                self.score += 50 * self.combo * self.level if self.combo > 0 else 0
                self.lines_cleared += lines
            else:
                self.combo = -1

            self.back_to_back = lines > 0
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(MIN_FALL_SPEED, self.base_fall_speed * (0.85 ** (self.level - 1)))
            self.update_high_score()
            return

        if lines == 0:
            self.combo = -1
            self.back_to_back = False
            return

        self.combo += 1
        base = LINE_CLEAR_SCORES.get(lines, 0) * self.level

        if lines == 4:
            if self.back_to_back:
                base = int(base * 1.5)
            self.back_to_back = True
        else:
            self.back_to_back = False

        combo_bonus = 50 * self.combo * self.level if self.combo > 0 else 0

        self.score += base + combo_bonus
        self.lines_cleared += lines
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(MIN_FALL_SPEED, self.base_fall_speed * (0.85 ** (self.level - 1)))
        self.update_high_score()

    def hard_drop(self):
        drop_distance = 0
        while not self.check_collision(0, 1, self.rotation):
            self.y += 1
            drop_distance += 1

        self.last_move_was_rotate = False
        self.score += drop_distance * 2
        self.update_high_score()
        self.lock_piece()

    def rotate(self):
        new_rot = (self.rotation + 1) % len(SHAPES[self.shape_key])

        for kick_x in (0, -1, 1, -2, 2):
            if not self.check_collision(kick_x, 0, new_rot):
                self.x += kick_x
                self.rotation = new_rot
                self.last_move_was_rotate = True
                return True
        return False

    def hold_piece(self):
        if self.hold_used:
            return False

        current = self.shape_key
        if self.held_piece is None:
            self.held_piece = current
            self.spawn_piece()
        else:
            self.shape_key, self.held_piece = self.held_piece, current
            self.rotation = 0
            self.x = WIDTH // 2
            self.y = 1
            self.last_move_was_rotate = False
            if self.check_collision(0, 0, self.rotation):
                self.game_over = True
                self.update_high_score()

        self.hold_used = True
        return True


def clear_screen():
    print("\033[2J\033[H", end="")


def tr(options, key, **kwargs):
    lang = options.get("language", "en")
    language_pack = TEXTS.get(lang, TEXTS["en"])
    template = language_pack.get(key, TEXTS["en"].get(key, key))
    return template.format(**kwargs)


def language_label(options, code):
    key = {
        "en": "english",
        "es": "spanish",
        "ru": "russian",
        "uk": "ukrainian",
        "be": "belarusian",
        "kk": "kazakh",
    }.get(code, "english")
    return tr(options, key)


def difficulty_label(options, difficulty):
    key = {
        "easy": "difficulty_easy",
        "normal": "difficulty_normal",
        "hard": "difficulty_hard",
        "extreme": "difficulty_extreme",
    }.get(difficulty, "difficulty_normal")
    return tr(options, key)


def show_main_menu(options):
    while True:
        clear_screen()
        print(tr(options, "main_title"))
        print(tr(options, "version"))
        print(f"1. {tr(options, 'play')}")
        print(f"2. {tr(options, 'options')}")
        print(f"3. {tr(options, 'exit')}")
        choice = input(tr(options, "select_1_3")).strip().lower()

        if choice in ("1", "play", "jugar", "играть", "p"):
            return "play"
        if choice in ("2", "options", "opciones", "опции", "o"):
            return "options"
        if choice in ("3", "exit", "salir", "выход", "e", "q"):
            return "exit"


def show_language_menu(options):
    while True:
        clear_screen()
        print(tr(options, "language_title"))
        print(tr(options, "language_current", language=language_label(options, options["language"])))
        print(f"1. {tr(options, 'english')}")
        print(f"2. {tr(options, 'spanish')}")
        print(f"3. {tr(options, 'russian')}")
        print(f"4. {tr(options, 'ukrainian')}")
        print(f"5. {tr(options, 'belarusian')}")
        print(f"6. {tr(options, 'kazakh')}")
        print(f"7. {tr(options, 'back')}")
        choice = input(tr(options, "select_1_7")).strip().lower()

        if choice == "1":
            options["language"] = "en"
        elif choice == "2":
            options["language"] = "es"
        elif choice == "3":
            options["language"] = "ru"
        elif choice == "4":
            options["language"] = "uk"
        elif choice == "5":
            options["language"] = "be"
        elif choice == "6":
            options["language"] = "kk"
        elif choice == "7":
            return


def show_options_menu(options):
    while True:
        clear_screen()
        ghost_state = tr(options, "state_on") if options["show_ghost"] else tr(options, "state_off")
        print(tr(options, "options_title"))
        print(f"1. {tr(options, 'ghost_piece')}: {ghost_state}")
        print(f"2. {tr(options, 'difficulty')}: {difficulty_label(options, options['difficulty'])}")
        print(f"3. {tr(options, 'language')}: {language_label(options, options['language'])}")
        print(f"4. {tr(options, 'reset_defaults')}")
        print(f"5. {tr(options, 'back')}")
        choice = input(tr(options, "select_1_5")).strip().lower()

        if choice == "1":
            options["show_ghost"] = not options["show_ghost"]
        elif choice == "2":
            cycle = ["easy", "normal", "hard", "extreme"]
            cur = options.get("difficulty", "normal")
            idx = cycle.index(cur) if cur in cycle else 1
            options["difficulty"] = cycle[(idx + 1) % len(cycle)]
        elif choice == "3":
            show_language_menu(options)
        elif choice == "4":
            options.clear()
            options.update(DEFAULT_OPTIONS)
        elif choice in ("5", "b", "back"):
            return


def run_game(options):
    game = Tetris(options)
    clear_screen()

    paused = False
    show_controls = False
    last_fall_time = time.time()
    one_shot_keys = {"up": False, "space": False, "shift": False, "p": False, "r": False, "q": False, "h": False}

    def just_pressed(key):
        is_down = keyboard.is_pressed(key)
        was_down = one_shot_keys[key]
        one_shot_keys[key] = is_down
        return is_down and not was_down

    while True:
        game.draw(paused=paused, show_controls=show_controls)

        if just_pressed("q"):
            game.update_high_score()
            return

        if just_pressed("r"):
            game = Tetris(options)
            paused = False
            last_fall_time = time.time()
            clear_screen()
            continue

        if just_pressed("p"):
            paused = not paused

        if just_pressed("h"):
            show_controls = not show_controls

        if game.game_over:
            print(tr(options, "game_over"))
            time.sleep(0.05)
            continue

        if not paused:
            if keyboard.is_pressed("left"):
                game.move(-1, 0)
            if keyboard.is_pressed("right"):
                game.move(1, 0)
            if keyboard.is_pressed("down"):
                game.move(0, 1, soft_drop=True)
            if just_pressed("up"):
                game.rotate()
            if just_pressed("space"):
                game.hard_drop()
            if just_pressed("shift"):
                game.hold_piece()

            if time.time() - last_fall_time > game.fall_speed:
                game.move(0, 1)
                last_fall_time = time.time()

        time.sleep(0.05)


def main():
    options = dict(DEFAULT_OPTIONS)

    while True:
        action = show_main_menu(options)
        if action == "play":
            run_game(options)
        elif action == "options":
            show_options_menu(options)
        else:
            clear_screen()
            print(tr(options, "bye"))
            return


if __name__ == "__main__":
    main()
