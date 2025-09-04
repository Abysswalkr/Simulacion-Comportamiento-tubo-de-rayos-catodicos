import pygame
import sys
from constants import *
from crt_simulation import CRTSimulation
from slider import Slider
from button import Button, ToggleButton

class CRTApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Simulación de Tubo de Rayos Catódicos - Física 3")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicializar simulación
        self.simulation = CRTSimulation()
        
        # Crear controles de interfaz
        self.create_controls()
        
        # Font para labels
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Definir viewports
        self.lateral_viewport = pygame.Rect(LATERAL_VIEW_POS[0], LATERAL_VIEW_POS[1], 
                                          VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
        self.top_viewport = pygame.Rect(TOP_VIEW_POS[0], TOP_VIEW_POS[1], 
                                      VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
        self.front_viewport = pygame.Rect(FRONT_VIEW_POS[0], FRONT_VIEW_POS[1], 
                                        MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT)
    
    def create_controls(self):
        """Crea todos los controles de la interfaz"""
        x = CONTROL_PANEL_POS[0]
        y = CONTROL_PANEL_POS[1]
        
        # Slider de voltaje de aceleración
        self.voltage_acc_slider = Slider(
            x, y, 250, 30, 
            ACCELERATION_VOLTAGE_RANGE[0], ACCELERATION_VOLTAGE_RANGE[1], 
            1000, "Voltaje Aceleración", "V"
        )
        y += 80
        
        # Sliders de deflexión vertical
        self.voltage_vert_slider = Slider(
            x, y, 250, 30,
            DEFLECTION_VOLTAGE_RANGE[0], DEFLECTION_VOLTAGE_RANGE[1],
            0, "Voltaje Placas Verticales", "V"
        )
        y += 80
        
        # Slider de deflexión horizontal
        self.voltage_horiz_slider = Slider(
            x, y, 250, 30,
            DEFLECTION_VOLTAGE_RANGE[0], DEFLECTION_VOLTAGE_RANGE[1],
            0, "Voltaje Placas Horizontales", "V"
        )
        y += 80
        
        # Slider de persistencia
        self.persistence_slider = Slider(
            x, y, 250, 30,
            PERSISTENCE_RANGE[0], PERSISTENCE_RANGE[1],
            100, "Persistencia", "frames"
        )
        y += 80
        
        # Botón de modo sinusoidal
        self.sinusoidal_button = ToggleButton(
            x, y, 250, 40, 
            "Modo Manual", "Modo Sinusoidal", 
            False
        )
        y += 60
        
        # Controles para modo sinusoidal
        self.freq_vert_slider = Slider(
            x, y, 250, 30,
            FREQUENCY_RANGE[0], FREQUENCY_RANGE[1],
            1.0, "Frecuencia Vertical", "Hz"
        )
        y += 80
        
        self.freq_horiz_slider = Slider(
            x, y, 250, 30,
            FREQUENCY_RANGE[0], FREQUENCY_RANGE[1],
            1.5, "Frecuencia Horizontal", "Hz"
        )
        y += 80
        
        self.phase_vert_slider = Slider(
            x, y, 250, 30,
            PHASE_RANGE[0], PHASE_RANGE[1],
            0, "Fase Vertical", "°"
        )
        y += 80
        
        self.phase_horiz_slider = Slider(
            x, y, 250, 30,
            PHASE_RANGE[0], PHASE_RANGE[1],
            90, "Fase Horizontal", "°"
        )
        
        # Lista de todos los controles
        self.controls = [
            self.voltage_acc_slider,
            self.voltage_vert_slider, 
            self.voltage_horiz_slider,
            self.persistence_slider,
            self.sinusoidal_button,
            self.freq_vert_slider,
            self.freq_horiz_slider,
            self.phase_vert_slider,
            self.phase_horiz_slider
        ]
    
    def handle_events(self):
        """Maneja todos los eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Manejar eventos de controles
            for control in self.controls:
                if control.handle_event(event):
                    self.update_simulation_parameters()
    
    def update_simulation_parameters(self):
        """Actualiza los parámetros de la simulación basado en los controles"""
        self.simulation.V_acceleration = self.voltage_acc_slider.value
        self.simulation.V_vertical = self.voltage_vert_slider.value
        self.simulation.V_horizontal = self.voltage_horiz_slider.value
        self.simulation.persistence_frames = int(self.persistence_slider.value)
        self.simulation.sinusoidal_mode = self.sinusoidal_button.state
        
        # Parámetros sinusoidales
        self.simulation.frequency_vert = self.freq_vert_slider.value
        self.simulation.frequency_horiz = self.freq_horiz_slider.value
        self.simulation.phase_vert = self.phase_vert_slider.value
        self.simulation.phase_horiz = self.phase_horiz_slider.value
    
    def draw_viewport(self, viewport, title, color):
        """Dibuja el marco y título de un viewport"""
        pygame.draw.rect(self.screen, color, viewport, 2)
        pygame.draw.rect(self.screen, BLACK, viewport)
        
        # Título
        title_surface = self.font.render(title, True, WHITE)
        self.screen.blit(title_surface, (viewport.x, viewport.y - 25))
    
    def draw_trajectory(self, points, viewport, color):
        """Dibuja la trayectoria del haz de electrones"""
        if len(points) < 2:
            return
        
        # Ajustar puntos al viewport
        adjusted_points = []
        for x, y in points:
            adj_x = viewport.x + max(0, min(x, viewport.width))
            adj_y = viewport.y + max(0, min(y, viewport.height))
            adjusted_points.append((adj_x, adj_y))
        
        # Dibujar línea suavizada
        if len(adjusted_points) >= 2:
            pygame.draw.lines(self.screen, color, False, adjusted_points, 2)
        
        # Dibujar punto final más brillante
        if adjusted_points:
            pygame.draw.circle(self.screen, color, 
                             (int(adjusted_points[-1][0]), int(adjusted_points[-1][1])), 3)
    
    def draw_screen_trace(self):
        """Dibuja el rastro en la pantalla frontal con persistencia"""
        screen_points = self.simulation.get_screen_points()
        
        for x, y, intensity in screen_points:
            if (0 <= x < MAIN_SCREEN_WIDTH and 0 <= y < MAIN_SCREEN_HEIGHT):
                # Calcular color basado en intensidad
                green_value = int(255 * intensity)
                color = (0, green_value, 0)
                
                # Dibujar punto con tamaño basado en intensidad
                radius = max(1, int(4 * intensity)) 
                pygame.draw.circle(self.screen, color,
                                 (self.front_viewport.x + x, self.front_viewport.y + y), 
                                 radius)
    
    def draw_info_panel(self):
        """Dibuja panel con información física"""
        info_x = 20
        info_y = 540
        
        # Fondo del panel
        info_rect = pygame.Rect(info_x, info_y, 320, 240)
        pygame.draw.rect(self.screen, (20, 20, 20), info_rect)
        pygame.draw.rect(self.screen, WHITE, info_rect, 1)
        
        # Título
        title = self.font.render("Parámetros Físicos", True, WHITE)
        self.screen.blit(title, (info_x + 10, info_y + 10))
        
        # Información constante
        info_lines = [
            f"Tamaño pantalla: {SCREEN_SIZE*100:.0f} x {SCREEN_SIZE*100:.0f} cm",
            f"Separación placas: {PLATE_SEPARATION*100:.0f} cm", 
            f"Longitud placas: {PLATE_LENGTH*100:.0f} cm",
            f"Distancia placas-pantalla: {PLATE_TO_SCREEN_DISTANCE*100:.0f} cm",
            f"Distancia cañón-placas: {GUN_TO_PLATE_DISTANCE*100:.0f} cm",
            "",
            "Voltajes actuales:",
            f"• Aceleración: {self.simulation.V_acceleration:.0f} V",
            f"• Vertical: {self.simulation.V_vertical:.1f} V",
            f"• Horizontal: {self.simulation.V_horizontal:.1f} V"
        ]
        
        y_offset = info_y + 40
        for line in info_lines:
            if line == "":
                y_offset += 10
                continue
            text_surface = self.small_font.render(line, True, WHITE)
            self.screen.blit(text_surface, (info_x + 10, y_offset))
            y_offset += 18
        
        # Información dinámica
        if self.simulation.V_acceleration > 0:
            v_initial = (2 * ELECTRON_CHARGE * self.simulation.V_acceleration / ELECTRON_MASS)**0.5
            velocity_text = f"Velocidad inicial: {v_initial/1e6:.2f} × 10⁶ m/s"
            text_surface = self.small_font.render(velocity_text, True, GREEN)
            self.screen.blit(text_surface, (info_x + 10, y_offset + 10))
    
    def draw_controls_panel(self):
        """Dibuja el panel de controles"""
        panel_rect = pygame.Rect(CONTROL_PANEL_POS[0] - 10, CONTROL_PANEL_POS[1] - 10,
                                PANEL_WIDTH, WINDOW_HEIGHT - 40)
        pygame.draw.rect(self.screen, (15, 15, 15), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 1)
        
        # Título del panel
        title = self.font.render("Controles", True, WHITE)
        self.screen.blit(title, (CONTROL_PANEL_POS[0], CONTROL_PANEL_POS[1] - 30))
        
        # Dibujar todos los controles
        for control in self.controls:
            # Solo mostrar controles sinusoidales si está en modo sinusoidal
            if control in [self.freq_vert_slider, self.freq_horiz_slider, 
                          self.phase_vert_slider, self.phase_horiz_slider]:
                if self.simulation.sinusoidal_mode:
                    control.draw(self.screen)
            else:
                control.draw(self.screen)
    
    def run(self):
        """Loop principal de la aplicación"""
        print("Iniciando simulación CRT...")
        
        while self.running:
            try:
                # Manejar eventos
                self.handle_events()
                
                # Si el programa debe cerrarse, salir del loop
                if not self.running:
                    break
                
                # Actualizar simulación
                self.simulation.update()
                
                # Limpiar pantalla
                self.screen.fill(BLACK)
                
                # Dibujar viewports
                self.draw_viewport(self.lateral_viewport, "Vista Lateral (X-Y)", WHITE)
                self.draw_viewport(self.top_viewport, "Vista Superior (X-Z)", WHITE)  
                self.draw_viewport(self.front_viewport, "Pantalla Principal (Y-Z)", GREEN)
                
                # Dibujar estructura del CRT en cada vista
                self.simulation.draw_crt_structure(self.screen, "lateral", self.lateral_viewport)
                self.simulation.draw_crt_structure(self.screen, "top", self.top_viewport)
                self.simulation.draw_crt_structure(self.screen, "front", self.front_viewport)
                
                # Dibujar trayectorias
                lateral_points = self.simulation.get_lateral_view_points()
                top_points = self.simulation.get_top_view_points()
                
                self.draw_trajectory(lateral_points, self.lateral_viewport, YELLOW)
                self.draw_trajectory(top_points, self.top_viewport, ORANGE)
                
                # Dibujar rastro en pantalla frontal
                self.draw_screen_trace()
                
                # Dibujar paneles de información
                self.draw_info_panel()
                self.draw_controls_panel()
                
                # Mostrar el estado actual del modo
                mode_text = "MODO: " + ("SINUSOIDAL" if self.simulation.sinusoidal_mode else "MANUAL")
                mode_color = GREEN if self.simulation.sinusoidal_mode else WHITE
                mode_surface = self.font.render(mode_text, True, mode_color)
                self.screen.blit(mode_surface, (350, 15))
                
                #instrucciones
                instructions = [
                    "• Ajusta los voltajes para ver la deflexión del haz de electrones",
                    "• Activa el modo sinusoidal para generar figuras de Lissajous",
                    "• La persistencia controla cuánto tiempo permanece visible el rastro"
                ]
                
                # Título de instrucciones
                instr_title = self.font.render("Instrucciones:", True, WHITE)
                self.screen.blit(instr_title, (350, 480))
                
                y_pos = 505
                for instruction in instructions:
                    text_surface = self.small_font.render(instruction, True, WHITE)
                    self.screen.blit(text_surface, (350, y_pos))
                    y_pos += 18
                
                # Actualizar pantalla
                pygame.display.flip()
                self.clock.tick(FPS)
                
            except Exception as e:
                print(f"Error en el loop principal: {e}")
                # Continuar ejecutándose a pesar del error
                continue
        
        print("Cerrando simulación CRT...")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = CRTApp()
    app.run()