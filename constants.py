import math

# Constantes físicas
ELECTRON_MASS = 9.109e-31  # kg
ELECTRON_CHARGE = 1.602e-19  # C

# Dimensiones del CRT (en metros para cálculos)
SCREEN_SIZE = 0.40  # 40 cm
PLATE_SEPARATION = 0.02  # 2 cm
PLATE_LENGTH = 0.05  # 5 cm
PLATE_TO_SCREEN_DISTANCE = 0.30  # 30 cm
GUN_TO_PLATE_DISTANCE = 0.10  # 10 cm

# Configuración de pantalla
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Dimensiones de viewports
VIEWPORT_WIDTH = 250
VIEWPORT_HEIGHT = 200
PANEL_WIDTH = 300

# Rangos de controles
ACCELERATION_VOLTAGE_RANGE = (100, 2000)  # V
DEFLECTION_VOLTAGE_RANGE = (-100, 100)  # V
PERSISTENCE_RANGE = (1, 500)  # frames
FREQUENCY_RANGE = (0.1, 10.0)  # Hz
PHASE_RANGE = (0, 360)  # degrees

# Posiciones de viewports
LATERAL_VIEW_POS = (20, 20)
TOP_VIEW_POS = (20, 250)
FRONT_VIEW_POS = (20, 480)
CONTROL_PANEL_POS = (WINDOW_WIDTH - PANEL_WIDTH - 20, 20)

# Escalas para conversión pixel/metro
LATERAL_SCALE = 400  # pixels por metro
TOP_SCALE = 400
FRONT_SCALE = 500