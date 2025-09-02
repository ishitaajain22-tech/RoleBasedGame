import pygame
import sys
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG Game Collection")

# Colors
# Colors - Make sure these are all defined as RGB tuples
BACKGROUND = (20, 12, 28)
TEXT_COLOR = (222, 207, 184)
HIGHLIGHT = (255, 215, 0)
BUTTON_COLOR = (60, 40, 70)
BUTTON_HOVER = (90, 60, 100)
AETHERIAN_COLOR = (180, 50, 50)
MAGE_COLOR = (50, 100, 180)
ROGUE_COLOR = (50, 150, 50)
CHRONOS_COLOR = (50, 100, 180)
VOID_COLOR = (80, 30, 100)

# Fonts
title_font = pygame.font.Font(None, 72)
heading_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Game state
class GameState:
    def __init__(self):
        self.current_screen = "main_menu"
        self.player_role = None
        self.scenarios_completed = 0
        self.choices = {"Honor": 0, "Pragmatism": 0, "Curiosity": 0}
        self.role_profiles = {
            "Warrior": {"Honor": 3, "Pragmatism": 2, "Curiosity": 1},
            "Mage": {"Honor": 2, "Pragmatism": 1, "Curiosity": 3},
            "Rogue": {"Honor": 1, "Pragmatism": 3, "Curiosity": 2}
        }
        self.scenario_values = {
            1: {"A": {"Honor": 2, "Pragmatism": 0, "Curiosity": 0},
                "B": {"Honor": 0, "Pragmatism": 2, "Curiosity": 0},
                "C": {"Honor": 0, "Pragmatism": 0, "Curiosity": 2}},
            2: {"A": {"Honor": 2, "Pragmatism": 0, "Curiosity": 1},
                "B": {"Honor": 0, "Pragmatism": 2, "Curiosity": 0},
                "C": {"Honor": 1, "Pragmatism": 1, "Curiosity": 2}},
            3: {"A": {"Honor": 2, "Pragmatism": 1, "Curiosity": 0},
                "B": {"Honor": 0, "Pragmatism": 2, "Curiosity": 1},
                "C": {"Honor": 1, "Pragmatism": 0, "Curiosity": 2}},
            4: {"A": {"Honor": 3, "Pragmatism": 0, "Curiosity": 0},
                "B": {"Honor": 0, "Pragmatism": 3, "Curiosity": 0},
                "C": {"Honor": 0, "Pragmatism": 0, "Curiosity": 3}}
        }
        self.text_queue = []
        self.current_text = ""
        self.text_progress = 0
        self.text_speed = 2
        self.typing = False
        self.particles = []
        self.fade_alpha = 0
        self.fade_direction = 1
        
        # Chronos Legacy state
        self.time_era = "present"
        self.timeline_integrity = 100
        self.chronos_choices = {"Preservation": 0, "Intervention": 0, "Knowledge": 0}
        self.chronos_scenario = 1
        
        # Echoes of the Void state
        self.sanity = 100
        self.void_scenario = 1
        void_colors = [(30, 10, 40), (40, 15, 50), (50, 20, 60)]
        self.void_particles = []
        for _ in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 4)
            speed = random.uniform(0.5, 2.0)
            color = random.choice(void_colors)
            self.void_particles.append([x, y, size, speed, color])
        
        # Generate particles for background
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            speed = random.uniform(0.2, 1.0)
            self.particles.append([x, y, size, speed])

    def start_typing(self, text):
        self.text_queue = text.split(" ")
        self.current_text = ""
        self.text_progress = 0
        self.typing = True

    def update_typing(self):
        if self.typing and self.text_queue:
            if self.text_progress >= len(self.text_queue[0]):
                self.current_text += self.text_queue.pop(0) + " "
                self.text_progress = 0
            else:
                self.text_progress += self.text_speed
        elif not self.text_queue:
            self.typing = False

    def get_visible_text(self):
        if not self.text_queue:
            return self.current_text
        return self.current_text + self.text_queue[0][:int(self.text_progress)]
    
    def calculate_alignment(self):
        role_profile = self.role_profiles[self.player_role]
        alignment_score = 0
        
        for trait, value in self.choices.items():
            difference = abs(value - role_profile.get(trait, 0))
            alignment_score += (3 - difference)
        
        max_possible = 12
        return (alignment_score / max_possible) * 100

