import pygame
from constants import *

class Button:
    def __init__(self, x, y, width, height, text, font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.clicked = False
        self.hover = False
        
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hover:
                self.clicked = True
                return False  
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.clicked and self.hover:
                    self.clicked = False
                    return True  # Activar al soltar
                self.clicked = False
        
        return False
    
    def draw(self, screen):
        # Determinar color basado en estado
        if self.clicked:
            color = DARK_GRAY
            text_color = WHITE
        elif self.hover:
            color = LIGHT_GRAY
            text_color = BLACK
        else:
            color = GRAY
            text_color = WHITE
        
        # Dibujar botón
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Dibujar texto centrado
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class ToggleButton(Button):
    def __init__(self, x, y, width, height, text_off, text_on, initial_state=False, font_size=20):
        super().__init__(x, y, width, height, text_off, font_size)
        self.text_off = text_off
        self.text_on = text_on
        self.state = initial_state
        self.last_click_time = 0  
        self.update_text()
    
    def update_text(self):
        self.text = self.text_on if self.state else self.text_off
    
    def handle_event(self, event):
        import time
        current_time = time.time()
        
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hover:
                self.clicked = True
                return False
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.clicked and self.hover:
                # Evitar clics múltiples muy rápidos
                if current_time - self.last_click_time > 0.1:  # 100ms de cooldown
                    self.clicked = False
                    self.state = not self.state
                    self.update_text()
                    self.last_click_time = current_time
                    return True
                else:
                    self.clicked = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.clicked = False
        
        return False
    
    def draw(self, screen):
        # Cambiar colores basado en estado
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
        if self.state:
            # Estado activado
            if self.clicked:
                color = (0, 120, 0)
            elif self.hover:
                color = (0, 200, 0)
            else:
                color = (0, 150, 0)
            text_color = WHITE
        else:
            # Estado desactivado
            if self.clicked:
                color = DARK_GRAY
            elif self.hover:
                color = LIGHT_GRAY
                text_color = BLACK
            else:
                color = GRAY
                text_color = WHITE
            if not self.hover:
                text_color = WHITE
        
        # Dibujar botón
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Dibujar texto centrado
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)