import random
import pygame

# --- Tunable constants -------------------------------------------------------
PRESS_FORCE = 4.2            # how far one valid key press pulls the arm
PRESS_COST = 2.5             # stamina spent per valid press
STAMINA_REGEN = 0.2         # stamina regained per frame
EXHAUST_THRESHOLD = 10.0     # at or below this, input is disabled

# AI surge cycle (times in milliseconds)
AI_BUILD_RATE = (0.35, 0.65)         # energy gained per frame while building (random range)
AI_SURGE_TIME = (1000, 2000)         # surge lasts 1-2 seconds
AI_TIRED_TIME = 2000                 # exhausted period after a surge
AI_NORMAL_MULT = 1.0
AI_SURGE_MULT = 2.5
AI_TIRED_MULT = 0.25


class GameEngine:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.arm_position = 0.0
        self.target_limit = 100.0
        self.last_key = None

        self.stamina = 100.0
        self.max_stamina = 100.0

        self.winner = None
        self.game_state = "PLAYING"
        self.ai_strength = 0.35

        # AI surge state machine: BUILDING -> SURGE -> TIRED -> BUILDING ...
        self.ai_state = "BUILDING"
        self.ai_energy = 0.0
        self.ai_state_end = 0        # tick time when SURGE/TIRED ends

        self.font_big = pygame.font.SysFont(None, 44)
        self.font_med = pygame.font.SysFont(None, 26)

    # ------------------------------------------------------------------ input
    def is_exhausted(self):
        return self.stamina <= EXHAUST_THRESHOLD

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if self.is_exhausted():
                return

            # TASK 1 FIX: the player wins at -target_limit, so pulling must SUBTRACT.
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                if self.last_key != event.key:
                    self.arm_position -= PRESS_FORCE
                    self.stamina = max(0.0, self.stamina - PRESS_COST)
                    self.last_key = event.key

    # ----------------------------------------------------------------- update
    def _update_ai(self):
        """TASK 2: computer builds energy, surges for 1-2s, then is exhausted."""
        now = pygame.time.get_ticks()

        if self.ai_state == "BUILDING":
            self.ai_energy = min(100.0, self.ai_energy + random.uniform(*AI_BUILD_RATE))
            if self.ai_energy >= 100.0:
                self.ai_state = "SURGE"
                self.ai_state_end = now + random.randint(*AI_SURGE_TIME)
            mult = AI_NORMAL_MULT

        elif self.ai_state == "SURGE":
            mult = AI_SURGE_MULT
            # energy visibly drains over the surge
            remaining = max(0, self.ai_state_end - now)
            self.ai_energy = max(0.0, min(100.0, remaining / 20.0))
            if now >= self.ai_state_end:
                self.ai_state = "TIRED"
                self.ai_state_end = now + AI_TIRED_TIME
                self.ai_energy = 0.0

        else:  # TIRED
            mult = AI_TIRED_MULT
            if now >= self.ai_state_end:
                self.ai_state = "BUILDING"
                self.ai_energy = 0.0

        ai_variance = random.uniform(0.3, 1.0)
        self.arm_position += self.ai_strength * ai_variance * mult

    def update(self):
        if self.game_state != "PLAYING":
            return

        self._update_ai()

        if self.stamina < self.max_stamina:
            self.stamina = min(self.max_stamina, self.stamina + STAMINA_REGEN)

        if self.arm_position <= -self.target_limit:
            self.winner = "PLAYER"
            self.game_state = "GAME_OVER"
        elif self.arm_position >= self.target_limit:
            self.winner = "COMPUTER"
            self.game_state = "GAME_OVER"

    def reset(self):
        self.arm_position = 0.0
        self.stamina = 100.0
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"
        self.ai_state = "BUILDING"
        self.ai_energy = 0.0
        self.ai_state_end = 0

    # ----------------------------------------------------------------- render
    def render(self, screen):
        screen.fill((25, 28, 35))
        now = pygame.time.get_ticks()
        exhausted = self.is_exhausted()
        flash_on = (now // 200) % 2 == 0

        title_surf = self.font_big.render("ARM WRESTLE SHOWDOWN", True, (240, 240, 240))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 12))

        player_header = self.font_med.render("PLAYER", True, (80, 160, 255))
        computer_header = self.font_med.render("COMPUTER", True, (255, 100, 80))
        screen.blit(player_header, (60, 55))
        screen.blit(computer_header, (self.width - 150, 55))

        # Computer energy bar + state label (Task 2 feedback)
        ai_bar_x, ai_bar_y, ai_bar_w = self.width - 150, 80, 100
        pygame.draw.rect(screen, (45, 50, 60), (ai_bar_x, ai_bar_y, ai_bar_w, 10), border_radius=4)
        ai_colors = {"BUILDING": (240, 190, 60), "SURGE": (255, 70, 50), "TIRED": (110, 120, 140)}
        fill_w = int(ai_bar_w * self.ai_energy / 100.0)
        pygame.draw.rect(screen, ai_colors[self.ai_state], (ai_bar_x, ai_bar_y, fill_w, 10), border_radius=4)
        if self.ai_state == "SURGE":
            ai_label = self.font_med.render("SURGE!", True, (255, 70, 50))
            screen.blit(ai_label, (ai_bar_x - 80, 50))
        elif self.ai_state == "TIRED":
            ai_label = self.font_med.render("tired...", True, (150, 160, 180))
            screen.blit(ai_label, (ai_bar_x - 80, 50))

        table_rect = pygame.Rect(40, 100, self.width - 80, 310)
        pygame.draw.rect(screen, (110, 50, 15), table_rect, border_radius=14)
        pygame.draw.rect(screen, (70, 30, 8), table_rect, width=5, border_radius=14)

        pygame.draw.line(screen, (45, 18, 4), (self.width // 2, 100), (self.width // 2, 410), 4)

        offset_x = (self.arm_position / self.target_limit) * 95
        hand_x = (self.width // 2) + int(offset_x)
        hand_y = 235

        p_shoulder = (70, 330)
        p_elbow = (140, 215)
        c_shoulder = (self.width - 70, 330)
        c_elbow = (self.width - 140, 215)

        # Task 3/4: player's arm trembles while exhausted
        p_hand = (hand_x, hand_y)
        if exhausted and self.game_state == "PLAYING":
            p_elbow = (p_elbow[0] + random.randint(-3, 3), p_elbow[1] + random.randint(-3, 3))
            p_hand = (hand_x + random.randint(-3, 3), hand_y + random.randint(-3, 3))

        pygame.draw.line(screen, (200, 145, 110), p_shoulder, p_elbow, 32)
        pygame.draw.line(screen, (215, 160, 125), p_elbow, p_hand, 26)
        pygame.draw.circle(screen, (185, 130, 95), p_elbow, 18)

        pygame.draw.line(screen, (170, 110, 85), c_shoulder, c_elbow, 32)
        pygame.draw.line(screen, (185, 125, 95), c_elbow, (hand_x, hand_y), 26)
        pygame.draw.circle(screen, (150, 95, 70), c_elbow, 18)

        pygame.draw.circle(screen, (225, 175, 140), p_hand, 24)
        pygame.draw.circle(screen, (160, 115, 85), p_hand, 24, width=3)

        # Stamina bar
        stamina_label = self.font_med.render("STAMINA", True, (220, 220, 220))
        screen.blit(stamina_label, (40, 445))

        stamina_bg = pygame.Rect(140, 448, 240, 22)
        stamina_fill = pygame.Rect(140, 448, int(240 * (self.stamina / self.max_stamina)), 22)
        pygame.draw.rect(screen, (45, 50, 60), stamina_bg, border_radius=6)

        if exhausted:
            # flashing red bar + flashing outline on the whole track
            bar_color = (255, 40, 40) if flash_on else (120, 20, 20)
            if flash_on:
                pygame.draw.rect(screen, (255, 40, 40), stamina_bg, width=2, border_radius=6)
        elif self.stamina > 25:
            bar_color = (60, 210, 100)
        else:
            bar_color = (220, 60, 60)
        pygame.draw.rect(screen, bar_color, stamina_fill, border_radius=6)

        # Exhaustion marker at the usable threshold
        thresh_x = 140 + int(240 * (EXHAUST_THRESHOLD / self.max_stamina))
        pygame.draw.line(screen, (240, 240, 240), (thresh_x, 444), (thresh_x, 474), 1)

        if exhausted and self.game_state == "PLAYING":
            if flash_on:
                warn = self.font_med.render("EXHAUSTED!", True, (255, 60, 60))
                screen.blit(warn, (395, 447))
            hint = self.font_med.render("Recovering... can't pull", True, (200, 130, 130))
            screen.blit(hint, (40, 485))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            win_text = "PLAYER WINS THE MATCH!" if self.winner == "PLAYER" else "COMPUTER WINS!"
            color = (80, 240, 100) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 45)
            )

            restart_surf = self.font_med.render(
                "Press [R] to Rematch", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )