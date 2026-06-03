import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import random
from datetime import datetime

# ==================== DATA ====================
RACES = {
    "Человек": {
        "description": "Универсальные и адаптивные",
        "base_stats": {"Сила": 10, "Ловкость": 10, "Телосложение": 10, "Интеллект": 10, "Мудрость": 10, "Харизма": 10},
        "bonuses": {"Сила": 1, "Ловкость": 1, "Телосложение": 1, "Интеллект": 1, "Мудрость": 1, "Харизма": 1}
    },
    "Эльф": {
        "description": "Благородные и долгоживущие",
        "base_stats": {"Сила": 8, "Ловкость": 14, "Телосложение": 8, "Интеллект": 12, "Мудрость": 12, "Харизма": 10},
        "bonuses": {"Ловкость": 2, "Интеллект": 1}
    },
    "Дварф": {
        "description": "Крепкие и упорные горные жители",
        "base_stats": {"Сила": 12, "Ловкость": 8, "Телосложение": 14, "Интеллект": 10, "Мудрость": 12, "Харизма": 6},
        "bonuses": {"Телосложение": 2, "Сила": 1}
    },
    "Орк": {
        "description": "Мощные воины",
        "base_stats": {"Сила": 14, "Ловкость": 10, "Телосложение": 12, "Интеллект": 6, "Мудрость": 8, "Харизма": 6},
        "bonuses": {"Сила": 2, "Телосложение": 1}
    },
    "Гном": {
        "description": "Изобретательные и хитрые",
        "base_stats": {"Сила": 8, "Ловкость": 10, "Телосложение": 12, "Интеллект": 14, "Мудрость": 10, "Харизма": 8},
        "bonuses": {"Интеллект": 2, "Телосложение": 1}
    },
    "Полуэльф": {
        "description": "Между двух миров",
        "base_stats": {"Сила": 10, "Ловкость": 12, "Телосложение": 10, "Интеллект": 10, "Мудрость": 10, "Харизма": 12},
        "bonuses": {"Харизма": 2, "Ловкость": 1}
    }
}

CLASSES = {
    "Воин": {
        "description": "Мастер боя и оружия",
        "hit_die": 10,
        "primary_stat": "Сила",
        "saves": ["Сила", "Телосложение"],
        "skills": ["Атлетика", "Запугивание", "Выживание", "Восприятие"]
    },
    "Маг": {
        "description": "Властелин арканной магии",
        "hit_die": 6,
        "primary_stat": "Интеллект",
        "saves": ["Интеллект", "Мудрость"],
        "skills": ["Магия", "История", "Анализ", "Медицина"]
    },
    "Плут": {
        "description": "Мастер скрытности и ловкости",
        "hit_die": 8,
        "primary_stat": "Ловкость",
        "saves": ["Ловкость", "Интеллект"],
        "skills": ["Акробатика", "Ловкость рук", "Скрытность", "Обман"]
    },
    "Клирик": {
        "description": "Служитель божества",
        "hit_die": 8,
        "primary_stat": "Мудрость",
        "saves": ["Мудрость", "Харизма"],
        "skills": ["Медицина", "Проницательность", "Религия", "Убеждение"]
    },
    "Варвар": {
        "description": "Яростный воин диких земель",
        "hit_die": 12,
        "primary_stat": "Сила",
        "saves": ["Сила", "Телосложение"],
        "skills": ["Атлетика", "Запугивание", "Выживание", "Восприятие"]
    },
    "Бард": {
        "description": "Вдохновляющий музыкант и заклинатель",
        "hit_die": 8,
        "primary_stat": "Харизма",
        "saves": ["Ловкость", "Харизма"],
        "skills": ["Акробатика", "Обман", "Выступление", "Убеждение"]
    }
}

ALIGNMENTS = [
    "Законно-добрый", "Нейтрально-добрый", "Хаотично-добрый",
    "Законно-нейтральный", "Истинно нейтральный", "Хаотично-нейтральный",
    "Законно-злой", "Нейтрально-злой", "Хаотично-злой"
]

BACKGROUNDS = [
    "Аколит", "Преступник", "Народный герой", "Артист", "Мудрец",
    "Солдат", "Авантюрист", "Торговец", "Отшельник", "Благородный"
]