# Create game state
game_state = GameState()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        # Ensure colors are tuples
        self.color = tuple(color) if hasattr(color, '__iter__') else BUTTON_COLOR
        self.hover_color = tuple(hover_color) if hasattr(hover_color, '__iter__') else BUTTON_HOVER
        
    def draw(self, surface):
        color = tuple(self.hover_color) if self.hovered else tuple(self.color)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, tuple(HIGHLIGHT), self.rect, 3)
        
        text_surf = text_font.render(self.text, True, tuple(TEXT_COLOR))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.action:
                self.action()
            return True
        return False

# Game selection functions
def select_aetherian():
    game_state.current_screen = "aetherian_intro"

def select_chronos():
    game_state.current_screen = "chronos_intro"

def select_void():
    game_state.current_screen = "void_intro"

def return_to_menu():
    game_state.current_screen = "main_menu"
    # Reset game states
    game_state.player_role = None
    game_state.scenarios_completed = 0
    game_state.choices = {"Honor": 0, "Pragmatism": 0, "Curiosity": 0}
    game_state.time_era = "present"
    game_state.timeline_integrity = 100
    game_state.chronos_choices = {"Preservation": 0, "Intervention": 0, "Knowledge": 0}
    game_state.chronos_scenario = 1
    game_state.sanity = 100
    game_state.void_scenario = 1

# Aetherian Gauntlet functions
def select_warrior():
    game_state.player_role = "Warrior"
    game_state.current_screen = "aetherian_scenario_1"

def select_mage():
    game_state.player_role = "Mage"
    game_state.current_screen = "aetherian_scenario_1"

def select_rogue():
    game_state.player_role = "Rogue"
    game_state.current_screen = "aetherian_scenario_1"

def make_choice(choice):
    scenario_num = game_state.scenarios_completed + 1
    values = game_state.scenario_values[scenario_num][choice]
    for trait, value in values.items():
        game_state.choices[trait] += value
    
    game_state.scenarios_completed += 1
    
    if game_state.scenarios_completed < 4:
        game_state.current_screen = f"aetherian_scenario_{game_state.scenarios_completed + 1}"
    else:
        game_state.current_screen = "aetherian_judgment"

# Chronos Legacy functions
def chronos_make_choice(choice):
    if choice == "preserve":
        game_state.chronos_choices["Preservation"] += 1
        game_state.timeline_integrity = min(100, game_state.timeline_integrity + 5)
    elif choice == "intervene":
        game_state.chronos_choices["Intervention"] += 1
        game_state.timeline_integrity = max(0, game_state.timeline_integrity - 10)
    elif choice == "knowledge":
        game_state.chronos_choices["Knowledge"] += 1
    
    game_state.chronos_scenario += 1
    
    if game_state.chronos_scenario <= 3:
        if game_state.time_era == "present":
            game_state.time_era = "past"
        elif game_state.time_era == "past":
            game_state.time_era = "future"
        game_state.current_screen = "chronos_scenario_1"
    else:
        game_state.current_screen = "chronos_ending"

# Echoes of the Void functions
def void_make_choice(choice):
    if choice == "destroy":
        game_state.sanity = min(100, game_state.sanity + 10)
    elif choice == "use":
        game_state.sanity = max(0, game_state.sanity - 20)
    elif choice == "study":
        game_state.sanity = max(0, game_state.sanity - 5)
    
    game_state.void_scenario += 1
    
    if game_state.void_scenario <= 4:
        game_state.current_screen = f"void_scenario_{game_state.void_scenario}"
    else:
        if game_state.sanity <= 30:
            game_state.current_screen = "void_ending_madness"
        elif game_state.sanity >= 80:
            game_state.current_screen = "void_ending_safe"
        else:
            game_state.current_screen = "void_ending_mixed"

