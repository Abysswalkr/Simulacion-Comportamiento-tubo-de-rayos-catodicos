import numpy as np
import pygame
import math
from constants import *

class ElectronBeam:
    def __init__(self):
        self.trajectory_points = []
        self.screen_history = []  # Para persistencia
        self.persistence_frames = 100
        
    def calculate_trajectory(self, V_acc, V_vert, V_horiz):
        """
        Calcula la trayectoria del haz de electrones
        V_acc: Voltaje de aceleración (V)
        V_vert: Voltaje de placas verticales (V)
        V_horiz: Voltaje de placas horizontales (V)
        """
        # Velocidad inicial después de aceleración
        if V_acc <= 0:
            return [], 0, 0
            
        v_initial = math.sqrt(2 * ELECTRON_CHARGE * V_acc / ELECTRON_MASS)
        
        # Puntos de trayectoria
        points = []
        
        # 1. Desde el cañón hasta las placas (movimiento rectilíneo)
        x_gun_to_plates = np.linspace(0, GUN_TO_PLATE_DISTANCE, 20)
        for x in x_gun_to_plates:
            points.append((x, 0, 0))  # (x, y, z)
        
        # 2. Entre las placas (deflexión)
        x_plates = np.linspace(GUN_TO_PLATE_DISTANCE, 
                              GUN_TO_PLATE_DISTANCE + PLATE_LENGTH, 30)
        
        # Campo eléctrico entre placas
        E_vert = V_vert / PLATE_SEPARATION if PLATE_SEPARATION > 0 else 0
        E_horiz = V_horiz / PLATE_SEPARATION if PLATE_SEPARATION > 0 else 0
        
        # Aceleración en las placas
        a_vert = -ELECTRON_CHARGE * E_vert / ELECTRON_MASS  # Negativo porque el electrón tiene carga negativa
        a_horiz = -ELECTRON_CHARGE * E_horiz / ELECTRON_MASS
        
        # Tiempo en las placas
        t_plates = PLATE_LENGTH / v_initial
        
        for i, x in enumerate(x_plates):
            t = (i / (len(x_plates) - 1)) * t_plates if len(x_plates) > 1 else 0
            y = 0.5 * a_vert * t * t
            z = 0.5 * a_horiz * t * t
            points.append((x, y, z))
        
        # Velocidad al salir de las placas
        v_vert_exit = a_vert * t_plates
        v_horiz_exit = a_horiz * t_plates
        
        # Posición al salir de las placas
        y_exit = 0.5 * a_vert * t_plates * t_plates
        z_exit = 0.5 * a_horiz * t_plates * t_plates
        
        # 3. Desde las placas hasta la pantalla (movimiento rectilíneo uniforme)
        x_to_screen = np.linspace(GUN_TO_PLATE_DISTANCE + PLATE_LENGTH,
                                 GUN_TO_PLATE_DISTANCE + PLATE_LENGTH + PLATE_TO_SCREEN_DISTANCE, 40)
        
        for x in x_to_screen:
            t_travel = (x - GUN_TO_PLATE_DISTANCE - PLATE_LENGTH) / v_initial
            y = y_exit + v_vert_exit * t_travel
            z = z_exit + v_horiz_exit * t_travel
            points.append((x, y, z))
        
        # Posición final en la pantalla
        x_screen = GUN_TO_PLATE_DISTANCE + PLATE_LENGTH + PLATE_TO_SCREEN_DISTANCE
        t_final = PLATE_TO_SCREEN_DISTANCE / v_initial
        y_final = y_exit + v_vert_exit * t_final
        z_final = z_exit + v_horiz_exit * t_final
        
        self.trajectory_points = points
        return points, y_final, z_final

