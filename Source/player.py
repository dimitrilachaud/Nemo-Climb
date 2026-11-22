import pygame
from .character import Character


class Player:
    def __init__(self, x, y, character=None):
        self.width, self.height = 42, 54
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 300
        self.jump_strength = 690
        self.gravity = 1750
        self.character = character or Character()
        self.is_alive = True
        self.is_grounded = True
        self.facing_left = False
        self.hurt_animation = False
        self.standing_platform = None
        self.flying = False
        self.flight_speed = 300
        self.double_jump_active = False
        self.air_jumps_used = 0

    def handle_input(self, keys):
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        vertical = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(
            keys[pygame.K_UP] or keys[pygame.K_w]
        )
        if self.flying:
            movement = pygame.Vector2(direction, vertical)
            if movement.length_squared() > 1:
                movement = movement.normalize()
            self.velocity.update(movement.x * self.flight_speed,
                                 movement.y * self.flight_speed)
        else:
            self.velocity.x = direction * self.speed
        if direction:
            self.facing_left = direction < 0
            self.character.facing_left = self.facing_left

    def jump(self):
        if self.is_grounded and self.is_alive:
            self.velocity.y = -self.jump_strength
            self.is_grounded = False
            self.standing_platform = None
            self.air_jumps_used = 1
            return True
        elif self.is_alive and self.double_jump_active and self.air_jumps_used < 2:
            self.velocity.y = -self.jump_strength
            self.air_jumps_used += 1
            return True
        return False

    def set_double_jump_active(self, active):
        self.double_jump_active = bool(active)

    def refresh_double_jump_on_landing(self):
        # Reset unconditionally; the boots timer controls whether the extra
        # jump can be used on the next takeoff.
        self.air_jumps_used = 0

    def apply_gravity(self, dt):
        self.velocity.y += self.gravity * dt

    def toggle_flight(self):
        self.flying = not self.flying
        self.velocity.update(0, 0)
        self.is_grounded = False
        self.standing_platform = None
        return self.flying

    def check_platform_collision(self, platforms, previous_bottom):
        if self.velocity.y <= 0:
            return None
        for platform in platforms:
            if (previous_bottom <= platform.rect.top and
                    self.rect.bottom >= platform.rect.top and
                    self.rect.right > platform.rect.left and
                    self.rect.left < platform.rect.right):
                self.rect.bottom = platform.rect.top
                self.position.y = self.rect.y
                self.velocity.y = 0
                self.is_grounded = True
                self.standing_platform = platform
                self.air_jumps_used = 0
                return platform
        return None

    def update(self, dt, platforms, screen_width):
        if self.flying:
            self.position += self.velocity * dt
            self.rect.topleft = (round(self.position.x), round(self.position.y))
            if self.rect.right < 0:
                self.rect.left = screen_width
            elif self.rect.left > screen_width:
                self.rect.right = 0
            self.position.x = self.rect.x
            self.is_grounded = False
            self.standing_platform = None
            animation = "jump" if self.velocity.length_squared() else "idle"
            self.character.update_animation(dt, animation)
            return None

        if self.is_grounded and self.standing_platform is not None:
            self.position.x += self.standing_platform.delta_x
            self.rect.x = round(self.position.x)
        previous_bottom = self.rect.bottom
        self.is_grounded = False
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.apply_gravity(dt)
        self.rect.topleft = (round(self.position.x), round(self.position.y))

        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        self.position.x = self.rect.x

        landed_platform = self.check_platform_collision(platforms, previous_bottom)
        if self.hurt_animation:
            animation = "hurt"
        elif self.velocity.y < -80 or self.velocity.y > 80:
            animation = "jump"
        elif abs(self.velocity.x) > 5:
            animation = "walk"
        else:
            animation = "idle"
        self.character.facing_left = self.facing_left
        self.character.update_animation(dt, animation)
        return landed_platform

    def check_hazard_collision(self, hazards):
        return any(hazard.check_collision(self.rect) for hazard in hazards)

    def set_hurt(self):
        self.is_alive = False
        self.hurt_animation = True
        self.character.update_animation(0, "hurt")

    def draw(self, surface, camera):
        self.character.draw(surface, camera.apply(self.rect))

    def reset(self, x, y):
        self.position.update(x, y)
        self.rect.topleft = (x, y)
        self.velocity.update(0, 0)
        self.is_alive = True
        self.is_grounded = True
        self.hurt_animation = False
        self.standing_platform = None
        self.flying = False
        self.double_jump_active = False
        self.air_jumps_used = 0
