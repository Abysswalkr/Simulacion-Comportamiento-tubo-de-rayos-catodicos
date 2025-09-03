import pygame
from constants import *

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label, unit=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.unit = unit
        self.dragging = False
        self.font = pygame.font.Font(None, 20)
        
        # Calcular posición inicial del handle
        self.handle_radius = height // 2
        self.track_rect = pygame.Rect(x + self.handle_radius, y + height//4, 
                                    width - 2*self.handle_radius, height//2)
        self.update_handle_pos()
    
    def update_handle_pos(self):
        # Calcular posición del handle basada en el valor
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.track_rect.x + ratio * self.track_rect.width
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                mouse_x, mouse_y = event.pos
                handle_rect = pygame.Rect(self.handle_x - self.handle_radius, 
                                        self.rect.y, 
                                        2*self.handle_radius, self.rect.height)
                if handle_rect.collidepoint(mouse_x, mouse_y):
                    self.dragging = True
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            # Limitar el handle al track
            self.handle_x = max(self.track_rect.x, 
                              min(mouse_x, self.track_rect.x + self.track_rect.width))
            
            # Calcular nuevo valor
            ratio = (self.handle_x - self.track_rect.x) / self.track_rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            return True
        
        return False
    
    def set_value(self, value):
        self.value = max(self.min_val, min(self.max_val, value))
        self.update_handle_pos()
    
    def draw(self, screen):
        # Dibujar track
        pygame.draw.rect(screen, DARK_GRAY, self.track_rect)
        pygame.draw.rect(screen, WHITE, self.track_rect, 2)
        
        # Dibujar handle
        pygame.draw.circle(screen, LIGHT_GRAY, (int(self.handle_x), self.rect.centery), 
                          self.handle_radius)
        pygame.draw.circle(screen, WHITE, (int(self.handle_x), self.rect.centery), 
                          self.handle_radius, 2)
        
        # Dibujar label
        label_surface = self.font.render(self.label, True, WHITE)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # Dibujar valor
        if isinstance(self.value, float):
            value_text = f"{self.value:.2f} {self.unit}"
        else:
            value_text = f"{int(self.value)} {self.unit}"
        value_surface = self.font.render(value_text, True, WHITE)
        screen.blit(value_surface, (self.rect.x, self.rect.y + self.rect.height + 5))