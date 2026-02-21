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
LEADERBOARD_LIMIT = 10


def _sanitize_initials(text):
    cleaned = "".join(ch for ch in text.upper() if ch.isalnum())
    return (cleaned[:3] or "AAA")


def _normalize_leaderboard(entries):
    normalized = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        try:
            score = int(entry.get("score", 0))
        except (TypeError, ValueError):
            continue
        initials = _sanitize_initials(str(entry.get("initials", "")))
        normalized.append({"initials": initials, "score": score})
    normalized.sort(key=lambda e: e["score"], reverse=True)
    return normalized[:LEADERBOARD_LIMIT]


def load_scores_data():
    data = {"high_score": 0, "leaderboard": []}
    try:
        if HIGH_SCORE_FILE.exists():
            raw = json.loads(HIGH_SCORE_FILE.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                data["high_score"] = int(raw.get("high_score", 0))
                data["leaderboard"] = _normalize_leaderboard(raw.get("leaderboard", []))
    except (OSError, json.JSONDecodeError, ValueError, TypeError):
        pass

    if data["leaderboard"]:
        data["high_score"] = max(data["high_score"], data["leaderboard"][0]["score"])
    return data


def save_scores_data(data):
    payload = {
        "high_score": int(data.get("high_score", 0)),
        "leaderboard": _normalize_leaderboard(data.get("leaderboard", [])),
    }
    try:
        HIGH_SCORE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError:
        pass


def score_qualifies_for_leaderboard(score):
    if score <= 0:
        return False
    data = load_scores_data()
    board = data["leaderboard"]
    if len(board) < LEADERBOARD_LIMIT:
        return True
    return score > board[-1]["score"]


def add_leaderboard_entry(initials, score):
    if score <= 0:
        return
    data = load_scores_data()
    board = data["leaderboard"]
    board.append({"initials": _sanitize_initials(initials), "score": int(score)})
    data["leaderboard"] = _normalize_leaderboard(board)
    if data["leaderboard"]:
        data["high_score"] = max(int(data.get("high_score", 0)), data["leaderboard"][0]["score"])
    save_scores_data(data)

DEFAULT_OPTIONS = {
    "show_ghost": True,
    "language": "en",
    "difficulty": "normal",
}

LANGUAGE_ORDER = ["en", "es", "ru", "uk", "be", "kk", "fr", "de", "it", "ka", "hy", "az", "nl", "vl", "fy"]

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
        "version": "Version rc-1.05.00",
        "options": "Options",
        "leaderboard": "Leaderboard",
        "exit": "Exit",
        "select_1_3": "Select an option (1-3): ",
        "select_1_4": "Select an option (1-4): ",
        "select_1_5": "Select an option (1-5): ",
        "select_1_7": "Select an option (1-7): ",
        "select_1_10": "Select an option (1-10): ",
        "select_1_13": "Select an option (1-13): ",
        "select_1_16": "Select an option (1-16): ",
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
        "french": "French",
        "german": "German",
        "italian": "Italian",
        "georgian": "Georgian",
        "armenian": "Armenian",
        "azerbaijani": "Azerbaijani",
        "dutch": "Dutch",
        "flemish": "Flemish",
        "frisian": "Frisian",
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
        "leaderboard_title": "--- LEADERBOARD ---",
        "no_scores": "No scores yet.",
        "initials_prompt": "New leaderboard score. Enter initials (3 chars): ",
        "initials_saved": "Saved: {initials} - {score}",
        "press_enter": "Press Enter to continue...",
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
        "version": "Versión cal-1.05.00",
        "options": "Opciones",
        "exit": "Salir",
        "select_1_3": "Selecciona una opcion (1-3): ",
        "select_1_4": "Selecciona una opcion (1-4): ",
        "select_1_5": "Selecciona una opcion (1-5): ",
        "select_1_7": "Selecciona una opcion (1-7): ",
        "select_1_10": "Selecciona una opcion (1-10): ",
        "select_1_13": "Selecciona una opcion (1-13): ",
        "select_1_16": "Selecciona una opcion (1-16): ",
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
        "french": "Frances",
        "german": "Aleman",
        "italian": "Italiano",
        "georgian": "Georgiano",
        "armenian": "Armenio",
        "azerbaijani": "Azerbaiyano",
        "dutch": "Neerlandes",
        "flemish": "Flamenco",
        "frisian": "Frison",
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
█████ ████   █████   ████  █   █   ████
  █       █    █    █   █  █  ██  █        
  █     ██     █     ████  █ █ █  █    
  █       █    █    █   █  ██  █  █       
  █   ████     █    █   █  █   █   ████ 
""",
        "version": "Версия КНР-1.05.00",
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
        "main_title": """
█████ ████   █████   ████  █████   ████
  █       █    █    █   █    █    █        
  █     ██     █     ████    █    █    
  █       █    █    █   █    █    █       
  █   ████     █    █   █  █████   ████ 
""",
        "version": "Версія ЗК-1.05.00",
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
        "main_title": """
█████ ████   █████   ████  █████   ████
  █       █    █    █   █    █    █        
  █     ██     █     ████    █    █    
  █       █    █    █   █    █    █       
  █   ████     █    █   █  █████   ████ 
""",
        "version": "Версія КНВ-1.05.00",
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
        "main_title": """
█████ ████   █████   ████  █   █   ████
  █       █    █    █   █  █  ██  █        
  █     ██     █     ████  █ █ █  █    
  █       █    █    █   █  ██  █  █       
  █   ████     █    █   █  █   █   ████ 
""",
        "version": "Нұсқа КБ-1.05.00",
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
    "fr": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Jouer",
        "version": "Version rc-1.05.00",
        "options": "Options",
        "exit": "Quitter",
        "select_1_3": "Choisissez une option (1-3): ",
        "select_1_4": "Choisissez une option (1-4): ",
        "select_1_5": "Choisissez une option (1-5): ",
        "select_1_10": "Choisissez une option (1-10): ",
        "options_title": "--- OPTIONS ---",
        "ghost_piece": "Piece fantome",
        "difficulty": "Difficulte",
        "language": "Langue",
        "reset_defaults": "Reinitialiser",
        "back": "Retour",
        "state_on": "ACTIF",
        "state_off": "INACTIF",
        "language_title": "--- LANGUE ---",
        "language_current": "Actuelle: {language}",
        "english": "Anglais",
        "spanish": "Espagnol",
        "russian": "Russe",
        "ukrainian": "Ukrainien",
        "belarusian": "Bielorusse",
        "kazakh": "Kazakh",
        "french": "Francais",
        "german": "Allemand",
        "italian": "Italien",
        "difficulty_easy": "Facile",
        "difficulty_normal": "Normal",
        "difficulty_hard": "Difficile",
        "difficulty_extreme": "Extreme",
        "game_header": "--- TETRIS --- SCORE: {score} | RECORD: {high} | NIVEAU: {level} | LIGNES: {lines}",
        "hold": "RESERVE:",
        "next": "SUIVANT:",
        "empty": "(vide)",
        "paused": "PAUSE - Appuyez sur P pour reprendre",
        "controls_1": "Haut: Rotation | Gauche/Droite: Deplacer | Bas: Descente douce | Espace: Chute rapide",
        "controls_2": "Shift: Garder | P: Pause | R: Recommencer | Q: Menu",
        "controls_hint": "Appuyez sur H pour afficher/masquer les commandes",
        "game_over": "PARTIE TERMINEE - Appuyez sur R pour recommencer ou Q pour le menu",
        "bye": "Au revoir",
    },
    "de": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Spielen",
        "version": "Version rc-1.05.00",
        "options": "Optionen",
        "exit": "Beenden",
        "select_1_3": "Option waehlen (1-3): ",
        "select_1_4": "Option waehlen (1-4): ",
        "select_1_5": "Option waehlen (1-5): ",
        "select_1_10": "Option waehlen (1-10): ",
        "options_title": "--- OPTIONEN ---",
        "ghost_piece": "Geisterstein",
        "difficulty": "Schwierigkeit",
        "language": "Sprache",
        "reset_defaults": "Zuruecksetzen",
        "back": "Zurueck",
        "state_on": "AN",
        "state_off": "AUS",
        "language_title": "--- SPRACHE ---",
        "language_current": "Aktuell: {language}",
        "english": "Englisch",
        "spanish": "Spanisch",
        "russian": "Russisch",
        "ukrainian": "Ukrainisch",
        "belarusian": "Belarussisch",
        "kazakh": "Kasachisch",
        "french": "Franzoesisch",
        "german": "Deutsch",
        "italian": "Italienisch",
        "difficulty_easy": "Leicht",
        "difficulty_normal": "Normal",
        "difficulty_hard": "Schwer",
        "difficulty_extreme": "Extrem",
        "game_header": "--- TETRIS --- PUNKTE: {score} | REKORD: {high} | LEVEL: {level} | LINIEN: {lines}",
        "hold": "HALTEN:",
        "next": "NAECHSTE:",
        "empty": "(leer)",
        "paused": "PAUSE - Druecke P zum Fortsetzen",
        "controls_1": "Oben: Drehen | Links/Rechts: Bewegen | Unten: Soft Drop | Leertaste: Hard Drop",
        "controls_2": "Shift: Halten | P: Pause | R: Neustart | Q: Menue",
        "controls_hint": "Druecke H, um Steuerung ein/auszublenden",
        "game_over": "SPIEL VORBEI - Druecke R fuer Neustart oder Q fuer Menue",
        "bye": "Tschuess",
    },
    "it": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Gioca",
        "version": "Versione rc-1.05.00",
        "options": "Opzioni",
        "exit": "Esci",
        "select_1_3": "Seleziona un'opzione (1-3): ",
        "select_1_4": "Seleziona un'opzione (1-4): ",
        "select_1_5": "Seleziona un'opzione (1-5): ",
        "select_1_10": "Seleziona un'opzione (1-10): ",
        "options_title": "--- OPZIONI ---",
        "ghost_piece": "Pezzo fantasma",
        "difficulty": "Difficolta",
        "language": "Lingua",
        "reset_defaults": "Ripristina",
        "back": "Indietro",
        "state_on": "ON",
        "state_off": "OFF",
        "language_title": "--- LINGUA ---",
        "language_current": "Corrente: {language}",
        "english": "Inglese",
        "spanish": "Spagnolo",
        "russian": "Russo",
        "ukrainian": "Ucraino",
        "belarusian": "Bielorusso",
        "kazakh": "Kazako",
        "french": "Francese",
        "german": "Tedesco",
        "italian": "Italiano",
        "difficulty_easy": "Facile",
        "difficulty_normal": "Normale",
        "difficulty_hard": "Difficile",
        "difficulty_extreme": "Estremo",
        "game_header": "--- TETRIS --- PUNTEGGIO: {score} | RECORD: {high} | LIVELLO: {level} | LINEE: {lines}",
        "hold": "HOLD:",
        "next": "PROSSIMI:",
        "empty": "(vuoto)",
        "paused": "PAUSA - Premi P per continuare",
        "controls_1": "Su: Ruota | Sinistra/Destra: Muovi | Giu: Discesa lenta | Spazio: Caduta rapida",
        "controls_2": "Shift: Hold | P: Pausa | R: Riavvia | Q: Menu",
        "controls_hint": "Premi H per mostrare/nascondere i comandi",
        "game_over": "PARTITA FINITA - Premi R per riavviare o Q per il menu",
        "bye": "Ciao",
    },
    "ka": {
        "main_title": """
  █     ███     █     ████        █    
  █    █   █    █    █            █    
 ███       █   ███    █ █    ███  █  █   ███ 
█   █  █   █  █   █  █ █ █  █   █ █   █ █   █
 ███    ███    ███   █   █  █   █  ███  █   █
""",
        "play": "თამაში",
        "version": "ვერსია ქრთ-1.05.00",
        "options": "პარამეტრები",
        "leaderboard": "ლიდერბორდი",
        "exit": "გასვლა",
        "select_1_4": "აირჩიეთ ვარიანტი (1-4): ",
        "select_1_5": "აირჩიეთ ვარიანტი (1-5): ",
        "select_1_13": "აირჩიეთ ვარიანტი (1-13): ",
        "options_title": "--- პარამეტრები ---",
        "ghost_piece": "აჩრდილის ფიგურა",
        "difficulty": "სირთულე",
        "language": "ენა",
        "reset_defaults": "საწყისზე დაბრუნება",
        "back": "უკან",
        "state_on": "ჩართული",
        "state_off": "გამორთული",
        "language_title": "--- ენა ---",
        "language_current": "მიმდინარე: {language}",
        "english": "ინგლისური",
        "spanish": "ესპანური",
        "russian": "რუსული",
        "ukrainian": "უკრაინული",
        "belarusian": "ბელარუსული",
        "kazakh": "ყაზახური",
        "french": "ფრანგული",
        "german": "გერმანული",
        "italian": "იტალიური",
        "georgian": "ქართული",
        "armenian": "სომხური",
        "azerbaijani": "აზერბაიჯანული",
        "difficulty_easy": "მარტივი",
        "difficulty_normal": "საშუალო",
        "difficulty_hard": "რთული",
        "difficulty_extreme": "ექსტრემალური",
        "game_header": "--- ტეტრისი --- ქულა: {score} | რეკორდი: {high} | დონე: {level} | ხაზები: {lines}",
        "hold": "დაჭერა:",
        "next": "შემდეგი:",
        "empty": "(ცარიელი)",
        "paused": "პაუზა - გაგრძელებისთვის დააჭირეთ P",
        "controls_1": "ზემოთ: მობრუნება | მარცხ/მარჯვ: მოძრაობა | ქვემოთ: ნელი ვარდნა | Space: სწრაფი ვარდნა",
        "controls_2": "Shift: დაჭერა | P: პაუზა | R: თავიდან | Q: მენიუ",
        "controls_hint": "H-ს დაჭერით აჩვენეთ/დამალეთ მართვა",
        "game_over": "თამაში დასრულდა - R თავიდან ან Q მენიუში",
        "leaderboard_title": "--- ლიდერბორდი ---",
        "no_scores": "ქულები ჯერ არ არის.",
        "initials_prompt": "ახალი შედეგი! შეიყვანეთ ინიციალები (3 სიმბოლო): ",
        "initials_saved": "შენახულია: {initials} - {score}",
        "press_enter": "გასაგრძელებლად Enter...",
        "bye": "ნახვამდის",
    },
    "hy": {
        "main_title": """
█████ █      █   █   █████ █     █   █
█     █      █  █ █  █   █ █     █   █
█████ █████  █  █ █  █   █ █████ █   █
    █ █      █  █ █  █     █   █ █   █
█████ █████  ████ █  █     █     █████
""",
        "play": "Խաղալ",
        "version": "Տարբերակ հտ-1.05.00",
        "options": "Կարգավորումներ",
        "leaderboard": "Վարկանիշ",
        "exit": "Ելք",
        "select_1_4": "Ընտրեք տարբերակ (1-4): ",
        "select_1_5": "Ընտրեք տարբերակ (1-5): ",
        "select_1_13": "Ընտրեք տարբերակ (1-13): ",
        "options_title": "--- ԿԱՐԳԱՎՈՐՈՒՄՆԵՐ ---",
        "ghost_piece": "Ուրվական ֆիգուր",
        "difficulty": "Դժվարություն",
        "language": "Լեզու",
        "reset_defaults": "Վերակայել",
        "back": "Հետ",
        "state_on": "Միացված",
        "state_off": "Անջատված",
        "language_title": "--- ԼԵԶՈՒ ---",
        "language_current": "Ընթացիկ: {language}",
        "english": "Անգլերեն",
        "spanish": "Իսպաներեն",
        "russian": "Ռուսերեն",
        "ukrainian": "Ուկրաիներեն",
        "belarusian": "Բելառուսերեն",
        "kazakh": "Ղազախերեն",
        "french": "Ֆրանսերեն",
        "german": "Գերմաներեն",
        "italian": "Իտալերեն",
        "georgian": "Վրացերեն",
        "armenian": "Հայերեն",
        "azerbaijani": "Ադրբեջաներեն",
        "difficulty_easy": "Հեշտ",
        "difficulty_normal": "Նորմալ",
        "difficulty_hard": "Դժվար",
        "difficulty_extreme": "Էքստրիմ",
        "game_header": "--- TETRIS --- ՄԻԱՎՈՐ: {score} | ՌԵԿՈՐԴ: {high} | ՄԱԿԱՐԴԱԿ: {level} | ԳԾԵՐ: {lines}",
        "hold": "ՊԱՀԵԼ:",
        "next": "ՀԱՋՈՐԴԸ:",
        "empty": "(դատարկ)",
        "paused": "ԴԱԴԱՐ - Շարունակելու համար սեղմեք P",
        "controls_1": "Վերև: Պտտել | Ձախ/Աջ: Շարժել | Ներքև: Դանդաղ իջեցում | Space: Արագ իջեցում",
        "controls_2": "Shift: Պահել | P: Դադար | R: Վերսկսել | Q: Մենյու",
        "controls_hint": "Սեղմեք H՝ կառավարումը ցույց տալու/թաքցնելու համար",
        "game_over": "ԽԱՂԸ ՎԵՐՋԱՑԱՎ - Սեղմեք R՝ նորից կամ Q՝ մենյու",
        "leaderboard_title": "--- ՎԱՐԿԱՆԻՇ ---",
        "no_scores": "Միավորներ դեռ չկան։",
        "initials_prompt": "Նոր արդյունք։ Մուտքագրեք սկզբնատառերը (3): ",
        "initials_saved": "Պահվեց: {initials} - {score}",
        "press_enter": "Շարունակելու համար Enter...",
        "bye": "Ցտեսություն",
    },
    "az": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Oyna",
        "version": "Versiya azr-1.05.00",
        "options": "Seçimlər",
        "leaderboard": "Liderlər cədvəli",
        "exit": "Çıxış",
        "select_1_4": "Seçim edin (1-4): ",
        "select_1_5": "Seçim edin (1-5): ",
        "select_1_13": "Seçim edin (1-13): ",
        "options_title": "--- SEÇİMLƏR ---",
        "ghost_piece": "Kölgə fiqur",
        "difficulty": "Çətinlik",
        "language": "Dil",
        "reset_defaults": "Sıfırla",
        "back": "Geri",
        "state_on": "AÇIQ",
        "state_off": "QAPALI",
        "language_title": "--- DİL ---",
        "language_current": "Cari: {language}",
        "english": "İngilis",
        "spanish": "İspan",
        "russian": "Rus",
        "ukrainian": "Ukrayna",
        "belarusian": "Belarus",
        "kazakh": "Qazax",
        "french": "Fransız",
        "german": "Alman",
        "italian": "İtalyan",
        "georgian": "Gürcü",
        "armenian": "Erməni",
        "azerbaijani": "Azərbaycan",
        "difficulty_easy": "Asan",
        "difficulty_normal": "Normal",
        "difficulty_hard": "Çətin",
        "difficulty_extreme": "Ekstrem",
        "game_header": "--- TETRIS --- XAL: {score} | REKORD: {high} | SƏVİYYƏ: {level} | XƏTLƏR: {lines}",
        "hold": "SAXLA:",
        "next": "NÖVBƏTİ:",
        "empty": "(boş)",
        "paused": "PAUZA - Davam üçün P basın",
        "controls_1": "Yuxarı: Döndür | Sol/Sağ: Hərəkət | Aşağı: Yumşaq düşüş | Space: Sərt düşüş",
        "controls_2": "Shift: Saxla | P: Pauza | R: Yenidən başla | Q: Menyu",
        "controls_hint": "İdarəni göstərmək/gizlətmək üçün H basın",
        "game_over": "OYUN BİTDİ - Yenidən başlamaq üçün R, menyu üçün Q",
        "leaderboard_title": "--- LİDERLƏR CƏDVƏLİ ---",
        "no_scores": "Hələ xal yoxdur.",
        "initials_prompt": "Yeni nəticə! İnitialları daxil edin (3 simvol): ",
        "initials_saved": "Yadda saxlanıldı: {initials} - {score}",
        "press_enter": "Davam etmək üçün Enter...",
        "bye": "Sağ ol",
    },
    "nl": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Spelen",
        "version": "Versie nl-1.05.00",
        "options": "Opties",
        "leaderboard": "Ranglijst",
        "exit": "Afsluiten",
        "select_1_4": "Kies een optie (1-4): ",
        "select_1_5": "Kies een optie (1-5): ",
        "select_1_16": "Kies een optie (1-16): ",
        "options_title": "--- OPTIES ---",
        "ghost_piece": "Spookstuk",
        "difficulty": "Moeilijkheid",
        "language": "Taal",
        "reset_defaults": "Herstellen",
        "back": "Terug",
        "state_on": "AAN",
        "state_off": "UIT",
        "language_title": "--- TAAL ---",
        "language_current": "Huidig: {language}",
        "english": "Engels",
        "spanish": "Spaans",
        "russian": "Russisch",
        "ukrainian": "Oekraïens",
        "belarusian": "Belarussisch",
        "kazakh": "Kazachs",
        "french": "Frans",
        "german": "Duits",
        "italian": "Italiaans",
        "georgian": "Georgisch",
        "armenian": "Armeens",
        "azerbaijani": "Azerbeidzjaans",
        "dutch": "Nederlands",
        "flemish": "Vlaams",
        "frisian": "Fries",
        "difficulty_easy": "Makkelijk",
        "difficulty_normal": "Normaal",
        "difficulty_hard": "Moeilijk",
        "difficulty_extreme": "Extreem",
        "game_header": "--- TETRIS --- SCORE: {score} | HIGH: {high} | LEVEL: {level} | LIJNEN: {lines}",
        "hold": "BEWAAR:",
        "next": "VOLGENDE:",
        "empty": "(leeg)",
        "paused": "PAUZE - Druk op P om verder te gaan",
        "controls_1": "Omhoog: Draaien | Links/Rechts: Bewegen | Omlaag: Zachte val | Spatie: Harde val",
        "controls_2": "Shift: Bewaar | P: Pauze | R: Herstart | Q: Menu",
        "controls_hint": "Druk op H om besturing te tonen/verbergen",
        "game_over": "SPEL VOORBIJ - Druk op R voor herstart of Q voor menu",
        "leaderboard_title": "--- RANGLIJST ---",
        "no_scores": "Nog geen scores.",
        "initials_prompt": "Nieuwe ranglijstscore. Initialen (3 tekens): ",
        "initials_saved": "Opgeslagen: {initials} - {score}",
        "press_enter": "Druk op Enter om door te gaan...",
        "bye": "Tot ziens",
    },
    "vl": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Spelen",
        "version": "Versie vl-1.05.00",
        "options": "Opties",
        "leaderboard": "Klassement",
        "exit": "Afsluiten",
        "select_1_4": "Kies een optie (1-4): ",
        "select_1_5": "Kies een optie (1-5): ",
        "select_1_16": "Kies een optie (1-16): ",
        "options_title": "--- OPTIES ---",
        "ghost_piece": "Spookblok",
        "difficulty": "Moeilijkheid",
        "language": "Taal",
        "reset_defaults": "Herstellen",
        "back": "Terug",
        "state_on": "AAN",
        "state_off": "UIT",
        "language_title": "--- TAAL ---",
        "language_current": "Huidig: {language}",
        "english": "Engels",
        "spanish": "Spaans",
        "russian": "Russisch",
        "ukrainian": "Oekraïens",
        "belarusian": "Wit-Russisch",
        "kazakh": "Kazachs",
        "french": "Frans",
        "german": "Duits",
        "italian": "Italiaans",
        "georgian": "Georgisch",
        "armenian": "Armeens",
        "azerbaijani": "Azerbeidzjaans",
        "dutch": "Nederlands",
        "flemish": "Vlaams",
        "frisian": "Fries",
        "difficulty_easy": "Makkelijk",
        "difficulty_normal": "Normaal",
        "difficulty_hard": "Moeilijk",
        "difficulty_extreme": "Extreem",
        "game_header": "--- TETRIS --- SCORE: {score} | HIGH: {high} | LEVEL: {level} | LIJNEN: {lines}",
        "hold": "HOUD:",
        "next": "VOLGENDE:",
        "empty": "(leeg)",
        "paused": "PAUZE - Druk op P om verder te doen",
        "controls_1": "Omhoog: Draaien | Links/Rechts: Bewegen | Omlaag: Zachte val | Spatie: Harde val",
        "controls_2": "Shift: Hou vast | P: Pauze | R: Herstart | Q: Menu",
        "controls_hint": "Druk op H om de besturing te tonen/verbergen",
        "game_over": "GAME OVER - Druk op R voor herstart of Q voor menu",
        "leaderboard_title": "--- KLASSEMENT ---",
        "no_scores": "Nog geen scores.",
        "initials_prompt": "Nieuwe score in klassement. Initialen (3 tekens): ",
        "initials_saved": "Opgeslagen: {initials} - {score}",
        "press_enter": "Druk op Enter om verder te gaan...",
        "bye": "Daag",
    },
    "fy": {
        "main_title": """
█████ █████ █████  ████  █████ █████
  █   █       █   █   █    █   █    
  █   ████    █    ████    █   █████
  █   █       █   █   █    █       █
  █   █████   █   █   █  █████ █████ 
""",
        "play": "Spylje",
        "version": "Ferzje fy-1.05.00",
        "options": "Opsjes",
        "leaderboard": "Klassemint",
        "exit": "Ofslute",
        "select_1_4": "Kies in opsje (1-4): ",
        "select_1_5": "Kies in opsje (1-5): ",
        "select_1_16": "Kies in opsje (1-16): ",
        "options_title": "--- OPSJES ---",
        "ghost_piece": "Spoekstik",
        "difficulty": "Muoilikheid",
        "language": "Taal",
        "reset_defaults": "Weromsette",
        "back": "Werom",
        "state_on": "OAN",
        "state_off": "UT",
        "language_title": "--- TAAL ---",
        "language_current": "No: {language}",
        "english": "Ingelsk",
        "spanish": "Spaansk",
        "russian": "Russysk",
        "ukrainian": "Oekraïnsk",
        "belarusian": "Wyt-Russysk",
        "kazakh": "Kazachsk",
        "french": "Frânsk",
        "german": "Dútsk",
        "italian": "Italiaansk",
        "georgian": "Georgysk",
        "armenian": "Armeensk",
        "azerbaijani": "Azerbeidzjaansk",
        "dutch": "Nederlânsk",
        "flemish": "Flaamsk",
        "frisian": "Frysk",
        "difficulty_easy": "Maklik",
        "difficulty_normal": "Normaal",
        "difficulty_hard": "Dreech",
        "difficulty_extreme": "Ekstreem",
        "game_header": "--- TETRIS --- PUNTEN: {score} | HEGE: {high} | LEVEL: {level} | LINIEN: {lines}",
        "hold": "FÊST:",
        "next": "FOLGJEND:",
        "empty": "(leech)",
        "paused": "PAUZE - Druk op P om troch te gean",
        "controls_1": "Omheech: Draaie | Links/Rjochts: Ferpleatse | Omleech: Sêfte drop | Spaasje: Hurde drop",
        "controls_2": "Shift: Fêsthâlde | P: Pauze | R: Opnij | Q: Menu",
        "controls_hint": "Druk op H om bestjoering te sjen/ferbergjen",
        "game_over": "SPUL OER - Druk op R foar opnij of Q foar menu",
        "leaderboard_title": "--- KLASSEMINT ---",
        "no_scores": "Noch gjin scores.",
        "initials_prompt": "Nije klassemintscore. Inisjalen (3 tekens): ",
        "initials_saved": "Bewarre: {initials} - {score}",
        "press_enter": "Druk op Enter om troch te gean...",
        "bye": "Oant sjen",
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
        return int(load_scores_data().get("high_score", 0))

    def save_high_score(self):
        data = load_scores_data()
        data["high_score"] = int(self.high_score)
        save_scores_data(data)

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

    def draw(self, paused=False, show_controls=False, status_message=None):
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

        if status_message:
            lines.append(status_message)
        elif paused:
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
        "fr": "french",
        "de": "german",
        "it": "italian",
        "ka": "georgian",
        "hy": "armenian",
        "az": "azerbaijani",
        "nl": "dutch",
        "vl": "flemish",
        "fy": "frisian",
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
        print(f"3. {tr(options, 'leaderboard')}")
        print(f"4. {tr(options, 'exit')}")
        choice = input(tr(options, "select_1_4")).strip().lower()

        if choice in ("1", "play", "jugar", "играть", "p"):
            return "play"
        if choice in ("2", "options", "opciones", "опции", "o"):
            return "options"
        if choice in ("3", "leaderboard", "l"):
            return "leaderboard"
        if choice in ("4", "exit", "e", "q"):
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
        print(f"7. {tr(options, 'french')}")
        print(f"8. {tr(options, 'german')}")
        print(f"9. {tr(options, 'italian')}")
        print(f"10. {tr(options, 'georgian')}")
        print(f"11. {tr(options, 'armenian')}")
        print(f"12. {tr(options, 'azerbaijani')}")
        print(f"13. {tr(options, 'dutch')}")
        print(f"14. {tr(options, 'flemish')}")
        print(f"15. {tr(options, 'frisian')}")
        print(f"16. {tr(options, 'back')}")
        choice = input(tr(options, "select_1_16")).strip().lower()

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
            options["language"] = "fr"
        elif choice == "8":
            options["language"] = "de"
        elif choice == "9":
            options["language"] = "it"
        elif choice == "10":
            options["language"] = "ka"
        elif choice == "11":
            options["language"] = "hy"
        elif choice == "12":
            options["language"] = "az"
        elif choice == "13":
            options["language"] = "nl"
        elif choice == "14":
            options["language"] = "vl"
        elif choice == "15":
            options["language"] = "fy"
        elif choice == "16":
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


def show_leaderboard(options):
    clear_screen()
    print(tr(options, "leaderboard_title"))
    data = load_scores_data()
    board = data.get("leaderboard", [])
    if not board:
        print(tr(options, "no_scores"))
    else:
        for i, entry in enumerate(board, start=1):
            print(f"{i:>2}. {entry['initials']}  {entry['score']}")
    input(tr(options, "press_enter"))


def prompt_for_leaderboard_initials(options, score):
    if not score_qualifies_for_leaderboard(score):
        return
    clear_screen()
    print(tr(options, "leaderboard_title"))
    initials = input(tr(options, "initials_prompt")).strip()
    initials = _sanitize_initials(initials)
    add_leaderboard_entry(initials, score)
    print(tr(options, "initials_saved", initials=initials, score=score))
    input(tr(options, "press_enter"))


def run_game(options):
    game = Tetris(options)
    clear_screen()

    paused = False
    score_submitted = False
    show_controls = False
    last_fall_time = time.time()
    one_shot_keys = {"up": False, "space": False, "shift": False, "p": False, "r": False, "q": False, "h": False}

    def just_pressed(key):
        is_down = keyboard.is_pressed(key)
        was_down = one_shot_keys[key]
        one_shot_keys[key] = is_down
        return is_down and not was_down

    while True:
        status_message = tr(options, "game_over") if game.game_over else None
        game.draw(paused=paused, show_controls=show_controls, status_message=status_message)

        if just_pressed("q"):
            game.update_high_score()
            return

        if just_pressed("r"):
            game = Tetris(options)
            paused = False
            score_submitted = False
            last_fall_time = time.time()
            clear_screen()
            continue

        if just_pressed("p"):
            paused = not paused

        if just_pressed("h"):
            show_controls = not show_controls

        if game.game_over:
            if not score_submitted:
                prompt_for_leaderboard_initials(options, game.score)
                game.high_score = game.load_high_score()
                score_submitted = True
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
        elif action == "leaderboard":
            show_leaderboard(options)
        else:
            clear_screen()
            print(tr(options, "bye"))
            return


if __name__ == "__main__":
    main()