PORTRAIT_COLORS = {
    "skin": ["#F5DEB3", "#D2B48C", "#8B7355", "#5C4033", "#3B2F2F", "#FFE0BD", "#E8BEAC"],
    "hair": ["#000000", "#4A3728", "#8B4513", "#FFD700", "#C0C0C0", "#FF4500", "#FFFFFF", "#8B0000"],
    "eyes": ["#4B8B3B", "#5B4B3A", "#4A6FA5", "#8B7355", "#808080", "#4A2C2A", "#6B4226"],
    "clothes": ["#8B0000", "#2F4F4F", "#4B0082", "#006400", "#8B4513", "#191970", "#556B2F", "#800080"]
}

PORTRAIT_FEATURES = {
    "face_shapes": ["oval", "round", "square", "heart"],
    "hair_styles": ["short", "long", "bald", "ponytail", "mohawk", "curly"],
    "facial_features": ["none", "beard", "mustache", "goatee", "scar", "glasses"]
}


# ==================== PORTRAIT GENERATOR ====================
class PortraitGenerator:
    def __init__(self, canvas_width=200, canvas_height=250):
        self.width = canvas_width
        self.height = canvas_height

    def generate_portrait(self, canvas, race, char_class, gender="Мужской", seed=None):
        """Генерирует портрет персонажа на Canvas"""
        if seed:
            random.seed(seed)

        canvas.delete("all")

        # Выбор цветов
        skin_color = random.choice(PORTRAIT_COLORS["skin"])
        hair_color = random.choice(PORTRAIT_COLORS["hair"])
        eye_color = random.choice(PORTRAIT_COLORS["eyes"])
        clothes_color = random.choice(PORTRAIT_COLORS["clothes"])

        face_shape = random.choice(PORTRAIT_FEATURES["face_shapes"])
        hair_style = random.choice(PORTRAIT_FEATURES["hair_styles"])
        facial_feature = random.choice(PORTRAIT_FEATURES["facial_features"])

        # Модификации по расе
        if race == "Орк":
            skin_color = random.choice(["#5C8A5C", "#4A6741", "#6B8E6B", "#3D5C3D"])
            face_shape = "square"
        elif race == "Эльф":
            face_shape = "heart"
            hair_style = random.choice(["long", "ponytail"])
        elif race == "Дварф":
            face_shape = "round"
            facial_feature = random.choice(["beard", "mustache", "goatee"])
        elif race == "Гном":
            face_shape = "round"
            facial_feature = random.choice(["beard", "goatee"])

        cx, cy = self.width // 2, self.height // 2

        # Фон
        canvas.create_rectangle(0, 0, self.width, self.height, fill="#2C2C2C", outline="")

        # Плащ/одежда (нижняя часть)
        canvas.create_polygon(
            cx - 70, cy + 40,
            cx + 70, cy + 40,
            cx + 90, self.height,
            cx - 90, self.height,
            fill=clothes_color, outline="#1a1a1a", width=2
        )

        # Воротник
        canvas.create_polygon(
            cx - 40, cy + 35,
            cx + 40, cy + 35,
            cx + 50, cy + 70,
            cx - 50, cy + 70,
            fill="#333333", outline="#1a1a1a", width=1
        )

        # Шея
        canvas.create_rectangle(cx - 20, cy + 20, cx + 20, cy + 50, 
                               fill=skin_color, outline="")

        # Лицо (форма)
        if face_shape == "oval":
            canvas.create_oval(cx - 45, cy - 50, cx + 45, cy + 50, 
                              fill=skin_color, outline="#1a1a1a", width=2)
        elif face_shape == "round":
            canvas.create_oval(cx - 48, cy - 48, cx + 48, cy + 48, 
                              fill=skin_color, outline="#1a1a1a", width=2)
        elif face_shape == "square":
            canvas.create_polygon(
                cx - 45, cy - 45,
                cx + 45, cy - 45,
                cx + 48, cy + 45,
                cx - 48, cy + 45,
                fill=skin_color, outline="#1a1a1a", width=2
            )
        elif face_shape == "heart":
            canvas.create_polygon(
                cx, cy - 55,
                cx + 50, cy - 20,
                cx + 45, cy + 45,
                cx - 45, cy + 45,
                cx - 50, cy - 20,
                fill=skin_color, outline="#1a1a1a", width=2
            )

        # Уши (для эльфов и полуэльфов)
        if race in ["Эльф", "Полуэльф"]:
            canvas.create_polygon(cx - 50, cy - 10, cx - 65, cy - 25, cx - 50, cy - 30, 
                                 fill=skin_color, outline="#1a1a1a", width=1)
            canvas.create_polygon(cx + 50, cy - 10, cx + 65, cy - 25, cx + 50, cy - 30, 
                                 fill=skin_color, outline="#1a1a1a", width=1)

        # Глаза
        eye_y = cy - 10
        canvas.create_oval(cx - 25, eye_y - 8, cx - 10, eye_y + 8, fill="white", outline="#1a1a1a")
        canvas.create_oval(cx + 10, eye_y - 8, cx + 25, eye_y + 8, fill="white", outline="#1a1a1a")
        canvas.create_oval(cx - 20, eye_y - 4, cx - 13, eye_y + 4, fill=eye_color, outline="")
        canvas.create_oval(cx + 15, eye_y - 4, cx + 22, eye_y + 4, fill=eye_color, outline="")
        canvas.create_oval(cx - 17, eye_y - 1, cx - 15, eye_y + 1, fill="black", outline="")
        canvas.create_oval(cx + 18, eye_y - 1, cx + 20, eye_y + 1, fill="black", outline="")

        # Брови
        brow_y = cy - 22
        if gender == "Мужской":
            canvas.create_line(cx - 28, brow_y, cx - 8, brow_y - 3, fill=hair_color, width=3)
            canvas.create_line(cx + 8, brow_y - 3, cx + 28, brow_y, fill=hair_color, width=3)
        else:
            canvas.create_line(cx - 28, brow_y, cx - 8, brow_y, fill=hair_color, width=2)
            canvas.create_line(cx + 8, brow_y, cx + 28, brow_y, fill=hair_color, width=2)

        # Нос
        canvas.create_polygon(
            cx - 5, cy + 5,
            cx + 5, cy + 5,
            cx + 2, cy + 25,
            cx - 2, cy + 25,
            fill=skin_color, outline="#1a1a1a", width=1
        )

        # Рот
        mouth_y = cy + 30
        if facial_feature in ["beard", "goatee"]:
            canvas.create_arc(cx - 20, mouth_y - 5, cx + 20, mouth_y + 15, 
                            start=0, extent=180, fill="#2C2C2C", outline="#1a1a1a")
        else:
            canvas.create_arc(cx - 15, mouth_y - 5, cx + 15, mouth_y + 10, 
                            start=0, extent=180, fill="#CC6666", outline="#1a1a1a")

        # Волосы
        if hair_style != "bald":
            if hair_style == "short":
                canvas.create_arc(cx - 50, cy - 60, cx + 50, cy + 10, 
                                start=0, extent=180, fill=hair_color, outline="#1a1a1a")
            elif hair_style == "long":
                canvas.create_arc(cx - 52, cy - 60, cx + 52, cy + 10, 
                                start=0, extent=180, fill=hair_color, outline="#1a1a1a")
                canvas.create_rectangle(cx - 52, cy - 10, cx - 35, cy + 60, 
                                       fill=hair_color, outline="#1a1a1a")
                canvas.create_rectangle(cx + 35, cy - 10, cx + 52, cy + 60, 
                                       fill=hair_color, outline="#1a1a1a")
            elif hair_style == "ponytail":
                canvas.create_arc(cx - 50, cy - 60, cx + 50, cy + 10, 
                                start=0, extent=180, fill=hair_color, outline="#1a1a1a")
                canvas.create_polygon(
                    cx - 10, cy - 20,
                    cx + 10, cy - 20,
                    cx + 5, cy + 80,
                    cx - 5, cy + 80,
                    fill=hair_color, outline="#1a1a1a"
                )
            elif hair_style == "mohawk":
                canvas.create_polygon(
                    cx - 8, cy - 65,
                    cx + 8, cy - 65,
                    cx + 5, cy + 20,
                    cx - 5, cy + 20,
                    fill=hair_color, outline="#1a1a1a"
                )
            elif hair_style == "curly":
                for i in range(-40, 41, 15):
                    canvas.create_oval(cx + i - 10, cy - 55, cx + i + 10, cy - 35, 
                                      fill=hair_color, outline="#1a1a1a")

        # Лицевые особенности
        if facial_feature == "beard":
            canvas.create_polygon(
                cx - 45, cy + 15,
                cx + 45, cy + 15,
                cx + 40, cy + 50,
                cx, cy + 55,
                cx - 40, cy + 50,
                fill=hair_color, outline="#1a1a1a"
            )
        elif facial_feature == "mustache":
            canvas.create_arc(cx - 20, cy + 15, cx + 20, cy + 30, 
                            start=0, extent=180, fill=hair_color, outline="#1a1a1a")
        elif facial_feature == "goatee":
            canvas.create_polygon(
                cx - 10, cy + 25,
                cx + 10, cy + 25,
                cx + 5, cy + 50,
                cx - 5, cy + 50,
                fill=hair_color, outline="#1a1a1a"
            )
        elif facial_feature == "scar":
            canvas.create_line(cx + 15, cy - 30, cx + 35, cy - 10, fill="#8B0000", width=2)
            canvas.create_line(cx + 18, cy - 28, cx + 32, cy - 12, fill="#CC6666", width=1)
        elif facial_feature == "glasses":
            canvas.create_oval(cx - 28, eye_y - 12, cx - 8, eye_y + 12, 
                              fill="", outline="#333", width=2)
            canvas.create_oval(cx + 8, eye_y - 12, cx + 28, eye_y + 12, 
                              fill="", outline="#333", width=2)
            canvas.create_line(cx - 8, eye_y, cx + 8, eye_y, fill="#333", width=2)

        # Рамка
        canvas.create_rectangle(0, 0, self.width, self.height, outline="#D4AF37", width=3)

        if seed:
            random.seed(None)


