import math
import pygame


class PowerUp:
    TYPES = ("heart", "boots", "snowflake")

    def __init__(self, x, y, power_type):
        self.power_type = power_type if power_type in self.TYPES else "heart"
        self.rect = pygame.Rect(x, y, 28, 28)
        self.base_y = y
        self.phase = 0.0
        self.is_active = True

    def update(self, dt):
        self.phase += dt
        self.rect.y = round(self.base_y + math.sin(self.phase * 4) * 3)

    def draw(self, surface, camera):
        if not self.is_active:
            return
        rect = camera.apply(self.rect)
        self.draw_icon(surface, rect, self.power_type)

    def check_collision(self, player_rect):
        return self.is_active and self.rect.colliderect(player_rect)

    @staticmethod
    def draw_icon(surface, rect, power_type):
        x, y, w, h = rect
        if power_type == "heart":
            color = (246, 91, 125)
            pygame.draw.circle(surface, color, (x + round(w * .36), y + round(h * .36)), max(3, round(w * .22)))
            pygame.draw.circle(surface, color, (x + round(w * .64), y + round(h * .36)), max(3, round(w * .22)))
            pygame.draw.polygon(surface, color,
                                [(x + round(w * .15), y + round(h * .40)),
                                 (x + round(w * .85), y + round(h * .40)),
                                 (x + round(w * .50), y + round(h * .88))])
            pygame.draw.circle(surface, (255, 196, 205),
                               (x + round(w * .34), y + round(h * .27)), max(1, round(w * .05)))
        elif power_type == "boots":
            color = (238, 184, 91)
            left_boot = [(x + round(w * .15), y + round(h * .18)),
                         (x + round(w * .42), y + round(h * .18)),
                         (x + round(w * .42), y + round(h * .58)),
                         (x + round(w * .52), y + round(h * .72)),
                         (x + round(w * .48), y + round(h * .84)),
                         (x + round(w * .12), y + round(h * .84)),
                         (x + round(w * .12), y + round(h * .68)),
                         (x + round(w * .22), y + round(h * .58))]
            right_boot = [(px + round(w * .38), py - round(h * .05)) for px, py in left_boot]
            pygame.draw.polygon(surface, color, left_boot)
            pygame.draw.polygon(surface, color, right_boot)
            pygame.draw.line(surface, (255, 231, 166), left_boot[5], left_boot[4], 2)
            pygame.draw.line(surface, (255, 231, 166), right_boot[5], right_boot[4], 2)
        else:
            color = (115, 221, 246)
            center = (x + w // 2, y + h // 2)
            end_radius = round(min(w, h) * .43)
            for angle in range(0, 360, 60):
                radians = math.radians(angle)
                ex = center[0] + round(math.cos(radians) * end_radius)
                ey = center[1] + round(math.sin(radians) * end_radius)
                pygame.draw.line(surface, color, center, (ex, ey), max(2, round(w * .09)))
                for branch_angle in (angle + 135, angle + 225):
                    br = math.radians(branch_angle)
                    bx = ex - round(math.cos(br) * end_radius * .24)
                    by = ey - round(math.sin(br) * end_radius * .24)
                    pygame.draw.line(surface, color, (ex, ey), (bx, by), max(1, round(w * .06)))
            pygame.draw.circle(surface, (225, 250, 255), center, max(2, round(w * .08)))
