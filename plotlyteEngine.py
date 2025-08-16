

import subprocess
import time
import random
import os
import sys
import json
import pygame
from pygame.locals import *
from PIL import Image

# --- Optional: DotDot credits (won't crash if not installed) ---
try:
    from dotdot import DotDot
    DotDot.credits("Plotlyte")
except Exception:
    pass


# -----------------------------
# Core primitives
# -----------------------------
class Object:
    def __init__(self, pos=(0, 0)):
        # world-space float position
        self.position = tuple(map(float, pos))
        self.texture = None  # pygame.Surface OR (frames, animations)
        self.hitbox = None   # Hitbox

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def set_pos(self, x, y):
        self.position = (float(x), float(y))


class Hitbox:
    """Simple AABB hitbox backed by pygame.Rect.
    Attach to an Object and call update_from_object(obj) each frame.
    """

    def __init__(self, width, height, offset=(0, 0)):
        self.offset = offset
        self.width = int(width)
        self.height = int(height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def update_from_object(self, obj):
        ox, oy = self.offset
        self.rect.topleft = (int(obj.x + ox), int(obj.y + oy))

    def collides_with(self, other: "Hitbox") -> bool:
        return self.rect.colliderect(other.rect)


class Pawn(Object):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.health = 100.0
        self.controls = {}
        self.control_set = None  # "main" | "ai"
        self.attack_key = None
        self.speed = 140.0  # pixels / second

        # AI plumbing
        self.ai_behavior = None  # set to a callable(player_pos, dt)
        self._ai_random_timer = 0.0

        # Animation state (per-entity)
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.current_animation_name = "idle"

    # ---------- AI behaviors (no sleeps; dt-driven) ----------
    def ai_move_towards_player_easy(self, player_pos, dt):
        px, py = player_pos
        x, y = self.position
        step = 70.0 * dt
        if x < px:
            x += step
        elif x > px:
            x -= step
        if y < py:
            y += step
        elif y > py:
            y -= step
        self.set_pos(x, y)

    def ai_move_towards_player_hard(self, player_pos, dt):
        px, py = player_pos
        x, y = self.position
        step = 140.0 * dt
        if x < px:
            x += step
        elif x > px:
            x -= step
        if y < py:
            y += step
        elif y > py:
            y -= step
        self.set_pos(x, y)

    def ai_random_movement(self, player_pos, dt):  # player_pos unused
        # Wander randomly every 0.4–1.2s
        self._ai_random_timer -= dt
        if self._ai_random_timer <= 0:
            self._ai_random_timer = random.uniform(0.4, 1.2)
            dx = random.choice([-1, 1]) * random.uniform(20, 60)
            dy = random.choice([-1, 1]) * random.uniform(20, 60)
            self.set_pos(self.x + dx, self.y + dy)


class Texture:
    @staticmethod
    def static(filename) -> pygame.Surface:
        pygame.init()
        pygame.display.set_mode((1, 1))  # tiny dummy window

        surf = pygame.image.load(filename)
        return surf.convert_alpha()

    @staticmethod
    def animated(filename, animations_file):
        """Load an ico/gif/etc with PIL, slice frames, and map animations from JSON.
        Returns (frames_surfaces: list[Surface], animations: dict)
        animations JSON example:
        {
            "idle": [0],
            "walk": [0,1,2,3],
            "attack": [4,5,6,7]
        }
        """
        with Image.open(filename) as img:
            frames = []
            for i in range(getattr(img, "n_frames", 1)):
                try:
                    img.seek(i)
                except EOFError:
                    break
                frame = img.convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                surf = pygame.image.fromstring(data, size, mode).convert_alpha()
                frames.append(surf)

        with open(animations_file, "r", encoding="utf-8") as f:
            animations = json.load(f)

        return frames, animations  # pre-converted to pygame surfaces


class Game:
    def __init__(self):
        self.entities: list[Pawn] = []
        self.objects: list[Object] = []
        self.name = "Untitled Game"
        self.FPS = 60

    def add_entity(self, entity: Pawn):
        self.entities.append(entity)

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def run(self, level, player):
        MainLoop(self, level, player).run()


class Level:
    def __init__(self, size=(800, 600)):
        self.background = None
        self.foreground = None
        self.dimensions = {"w": size[0], "h": size[1]}
        self.exits = []
        self.player_spawn = (0, 0)

    def load(self):
        pass

    def unload(self):
        pass


# -----------------------------
# Main loop
# -----------------------------
class MainLoop:
    def __init__(self, game: Game, current_level: Level, player: Pawn):
        self.game = game
        self.level = current_level
        self.player = player

        pygame.init()
        self.screen = pygame.display.set_mode((self.level.dimensions["w"], self.level.dimensions["h"]))
        pygame.display.set_caption(self.game.name)
        self.clock = pygame.time.Clock()

        # Ensure player hitbox exists if texture exists
        if self.player.texture and not self.player.hitbox:
            tex = self._resolve_current_surface(self.player)
            self.player.hitbox = Hitbox(tex.get_width(), tex.get_height())

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(self.game.FPS) / 1000.0  # seconds

            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # --- Player Input ---
            keys = pygame.key.get_pressed()
            if self.player.control_set == "main":
                x, y = self.player.position
                spd = self.player.speed * dt
                if keys[pygame.K_w]:
                    y -= spd
                if keys[pygame.K_s]:
                    y += spd
                if keys[pygame.K_a]:
                    x -= spd
                if keys[pygame.K_d]:
                    x += spd
                self.player.set_pos(x, y)

            # --- Update AI Pawns ---
            for entity in self.game.entities:
                if isinstance(entity, Pawn) and entity.control_set == "ai" and callable(entity.ai_behavior):
                    entity.ai_behavior(self.player.position, dt)

                # Update hitboxes if present
                if entity.hitbox:
                    entity.hitbox.update_from_object(entity)

            # Update player hitbox
            if self.player.hitbox:
                self.player.hitbox.update_from_object(self.player)

            # Collision: AI vs Player
            for entity in self.game.entities:
                if isinstance(entity, Pawn) and entity.hitbox and self.player.hitbox:
                    if entity.hitbox.collides_with(self.player.hitbox):
                        self.player.health = max(0.0, self.player.health - 10.0 * dt)
            # Collision: AI vs AI
            for i, entity in enumerate(self.game.entities):
                if not entity.hitbox:
                    continue
                for other in self.game.entities[i+1:]:
                    if not other.hitbox:
                        continue
                    if entity.hitbox.collides_with(other.hitbox):
                        # GO AWAY STUPID AI!!!!
                        ex, ey = entity.position
                        ox, oy = other.position
                        entity.set_pos(ex - 5, ey - 5)
                        other.set_pos(ox + 5, oy + 5)


            # --- Render ---
            self.screen.fill((0, 0, 0))

            # Background
            if self.level.background:
                self.screen.blit(self.level.background, (0, 0))

            # Objects
            for obj in self.game.objects:
                surf = self._resolve_current_surface(obj, dt)
                if surf is not None:
                    self.screen.blit(surf, (int(obj.x), int(obj.y)))

            # Pawns (including player)
            for entity in [*self.game.entities, self.player]:
                surf = self._resolve_current_surface(entity, dt)
                if surf is not None:
                    self.screen.blit(surf, (int(entity.x), int(entity.y)))

            # Foreground
            if self.level.foreground:
                self.screen.blit(self.level.foreground, (0, 0))

            # Optional: draw hitboxes for debugging
            # for entity in [*self.game.entities, self.player]:
            #     if entity.hitbox:
            #         pygame.draw.rect(self.screen, (255, 255, 255), entity.hitbox.rect, 1)

            pygame.display.update()

        pygame.quit()
        sys.exit(0)

    # --- Helpers ---
    def _resolve_current_surface(self, obj: Object, dt: float | None = None) -> pygame.Surface | None:
        tex = obj.texture
        if tex is None:
            return None
        # Animated: (frames, animations)
        if isinstance(tex, tuple) and len(tex) == 2 and isinstance(tex[0], list) and isinstance(tex[1], dict):
            return self._get_current_frame(obj, dt or 0.0)
        # Static: pygame.Surface
        if isinstance(tex, pygame.Surface):
            return tex
        return None

    def _get_current_frame(self, pawn: Pawn, dt: float) -> pygame.Surface:
        frames, animations = pawn.texture
        # Pick animation name by simple heuristic (you can set pawn.current_animation_name yourself)
        vx = vy = 0.0
        # If last movement changed position this frame, swap to walk
        # (A more robust system would store previous position; keeping it simple here.)
        current_anim = animations.get(getattr(pawn, "current_animation_name", "walk"), animations.get("walk", [0]))
        frame_duration = 0.1  # seconds per frame (tweak per anim later)

        pawn.animation_timer += dt
        if pawn.animation_timer >= frame_duration:
            pawn.animation_timer = 0.0
            pawn.animation_frame = (pawn.animation_frame + 1) % max(1, len(current_anim))

        idx = current_anim[pawn.animation_frame]
        return frames[idx]


# -----------------------------
# Example usage / bootstrap
# -----------------------------
if __name__ == "__main__":
    # Game + Level
    game = Game()
    game.name = "Plotlyte Demo"

    level = Level(size=(800, 600))
    level.background = pygame.Surface((800, 600))
    level.background.fill((50, 150, 50))  # green grass vibes

    # Player (red square)
    player = Pawn((400, 300))
    player.control_set = "main"
    player_surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    player_surf.fill((255, 60, 60))
    player.texture = player_surf
    player.hitbox = Hitbox(28, 28)

    # Enemy (blue square) with AI
    enemy = Pawn((200, 120))
    enemy.control_set = "ai"
    enemy_surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    enemy_surf.fill((60, 120, 255))
    # As an animated example, fake two-frame blink using the same surface
    frames = [enemy_surf, enemy_surf.copy()]
    frames[1].fill((60, 90, 220))
    enemy.texture = (frames, {"walk": [0, 1], "idle": [0]})
    enemy.hitbox = Hitbox(28, 28)

    # Choose AI behavior
    enemy.ai_behavior = enemy.ai_move_towards_player_easy  # or enemy.ai_move_towards_player_hard / enemy.ai_random_movement

    game.add_entity(enemy)

    # Run
    game.run(level, player)