# ==================== CHARACTER MODEL ====================
class Character:
    def __init__(self):
        self.name = ""
        self.race = ""
        self.char_class = ""
        self.level = 1
        self.alignment = ""
        self.background = ""
        self.gender = "Мужской"
        self.age = 20
        self.height = ""
        self.weight = ""
        self.description = ""

        self.stats = {
            "Сила": 10, "Ловкость": 10, "Телосложение": 10,
            "Интеллект": 10, "Мудрость": 10, "Харизма": 10
        }

        self.hp = 0
        self.ac = 10
        self.proficiency_bonus = 2
        self.portrait_seed = None

    def calculate_stats(self):
        """Рассчитывает итоговые характеристики с учетом расы и класса"""
        if self.race in RACES:
            race_data = RACES[self.race]
            base = race_data["base_stats"].copy()
            bonuses = race_data["bonuses"]

            for stat, value in base.items():
                self.stats[stat] = value + bonuses.get(stat, 0)

        # Расчет HP
        if self.char_class in CLASSES:
            con_mod = (self.stats["Телосложение"] - 10) // 2
            hit_die = CLASSES[self.char_class]["hit_die"]
            self.hp = hit_die + con_mod

        # Расчет AC (без доспехов)
        dex_mod = (self.stats["Ловкость"] - 10) // 2
        self.ac = 10 + dex_mod

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "class": self.char_class,
            "level": self.level,
            "alignment": self.alignment,
            "background": self.background,
            "gender": self.gender,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "description": self.description,
            "stats": self.stats,
            "hp": self.hp,
            "ac": self.ac,
            "proficiency_bonus": self.proficiency_bonus,
            "portrait_seed": self.portrait_seed,
            "created_at": datetime.now().isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        char = cls()
        char.name = data.get("name", "")
        char.race = data.get("race", "")
        char.char_class = data.get("class", "")
        char.level = data.get("level", 1)
        char.alignment = data.get("alignment", "")
        char.background = data.get("background", "")
        char.gender = data.get("gender", "Мужской")
        char.age = data.get("age", 20)
        char.height = data.get("height", "")
        char.weight = data.get("weight", "")
        char.description = data.get("description", "")
        char.stats = data.get("stats", char.stats)
        char.hp = data.get("hp", 0)
        char.ac = data.get("ac", 10)
        char.proficiency_bonus = data.get("proficiency_bonus", 2)
        char.portrait_seed = data.get("portrait_seed")
        return char


