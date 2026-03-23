import pygame
from .timer import CooldownTimer
from .projectiles import Projectile
from .fireball import Fireball
from .lightning import ChainLightning
from.summon import Summon
class Player(pygame.sprite.Sprite):
    """
    Main player character.
    """

    def __init__(self, settings, x, y):
        """
        Initialize player.
        """
        super().__init__()
        self.settings = settings
        self.size = settings.player_size

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(settings.color_player)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.x = float(self.pos.x)
        self.y = float(self.pos.y)

        # Vectors
        self.vel_x = 0
        self.vel_y = 0
        self.knockback = pygame.Vector2(0, 0)
        self.dash_vel = pygame.Vector2(0, 0)  # New Dash Vector

        self.health = settings.max_health
        self.mana = settings.player_max_mana

        self.dash_timer = CooldownTimer(settings.dash_cooldown)
        self.shoot_timer = CooldownTimer(settings.projectile_cooldown)
        self.heal_timer = CooldownTimer(settings.heal_cooldown)
        self.last_hit_time = 0
        self.spell= 4

    def handle_input(self, cam_x, cam_y):
        """
        Handle Keys (WASD) and Mouse.
        """
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        self.vel_y = 0
        speed = self.settings.player_speed

        # --- WASD MOVEMENT ---
        # Only allow input if not heavily stunned
        if self.knockback.length() < 2:
            if keys[pygame.K_a]:
                self.vel_x = -speed

            if keys[pygame.K_d]:
                self.vel_x = speed

            if keys[pygame.K_w]:
                self.vel_y = -speed

            if keys[pygame.K_s]:
                self.vel_y = speed

            if keys[pygame.K_1]:
                self.spell_selection(1)

            if keys[pygame.K_2]:
                self.spell_selection(2)

            if keys[pygame.K_3]:
                self.spell_selection(3)

            if keys[pygame.K_4]:
                self.spell_selection(4)

            if keys[pygame.K_5]:
                self.spell_selection(5)

        # --- DASH (Shift) ---
        if keys[pygame.K_LSHIFT] and self.dash_timer.is_ready():
            # Check if the player is moving
            if self.vel_x != 0 or self.vel_y != 0:
                # Calculate normalized direction
                move_dir = pygame.Vector2(self.vel_x, self.vel_y)

                if move_dir.length() > 0:
                    move_dir = move_dir.normalize()

                # Apply Impulse Force
                self.dash_vel = move_dir * self.settings.dash_force

                # Start Cooldown
                self.dash_timer.trigger()
                self.is_dashing = True

        # --- SHOOT (Left Click) ---
        mouse_buttons = pygame.mouse.get_pressed()

        if self.spell == 1:
            if mouse_buttons[0] and self.mana > self.settings.heal_spell_cost and self.heal_timer.is_ready() and self.health < self.settings.max_health:
                self.mana -= self.settings.heal_spell_cost
                self.health += self.settings.heal_spell_amount
                self.heal_timer.trigger()

        if self.spell == 2:
            if mouse_buttons[0] and self.mana >= self.settings.water_bullet_spell_cost and self.shoot_timer.is_ready():
                self.shoot_timer.trigger()
                return self.create_projectile(cam_x, cam_y)

        if mouse_buttons[0] and self.spell == 3 and self.shoot_timer.is_ready():
            if self.mana >= self.settings.fireball_spell_cost:
                self.shoot_timer.trigger()
                return self.create_fireball(cam_x, cam_y)

        if self.spell == 4:
            if mouse_buttons[0] and self.mana >= self.settings.lightning_cost and self.shoot_timer.is_ready():
                self.shoot_timer.trigger()
                return self.create_chain_lightning(cam_x,cam_y)

        if self.spell == 5:
            if mouse_buttons[0] and self.mana >= self.settings.summon_spell_cost and self.shoot_timer.is_ready():
                self.shoot_timer.trigger()
                return self.summon_spell()
        return None

    def spell_selection(self,choice):

    ## --- Heal Spell --- #
        if choice == 1:
            self.spell = 1

    # --- water bullet spell --- #
        if choice == 2:
            self.spell = 2

    # --- Fireball spell ---#

        if choice == 3:
            self.spell = 3

    # --- Lightning spell ---#

        if choice == 4:
            self.spell = 4

    # --- Summon Spell --- #

        if choice == 5:
            self.spell = 5

    def create_projectile(self, cam_x, cam_y):
        """
        Creates a projectile aimed at mouse.
        """
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        world_mouse = mouse_pos + pygame.Vector2(cam_x, cam_y)
        player_center = pygame.Vector2(self.rect.center)

        direction = world_mouse - player_center
        if direction.length() > 0:
            direction = direction.normalize()
            self.mana -= self.settings.water_bullet_spell_cost
            return Projectile(self.settings, player_center.x, player_center.y, direction, "Player")

        return None

    def create_fireball(self, cam_x, cam_y):
        """Creates a fireball aimed at mouse."""
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        world_mouse = mouse_pos + pygame.Vector2(cam_x, cam_y)
        player_center = pygame.Vector2(self.rect.center)
        direction = world_mouse - player_center

        if direction.length() > 0:
            direction = direction.normalize()
            self.mana -= self.settings.fireball_spell_cost
            return Fireball(self.settings, player_center.x, player_center.y, direction)
        return None

    def create_chain_lightning(self,cam_x,cam_y):
        self.mana -= self.settings.lightning_cost
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos() + pygame.Vector2(cam_x,cam_y))
        return ChainLightning(self.settings, self.rect.center , mouse_pos)

    def summon_spell(self):
        return Summon(self.settings,"Player","enemy",self.pos)


    def apply_knockback(self, direction_vector):
        """
        Add impulse force to player.
        """
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.settings.iframe_duration:
            self.knockback = direction_vector * self.settings.knockback_strength

    def take_damage(self, amount):
        """
        Lose health with I-Frames.
        """
        now = pygame.time.get_ticks()

        if now - self.last_hit_time > self.settings.iframe_duration:
            self.health -= amount
            self.last_hit_time = now

            if self.health < 0:
                self.health = 0

    def get_position(self):
        """Return the player's current position as a tuple."""
        return self.rect.center

    def update(self, collision_machine, walls):
        """
        Physics and Updates.
        """
        # Mana Regen
        if self.mana < self.settings.player_max_mana:
            self.mana += self.settings.mana_regen

        # --- PHYSICS ENGINE ---

        # 1. Apply Dash Friction
        self.dash_vel *= self.settings.dash_friction
        # Stop micro-sliding
        if self.dash_vel.length() < 0.5:
            self.dash_vel = pygame.Vector2(0, 0)

        # 2. Apply Knockback Friction
        self.knockback *= self.settings.knockback_friction
        if self.knockback.length() < 0.5:
            self.knockback = pygame.Vector2(0, 0)

        # 3. Combine Forces (Input + Dash + Knockback)
        self.vel_x += self.dash_vel.x + self.knockback.x
        self.vel_y += self.dash_vel.y + self.knockback.y

        # 4. Resolve Wall Collisions (Sub-Stepping prevents clipping)
        collision_machine.resolve_wall_collision(self, walls)

        # 5. Map Clamping
        map_w = self.settings.map_width_tiles * self.settings.tile_size
        map_h = self.settings.map_height_tiles * self.settings.tile_size

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > map_w - self.size:
            self.x = map_w - self.size
        if self.y > map_h - self.size:
            self.y = map_h - self.size

        # 6. Sync Rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        ## --- Stats Check ---

        if self.health > self.settings.max_health:
            self.health = self.settings.max_health

        ## --- Update Vector2 --- #

        self.pos.x=self.x
        self.pos.y=self.y

    def draw(self, surface, cam_x, cam_y):
        """
        Draw relative to camera.
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y

        # Flash effect for I-Frames
        if pygame.time.get_ticks() - self.last_hit_time < self.settings.iframe_duration:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                pygame.draw.rect(surface, (255, 255, 255), draw_rect)
                return

        pygame.draw.rect(surface, self.settings.color_player, draw_rect)