# Draw functions for each screen
def draw_main_menu():
    # Draw background
    screen.fill(BACKGROUND)
    
    # Draw particles
    for particle in game_state.particles:
        x, y, size, speed = particle
        pygame.draw.circle(screen, (100, 80, 120), (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw title
    title_text = title_font.render("RPG GAME COLLECTION", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 80))
    
    subtitle_text = heading_font.render("Choose Your Adventure", True, TEXT_COLOR)
    screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 150))
    
    # Draw game selection buttons
    button_width, button_height = 600, 120
    button_y_start = 250
    button_spacing = 150
    
    aetherian_btn = Button(
        SCREEN_WIDTH//2 - button_width//2, 
        button_y_start, 
        button_width, 
        button_height, 
        "Aetherian Gauntlet: Role-Based Adventure", 
        AETHERIAN_COLOR,
        (210, 70, 70),
        select_aetherian
    )
    
    chronos_btn = Button(
        SCREEN_WIDTH//2 - button_width//2, 
        button_y_start + button_spacing, 
        button_width, 
        button_height, 
        "Chronos Legacy: Time Manipulation Adventure", 
        CHRONOS_COLOR,
        (70, 130, 210),
        select_chronos
    )
    
    void_btn = Button(
        SCREEN_WIDTH//2 - button_width//2, 
        button_y_start + button_spacing * 2, 
        button_width, 
        button_height, 
        "Echoes of the Void: Cosmic Horror Mystery", 
        VOID_COLOR,
        (110, 50, 130),
        select_void
    )
    
    # Draw game descriptions
    descriptions = [
        "A choice-driven RPG where your decisions determine your alignment with your chosen role",
        "Manipulate time across different eras in this narrative adventure with branching timelines",
        "Investigate cosmic horrors in this psychological thriller with sanity mechanics"
    ]
    
    for i, desc in enumerate(descriptions):
        text = small_font.render(desc, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 
                          button_y_start + button_height + 10 + i * button_spacing))
    
    mouse_pos = pygame.mouse.get_pos()
    buttons = [aetherian_btn, chronos_btn, void_btn]
    
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    # Draw footer
    footer_text = small_font.render("Select a game to begin your adventure...", True, TEXT_COLOR)
    screen.blit(footer_text, (SCREEN_WIDTH//2 - footer_text.get_width()//2, SCREEN_HEIGHT - 50))
    
    return buttons

def draw_aetherian_intro():
    screen.fill(BACKGROUND)
    
    # Draw particles
    for particle in game_state.particles:
        x, y, size, speed = particle
        pygame.draw.circle(screen, (100, 80, 120), (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw title
    title_text = title_font.render("AETHERIAN GAUNTLET", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    subtitle_text = heading_font.render("A Role-Based Adventure", True, TEXT_COLOR)
    screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 180))
    
    # Draw introduction text
    intro_lines = [
        "You wake in a cold, stone cell. The roar of a",
        "distant crowd shakes dust from the ceiling.",
        "",
        "A grizzled guard slides a meal through the bars.",
        "'Eat up, rookie,' he grunts. 'The Proving Grounds",
        "await. What's your specialty? Don't lie to yourself.",
        "It's the only thing that'll keep you alive out there.'"
    ]
    
    for i, line in enumerate(intro_lines):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*40))
    
    # Draw role selection buttons with auto-sizing
    warrior_text = "Choose Warrior - Path of Strength"
    mage_text = "Choose Mage - Path of Knowledge"
    rogue_text = "Choose Rogue - Path of Cunning"
    
    warrior_width = text_font.size(warrior_text)[0] + 40
    mage_width = text_font.size(mage_text)[0] + 40
    rogue_width = text_font.size(rogue_text)[0] + 40
    
    warrior_btn = Button(SCREEN_WIDTH//2 - warrior_width//2, 550, warrior_width, 50, warrior_text, 
                    tuple(AETHERIAN_COLOR), (210, 70, 70), select_warrior)
    mage_btn = Button(SCREEN_WIDTH//2 - mage_width//2, 620, mage_width, 50, mage_text, 
                 tuple(MAGE_COLOR), (70, 130, 210), select_mage)
    rogue_btn = Button(SCREEN_WIDTH//2 - rogue_width//2, 700, rogue_width, 50, rogue_text, 
                  tuple(ROGUE_COLOR), (70, 180, 70), select_rogue)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    buttons = [warrior_btn, mage_btn, rogue_btn, back_btn]
    
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_aetherian_scenario_1():
    screen.fill(BACKGROUND)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 1: The Wounded Beast", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario text
    scenario_text = [
        "Your first fight is against a chained Wolf-Hyena.",
        "You defeat it, but it's wounded, not dead.",
        "It whimpers, cowering before you. The crowd awaits your decision."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 140 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Finish it quickly and mercifully",
        "B. Leave it alive as a distraction for the next gladiator",
        "C. Spare it to have the arena alchemists examine it"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 300 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    for i, choice in enumerate(choices):
        btn = Button(SCREEN_WIDTH//2 - 100, 450 + i*60, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=lambda c=choice: make_choice(c))
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_aetherian_scenario_2():
    screen.fill(BACKGROUND)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 2: The Rival", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario image (placeholder)
    pygame.draw.rect(screen, (50, 40, 60), (SCREEN_WIDTH//2 - 300, 120, 600, 200))
    pygame.draw.rect(screen, (120, 100, 140), (SCREEN_WIDTH//2 - 300, 120, 600, 200), 3)
    
    # Draw scenario text
    scenario_text = [
        "A gladiator from your same role has become your rival.",
        "Before a crucial team battle, they offer you a proposal",
        "to work together."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 340 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Refuse. You will defeat them fairly in the arena",
        "B. Accept, but plan to betray them during the match",
        "C. Accept and propose a genuine combo move"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 480 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    for i, choice in enumerate(choices):
        btn = Button(SCREEN_WIDTH//2 - 100, 600 + i*60, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=lambda c=choice: make_choice(c))
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_aetherian_scenario_3():
    screen.fill(BACKGROUND)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 3: The Corrupt Guard", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario image (placeholder)
    pygame.draw.rect(screen, (50, 40, 60), (SCREEN_WIDTH//2 - 300, 120, 600, 200))
    pygame.draw.rect(screen, (120, 100, 140), (SCREEN_WIDTH//2 - 300, 120, 600, 200), 3)
    
    # Draw scenario text
    scenario_text = [
        "A guard approaches you with an offer: he can make",
        "your next fight easier in exchange for a share of",
        "your winnings. This is strictly against arena rules."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 340 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Refuse and report the guard to authorities",
        "B. Accept the offer without hesitation",
        "C. Pretend to accept, but gather evidence to blackmail him"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 480 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    for i, choice in enumerate(choices):
        btn = Button(SCREEN_WIDTH//2 - 100, 600 + i*60, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=lambda c=choice: make_choice(c))
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_aetherian_scenario_4():
    screen.fill(BACKGROUND)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 4: The Dark Secret", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario image (placeholder)
    pygame.draw.rect(screen, (50, 40, 60), (SCREEN_WIDTH//2 - 300, 120, 600, 200))
    pygame.draw.rect(screen, (120, 100, 140), (SCREEN_WIDTH//2 - 300, 120, 600, 200), 3)
    
    # Draw scenario text
    scenario_text = [
        "You overhear the Arena Master plotting to assassinate",
        "the benevolent Emperor. He plans to use the chaos of",
        "the games as a cover for his treachery."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 340 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Confront the Arena Master to protect the realm",
        "B. Use the distraction to escape the arena forever",
        "C. Blackmail the Arena Master for your freedom and power"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 480 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    for i, choice in enumerate(choices):
        btn = Button(SCREEN_WIDTH//2 - 100, 600 + i*60, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=lambda c=choice: make_choice(c))
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_aetherian_judgment():
    screen.fill(BACKGROUND)
    
    # Calculate alignment
    alignment_percent = game_state.calculate_alignment()
    
    # Draw judgment title
    title_text = heading_font.render("Final Judgment", True, HIGHLIGHT)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw spectral judge image (placeholder)
    pygame.draw.circle(screen, (70, 60, 90), (SCREEN_WIDTH//2, 200), 80)
    pygame.draw.circle(screen, (180, 170, 190), (SCREEN_WIDTH//2, 200), 80, 3)
    
    # Draw alignment meter first
    meter_width = 600
    meter_y = 320
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH//2 - meter_width//2, meter_y, meter_width, 20))
    pygame.draw.rect(screen, HIGHLIGHT, (SCREEN_WIDTH//2 - meter_width//2, meter_y, meter_width * (alignment_percent/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (SCREEN_WIDTH//2 - meter_width//2, meter_y, meter_width, 20), 2)
    
    percent_text = text_font.render(f"Alignment with {game_state.player_role} path: {alignment_percent:.1f}%", True, TEXT_COLOR)
    screen.blit(percent_text, (SCREEN_WIDTH//2 - percent_text.get_width()//2, meter_y + 30))
    
    # Draw judgment text
    if alignment_percent >= 70:
        judgment_text = [
            "The spectral Judge appears before you:",
            "",
            "'You have walked your chosen path without deviation.",
            "Your nature is pure. You are not a prisoner of the",
            "arena; you are its embodiment. You are free, and",
            "your name shall be etched among the true Adepts.'"
        ]
        
        title_map = {
            "Warrior": "The Honorable Blade",
            "Mage": "The Arcane Prodigy",
            "Rogue": "The Whispering Shadow"
        }
        title = title_map[game_state.player_role]
        
        result_text = [
            f"You are hailed as the ideal {game_state.player_role}.",
            f"Your story becomes legend. You are now known as {title}!"
        ]
    else:
        judgment_text = [
            "The spectral Judge appears before you:",
            "",
            "'Power you sought, and power you gained.",
            "But you lost yourself in the process. You wield",
            "your skills without true understanding of their",
            "nature. You are powerful... but you are an Aberration.'"
        ]
        
        title_map = {
            "Warrior": "The Oathbreaker",
            "Mage": "The Mad Scholar",
            "Rogue": "The Unpredictable"
        }
        title = title_map[game_state.player_role]
        
        result_text = [
            "You are granted freedom, but you are shunned.",
            f"You are a cautionary tale. You are now known as {title}!"
        ]
    
    # Draw judgment text
    for i, line in enumerate(judgment_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 380 + i*25))
    
    # Draw result text
    for i, line in enumerate(result_text):
        text = heading_font.render(line, True, HIGHLIGHT)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 550 + i*35))
    
    # Draw restart button
    restart_btn = Button(SCREEN_WIDTH//2 - 100, 650, 200, 50, "Play Again", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    mouse_pos = pygame.mouse.get_pos()
    restart_btn.update(mouse_pos)
    restart_btn.draw(screen)
    
    return [restart_btn]

# Chronos Legacy screens
def draw_chronos_intro():
    screen.fill(BACKGROUND)
    
    # Draw title
    title_text = title_font.render("CHRONOS LEGACY", True, CHRONOS_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    subtitle_text = heading_font.render("A Time Manipulation Adventure", True, TEXT_COLOR)
    screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 180))
    
    # Draw intro text
    intro_lines = [
        "You awaken as a Time Weaver, part of an ancient order",
        "that maintains the flow of time. The Timeless Library",
        "has been corrupted, causing temporal rifts across history.",
        "Your mentor is missing. You must journey through different",
        "eras to restore balance before reality unravels completely."
    ]
    
    for i, line in enumerate(intro_lines):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*40))
    
    # Draw start button
    start_btn = Button(SCREEN_WIDTH//2 - 100, 500, 200, 50, "Begin Journey", CHRONOS_COLOR, (70, 130, 210), 
                      lambda: setattr(game_state, 'current_screen', 'chronos_scenario_1'))
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    buttons = [start_btn, back_btn]
    
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_chronos_scenario_1():
    screen.fill(BACKGROUND)
    
    # Draw era indicator
    era_text = heading_font.render(f"Current Era: {game_state.time_era.capitalize()}", True, CHRONOS_COLOR)
    screen.blit(era_text, (SCREEN_WIDTH//2 - era_text.get_width()//2, 50))
    
    # Draw timeline integrity meter with frame
    integrity_text = text_font.render(f"Timeline Integrity: {game_state.timeline_integrity}%", True, TEXT_COLOR)
    screen.blit(integrity_text, (50, 100))
    
    meter_width = 200
    pygame.draw.rect(screen, (30, 30, 30), (50, 130, meter_width, 20))
    pygame.draw.rect(screen, CHRONOS_COLOR, (50, 130, meter_width * (game_state.timeline_integrity/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (50, 130, meter_width, 20), 2)
    
    # Draw scenario
    if game_state.time_era == "present":
        scenario_text = [
            "You discover a temporal rift in your present time.",
            "A historian is about to destroy an ancient artifact",
            "that he believes is dangerous, but you know it's",
            "essential for maintaining the timeline balance."
        ]
        
        choice_text = [
            "A. Preserve the timeline - stop the historian",
            "B. Intervene - let him destroy the artifact",
            "C. Study the artifact first before deciding"
        ]
    elif game_state.time_era == "past":
        scenario_text = [
            "You travel to ancient Egypt. A priest is about to",
            "erase knowledge of mathematics from the records,",
            "fearing it gives too much power to common people."
        ]
        
        choice_text = [
            "A. Preserve knowledge - stop the priest",
            "B. Intervene - let him erase the knowledge",
            "C. Study the mathematical texts first"
        ]
    else:  # future
        scenario_text = [
            "You arrive in a dystopian future where time has",
            "broken down. The last survivors want to use a",
            "dangerous time device to reset everything."
        ]
        
        choice_text = [
            "A. Preserve the timeline - stop them from using the device",
            "B. Intervene - let them reset time",
            "C. Study the time device first"
        ]
    
    # Draw scenario text
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*40))
    
    # Draw choices
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    actions = [
        lambda: chronos_make_choice("preserve"),
        lambda: chronos_make_choice("intervene"),
        lambda: chronos_make_choice("knowledge")
    ]
    
    for i, (choice, action) in enumerate(zip(choices, actions)):
        btn = Button(SCREEN_WIDTH//2 - 100, 500 + i*70, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=action)
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_chronos_ending():
    screen.fill(BACKGROUND)
    
    # Draw ending based on timeline integrity
    if game_state.timeline_integrity >= 80:
        title_text = heading_font.render("The Preserver of Time", True, CHRONOS_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        ending_text = [
            "You have successfully maintained the timeline,",
            "preserving the flow of history without major disruptions.",
            "The Temporal Council appoints you as the new Head Weaver,",
            "entrusting you with the protection of all timelines."
        ]
    elif game_state.timeline_integrity >= 50:
        title_text = heading_font.render("The Balanced Weaver", True, CHRONOS_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        ending_text = [
            "You managed to maintain a delicate balance in the timeline,",
            "though some alterations remain. The Temporal Council",
            "recognizes your efforts but places you under supervision",
            "as you continue your training."
        ]
    else:
        title_text = heading_font.render("The Timeline Breaker", True, CHRONOS_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        ending_text = [
            "Your actions have caused significant damage to the timeline,",
            "creating multiple paradoxes and alternate realities.",
            "The Temporal Council exiles you to a unstable timeline",
            "where you must live with the consequences of your choices."
        ]
    
    # Draw ending text
    for i, line in enumerate(ending_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))
    
    # Draw timeline integrity meter
    meter_text = text_font.render(f"Final Timeline Integrity: {game_state.timeline_integrity}%", True, TEXT_COLOR)
    screen.blit(meter_text, (SCREEN_WIDTH//2 - meter_text.get_width()//2, 400))
    
    meter_width = 600
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH//2 - meter_width//2, 450, meter_width, 20))
    pygame.draw.rect(screen, CHRONOS_COLOR, (SCREEN_WIDTH//2 - meter_width//2, 450, meter_width * (game_state.timeline_integrity/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (SCREEN_WIDTH//2 - meter_width//2, 450, meter_width, 20), 2)
    
    # Draw menu button
    menu_btn = Button(SCREEN_WIDTH//2 - 100, 550, 200, 50, "Return to Menu", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    menu_btn.update(mouse_pos)
    menu_btn.draw(screen)
    
    return [menu_btn]

# Echoes of the Void screens
def draw_void_intro():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw title
    title_text = title_font.render("ECHOES OF THE VOID", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    subtitle_text = heading_font.render("A Cosmic Horror Mystery", True, TEXT_COLOR)
    screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 180))
    
    # Draw intro text
    intro_lines = [
        "You arrive at the remote research station 'Event Horizon'",
        "near the edge of known space. The station has gone silent.",
        "As you explore, you discover the crew has been transformed",
        "by an unknown cosmic entity. Ancient alien artifacts allow",
        "communication with beings from outside our dimension,",
        "but at what cost to your sanity?"
    ]
    
    for i, line in enumerate(intro_lines):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*40))
    
    # Draw start button
    start_btn = Button(SCREEN_WIDTH//2 - 150, 500, 300, 50, "Begin Investigation", VOID_COLOR, (110, 50, 130), 
                      lambda: setattr(game_state, 'current_screen', 'void_scenario_1'))
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    buttons = [start_btn, back_btn]
    
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_void_scenario_1():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw sanity meter with frame
    sanity_text = text_font.render(f"Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (50, 100))
    
    meter_width = 150
    pygame.draw.rect(screen, (30, 30, 30), (50, 130, meter_width, 20))
    pygame.draw.rect(screen, VOID_COLOR, (50, 130, meter_width * (game_state.sanity/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (50, 130, meter_width, 20), 2)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 1: The Artifact", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario text
    scenario_text = [
        "You discover the first alien artifact in the research lab.",
        "It pulsates with an otherworldly energy and seems to whisper",
        "to you. The station logs indicate the crew was studying",
        "this object before they disappeared."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Destroy the artifact - it's too dangerous",
        "B. Use the artifact - harness its power",
        "C. Study the artifact - learn its secrets"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    actions = [
        lambda: void_make_choice("destroy"),
        lambda: void_make_choice("use"),
        lambda: void_make_choice("study")
    ]
    
    for i, (choice, action) in enumerate(zip(choices, actions)):
        btn = Button(SCREEN_WIDTH//2 - 100, 500 + i*70, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=action)
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_void_scenario_2():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw sanity meter with frame
    sanity_text = text_font.render(f"Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (50, 100))
    
    meter_width = 150
    pygame.draw.rect(screen, (30, 30, 30), (50, 130, meter_width, 20))
    pygame.draw.rect(screen, VOID_COLOR, (50, 130, meter_width * (game_state.sanity/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (50, 130, meter_width, 20), 2)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 2: The Survivor", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario text
    scenario_text = [
        "You find a surviving crew member hiding in the ventilation system.",
        "She's terrified but has valuable information about what happened.",
        "She begs you to help her escape, but helping her would mean",
        "abandoning your investigation and potentially allowing the",
        "entity to spread to other systems."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Save the survivor - prioritize human life",
        "B. Continue investigating - the mission comes first",
        "C. Question her thoroughly - get all information first"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    actions = [
        lambda: void_make_choice("destroy"),
        lambda: void_make_choice("use"),
        lambda: void_make_choice("study")
    ]
    
    for i, (choice, action) in enumerate(zip(choices, actions)):
        btn = Button(SCREEN_WIDTH//2 - 100, 500 + i*70, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=action)
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_void_scenario_3():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw sanity meter with frame
    sanity_text = text_font.render(f"Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (50, 100))
    
    meter_width = 150
    pygame.draw.rect(screen, (30, 30, 30), (50, 130, meter_width, 20))
    pygame.draw.rect(screen, VOID_COLOR, (50, 130, meter_width * (game_state.sanity/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (50, 130, meter_width, 20), 2)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 3: The Entity", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario text
    scenario_text = [
        "You come face to face with the cosmic entity itself.",
        "It offers you unimaginable knowledge and power in exchange",
        "for allowing it to use you as a gateway to our dimension.",
        "You feel its presence in your mind, tempting you with",
        "visions of cosmic understanding beyond human comprehension."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Resist the entity - fight its influence",
        "B. Embrace the entity - accept its power",
        "C. Bargain with the entity - seek a middle path"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    actions = [
        lambda: void_make_choice("destroy"),
        lambda: void_make_choice("use"),
        lambda: void_make_choice("study")
    ]
    
    for i, (choice, action) in enumerate(zip(choices, actions)):
        btn = Button(SCREEN_WIDTH//2 - 100, 500 + i*70, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=action)
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_void_scenario_4():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw sanity meter with frame
    sanity_text = text_font.render(f"Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (50, 100))
    
    meter_width = 150
    pygame.draw.rect(screen, (30, 30, 30), (50, 130, meter_width, 20))
    pygame.draw.rect(screen, VOID_COLOR, (50, 130, meter_width * (game_state.sanity/100), 20))
    pygame.draw.rect(screen, TEXT_COLOR, (50, 130, meter_width, 20), 2)
    
    # Draw scenario title
    title_text = heading_font.render("Scenario 4: The Final Choice", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw scenario text
    scenario_text = [
        "You've reached the heart of the station where the main",
        "dimensional rift is located. The entity is at its strongest here.",
        "You have the means to seal the rift permanently, but doing so",
        "would trap you on this side. Alternatively, you could attempt",
        "to control the rift, with unpredictable consequences."
    ]
    
    for i, line in enumerate(scenario_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*40))
    
    # Draw choices
    choice_text = [
        "A. Seal the rift - sacrifice yourself to save humanity",
        "B. Control the rift - attempt to master its power",
        "C. Escape - leave the station and warn others"
    ]
    
    for i, line in enumerate(choice_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 350 + i*40))
    
    # Draw choice buttons
    buttons = []
    choices = ["A", "B", "C"]
    actions = [
        lambda: void_make_choice("destroy"),
        lambda: void_make_choice("use"),
        lambda: void_make_choice("study")
    ]
    
    for i, (choice, action) in enumerate(zip(choices, actions)):
        btn = Button(SCREEN_WIDTH//2 - 100, 500 + i*70, 200, 50, f"Choose {choice}", 
                    BUTTON_COLOR, BUTTON_HOVER, action=action)
        buttons.append(btn)
    
    back_btn = Button(50, 50, 150, 40, "Back", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    buttons.append(back_btn)
    
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw(screen)
    
    return buttons

def draw_void_ending_madness():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw ending title
    title_text = heading_font.render("Descended into Madness", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    # Draw ending text
    ending_text = [
        "The cosmic entity has consumed your mind. You now see",
        "the true nature of reality, but it has driven you insane.",
        "You become a vessel for the entity, spreading its influence",
        "to new worlds and dimensions. Your humanity is lost,",
        "but you have gained unimaginable power at a terrible cost."
    ]
    
    for i, line in enumerate(ending_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))
    
    # Draw final sanity
    sanity_text = text_font.render(f"Final Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (SCREEN_WIDTH//2 - sanity_text.get_width()//2, 450))
    
    # Draw menu button
    menu_btn = Button(SCREEN_WIDTH//2 - 100, 550, 200, 50, "Return to Menu", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    menu_btn.update(mouse_pos)
    menu_btn.draw(screen)
    
    return [menu_btn]

def draw_void_ending_safe():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw ending title
    title_text = heading_font.render("The Void Contained", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    # Draw ending text
    ending_text = [
        "You successfully contained the cosmic entity and sealed",
        "the rift between dimensions. The station is destroyed,",
        "but you managed to save the surviving crew members.",
        "Your report leads to a galaxy-wide warning about the dangers",
        "of researching alien artifacts without proper safeguards."
    ]
    
    for i, line in enumerate(ending_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))
    
    # Draw final sanity
    sanity_text = text_font.render(f"Final Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (SCREEN_WIDTH//2 - sanity_text.get_width()//2, 450))
    
    # Draw menu button
    menu_btn = Button(SCREEN_WIDTH//2 - 100, 550, 200, 50, "Return to Menu", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    menu_btn.update(mouse_pos)
    menu_btn.draw(screen)
    
    return [menu_btn]

def draw_void_ending_mixed():
    screen.fill(BACKGROUND)
    
    # Draw void particles
    for particle in game_state.void_particles:
        x, y, size, speed, color = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        particle[1] += speed
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = 0
            particle[0] = random.randint(0, SCREEN_WIDTH)
    
    # Draw ending title
    title_text = heading_font.render("A Fragile Balance", True, VOID_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    # Draw ending text
    ending_text = [
        "You managed to contain the entity but not without cost.",
        "The rift is stabilized but not completely closed, requiring",
        "constant monitoring. You've retained some of your sanity",
        "but are forever changed by what you've experienced.",
        "You now lead the effort to study and control the entity,",
        "walking a fine line between discovery and damnation."
    ]
    
    for i, line in enumerate(ending_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))
    
    # Draw final sanity
    sanity_text = text_font.render(f"Final Sanity: {game_state.sanity}%", True, TEXT_COLOR)
    screen.blit(sanity_text, (SCREEN_WIDTH//2 - sanity_text.get_width()//2, 450))
    
    # Draw menu button
    menu_btn = Button(SCREEN_WIDTH//2 - 100, 550, 200, 50, "Return to Menu", BUTTON_COLOR, BUTTON_HOVER, return_to_menu)
    
    mouse_pos = pygame.mouse.get_pos()
    menu_btn.update(mouse_pos)
    menu_btn.draw(screen)
    
    return [menu_btn]

# Store current buttons globally
current_buttons = []

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Get buttons for current screen
    if game_state.current_screen == "main_menu":
        current_buttons = draw_main_menu()
    elif game_state.current_screen == "aetherian_intro":
        current_buttons = draw_aetherian_intro()
    elif game_state.current_screen.startswith("aetherian_scenario_"):
        scenario_num = int(game_state.current_screen.split("_")[-1])
        if scenario_num == 1:
            current_buttons = draw_aetherian_scenario_1()
        elif scenario_num == 2:
            current_buttons = draw_aetherian_scenario_2()
        elif scenario_num == 3:
            current_buttons = draw_aetherian_scenario_3()
        elif scenario_num == 4:
            current_buttons = draw_aetherian_scenario_4()
    elif game_state.current_screen == "aetherian_judgment":
        current_buttons = draw_aetherian_judgment()
    elif game_state.current_screen == "chronos_intro":
        current_buttons = draw_chronos_intro()
    elif game_state.current_screen == "chronos_scenario_1":
        current_buttons = draw_chronos_scenario_1()
    elif game_state.current_screen == "chronos_ending":
        current_buttons = draw_chronos_ending()
    elif game_state.current_screen == "void_intro":
        current_buttons = draw_void_intro()
    elif game_state.current_screen == "void_scenario_1":
        current_buttons = draw_void_scenario_1()
    elif game_state.current_screen == "void_scenario_2":
        current_buttons = draw_void_scenario_2()
    elif game_state.current_screen == "void_scenario_3":
        current_buttons = draw_void_scenario_3()
    elif game_state.current_screen == "void_scenario_4":
        current_buttons = draw_void_scenario_4()
    elif game_state.current_screen == "void_ending_madness":
        current_buttons = draw_void_ending_madness()
    elif game_state.current_screen == "void_ending_safe":
        current_buttons = draw_void_ending_safe()
    elif game_state.current_screen == "void_ending_mixed":
        current_buttons = draw_void_ending_mixed()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle button events
        for button in current_buttons:
            if button.handle_event(event):
                break
    
    # Update typing animation
    game_state.update_typing()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()