# ==================== MAIN APPLICATION ====================
class DnDCharacterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DnD Character Creator")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")

        self.character = Character()
        self.portrait_gen = PortraitGenerator()
        self.current_frame = None

        self.setup_styles()
        self.show_main_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#1a1a2e")
        style.configure("TLabel", background="#1a1a2e", foreground="#e0e0e0", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#D4AF37")
        style.configure("Subheader.TLabel", font=("Segoe UI", 14, "bold"), foreground="#C0C0C0")
        style.configure("Stat.TLabel", font=("Segoe UI", 12, "bold"), foreground="#D4AF37")

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = frame

        title = ttk.Label(frame, text="⚔️ DnD Character Creator ⚔️", style="Header.TLabel")
        title.pack(pady=(0, 30))

        subtitle = ttk.Label(frame, text="Создайте своего героя для приключений", 
                            font=("Segoe UI", 12), foreground="#888")
        subtitle.pack(pady=(0, 40))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()

        create_btn = tk.Button(btn_frame, text="🛡️ Создать персонажа", 
                              font=("Segoe UI", 14, "bold"),
                              bg="#4a6741", fg="white", activebackground="#5a7751",
                              padx=30, pady=15, cursor="hand2",
                              command=self.show_creation_menu)
        create_btn.pack(pady=10, fill="x")

        load_btn = tk.Button(btn_frame, text="📂 Загрузить персонажа", 
                            font=("Segoe UI", 14, "bold"),
                            bg="#4B0082", fg="white", activebackground="#5B1092",
                            padx=30, pady=15, cursor="hand2",
                            command=self.show_load_menu)
        load_btn.pack(pady=10, fill="x")

        exit_btn = tk.Button(btn_frame, text="🚪 Выйти", 
                            font=("Segoe UI", 12),
                            bg="#8B0000", fg="white", activebackground="#9B1010",
                            padx=30, pady=10, cursor="hand2",
                            command=self.root.quit)
        exit_btn.pack(pady=(20, 0), fill="x")

    def show_creation_menu(self):
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        # Header
        header = ttk.Label(frame, text="Создание персонажа", style="Header.TLabel")
        header.pack(pady=(0, 20))

        # Main content area
        content = ttk.Frame(frame)
        content.pack(fill="both", expand=True)

        # Left panel - Form
        left_panel = ttk.Frame(content, padding=10)
        left_panel.pack(side="left", fill="both", expand=True)

        # Name
        name_frame = ttk.Frame(left_panel)
        name_frame.pack(fill="x", pady=5)
        ttk.Label(name_frame, text="Имя персонажа:").pack(side="left")
        self.name_entry = ttk.Entry(name_frame, font=("Segoe UI", 11), width=30)
        self.name_entry.pack(side="left", padx=(10, 0))

        # Race selection
        race_frame = ttk.Frame(left_panel)
        race_frame.pack(fill="x", pady=10)
        ttk.Label(race_frame, text="Раса:").pack(side="left")
        self.race_var = tk.StringVar(value=list(RACES.keys())[0])
        race_combo = ttk.Combobox(race_frame, textvariable=self.race_var, 
                                  values=list(RACES.keys()), state="readonly", width=20)
        race_combo.pack(side="left", padx=(10, 0))
        race_combo.bind("<<ComboboxSelected>>", self.on_race_change)

        self.race_desc = ttk.Label(left_panel, text=RACES[list(RACES.keys())[0]]["description"], 
                                   foreground="#888", wraplength=400)
        self.race_desc.pack(anchor="w", pady=(0, 10))

        # Class selection
        class_frame = ttk.Frame(left_panel)
        class_frame.pack(fill="x", pady=10)
        ttk.Label(class_frame, text="Класс:").pack(side="left")
        self.class_var = tk.StringVar(value=list(CLASSES.keys())[0])
        class_combo = ttk.Combobox(class_frame, textvariable=self.class_var, 
                                   values=list(CLASSES.keys()), state="readonly", width=20)
        class_combo.pack(side="left", padx=(10, 0))
        class_combo.bind("<<ComboboxSelected>>", self.on_class_change)

        self.class_desc = ttk.Label(left_panel, text=CLASSES[list(CLASSES.keys())[0]]["description"], 
                                    foreground="#888", wraplength=400)
        self.class_desc.pack(anchor="w", pady=(0, 10))

        # Alignment
        align_frame = ttk.Frame(left_panel)
        align_frame.pack(fill="x", pady=5)
        ttk.Label(align_frame, text="Мировоззрение:").pack(side="left")
        self.align_var = tk.StringVar(value=ALIGNMENTS[4])
        align_combo = ttk.Combobox(align_frame, textvariable=self.align_var, 
                                   values=ALIGNMENTS, state="readonly", width=25)
        align_combo.pack(side="left", padx=(10, 0))

        # Background
        bg_frame = ttk.Frame(left_panel)
        bg_frame.pack(fill="x", pady=5)
        ttk.Label(bg_frame, text="Предыстория:").pack(side="left")
        self.bg_var = tk.StringVar(value=BACKGROUNDS[0])
        bg_combo = ttk.Combobox(bg_frame, textvariable=self.bg_var, 
                                values=BACKGROUNDS, state="readonly", width=20)
        bg_combo.pack(side="left", padx=(10, 0))

        # Gender
        gender_frame = ttk.Frame(left_panel)
        gender_frame.pack(fill="x", pady=5)
        ttk.Label(gender_frame, text="Пол:").pack(side="left")
        self.gender_var = tk.StringVar(value="Мужской")
        ttk.Radiobutton(gender_frame, text="Мужской", variable=self.gender_var, 
                       value="Мужской").pack(side="left", padx=(10, 0))
        ttk.Radiobutton(gender_frame, text="Женский", variable=self.gender_var, 
                       value="Женский").pack(side="left", padx=(10, 0))

        # Age
        age_frame = ttk.Frame(left_panel)
        age_frame.pack(fill="x", pady=5)
        ttk.Label(age_frame, text="Возраст:").pack(side="left")
        self.age_var = tk.IntVar(value=25)
        ttk.Spinbox(age_frame, from_=16, to=500, textvariable=self.age_var, width=10).pack(side="left", padx=(10, 0))

        # Description
        desc_frame = ttk.Frame(left_panel)
        desc_frame.pack(fill="x", pady=10)
        ttk.Label(desc_frame, text="Описание:").pack(anchor="w")
        self.desc_text = tk.Text(desc_frame, height=4, width=50, font=("Segoe UI", 10),
                                bg="#16213e", fg="#e0e0e0", insertbackground="white")
        self.desc_text.pack(pady=(5, 0))

        # Right panel - Portrait and Preview
        right_panel = ttk.Frame(content, padding=10)
        right_panel.pack(side="right", fill="y")

        ttk.Label(right_panel, text="Портрет", style="Subheader.TLabel").pack()

        self.portrait_canvas = tk.Canvas(right_panel, width=200, height=250, bg="#2C2C2C", 
                                        highlightthickness=0)
        self.portrait_canvas.pack(pady=10)

        regen_btn = tk.Button(right_panel, text="🎲 Перегенерировать", 
                             font=("Segoe UI", 10),
                             bg="#555", fg="white", activebackground="#666",
                             padx=15, pady=5, cursor="hand2",
                             command=self.regenerate_portrait)
        regen_btn.pack(pady=5)

        # Stats preview
        ttk.Label(right_panel, text="Характеристики", style="Subheader.TLabel").pack(pady=(20, 10))
        self.stats_frame = ttk.Frame(right_panel)
        self.stats_frame.pack()
        self.update_stats_preview()

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)

        back_btn = tk.Button(btn_frame, text="◀ Назад", 
                            font=("Segoe UI", 11),
                            bg="#555", fg="white", activebackground="#666",
                            padx=20, pady=8, cursor="hand2",
                            command=self.show_main_menu)
        back_btn.pack(side="left", padx=5)

        create_btn = tk.Button(btn_frame, text="✨ Создать персонажа", 
                              font=("Segoe UI", 12, "bold"),
                              bg="#D4AF37", fg="#1a1a2e", activebackground="#E4BF47",
                              padx=25, pady=10, cursor="hand2",
                              command=self.create_character)
        create_btn.pack(side="left", padx=5)

        # Initial portrait
        self.regenerate_portrait()

    def on_race_change(self, event=None):
        race = self.race_var.get()
        if race in RACES:
            self.race_desc.config(text=RACES[race]["description"])
        self.update_stats_preview()
        self.regenerate_portrait()

    def on_class_change(self, event=None):
        char_class = self.class_var.get()
        if char_class in CLASSES:
            self.class_desc.config(text=CLASSES[char_class]["description"])
        self.update_stats_preview()

    def update_stats_preview(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        race = self.race_var.get()
        char_class = self.class_var.get()

        temp_char = Character()
        temp_char.race = race
        temp_char.char_class = char_class
        temp_char.calculate_stats()

        for i, (stat, value) in enumerate(temp_char.stats.items()):
            mod = (value - 10) // 2
            mod_str = f"+{mod}" if mod >= 0 else str(mod)

            stat_frame = ttk.Frame(self.stats_frame)
            stat_frame.grid(row=i // 2, column=i % 2, padx=10, pady=3, sticky="w")

            ttk.Label(stat_frame, text=f"{stat}:", style="Stat.TLabel", width=12).pack(side="left")
            ttk.Label(stat_frame, text=f"{value} ({mod_str})", font=("Segoe UI", 11, "bold")).pack(side="left")

        # HP and AC
        info_frame = ttk.Frame(self.stats_frame)
        info_frame.grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Label(info_frame, text=f"HP: {temp_char.hp}", style="Stat.TLabel").pack(side="left", padx=10)
        ttk.Label(info_frame, text=f"AC: {temp_char.ac}", style="Stat.TLabel").pack(side="left", padx=10)

    def regenerate_portrait(self):
        self.character.portrait_seed = random.randint(1, 100000)
        self.portrait_gen.generate_portrait(
            self.portrait_canvas, 
            self.race_var.get(), 
            self.class_var.get(),
            self.gender_var.get(),
            self.character.portrait_seed
        )

    def create_character(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Пожалуйста, введите имя персонажа!")
            return

        self.character.name = name
        self.character.race = self.race_var.get()
        self.character.char_class = self.class_var.get()
        self.character.alignment = self.align_var.get()
        self.character.background = self.bg_var.get()
        self.character.gender = self.gender_var.get()
        self.character.age = self.age_var.get()
        self.character.description = self.desc_text.get("1.0", "end-1c")

        self.character.calculate_stats()

        self.show_character_sheet()

    def show_character_sheet(self):
        self.clear_frame()

        char = self.character

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        # Header
        header = ttk.Label(frame, text=f"📜 {char.name}", style="Header.TLabel")
        header.pack()

        subheader = ttk.Label(frame, text=f"{char.race} | {char.char_class} | Уровень {char.level}", 
                             font=("Segoe UI", 13), foreground="#C0C0C0")
        subheader.pack(pady=(0, 20))

        # Main content
        content = ttk.Frame(frame)
        content.pack(fill="both", expand=True)

        # Left - Portrait and basic info
        left = ttk.Frame(content, padding=10)
        left.pack(side="left", fill="y")

        portrait_canvas = tk.Canvas(left, width=200, height=250, bg="#2C2C2C", highlightthickness=0)
        portrait_canvas.pack()
        self.portrait_gen.generate_portrait(portrait_canvas, char.race, char.char_class, 
                                           char.gender, char.portrait_seed)

        info_frame = ttk.Frame(left, padding=10)
        info_frame.pack(pady=10, fill="x")

        info_items = [
            ("Мировоззрение", char.alignment),
            ("Предыстория", char.background),
            ("Пол", char.gender),
            ("Возраст", f"{char.age} лет"),
        ]

        for label, value in info_items:
            row = ttk.Frame(info_frame)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=f"{label}:", style="Stat.TLabel", width=15).pack(side="left")
            ttk.Label(row, text=value).pack(side="left")

        # Center - Stats
        center = ttk.Frame(content, padding=20)
        center.pack(side="left", fill="both", expand=True)

        ttk.Label(center, text="Характеристики", style="Subheader.TLabel").pack()

        stats_box = ttk.Frame(center, padding=10)
        stats_box.pack(pady=10, fill="x")

        for stat, value in char.stats.items():
            mod = (value - 10) // 2
            mod_str = f"+{mod}" if mod >= 0 else str(mod)

            row = ttk.Frame(stats_box)
            row.pack(fill="x", pady=3)

            # Stat box
            box = tk.Frame(row, bg="#16213e", padx=15, pady=8)
            box.pack(fill="x")

            tk.Label(box, text=stat, bg="#16213e", fg="#D4AF37", 
                    font=("Segoe UI", 11, "bold"), width=12).pack(side="left")
            tk.Label(box, text=str(value), bg="#16213e", fg="white", 
                    font=("Segoe UI", 14, "bold")).pack(side="left", padx=(20, 5))
            tk.Label(box, text=f"({mod_str})", bg="#16213e", fg="#888", 
                    font=("Segoe UI", 11)).pack(side="left")

        # Combat stats
        combat_frame = ttk.Frame(center, padding=10)
        combat_frame.pack(pady=10, fill="x")

        ttk.Label(combat_frame, text="Боевые характеристики", style="Subheader.TLabel").pack()

        combat_box = ttk.Frame(combat_frame)
        combat_box.pack(pady=5)

        for label, value in [("HP (Здоровье)", char.hp), ("AC (Класс брони)", char.ac), 
                             ("Бонус мастерства", f"+{char.proficiency_bonus}")]:
            cell = tk.Frame(combat_box, bg="#8B0000", padx=20, pady=10)
            cell.pack(side="left", padx=5)
            tk.Label(cell, text=label, bg="#8B0000", fg="#ccc", font=("Segoe UI", 9)).pack()
            tk.Label(cell, text=str(value), bg="#8B0000", fg="white", 
                    font=("Segoe UI", 16, "bold")).pack()

        # Class info
        if char.char_class in CLASSES:
            cls = CLASSES[char.char_class]
            class_frame = ttk.Frame(center, padding=10)
            class_frame.pack(fill="x", pady=10)

            ttk.Label(class_frame, text="Особенности класса", style="Subheader.TLabel").pack()

            ttk.Label(class_frame, text=f"Кость хитов: d{cls['hit_die']}", foreground="#888").pack(anchor="w")
            ttk.Label(class_frame, text=f"Ключевая характеристика: {cls['primary_stat']}", foreground="#888").pack(anchor="w")
            ttk.Label(class_frame, text=f"Спасброски: {', '.join(cls['saves'])}", foreground="#888").pack(anchor="w")
            ttk.Label(class_frame, text=f"Навыки: {', '.join(cls['skills'])}", foreground="#888", wraplength=350).pack(anchor="w")

        # Description
        if char.description:
            desc_frame = ttk.Frame(center, padding=10)
            desc_frame.pack(fill="x", pady=10)
            ttk.Label(desc_frame, text="Описание", style="Subheader.TLabel").pack(anchor="w")
            ttk.Label(desc_frame, text=char.description, foreground="#888", 
                     wraplength=400, justify="left").pack(anchor="w")

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)

        back_btn = tk.Button(btn_frame, text="◀ Назад", 
                            font=("Segoe UI", 11),
                            bg="#555", fg="white", activebackground="#666",
                            padx=20, pady=8, cursor="hand2",
                            command=self.show_creation_menu)
        back_btn.pack(side="left", padx=5)

        save_btn = tk.Button(btn_frame, text="💾 Сохранить в JSON", 
                            font=("Segoe UI", 12, "bold"),
                            bg="#4B0082", fg="white", activebackground="#5B1092",
                            padx=25, pady=10, cursor="hand2",
                            command=self.save_character)
        save_btn.pack(side="left", padx=5)

        menu_btn = tk.Button(btn_frame, text="🏠 Главное меню", 
                            font=("Segoe UI", 11),
                            bg="#4a6741", fg="white", activebackground="#5a7751",
                            padx=20, pady=8, cursor="hand2",
                            command=self.show_main_menu)
        menu_btn.pack(side="left", padx=5)

    def save_character(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"{self.character.name.replace(' ', '_')}.json"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.character.to_dict(), f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Успех", f"Персонаж сохранен в: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить:{str(e)}")

    def show_load_menu(self):
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = frame

        ttk.Label(frame, text="📂 Загрузка персонажа", style="Header.TLabel").pack(pady=(0, 20))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)

        load_btn = tk.Button(btn_frame, text="Выбрать JSON файл", 
                            font=("Segoe UI", 12, "bold"),
                            bg="#4B0082", fg="white", activebackground="#5B1092",
                            padx=30, pady=12, cursor="hand2",
                            command=self.load_character_file)
        load_btn.pack(pady=10, fill="x")

        back_btn = tk.Button(btn_frame, text="◀ Назад", 
                            font=("Segoe UI", 11),
                            bg="#555", fg="white", activebackground="#666",
                            padx=30, pady=10, cursor="hand2",
                            command=self.show_main_menu)
        back_btn.pack(pady=10, fill="x")

    def load_character_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.character = Character.from_dict(data)
                messagebox.showinfo("Успех", f"Персонаж '{self.character.name}' загружен!")
                self.show_character_sheet()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")


# ==================== MAIN ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = DnDCharacterApp(root)
    root.mainloop()