class CRTSimulation:
    def __init__(self):
        self.electron_beam = ElectronBeam()
        self.current_time = 0
        self.dt = 1/60  # 60 FPS
        
        # Variables de control
        self.V_acceleration = 1000  # V
        self.V_vertical = 0  # V  
        self.V_horizontal = 0  # V
        self.persistence_frames = 100
        
        # Modo sinusoidal
        self.sinusoidal_mode = False
        self.frequency_vert = 1.0  # Hz
        self.frequency_horiz = 1.5  # Hz
        self.phase_vert = 0  # degrees
        self.phase_horiz = 90  # degrees
        
        # Historia para persistencia
        self.screen_hits = []
        
    def update(self):
        """Actualiza la simulación"""
        self.current_time += self.dt
        
        # Calcular voltajes (manual o sinusoidal)
        if self.sinusoidal_mode:
            # Modo sinusoidal para Figuras de Lissajous
            V_vert = 50 * math.sin(2 * math.pi * self.frequency_vert * self.current_time + 
                                  math.radians(self.phase_vert))
            V_horiz = 50 * math.sin(2 * math.pi * self.frequency_horiz * self.current_time + 
                                   math.radians(self.phase_horiz))
        else:
            # Modo manual
            V_vert = self.V_vertical
            V_horiz = self.V_horizontal
        
        # Calcular trayectoria
        points, y_final, z_final = self.electron_beam.calculate_trajectory(
            self.V_acceleration, V_vert, V_horiz)
        
        # Agregar punto de impacto a la historia
        if abs(y_final) <= SCREEN_SIZE/2 and abs(z_final) <= SCREEN_SIZE/2:
            self.screen_hits.append({
                'pos': (y_final, z_final),
                'frame': self.current_time * 60  # Frame number
            })
        
        # Limpiar puntos antiguos basado en persistencia
        current_frame = self.current_time * 60
        self.screen_hits = [hit for hit in self.screen_hits 
                           if current_frame - hit['frame'] <= self.persistence_frames]
    
    def get_lateral_view_points(self):
        """Obtiene puntos para vista lateral (X-Y)"""
        if not self.electron_beam.trajectory_points:
            return []
        
        points = []
        for x, y, z in self.electron_beam.trajectory_points:
            # Convertir a coordenadas de pantalla
            screen_x = int(x * LATERAL_SCALE)
            screen_y = int(VIEWPORT_HEIGHT // 2 - y * LATERAL_SCALE)
            points.append((screen_x, screen_y))
        
        return points
    
    def get_top_view_points(self):
        """Obtiene puntos para vista superior (X-Z)"""
        if not self.electron_beam.trajectory_points:
            return []
        
        points = []
        for x, y, z in self.electron_beam.trajectory_points:
            # Convertir a coordenadas de pantalla
            screen_x = int(x * TOP_SCALE)
            screen_z = int(VIEWPORT_HEIGHT // 2 - z * TOP_SCALE)
            points.append((screen_x, screen_z))
        
        return points
    
    def get_screen_points(self):
        """Obtiene puntos para la pantalla frontal (Y-Z)"""
        points = []
        current_frame = self.current_time * 60
        
        for hit in self.screen_hits:
            y, z = hit['pos']
            age = current_frame - hit['frame']
            
            # Calcular intensidad basada en edad
            intensity = max(0, 1.0 - age / self.persistence_frames)
            
            # Convertir a coordenadas de pantalla
            screen_y = int(VIEWPORT_WIDTH // 2 + y * FRONT_SCALE)
            screen_z = int(VIEWPORT_HEIGHT // 2 - z * FRONT_SCALE)
            
            points.append((screen_y, screen_z, intensity))
        
        return points
    
    def draw_crt_structure(self, screen, view_type, viewport_rect):
        """Dibuja la estructura del CRT en cada vista"""
        x_offset = viewport_rect.x
        y_offset = viewport_rect.y
        
        if view_type == "lateral":
            # Dibujar placas verticales
            plate_x = int(GUN_TO_PLATE_DISTANCE * LATERAL_SCALE)
            plate_width = int(PLATE_LENGTH * LATERAL_SCALE)
            plate_separation = int(PLATE_SEPARATION/2 * LATERAL_SCALE)
            
            # Placa superior
            pygame.draw.rect(screen, WHITE, 
                           (x_offset + plate_x, y_offset + VIEWPORT_HEIGHT//2 - plate_separation - 5,
                            plate_width, 5))
            # Placa inferior  
            pygame.draw.rect(screen, WHITE,
                           (x_offset + plate_x, y_offset + VIEWPORT_HEIGHT//2 + plate_separation,
                            plate_width, 5))
            
            # Pantalla
            screen_x = int((GUN_TO_PLATE_DISTANCE + PLATE_LENGTH + PLATE_TO_SCREEN_DISTANCE) * LATERAL_SCALE)
            pygame.draw.line(screen, GREEN, 
                           (x_offset + screen_x, y_offset + 20),
                           (x_offset + screen_x, y_offset + VIEWPORT_HEIGHT - 20), 3)
            
        elif view_type == "top":
            # Dibujar placas horizontales
            plate_x = int(GUN_TO_PLATE_DISTANCE * TOP_SCALE)
            plate_width = int(PLATE_LENGTH * TOP_SCALE)
            plate_separation = int(PLATE_SEPARATION/2 * TOP_SCALE)
            
            # Placa izquierda
            pygame.draw.rect(screen, WHITE,
                           (x_offset + plate_x, y_offset + VIEWPORT_HEIGHT//2 - plate_separation - 5,
                            plate_width, 5))
            # Placa derecha
            pygame.draw.rect(screen, WHITE,
                           (x_offset + plate_x, y_offset + VIEWPORT_HEIGHT//2 + plate_separation,
                            plate_width, 5))
            
            # Pantalla
            screen_x = int((GUN_TO_PLATE_DISTANCE + PLATE_LENGTH + PLATE_TO_SCREEN_DISTANCE) * TOP_SCALE)
            pygame.draw.line(screen, GREEN,
                           (x_offset + screen_x, y_offset + 20),
                           (x_offset + screen_x, y_offset + VIEWPORT_HEIGHT - 20), 3)
        
        elif view_type == "front":
            # Dibujar borde de pantalla
            pygame.draw.rect(screen, GREEN, viewport_rect, 3)